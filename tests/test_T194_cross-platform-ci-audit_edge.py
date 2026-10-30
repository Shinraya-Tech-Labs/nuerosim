import pytest
from neurosim.omega_final import run_task


def test_T194_cross_platform_ci_audit_edge():
    with pytest.raises(ValueError):
        run_task("T194", {"input": {}})

