from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T195_deployment_hardening_report_unit():
    result = run_fixture(Path("tests/fixtures/omega/T195-deployment-hardening-report/valid.json"))
    assert result["task"] == "T195"
    assert result["result"]["status"] == "pass"

