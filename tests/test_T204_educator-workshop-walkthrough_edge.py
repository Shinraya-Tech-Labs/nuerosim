import pytest
from neurosim.omega_final import run_task


def test_T204_educator_workshop_walkthrough_edge():
    with pytest.raises(ValueError):
        run_task("T204", {"input": {}})

