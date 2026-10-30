import pytest
from neurosim.omega_final import run_task


def test_T210_release_readiness_verdict_edge():
    with pytest.raises(ValueError):
        run_task("T210", {"input": {}})

