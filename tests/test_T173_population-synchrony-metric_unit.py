from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T173_population_synchrony_metric_unit():
    result = run_fixture(Path("tests/fixtures/omega/T173-population-synchrony-metric/valid.json"))
    assert result["task"] == "T173"
    assert result["result"]["status"] == "pass"

