from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T176_parameter_sweep_confidence_summary_unit():
    result = run_fixture(Path("tests/fixtures/omega/T176-parameter-sweep-confidence-summary/valid.json"))
    assert result["task"] == "T176"
    assert result["result"]["status"] == "pass"

