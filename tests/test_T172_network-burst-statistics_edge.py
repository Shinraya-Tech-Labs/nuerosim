import pytest
from neurosim.omega_final import run_task


def test_T172_network_burst_statistics_edge():
    with pytest.raises(ValueError):
        run_task("T172", {"input": {}})

