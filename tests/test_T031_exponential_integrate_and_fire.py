import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
FIX=Path(__file__).parent/'fixtures/omega/T031-exponential-integrate-and-fire'
def test_T031_exponential_integrate_and_fire_unit():
 f=json.loads((FIX/'valid.json').read_text());c=Experiment.model_validate(f['experiment']);r=simulate(c);assert r['spikes'][0]==f['expected_spikes_ms'];assert r['manifest']['config']['model']=='eif'
def test_unknown_model_rejected():
 f=json.loads((FIX/'invalid.json').read_text())
 with pytest.raises(ValidationError): Experiment(model='unknown')
