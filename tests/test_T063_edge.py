from neurosim.plasticity_metrics import multiplicative_bound
def test_T063_edge(): assert 0<=multiplicative_bound(2,.1)<=1
