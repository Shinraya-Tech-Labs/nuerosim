import pytest
from neurosim.omega_final import run_task


def test_T183_auth_mode_design_for_public_demo_edge():
    with pytest.raises(ValueError):
        run_task("T183", {"input": {}})

