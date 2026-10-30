from neurosim.execution_tools import assign_seeds

def test_assign_seeds_zero_count():
    assert assign_seeds(10, 0) == []

