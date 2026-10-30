import pytest
from neurosim.omega_final import run_task


def test_T157_vectorized_lif_path_prototype_edge():
    with pytest.raises(ValueError):
        run_task("T157", {"input": {}})

