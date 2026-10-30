from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T181_api_rate_limit_validation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T181-api-rate-limit-validation/valid.json"))
    assert result["task"] == "T181"
    assert result["result"]["status"] == "pass"

