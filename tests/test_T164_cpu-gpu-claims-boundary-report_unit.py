from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T164_cpu_gpu_claims_boundary_report_unit():
    result = run_fixture(Path("tests/fixtures/omega/T164-cpu-gpu-claims-boundary-report/valid.json"))
    assert result["task"] == "T164"
    assert result["result"]["status"] == "pass"

