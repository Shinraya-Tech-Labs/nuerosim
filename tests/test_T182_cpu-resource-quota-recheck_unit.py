from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T182_cpu_resource_quota_recheck_unit():
    result = run_fixture(Path("tests/fixtures/omega/T182-cpu-resource-quota-recheck/valid.json"))
    assert result["task"] == "T182"
    assert result["result"]["status"] == "pass"

