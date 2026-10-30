from neurosim.interop_tools import seed_policy

def test_seed_policy_zero_count():
    assert seed_policy(7, 0) == []

