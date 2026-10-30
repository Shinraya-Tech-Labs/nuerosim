from neurosim.ui_contracts import stdp_trajectory

def test_stdp_trajectory_preserves_pairs():
    assert stdp_trajectory([0, 1], [1, 2]) == [(0, 1), (1, 2)]

