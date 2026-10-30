from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T172_network_burst_statistics_unit():
    result = run_fixture(Path("tests/fixtures/omega/T172-network-burst-statistics/valid.json"))
    assert result["task"] == "T172"
    assert result["result"]["status"] == "pass"

