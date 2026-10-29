import json
from pathlib import Path

import pytest
import numpy as np

from neurosim.event_schedule import audit_schedule
from neurosim.workbench.config import Experiment, Pulse
from neurosim.workbench.engine import simulate


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


def test_T007_event_scheduling_audit_real_event_integration():
    config = Experiment(
        model="lif",
        n=2,
        duration=25,
        record_every=1,
        probability=1,
        inhibitory_fraction=0,
        delay=2.01,
        pulses=[Pulse(start=0, stop=25, amplitude=3)],
    )
    result = simulate(config)
    report = audit_schedule(result)

    times = np.array(result["t"])
    target_voltage = np.array(result["voltage"])[1]
    arrival = result["spikes"][0][0] + report["effective_delay_ms"]
    assert report["effective_delay_ms"] == 2.025
    np.testing.assert_allclose(target_voltage[times <= arrival + 1e-9], -65, atol=1e-10)
    assert target_voltage[np.searchsorted(times, arrival + config.dt)] > -65
