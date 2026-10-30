import pytest
from neurosim.omega_final import run_task


def test_T190_database_migration_rehearsal_edge():
    with pytest.raises(ValueError):
        run_task("T190", {"input": {}})

