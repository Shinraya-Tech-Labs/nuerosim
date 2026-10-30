import pytest
from neurosim.omega_final import run_task


def test_T164_cpu_gpu_claims_boundary_report_edge():
    with pytest.raises(ValueError):
        run_task("T164", {"input": {}})

