from neurosim.ui_contracts import comparison_matrix

def test_comparison_matrix_uses_labels():
    assert comparison_matrix([{"label": "first"}]) == [["first"]]

