import pytest
from neurosim.omega_final import run_task


def test_T188_license_ownership_review_edge():
    with pytest.raises(ValueError):
        run_task("T188", {"input": {}})

