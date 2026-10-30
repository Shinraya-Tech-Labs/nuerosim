from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T175_parameter_sensitivity_one_at_a_time_unit():
    result = run_fixture(Path("tests/fixtures/omega/T175-parameter-sensitivity-one-at-a-time/valid.json"))
    assert result["task"] == "T175"
    assert result["result"]["status"] == "pass"

