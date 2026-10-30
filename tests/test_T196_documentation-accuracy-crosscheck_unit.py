from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T196_documentation_accuracy_crosscheck_unit():
    result = run_fixture(Path("tests/fixtures/omega/T196-documentation-accuracy-crosscheck/valid.json"))
    assert result["task"] == "T196"
    assert result["result"]["status"] == "pass"

