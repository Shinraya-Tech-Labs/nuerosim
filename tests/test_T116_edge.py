from neurosim.interop_tools import match_spikes

def test_spike_matching_accepts_tolerance_boundary():
    assert match_spikes([1.0], [1.1], 0.1)

