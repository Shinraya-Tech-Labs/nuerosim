import io
import time
import zipfile

import pytest
from fastapi.testclient import TestClient

from neurosim.workbench.api import create_app
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
from neurosim.workbench.morphology import parse_swc
from neurosim.workbench.store import Store, Worker


def wait(client, jid):
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        job = client.get(f"/experiments/{jid}").json()
        if job["status"] in ("completed", "cancelled", "failed"):
            return job
        time.sleep(0.02)
    pytest.fail("real worker did not finish in 15 seconds")


def test_execution_export_retry_restart(tmp_path):
    path = tmp_path / "jobs.db"
    config = Experiment(duration=10, pulses=[], model="lif").model_dump()
    with TestClient(create_app(path)) as c:
        assert c.get("/health").json()["worker_alive"]
        response = c.post("/experiments", json=config)
        assert response.status_code == 202
        jid = response.json()["id"]
        assert wait(c, jid)["status"] == "completed"
        result = c.get(f"/experiments/{jid}/results").json()
        assert result["voltage"] == simulate(Experiment(**config))["voltage"]
        manifest = c.get(f"/experiments/{jid}/manifest").json()
        assert result["manifest"] == manifest
        archive = zipfile.ZipFile(
            io.BytesIO(c.get(f"/experiments/{jid}/export").content)
        )
        assert {
            "manifest.json",
            "voltage.csv",
            "spikes.csv",
            "connectivity.csv",
        } <= set(archive.namelist())
        retry = c.post(f"/experiments/{jid}/retry").json()
        assert retry["parent_id"] == jid
        assert wait(c, retry["id"])["status"] == "completed"
    with TestClient(create_app(path)) as c:
        assert len(c.get("/experiments").json()) == 2
        assert c.get(f"/experiments/{jid}/results").json() == result
        assert c.delete(f"/experiments/{jid}").status_code == 204
        assert c.get(f"/experiments/{jid}").status_code == 404


def test_validation_cancel_unknown(tmp_path):
    with TestClient(create_app(tmp_path / "jobs.db")) as c:
        assert c.post("/experiments", json={"dt": -1}).status_code == 422
        assert c.post("/experiments", json={"backend": "cuda"}).status_code == 422
        assert c.get("/experiments/absent").status_code == 404
        config = Experiment(n=32, duration=1000, record_every=100).model_dump()
        jid = c.post("/experiments", json=config).json()["id"]
        assert c.get(f"/experiments/{jid}/results").status_code == 409
        assert c.post(f"/experiments/{jid}/retry").status_code == 409
        deadline = time.monotonic() + 5
        while (
            c.get(f"/experiments/{jid}").json()["status"] == "queued"
            and time.monotonic() < deadline
        ):
            time.sleep(0.02)
        assert c.get(f"/experiments/{jid}").json()["status"] == "running"
        assert c.post(f"/experiments/{jid}/cancel").status_code == 200
        assert wait(c, jid)["status"] == "cancelled"
        assert c.get(f"/experiments/{jid}/results").status_code == 409


def test_real_resource_failure_and_queued_cancel(tmp_path):
    with TestClient(create_app(tmp_path / "jobs.db")) as c:
        job = c.post(
            "/experiments",
            json={"n": 512, "probability": 1, "duration": 1, "pulses": []},
        ).json()
        failed = wait(c, job["id"])
        assert failed["status"] == "failed"
        assert "32768" in failed["error"]
    store = Store(tmp_path / "queue.db")
    job = store.create(Experiment())
    assert store.cancel(job["id"])["status"] == "cancelled"
    assert store.claim() is None


def test_failure_and_restart_recovery(tmp_path):
    store = Store(tmp_path / "jobs.db")
    interrupted = store.create(Experiment())
    assert store.claim() == interrupted["id"]
    # Corrupt persisted configuration exercises actual exception reporting, no mock runner.
    invalid = store.create(Experiment())
    with store.connection() as db:
        db.execute(
            "UPDATE jobs SET manifest=? WHERE id=?",
            ('{"config":{"dt":0}}', invalid["id"]),
        )
    worker = Worker(store)
    try:
        assert store.get(interrupted["id"])["status"] == "failed"
        deadline = time.monotonic() + 5
        while (
            store.get(invalid["id"])["status"] not in ("failed", "completed")
            and time.monotonic() < deadline
        ):
            time.sleep(0.02)
        assert store.get(invalid["id"])["status"] == "failed"
        assert "ValidationError" in store.get(invalid["id"])["error"]
        with pytest.raises(RuntimeError):
            Worker(store)
    finally:
        worker.close()


def test_swc_validation(tmp_path):
    text = "1 1 0 0 0 5 -1\n2 3 0 10 0 1 1"
    assert len(parse_swc(text)) == 2
    for bad in (
        text + "\n2 3 0 0 0 1 1",
        "1 1 nan 0 0 1 -1",
        "1 1 0 0 0 1 -1\n2 3 0 0 0 1 3\n3 3 0 0 0 1 2",
    ):
        with pytest.raises(ValueError):
            parse_swc(bad)
    with TestClient(create_app(tmp_path / "jobs.db")) as c:
        assert c.post("/morphology", json={"text": text}).status_code == 200
        assert c.post("/morphology", json={"text": "bad"}).status_code == 422


def test_queue_quota_and_manifest_change(tmp_path):
    import json

    store = Store(tmp_path / "quota.db")
    jobs = [store.create(Experiment()) for _ in range(16)]
    with pytest.raises(ValueError, match="16 active"):
        store.create(Experiment())
    for job in jobs:
        store.cancel(job["id"])
    job = store.create(Experiment())
    changed = job["manifest"]
    changed["numpy"] = "different environment"
    with store.connection() as db:
        db.execute(
            "UPDATE jobs SET manifest=? WHERE id=?", (json.dumps(changed), job["id"])
        )
    worker = Worker(store)
    try:
        deadline = time.monotonic() + 5
        while (
            store.get(job["id"])["status"] not in ("failed", "completed")
            and time.monotonic() < deadline
        ):
            time.sleep(0.02)
        assert store.get(job["id"])["status"] == "failed"
        assert "environment changed" in store.get(job["id"])["error"]
    finally:
        worker.close()
