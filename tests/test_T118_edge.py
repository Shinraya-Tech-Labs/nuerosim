from neurosim.interop_tools import discrepancy

def test_discrepancy_keeps_label():
    assert discrepancy("voltage", 0, 0)["label"] == "voltage"

