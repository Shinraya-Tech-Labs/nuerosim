import pytest
from neurosim.omega_final import run_task


def test_T187_sbom_generation_edge():
    with pytest.raises(ValueError):
        run_task("T187", {"input": {}})

