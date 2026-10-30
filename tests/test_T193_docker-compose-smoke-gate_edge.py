import pytest
from neurosim.omega_final import run_task


def test_T193_docker_compose_smoke_gate_edge():
    with pytest.raises(ValueError):
        run_task("T193", {"input": {}})

