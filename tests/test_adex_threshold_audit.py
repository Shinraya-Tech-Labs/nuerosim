import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.adex_threshold_audit import audit_fixture, audit_experiment

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T025-adex-threshold-dynamics"


def test_T025_adex_threshold_dynamics_unit():
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert report["numerical_cutoff_voltage_mV"] == -40
    assert report["spike_times_ms"] == [1.5, 4.0, 6.5, 9.0]
    assert report["spike_intervals_ms"] == [2.5, 2.5, 2.5]
    assert report["manifest"]["config"]["model"] == "adex"


def test_wrong_model_fixture_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


def test_invalid_units_and_tolerance_are_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["voltage"] = "V"
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="units must be"):
        audit_fixture(path)
    with pytest.raises(ValueError, match="finite and positive"):
        audit_experiment(fixture["experiment"], [], 0)


def test_high_drive_remains_finite_with_numerical_cutoff():
    data = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))["experiment"]
    data["pulses"][0]["amplitude"] = 100
    report = audit_experiment(data, [1.25, 3.5, 5.75, 8.0], 1e-12)
    assert report["passed"] is True
    assert report["spike_count"] == 4
    assert report["final_voltage_mV"] > -66


def test_cli_persists_threshold_report(tmp_path):
    output = tmp_path / "threshold.json"
    subprocess.run(
        [sys.executable, "-m", "neurosim.adex_threshold_audit", str(FIXTURES / "valid.json"), "--output", str(output)],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert report["numerical_cutoff_voltage_mV"] == -40
