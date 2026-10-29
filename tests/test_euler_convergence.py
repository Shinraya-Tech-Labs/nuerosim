import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.euler_convergence import audit_fixture


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T018-euler-convergence-harness"


def test_T018_euler_convergence_harness_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    lower, upper = fixture["expected"]["first_order_range"]
    assert report["passed"] is True
    assert report["dt_ms"] == [fixture["coarse_dt_ms"], fixture["fine_dt_ms"]]
    assert report["max_abs_error_mV"][1] < report["max_abs_error_mV"][0]
    assert lower <= report["observed_order"] <= upper
    assert all(m["config"]["solver"] == "euler" for m in report["manifests"])


def test_invalid_fixture_exceeds_hh_euler_step_bound():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("duration_ms", 0, "duration must be positive"),
        ("duration_ms", 20.001, "duration must be an integer multiple of dt"),
        ("fine_dt_ms", 0.005, "fine_dt_ms < coarse_dt_ms"),
        ("current_uA_cm2", float("nan"), "must be finite numbers"),
    ],
)
def test_invalid_grid_or_value_boundaries(tmp_path, field, value, error):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture[field] = value
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match=error):
        audit_fixture(path)


def test_cli_exposes_real_convergence_harness():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.euler_convergence", str(FIXTURES / "valid.json")],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["passed"] is True
    assert report["observed_order"] == pytest.approx(0.996244, abs=1e-5)
