from neurosim.interop_tools import reference_setup

def test_arbor_passive_cable_scope():
    assert reference_setup("Arbor", "passive-cable")["status"] == "optional"

