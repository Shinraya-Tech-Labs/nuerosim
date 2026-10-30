import pytest
from neurosim.omega_final import run_task


def test_T175_parameter_sensitivity_one_at_a_time_edge():
    with pytest.raises(ValueError):
        run_task("T175", {"input": {}})

