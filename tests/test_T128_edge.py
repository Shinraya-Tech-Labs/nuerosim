from neurosim.execution_tools import random_sweep

def test_random_sweep_respects_bounds():
    values = random_sweep(2, 10, low=-1, high=1)
    assert all(-1 <= value <= 1 for value in values)

