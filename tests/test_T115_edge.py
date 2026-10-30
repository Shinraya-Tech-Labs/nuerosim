from neurosim.interop_tools import tolerance_matrix

def test_tolerance_matrix_empty_axis_is_empty():
    assert tolerance_matrix([], [0.1]) == []

