import pytest
from neurosim.omega_final import run_task


def test_T200_cross_simulator_comparison_report_edge():
    with pytest.raises(ValueError):
        run_task("T200", {"input": {}})

