from neurosim.interop_tools import match_spikes

def test_spike_matching_rejects_length_mismatch():
    assert match_spikes([1], [1, 2], 0.1) is False

