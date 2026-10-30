from neurosim.ui_contracts import refractory_overlay

def test_refractory_overlay_handles_multiple_spikes():
    assert refractory_overlay([1, 4], 2)[1]["end_ms"] == 6

