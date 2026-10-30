from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T201_benchmark_reproducibility_notebook_unit():
    result = run_fixture(Path("tests/fixtures/omega/T201-benchmark-reproducibility-notebook/valid.json"))
    assert result["task"] == "T201"
    assert result["result"]["status"] == "pass"

