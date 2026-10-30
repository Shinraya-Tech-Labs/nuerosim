import pytest
from neurosim.omega_final import run_task


def test_T152_memory_rss_instrumentation_edge():
    with pytest.raises(ValueError):
        run_task("T152", {"input": {}})

