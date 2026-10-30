import pytest
from neurosim.omega_final import run_task


def test_T195_deployment_hardening_report_edge():
    with pytest.raises(ValueError):
        run_task("T195", {"input": {}})

