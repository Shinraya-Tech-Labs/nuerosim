from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T194_cross_platform_ci_audit_unit():
    result = run_fixture(Path("tests/fixtures/omega/T194-cross-platform-ci-audit/valid.json"))
    assert result["task"] == "T194"
    assert result["result"]["status"] == "pass"

