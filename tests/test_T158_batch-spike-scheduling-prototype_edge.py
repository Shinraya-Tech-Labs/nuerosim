import pytest
from neurosim.omega_final import run_task


def test_T158_batch_spike_scheduling_prototype_edge():
    with pytest.raises(ValueError):
        run_task("T158", {"input": {}})

