import pytest
from neurosim.omega_final import run_task


def test_T165_performance_choice_decision_log_edge():
    with pytest.raises(ValueError):
        run_task("T165", {"input": {}})

