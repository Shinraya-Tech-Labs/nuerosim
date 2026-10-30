import pytest
from neurosim.omega_final import run_task


def test_T171_intertrial_seed_variability_edge():
    with pytest.raises(ValueError):
        run_task("T171", {"input": {}})

