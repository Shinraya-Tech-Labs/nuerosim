from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T169_numerical_instability_warnings_unit():
    result = run_fixture(Path("tests/fixtures/omega/T169-numerical-instability-warnings/valid.json"))
    assert result["task"] == "T169"
    assert result["result"]["status"] == "pass"

