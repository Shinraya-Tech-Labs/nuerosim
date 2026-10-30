from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T166_input_current_fi_curves_unit():
    result = run_fixture(Path("tests/fixtures/omega/T166-input-current-fi-curves/valid.json"))
    assert result["task"] == "T166"
    assert result["result"]["status"] == "pass"

