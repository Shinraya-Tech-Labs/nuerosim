import pytest
from neurosim.omega_final import run_task


def test_T205_integration_test_full_run_edge():
    with pytest.raises(ValueError):
        run_task("T205", {"input": {}})

