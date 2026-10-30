from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T190_database_migration_rehearsal_unit():
    result = run_fixture(Path("tests/fixtures/omega/T190-database-migration-rehearsal/valid.json"))
    assert result["task"] == "T190"
    assert result["result"]["status"] == "pass"

