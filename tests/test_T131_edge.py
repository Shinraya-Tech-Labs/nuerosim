from neurosim.execution_tools import manifest_hash

def test_manifest_hash_is_key_order_stable():
    assert manifest_hash({"a": 1, "b": 2}) == manifest_hash({"b": 2, "a": 1})

