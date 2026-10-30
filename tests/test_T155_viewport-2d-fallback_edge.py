import pytest
from neurosim.omega_final import run_task


def test_T155_viewport_2d_fallback_edge():
    with pytest.raises(ValueError):
        run_task("T155", {"input": {}})

