from neurosim.interop_tools import license_provenance

def test_license_provenance_keeps_source():
    assert license_provenance("x", "MIT", "catalog")["source"] == "catalog"

