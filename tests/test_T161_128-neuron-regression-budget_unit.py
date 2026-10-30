from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T161_128_neuron_regression_budget_unit():
    result = run_fixture(Path("tests/fixtures/omega/T161-128-neuron-regression-budget/valid.json"))
    assert result["task"] == "T161"
    assert result["result"]["status"] == "pass"

