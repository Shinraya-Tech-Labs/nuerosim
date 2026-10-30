from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T203_researcher_api_examples_unit():
    result = run_fixture(Path("tests/fixtures/omega/T203-researcher-api-examples/valid.json"))
    assert result["task"] == "T203"
    assert result["result"]["status"] == "pass"

