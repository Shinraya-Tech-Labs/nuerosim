import pytest
from neurosim.omega_final import run_task


def test_T181_api_rate_limit_validation_edge():
    with pytest.raises(ValueError):
        run_task("T181", {"input": {}})

