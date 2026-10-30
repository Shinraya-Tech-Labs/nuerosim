from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T209_release_artifact_checksum_unit():
    result = run_fixture(Path("tests/fixtures/omega/T209-release-artifact-checksum/valid.json"))
    assert result["task"] == "T209"
    assert result["result"]["status"] == "pass"

