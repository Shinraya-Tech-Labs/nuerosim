import pytest
from neurosim.omega_final import run_task


def test_T182_cpu_resource_quota_recheck_edge():
    with pytest.raises(ValueError):
        run_task("T182", {"input": {}})

