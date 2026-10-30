import pytest
from neurosim.omega_final import run_task


def test_T169_numerical_instability_warnings_edge():
    with pytest.raises(ValueError):
        run_task("T169", {"input": {}})

