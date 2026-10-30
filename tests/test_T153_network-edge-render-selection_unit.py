from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T153_network_edge_render_selection_unit():
    result = run_fixture(Path("tests/fixtures/omega/T153-network-edge-render-selection/valid.json"))
    assert result["task"] == "T153"
    assert result["result"]["status"] == "pass"

