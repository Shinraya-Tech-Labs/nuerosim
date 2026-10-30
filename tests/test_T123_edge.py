import pytest
from neurosim.execution_tools import quota

def test_quota_rejects_over_limit():
    with pytest.raises(ValueError, match="quota exceeded"):
        quota(11, 10)

