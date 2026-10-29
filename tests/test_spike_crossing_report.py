import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.spike_crossing_report import audit_fixture

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T027-spike-crossing-precision-report"


def test_T027_spike_crossing_precision_report_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_fixture(FIXTURES / "valid.json")
    assert report["passed"] is True
    assert [row["spike_time_ms"] for row in report["crossings"]] == pytest.approx(fixture["expected_spike_times_ms"], abs=1e-12)
    assert [row["interpolated_crossing_ms"] for row in report["crossings"]] == pytest.approx(fixture["expected_interpolated_crossings_ms"], abs=1e-12)
    assert all(0 <= row["endpoint_offset_ms"] <= report["dt_ms"] for row in report["crossings"])
    assert report["manifest"]["config"]["model"] == "hh"


def test_downsampled_trace_boundary_is_rejected():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_fixture(FIXTURES / "invalid.json")


def test_invalid_units_are_rejected(tmp_path):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["units"]["time"] = "s"
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match="units must be"):
        audit_fixture(path)


def test_cli_persists_crossing_report(tmp_path):
    output = tmp_path / "crossings.json"
    subprocess.run(
        [sys.executable, "-m", "neurosim.spike_crossing_report", str(FIXTURES / "valid.json"), "--output", str(output)],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": "python"}, capture_output=True, text=True, check=True,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert all(row["endpoint_offset_ms"] <= report["maximum_crossing_offset_ms"] for row in report["crossings"])
