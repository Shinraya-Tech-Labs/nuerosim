from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T205_integration_test_full_run_unit():
    result = run_fixture(Path("tests/fixtures/omega/T205-integration-test-full-run/valid.json"))
    assert result["task"] == "T205"
    assert result["result"]["status"] == "pass"

