import copy
import json
from pathlib import Path

import pytest

from neurosim.units_audit import audit_units
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate


def test_T005_scientific_units_audit_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T005-scientific-units-audit/valid.json").read_text(
            encoding="utf-8"
        )
    )

    assert audit_units(fixture["result"]) == fixture["expected"]


def test_T005_scientific_units_audit_rejects_wrong_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T005-scientific-units-audit/invalid.json").read_text(
            encoding="utf-8"
        )
    )

    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_units(fixture["result"])


def test_T005_scientific_units_audit_boundaries():
    fixture = json.loads(
        Path("tests/fixtures/omega/T005-scientific-units-audit/valid.json").read_text(
            encoding="utf-8"
        )
    )
    zero_duration = copy.deepcopy(fixture["result"])
    zero_duration["manifest"]["config"]["duration"] = 0
    out_of_range_spike = copy.deepcopy(fixture["result"])
    out_of_range_spike["spikes"][0][-1] = 1001
    inconsistent_rate = copy.deepcopy(fixture["result"])
    inconsistent_rate["mean_rate_hz"] = 1.9

    with pytest.raises(ValueError, match="duration_ms must be positive"):
        audit_units(zero_duration)
    with pytest.raises(ValueError, match="spike_time_ms must be within"):
        audit_units(out_of_range_spike)
    with pytest.raises(ValueError, match="mean_rate_hz does not match"):
        audit_units(inconsistent_rate)


def test_T005_scientific_units_audit_real_result_integration():
    result = simulate(Experiment(duration=1, pulses=[]))

    report = audit_units(result)

    assert report["status"] == "pass"
    assert report["units"] == result["manifest"]["units"]
    assert report["mean_rate_hz"] == result["mean_rate_hz"]
