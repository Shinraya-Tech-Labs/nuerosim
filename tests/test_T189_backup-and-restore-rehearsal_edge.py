import pytest
from neurosim.omega_final import run_task


def test_T189_backup_and_restore_rehearsal_edge():
    with pytest.raises(ValueError):
        run_task("T189", {"input": {}})

