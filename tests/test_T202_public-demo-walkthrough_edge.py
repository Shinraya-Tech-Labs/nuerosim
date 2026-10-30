import pytest
from neurosim.omega_final import run_task


def test_T202_public_demo_walkthrough_edge():
    with pytest.raises(ValueError):
        run_task("T202", {"input": {}})

