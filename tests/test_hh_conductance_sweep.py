import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.hh_conductance_sweep import audit_fixture, run_sweep

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T023-hh-conductance-sweeps"


def test_T023_hh_conductance_sweeps_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert [row["spike_count"] for row in report["runs"]] == fixture["expected_spike_counts"]
    assert [row["final_voltage_mV"] for row in report["runs"]] == pytest.approx(fixture["expected_final_voltage_mV"], abs=fixture["voltage_tolerance_mV"])
    assert [row["manifest"]["config"]["parameters"]["g_na"] for row in report["runs"]] == fixture["g_na_mS_cm2"]


def test_duplicate_conductance_boundary_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


def test_invalid_units_are_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["conductance"] = "S/m^2"
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="units must be"):
        audit_fixture(path)


def test_conductance_bounds_and_sweep_size_are_enforced():
    data = {"model": "hh", "duration": 50, "dt": 0.025, "pulses": []}
    with pytest.raises(ValueError, match="within 0..240"):
        run_sweep(data, [60, 241])
    with pytest.raises(ValueError, match="2..12"):
        run_sweep(data, [120])
    with pytest.raises(ValueError, match="two million neuron-steps"):
        run_sweep({"model": "hh", "duration": 2000, "dt": 0.001, "pulses": []}, [60, 120])


def test_cli_persists_manifest_backed_sweep_output(tmp_path):
    output = tmp_path / "sweep.json"
    subprocess.run(
        [sys.executable, "-m", "neurosim.hh_conductance_sweep", str(FIXTURES / "valid.json"), "--output", str(output)],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert all(row["manifest"]["config"]["model"] == "hh" for row in report["runs"])
