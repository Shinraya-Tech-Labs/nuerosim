import pytest
from neurosim.omega_final import run_task


def test_T191_http_timeout_and_cancellation_edge():
    with pytest.raises(ValueError):
        run_task("T191", {"input": {}})

