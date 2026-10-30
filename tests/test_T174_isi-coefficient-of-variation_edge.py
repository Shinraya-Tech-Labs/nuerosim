import pytest
from neurosim.omega_final import run_task


def test_T174_isi_coefficient_of_variation_edge():
    with pytest.raises(ValueError):
        run_task("T174", {"input": {}})

