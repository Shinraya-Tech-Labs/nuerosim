import pytest
from neurosim.omega_final import run_task


def test_T185_dangerous_file_upload_checks_edge():
    with pytest.raises(ValueError):
        run_task("T185", {"input": {}})

