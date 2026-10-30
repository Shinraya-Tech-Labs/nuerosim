from neurosim.ui_contracts import morphology_view

def test_morphology_view_preserves_edges():
    assert morphology_view([{"id": 1}], [(1, 1)])["edges"] == [(1, 1)]

