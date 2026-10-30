from neurosim.interop_tools import registry

def test_registry_accepts_empty_entries():
    assert registry({} if False else []) == {}

