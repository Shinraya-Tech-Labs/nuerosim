from neurosim.execution_tools import progress_events

def test_progress_events_zero_total_is_complete():
    assert progress_events(0) == [{"step": 0, "fraction": 1}]

