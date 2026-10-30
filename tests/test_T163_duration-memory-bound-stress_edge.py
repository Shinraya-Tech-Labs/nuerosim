import pytest
from neurosim.omega_final import run_task


def test_T163_duration_memory_bound_stress_edge():
    with pytest.raises(ValueError):
        run_task("T163", {"input": {}})

