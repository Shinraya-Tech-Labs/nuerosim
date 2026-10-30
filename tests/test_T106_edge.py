from neurosim.interop_tools import reference_setup

def test_brian2_reference_is_explicitly_optional():
    result = reference_setup("Brian2", "lif")
    assert result["simulator"] == "Brian2" and result["status"] == "optional"

