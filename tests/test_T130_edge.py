from neurosim.execution_tools import aggregate

def test_aggregate_empty_values_are_explicit():
    assert aggregate({} if False else []) == {"count": 0, "mean": None, "min": None, "max": None}

