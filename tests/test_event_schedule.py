import json
from pathlib import Path

import pytest

from neurosim.event_schedule import audit_schedule


def test_T007_event_scheduling_audit_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T007-event-scheduling-audit/valid.json").read_text(
            encoding="utf-8"
        )
    )

    assert audit_schedule(fixture["result"]) == fixture["expected"]


def test_T007_event_scheduling_audit_rejects_inconsistent_delay():
    fixture = json.loads(
        Path("tests/fixtures/omega/T007-event-scheduling-audit/invalid.json").read_text(
            encoding="utf-8"
        )
    )

    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_schedule(fixture["result"])


def test_T007_event_scheduling_audit_minimum_grid_aligned_boundary():
    result = {
        "manifest": {"units": {"time": "ms"}, "config": {"delay": 0.025, "dt": 0.025}},
        "effective_delay_ms": 0.025,
    }

    report = audit_schedule(result)

    assert report["delay_steps"] == 1
    assert report["effective_delay_ms"] == report["requested_delay_ms"]
    assert report["rounding_ms"] == 0
