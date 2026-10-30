from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T152_memory_rss_instrumentation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T152-memory-rss-instrumentation/valid.json"))
    assert result["task"] == "T152"
    assert result["result"]["status"] == "pass"

