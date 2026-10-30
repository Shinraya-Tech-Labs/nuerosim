from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T204_educator_workshop_walkthrough_unit():
    result = run_fixture(Path("tests/fixtures/omega/T204-educator-workshop-walkthrough/valid.json"))
    assert result["task"] == "T204"
    assert result["result"]["status"] == "pass"

