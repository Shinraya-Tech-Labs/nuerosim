from neurosim.execution_tools import chunk

def test_chunk_exact_multiple():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

