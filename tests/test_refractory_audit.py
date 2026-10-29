import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.refractory_audit import audit_experiment, audit_fixture

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T026-refractory-period-scheduling"


def test_T026_refractory_period_scheduling_unit():
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert report["spike_times_ms"][0] == 0.775
    assert report["minimum_interspike_interval_ms"] == pytest.approx(2.775)
    assert report["minimum_interval_satisfied"] is True
    assert report["refractory_steps_at_dt"] == 80
    assert report["manifest"]["config"]["parameters"]["refractory"] == 2


def test_wrong_model_fixture_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


def test_invalid_units_and_tolerance_are_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["time"] = "s"
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="units must be"):
        audit_fixture(path)
    with pytest.raises(ValueError, match="finite and positive"):
        audit_experiment(fixture["experiment"], 0)


def test_cli_persists_refractory_schedule(tmp_path):
    output = tmp_path / "refractory.json"
    subprocess.run(
        [sys.executable, "-m", "neurosim.refractory_audit", str(FIXTURES / "valid.json"), "--output", str(output)],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert min(report["interspike_intervals_ms"]) >= report["configured_refractory_ms"]
