import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.golden_lif import audit_fixture


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T014-golden-lif-trace-fixture"


def test_T014_golden_lif_trace_fixture_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is fixture["expected"]["passed"] is True
    assert report["sample_count"] == fixture["expected"]["sample_count"] == 5
    assert report["spike_count"] == fixture["expected"]["spike_count"] == 0
    assert report["max_abs_error_mV"] < report["tolerance_mV"] == 1e-9
    assert report["manifest"]["config"]["model"] == "lif"


def test_invalid_unit_fixture_is_rejected():
    with pytest.raises(ValueError, match="units must be ms and mV"):
        audit_fixture(FIXTURES / "invalid.json")


def test_arrays_with_different_lengths_are_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["reference_voltage_mV"] = fixture["reference_voltage_mV"][:-1]
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="equal length"):
        audit_fixture(path)


def test_off_grid_time_is_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["sample_times_ms"][1] = 5.001
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="absent from the saved trace grid"):
        audit_fixture(path)


def test_reference_outside_tolerance_fails(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["reference_voltage_mV"][2] += 1
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    report = audit_fixture(path)
    assert report["passed"] is False
    assert report["max_abs_error_mV"] > report["tolerance_mV"]


def test_cli_exposes_fixture_audit():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.golden_lif", str(FIXTURES / "valid.json")],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["passed"] is True
