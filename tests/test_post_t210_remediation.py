import hashlib
import json
import os
import subprocess
import sys
import pytest
from fastapi.testclient import TestClient

from neurosim.omega_final import run_task
from neurosim.workbench.api import create_app
from neurosim.workbench.config import Experiment
from neurosim.workbench.store import Store
from neurosim.workbench.views import activity


def test_vectorized_lif_matches_independent_scalar_reference():
    payload = {"input": {"currents": [1, 2, 3], "dt": 0.1, "tau": 10, "rest": -65}}
    result = run_task("T157", payload)["result"]["voltages"]
    expected = [-65 + 0.1 * current / 10 for current in [1, 2, 3]]
    assert result == pytest.approx(expected)
    assert run_task("T157", {"input": {"currents": [2, 2], "dt": 0.1, "tau": 10}})["result"]["voltages"] == pytest.approx([-64.98, -64.98])
    assert run_task("T157", {"input": {"currents": 2, "dt": 0.1, "tau": 10}})["result"]["count"] == 1


@pytest.mark.parametrize("value", [10.9, True, -1, 0])
def test_resource_integer_validation(value):
    if value == 0:
        with pytest.raises(ValueError):
            run_task("T151", {"input": {"steps": value, "neurons": 1}})
    else:
        with pytest.raises(ValueError):
            run_task("T151", {"input": {"steps": value, "neurons": 1}})
    with pytest.raises(ValueError):
        run_task("T181", {"input": {"requests": value, "limit": -1}})


@pytest.mark.parametrize("value", ["false", "true", 0, 1, None, [], {}])
def test_release_gates_require_actual_booleans(value):
    with pytest.raises(ValueError):
        run_task("T210", {"input": {"checks": {"release": value}}})


def test_rss_rejects_negative_samples():
    with pytest.raises(ValueError):
        run_task("T152", {"input": {"samples": [1, -1]}})


def test_cli_malformed_nested_input_is_controlled(tmp_path):
    fixture = tmp_path / "bad.json"
    fixture.write_text(json.dumps({"task": "T184", "input": {"actions": ["GET"]}}), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.omega_final", "--fixture", str(fixture)],
        env={**os.environ, "PYTHONPATH": str(__import__("pathlib").Path("python").resolve())},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr


def test_checksum_hashes_artifact_bytes(tmp_path):
    artifact = tmp_path / "release.bin"
    artifact.write_bytes(b"artifact bytes")
    result = run_task("T209", {"input": {"path": str(artifact)}})["result"]
    assert result["sha256"] == hashlib.sha256(b"artifact bytes").hexdigest()


def test_history_is_batched_and_ordered(tmp_path):
    store = Store(tmp_path / "history.db")
    for index in range(7):
        store.create(Experiment(name=f"job-{index}"))
    rows = store.history(500)
    assert len(rows) == 7
    assert rows[0]["created"] >= rows[-1]["created"]
    assert all(isinstance(row["manifest"], dict) for row in rows)


def test_backup_restore_round_trip(tmp_path):
    source = Store(tmp_path / "source.db")
    job = source.create(Experiment(name="backup"))
    backup = tmp_path / "backup.db"
    source.backup_to(backup)
    restored = Store(tmp_path / "restored.db")
    restored.restore_from(backup)
    assert restored.get(job["id"])["manifest"] == job["manifest"]


def test_corrupt_backup_is_rejected(tmp_path):
    corrupt = tmp_path / "corrupt.db"
    corrupt.write_bytes(b"not sqlite")
    restored = Store(tmp_path / "restored.db")
    with pytest.raises(Exception):
        restored.restore_from(corrupt)


def test_activity_pagination_uses_materialized_order():
    result = {
        "spikes": [[3, 1], [2]],
        "activity_events": [
            {"time_ms": 1, "neuron_id": 0},
            {"time_ms": 2, "neuron_id": 1},
            {"time_ms": 3, "neuron_id": 0},
        ],
    }
    assert activity(result, 1, 1)["events"] == [{"time_ms": 2, "neuron_id": 1}]
    assert activity(result, 2, 2)["next_offset"] is None


def test_remote_api_requires_bearer_and_health_is_public(tmp_path, monkeypatch):
    monkeypatch.setenv("NEUROSIM_ALLOW_REMOTE", "1")
    monkeypatch.setenv("NEUROSIM_AUTH_TOKEN", "a-secure-test-token")
    with TestClient(create_app(tmp_path / "remote.db")) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/defaults").status_code == 401
        assert client.get("/defaults", headers={"Authorization": "Bearer a-secure-test-token"}).status_code == 200


def test_read_only_api_rejects_mutations(tmp_path, monkeypatch):
    monkeypatch.setenv("NEUROSIM_READ_ONLY", "1")
    with TestClient(create_app(tmp_path / "readonly.db")) as client:
        assert client.post("/experiments", json={"model": "lif", "duration": 1, "pulses": []}).status_code == 403


def test_remote_api_rejects_missing_token(monkeypatch):
    monkeypatch.setenv("NEUROSIM_ALLOW_REMOTE", "1")
    monkeypatch.delenv("NEUROSIM_AUTH_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="NEUROSIM_AUTH_TOKEN"):
        create_app()

