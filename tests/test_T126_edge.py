from neurosim.execution_tools import queue_state

def test_queue_state_empty():
    assert queue_state([]) == {"pending": 0, "items": []}

