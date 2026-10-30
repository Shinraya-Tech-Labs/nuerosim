import pytest
from neurosim.omega_final import run_task


def test_T160_profiling_flamegraph_capture_edge():
    with pytest.raises(ValueError):
        run_task("T160", {"input": {}})

