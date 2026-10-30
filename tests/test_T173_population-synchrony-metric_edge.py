import pytest
from neurosim.omega_final import run_task


def test_T173_population_synchrony_metric_edge():
    with pytest.raises(ValueError):
        run_task("T173", {"input": {}})

