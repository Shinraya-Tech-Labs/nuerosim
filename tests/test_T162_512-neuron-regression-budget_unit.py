from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T162_512_neuron_regression_budget_unit():
    result = run_fixture(Path("tests/fixtures/omega/T162-512-neuron-regression-budget/valid.json"))
    assert result["task"] == "T162"
    assert result["result"]["status"] == "pass"

