from neurosim.ui_contracts import firing_rate_chart

def test_firing_rate_chart_preserves_pairs():
    assert firing_rate_chart([0], [5]) == [(0, 5)]

