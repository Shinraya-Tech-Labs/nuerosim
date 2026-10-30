import pytest
from neurosim.omega_final import run_task


def test_T198_scientific_model_catalogue_final_edge():
    with pytest.raises(ValueError):
        run_task("T198", {"input": {}})

