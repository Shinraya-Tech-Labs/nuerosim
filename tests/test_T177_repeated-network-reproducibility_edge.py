import pytest
from neurosim.omega_final import run_task


def test_T177_repeated_network_reproducibility_edge():
    with pytest.raises(ValueError):
        run_task("T177", {"input": {}})

