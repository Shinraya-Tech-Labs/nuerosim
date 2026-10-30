from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T163_duration_memory_bound_stress_unit():
    result = run_fixture(Path("tests/fixtures/omega/T163-duration-memory-bound-stress/valid.json"))
    assert result["task"] == "T163"
    assert result["result"]["status"] == "pass"

