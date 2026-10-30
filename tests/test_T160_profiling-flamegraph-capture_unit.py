from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T160_profiling_flamegraph_capture_unit():
    result = run_fixture(Path("tests/fixtures/omega/T160-profiling-flamegraph-capture/valid.json"))
    assert result["task"] == "T160"
    assert result["result"]["status"] == "pass"

