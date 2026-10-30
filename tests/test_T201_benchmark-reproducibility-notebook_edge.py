import pytest
from neurosim.omega_final import run_task


def test_T201_benchmark_reproducibility_notebook_edge():
    with pytest.raises(ValueError):
        run_task("T201", {"input": {}})

