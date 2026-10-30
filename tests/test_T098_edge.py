from neurosim.schema_tools import nwb_spikes
def test_T098_edge(): assert nwb_spikes([])['spike_times_ms']==[]
