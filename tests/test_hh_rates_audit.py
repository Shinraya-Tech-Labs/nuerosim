import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.hh_rates_audit import audit_fixture, audit_rates


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T021-hh-gating-kinetics-edge-cases"


def test_T021_hh_gating_kinetics_edge_cases_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert report["units"] == fixture["units"]
    assert report["singularity_checks"] == {
        "alpha_m_at_minus40": True,
        "alpha_n_at_minus55": True,
        "near_minus40_continuous": True,
        "near_minus55_continuous": True,
    }
    assert report["near_limit_deviation_ms^-1"]["alpha_m"] <= fixture["continuity_tolerance_ms^-1"]
    assert report["near_limit_deviation_ms^-1"]["alpha_n"] <= fixture["continuity_tolerance_ms^-1"]
    assert all(
        rate >= 0
        for row in report["rates"]
        for key, rate in row.items()
        if key not in {"voltage_mV"}
    )


def test_invalid_fixture_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


@pytest.mark.parametrize("values", [[float("nan")], [float("inf")], [True]])
def test_nonfinite_or_boolean_voltage_is_rejected(values):
    with pytest.raises(ValueError, match="finite numbers"):
        audit_rates(values)


def test_nonpositive_continuity_tolerance_is_rejected():
    with pytest.raises(ValueError, match="continuity tolerance must be finite and positive"):
        audit_rates([-40, -55], 0)


def test_extreme_voltage_that_overflows_kinetics_is_rejected():
    with pytest.raises(ValueError, match="rates must be finite and non-negative"):
        audit_rates([-1e308])


def test_fixture_rejects_wrong_units(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["voltage"] = "V"
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match=r"units must be mV and ms\^-1"):
        audit_fixture(path)


def test_cli_exposes_rate_edge_audit():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.hh_rates_audit", str(FIXTURES / "valid.json")],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["passed"] is True
