import pytest
from neurosim.omega_final import run_task


def test_T206_windows_clean_install_validation_edge():
    with pytest.raises(ValueError):
        run_task("T206", {"input": {}})

