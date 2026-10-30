from neurosim.ui_contracts import current_plot

def test_current_plot_zips_to_shortest_series():
    assert current_plot([0, 1], [2]) == [{"time_ms": 0, "current": 2}]

