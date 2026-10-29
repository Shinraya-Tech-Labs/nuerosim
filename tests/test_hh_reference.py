import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.hh_reference import audit_fixture

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T022-hh-6-3-celsius-reference"


def test_T022_hh_6_3_celsius_reference_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    result = audit_fixture(FIXTURES / "valid.json")
    assert result["passed"]
    assert result["units"] == fixture["units"]
    assert result["max_rate_error_ms^-1"] <= fixture["tolerance"]
    assert result["max_gate_error"] <= fixture["tolerance"]
    assert result["max_initialization_error"] <= fixture["tolerance"]
    assert result["steady_state_gates"] == pytest.approx(fixture["expected_gates"], abs=fixture["tolerance"])


def test_unsupported_temperature_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="only the fixed 6.3 C"):
        audit_fixture(FIXTURES / "invalid.json")


@pytest.mark.parametrize("key,value", [("voltage_mV", float("nan")), ("tolerance", 0), ("tolerance", float("inf"))])
def test_invalid_numeric_inputs_are_rejected(tmp_path, key, value):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture[key] = value
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError):
        audit_fixture(path)


def test_fixture_rejects_wrong_units(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["temperature"] = "K"
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="units must be"):
        audit_fixture(path)


def test_cli_exposes_reference_audit():
    result = subprocess.run([sys.executable, "-m", "neurosim.hh_reference", str(FIXTURES / "valid.json")], cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["passed"] is True
