from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T200_cross_simulator_comparison_report_unit():
    result = run_fixture(Path("tests/fixtures/omega/T200-cross-simulator-comparison-report/valid.json"))
    assert result["task"] == "T200"
    assert result["result"]["status"] == "pass"

