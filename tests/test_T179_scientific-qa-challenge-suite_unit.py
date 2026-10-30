from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T179_scientific_qa_challenge_suite_unit():
    result = run_fixture(Path("tests/fixtures/omega/T179-scientific-qa-challenge-suite/valid.json"))
    assert result["task"] == "T179"
    assert result["result"]["status"] == "pass"

