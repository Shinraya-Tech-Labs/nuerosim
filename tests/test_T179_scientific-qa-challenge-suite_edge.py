import pytest
from neurosim.omega_final import run_task


def test_T179_scientific_qa_challenge_suite_edge():
    with pytest.raises(ValueError):
        run_task("T179", {"input": {}})

