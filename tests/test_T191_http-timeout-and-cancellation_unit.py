from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T191_http_timeout_and_cancellation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T191-http-timeout-and-cancellation/valid.json"))
    assert result["task"] == "T191"
    assert result["result"]["status"] == "pass"

