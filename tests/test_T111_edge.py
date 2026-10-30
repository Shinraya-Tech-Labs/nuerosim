from neurosim.interop_tools import reference_setup

def test_neuron_setup_is_optional():
    assert reference_setup("NEURON", "optional")["simulator"] == "NEURON"

