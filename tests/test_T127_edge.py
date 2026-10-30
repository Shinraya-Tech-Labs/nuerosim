from neurosim.execution_tools import grid_sweep

def test_grid_sweep_keeps_duplicate_values():
    assert grid_sweep([1, 1]) == [{"value": 1}, {"value": 1}]

