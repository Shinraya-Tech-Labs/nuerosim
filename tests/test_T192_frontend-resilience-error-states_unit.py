from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T192_frontend_resilience_error_states_unit():
    result = run_fixture(Path("tests/fixtures/omega/T192-frontend-resilience-error-states/valid.json"))
    assert result["task"] == "T192"
    assert result["result"]["status"] == "pass"

