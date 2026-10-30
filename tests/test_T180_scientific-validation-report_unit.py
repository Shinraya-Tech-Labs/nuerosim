from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T180_scientific_validation_report_unit():
    result = run_fixture(Path("tests/fixtures/omega/T180-scientific-validation-report/valid.json"))
    assert result["task"] == "T180"
    assert result["result"]["status"] == "pass"

