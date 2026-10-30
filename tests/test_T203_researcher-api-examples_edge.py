import pytest
from neurosim.omega_final import run_task


def test_T203_researcher_api_examples_edge():
    with pytest.raises(ValueError):
        run_task("T203", {"input": {}})

