from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T159_sparse_event_queue_microbench_unit():
    result = run_fixture(Path("tests/fixtures/omega/T159-sparse-event-queue-microbench/valid.json"))
    assert result["task"] == "T159"
    assert result["result"]["status"] == "pass"

