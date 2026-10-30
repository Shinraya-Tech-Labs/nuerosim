from neurosim.interop_tools import reference_setup

def test_pulse_scope_is_preserved():
    assert reference_setup("Brian2", "pulse")["scope"] == "pulse"

