import pytest
from neurosim.omega_final import run_task


def test_T159_sparse_event_queue_microbench_edge():
    with pytest.raises(ValueError):
        run_task("T159", {"input": {}})

