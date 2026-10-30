import pytest
from neurosim.omega_final import run_task


def test_T196_documentation_accuracy_crosscheck_edge():
    with pytest.raises(ValueError):
        run_task("T196", {"input": {}})

