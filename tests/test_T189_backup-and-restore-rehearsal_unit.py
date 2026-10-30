from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T189_backup_and_restore_rehearsal_unit():
    result = run_fixture(Path("tests/fixtures/omega/T189-backup-and-restore-rehearsal/valid.json"))
    assert result["task"] == "T189"
    assert result["result"]["status"] == "pass"

