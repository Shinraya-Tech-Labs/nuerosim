from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T188_license_ownership_review_unit():
    result = run_fixture(Path("tests/fixtures/omega/T188-license-ownership-review/valid.json"))
    assert result["task"] == "T188"
    assert result["result"]["status"] == "pass"

