from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T170_spike_time_jitter_evaluator_unit():
    result = run_fixture(Path("tests/fixtures/omega/T170-spike-time-jitter-evaluator/valid.json"))
    assert result["task"] == "T170"
    assert result["result"]["status"] == "pass"

