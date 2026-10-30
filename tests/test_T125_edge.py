from neurosim.execution_tools import cancellation

def test_cancellation_false_stays_false():
    assert cancellation(False) is False

