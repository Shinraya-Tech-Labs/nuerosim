import pytest
from neurosim.execution_tools import validate_input

def test_input_validation_reports_missing_fields():
    with pytest.raises(ValueError, match="missing required fields"):
        validate_input({}, ("model",))

