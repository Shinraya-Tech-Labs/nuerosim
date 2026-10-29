import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.golden_hh import audit_fixture


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T013-golden-hh-trace-fixture"


def test_T013_golden_hh_trace_fixture_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is fixture["expected"]["passed"] is True
    assert report["sample_count"] == fixture["expected"]["sample_count"] == 5
    assert report["spike_count"] == fixture["expected"]["spike_count"] == 2
    assert report["max_abs_error_mV"] < report["tolerance_mV"] == 0.02


def test_invalid_unit_fixture_is_rejected():
    with pytest.raises(ValueError, match="units must be ms and mV"):
        audit_fixture(FIXTURES / "invalid.json")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda data: data.update(sample_times_ms=[0, 10, 5, 15, 20]), "strictly increasing"),
        (lambda data: data.update(tolerance_mV=0), "finite positive number"),
        (lambda data: data.update(sample_times_ms=[0, 1]), "equal length"),
    ],
)
def test_fixture_boundaries_are_rejected(tmp_path, change, message):
    data = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    change(data)
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        audit_fixture(path)


def test_off_grid_sample_is_rejected(tmp_path):
    data = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    data["sample_times_ms"][1] = 5.001
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="absent from the saved trace grid"):
        audit_fixture(path)


def test_cli_exposes_fixture_audit():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.golden_hh", str(FIXTURES / "valid.json")],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["passed"] is True
