from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T158_batch_spike_scheduling_prototype_unit():
    result = run_fixture(Path("tests/fixtures/omega/T158-batch-spike-scheduling-prototype/valid.json"))
    assert result["task"] == "T158"
    assert result["result"]["status"] == "pass"

