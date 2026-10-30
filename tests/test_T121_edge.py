from neurosim.execution_tools import parse_v2

def test_parse_v2_normalizes_existing_schema():
    assert parse_v2({"schema_version": 1})["schema_version"] == 2

