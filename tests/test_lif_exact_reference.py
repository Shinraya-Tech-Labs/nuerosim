import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.lif_exact_reference import audit_fixture, compare_experiment

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T024-lif-exact-reference-solution"


def test_T024_lif_exact_reference_solution_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert report["max_abs_error_mV"] <= fixture["tolerance_mV"]
    assert report["fixture_reference_errors_mV"] == {"15": 0.0, "20": 0.0}
    assert report["manifest"]["config"]["model"] == "lif"


def test_threshold_crossing_reference_is_rejected():
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
        compare_experiment(fixture["experiment"], 0)


def test_wrong_model_or_multiple_neurons_are_rejected():
    with pytest.raises(ValueError, match="requires model='lif'"):
        compare_experiment({"model": "hh", "pulses": []}, 1e-8)
    with pytest.raises(ValueError, match="one neuron"):
        compare_experiment({"model": "lif", "n": 2, "pulses": []}, 1e-8)


def test_cli_persists_exact_reference_and_manifest(tmp_path):
    output = tmp_path / "lif-reference.json"
    subprocess.run(
        [sys.executable, "-m", "neurosim.lif_exact_reference", str(FIXTURES / "valid.json"), "--output", str(output)],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert len(report["exact_voltage_mV"]) == len(report["production_voltage_mV"])
