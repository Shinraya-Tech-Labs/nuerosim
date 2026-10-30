from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T168_solver_comparison_cards_unit():
    result = run_fixture(Path("tests/fixtures/omega/T168-solver-comparison-cards/valid.json"))
    assert result["task"] == "T168"
    assert result["result"]["status"] == "pass"

