import pytest
from neurosim.omega_final import run_task


def test_T151_performance_benchmark_baseline_edge():
    with pytest.raises(ValueError):
        run_task("T151", {"input": {}})

