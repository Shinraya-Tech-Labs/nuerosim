from neurosim.interop_tools import reference_setup

def test_no_synapse_scope_is_preserved():
    assert reference_setup("Brian2", "lif-no-synapse")["scope"] == "lif-no-synapse"

