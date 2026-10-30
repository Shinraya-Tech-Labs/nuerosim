from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T210_release_readiness_verdict_unit():
    result = run_fixture(Path("tests/fixtures/omega/T210-release-readiness-verdict/valid.json"))
    assert result["task"] == "T210"
    assert result["result"]["status"] == "pass"

