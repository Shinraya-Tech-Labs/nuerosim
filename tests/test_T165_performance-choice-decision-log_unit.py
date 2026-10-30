from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T165_performance_choice_decision_log_unit():
    result = run_fixture(Path("tests/fixtures/omega/T165-performance-choice-decision-log/valid.json"))
    assert result["task"] == "T165"
    assert result["result"]["status"] == "pass"

