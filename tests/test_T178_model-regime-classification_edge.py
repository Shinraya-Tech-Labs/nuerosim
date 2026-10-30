import pytest
from neurosim.omega_final import run_task


def test_T178_model_regime_classification_edge():
    with pytest.raises(ValueError):
        run_task("T178", {"input": {}})

