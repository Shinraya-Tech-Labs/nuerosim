import pytest
from neurosim.omega_final import run_task


def test_T161_128_neuron_regression_budget_edge():
    with pytest.raises(ValueError):
        run_task("T161", {"input": {}})

