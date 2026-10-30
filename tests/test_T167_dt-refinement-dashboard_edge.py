import pytest
from neurosim.omega_final import run_task


def test_T167_dt_refinement_dashboard_edge():
    with pytest.raises(ValueError):
        run_task("T167", {"input": {}})

