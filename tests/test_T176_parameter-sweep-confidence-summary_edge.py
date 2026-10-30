import pytest
from neurosim.omega_final import run_task


def test_T176_parameter_sweep_confidence_summary_edge():
    with pytest.raises(ValueError):
        run_task("T176", {"input": {}})

