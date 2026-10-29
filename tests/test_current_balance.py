import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.current_balance import audit_fixture, diagnose

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T028-current-balance-conservation-diagnostic"


def test_T028_current_balance_conservation_diagnostic_unit():
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert report["axial_currents_uA_cm2"] == [1.0, -3.0, 2.0]
    assert report["net_current_uA_cm2"] == 0


def test_one_compartment_boundary_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


def test_invalid_units_and_nonfinite_inputs_are_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["voltage"] = "V"
    path = tmp_path / "bad-units.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="units must be"):
        audit_fixture(path)
    with pytest.raises(ValueError, match="finite numbers"):
        diagnose([-65, float("nan")], 0.1)


def test_cli_persists_balance_report(tmp_path):
    output = tmp_path / "balance.json"
    subprocess.run([sys.executable, "-m", "neurosim.current_balance", str(FIXTURES / "valid.json"), "--output", str(output)], cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True)
    assert json.loads(output.read_text(encoding="utf-8"))["net_current_uA_cm2"] == 0
