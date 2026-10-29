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
