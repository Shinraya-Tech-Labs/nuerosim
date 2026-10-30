from neurosim.interop_tools import integration_suite

def test_integration_suite_handles_empty_cases():
    assert integration_suite([]) == {"case_count": 0, "cases": []}

