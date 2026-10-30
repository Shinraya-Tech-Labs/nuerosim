import pytest
from neurosim.omega_final import run_task


def test_T154_viewport_lod_policy_edge():
    with pytest.raises(ValueError):
        run_task("T154", {"input": {}})

