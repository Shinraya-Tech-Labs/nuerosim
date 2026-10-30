import pytest
from neurosim.omega_final import run_task


def test_T166_input_current_fi_curves_edge():
    with pytest.raises(ValueError):
        run_task("T166", {"input": {}})

