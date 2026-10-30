import pytest
from neurosim.omega_final import run_task


def test_T197_legacy_claim_cleanup_edge():
    with pytest.raises(ValueError):
        run_task("T197", {"input": {}})

