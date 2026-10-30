import pytest
from neurosim.omega_final import run_task


def test_T153_network_edge_render_selection_edge():
    with pytest.raises(ValueError):
        run_task("T153", {"input": {}})

