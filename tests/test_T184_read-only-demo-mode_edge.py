import pytest
from neurosim.omega_final import run_task


def test_T184_read_only_demo_mode_edge():
    with pytest.raises(ValueError):
        run_task("T184", {"input": {}})

