import pytest
from neurosim.omega_final import run_task


def test_T180_scientific_validation_report_edge():
    with pytest.raises(ValueError):
        run_task("T180", {"input": {}})

