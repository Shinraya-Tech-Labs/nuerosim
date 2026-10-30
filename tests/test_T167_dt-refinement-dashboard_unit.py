from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T167_dt_refinement_dashboard_unit():
    result = run_fixture(Path("tests/fixtures/omega/T167-dt-refinement-dashboard/valid.json"))
    assert result["task"] == "T167"
    assert result["result"]["status"] == "pass"

