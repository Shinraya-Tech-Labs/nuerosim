import pytest
from neurosim.omega_final import run_task


def test_T168_solver_comparison_cards_edge():
    with pytest.raises(ValueError):
        run_task("T168", {"input": {}})

