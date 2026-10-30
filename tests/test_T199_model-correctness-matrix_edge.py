import pytest
from neurosim.omega_final import run_task


def test_T199_model_correctness_matrix_edge():
    with pytest.raises(ValueError):
        run_task("T199", {"input": {}})

