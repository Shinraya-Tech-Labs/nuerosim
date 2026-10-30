import pytest
from neurosim.omega_final import run_task


def test_T192_frontend_resilience_error_states_edge():
    with pytest.raises(ValueError):
        run_task("T192", {"input": {}})

