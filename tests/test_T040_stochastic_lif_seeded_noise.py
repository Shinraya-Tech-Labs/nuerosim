import json
from pathlib import Path
import pytest
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T040-stochastic-lif-seeded-noise/valid.json'
def test_T040_stochastic_lif_seeded_noise_unit():
 f=json.loads(F.read_text());c=Experiment.model_validate(f['experiment']);a=simulate(c);b=simulate(c);assert a['final_state'][0][0]==pytest.approx(f['expected_final_voltage_mV']);assert a['voltage']==b['voltage']
