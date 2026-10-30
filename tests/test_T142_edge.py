from neurosim.ui_contracts import arrow_edges

def test_arrow_edges_marks_every_edge_directed():
    assert all(edge["directed"] for edge in arrow_edges([(0, 1), (1, 2)]))

