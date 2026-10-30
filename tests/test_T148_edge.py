from neurosim.ui_contracts import svg_metadata

def test_svg_metadata_supports_physical_units():
    assert svg_metadata(10, 20, "mm")["units"] == "mm"

