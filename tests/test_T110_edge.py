from neurosim.interop_tools import discrepancy

def test_delay_discrepancy_is_signed():
    assert discrepancy("delay", 2, 1)["delta"] == -1

