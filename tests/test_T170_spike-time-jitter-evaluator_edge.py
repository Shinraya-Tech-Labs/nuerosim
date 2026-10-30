import pytest
from neurosim.omega_final import run_task


def test_T170_spike_time_jitter_evaluator_edge():
    with pytest.raises(ValueError):
        run_task("T170", {"input": {}})

