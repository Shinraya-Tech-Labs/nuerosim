from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T197_legacy_claim_cleanup_unit():
    result = run_fixture(Path("tests/fixtures/omega/T197-legacy-claim-cleanup/valid.json"))
    assert result["task"] == "T197"
    assert result["result"]["status"] == "pass"

