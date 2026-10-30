from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T151_performance_benchmark_baseline_unit():
    result = run_fixture(Path("tests/fixtures/omega/T151-performance-benchmark-baseline/valid.json"))
    assert result["task"] == "T151"
    assert result["result"]["status"] == "pass"

