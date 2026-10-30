from neurosim.ui_contracts import compare_runs

def test_compare_runs_empty():
    assert compare_runs([]) == {"run_count": 0, "runs": []}

