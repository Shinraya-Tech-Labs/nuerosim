import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.adaptive_reference import audit_fixture


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T020-adaptive-reference-comparisons"


def test_T020_adaptive_reference_comparisons_unit():
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert report["sample_count"] == 201
    assert report["reference_delta_max_mV"] <= report["reference_limit_mV"]
    assert report["rk4_error_max_mV"] <= report["rk4_limit_mV"]
    assert report["manifest"]["config"]["solver"] == "rk4"


def test_invalid_tolerance_fixture_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda data: data.update(units={"time": "s", "current": "uA/cm^2", "voltage": "mV"}), "units must be"),
        (lambda data: data.update(duration_ms=0), "duration_ms and dt_ms must be positive"),
        (lambda data: data.update(loose_atol_mV=0), "loose DOP853 tolerances"),
        (lambda data: data.update(record_every=0), "greater than or equal to 1"),
        (lambda data: data.update(current_uA_cm2=101), "less than or equal to 100"),
    ],
)
def test_invalid_units_tolerances_and_config_are_rejected(tmp_path, change, message):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    change(fixture)
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        audit_fixture(path)


def test_numeric_reference_limit_failure_is_reported(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["reference_limit_mV"] = 1e-12
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    report = audit_fixture(path)
    assert report["passed"] is False


def test_cli_exposes_adaptive_reference_comparison():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.adaptive_reference", str(FIXTURES / "valid.json")],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["passed"] is True
