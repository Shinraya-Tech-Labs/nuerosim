from neurosim.execution_tools import validate_archive

def test_archive_validation_rejects_missing_config():
    assert validate_archive([{"schema_version": 1}]) is False

