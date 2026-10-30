import pytest
from neurosim.omega_final import run_task


def test_T209_release_artifact_checksum_edge():
    with pytest.raises(ValueError):
        run_task("T209", {"input": {}})

