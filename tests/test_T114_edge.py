from neurosim.interop_tools import integration_suite

def test_event_suite_keeps_case_order():
    cases = [{"event": 1}, {"event": 2}]
    assert integration_suite(cases)["cases"] == cases

