import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T033-izhikevich-regular-spiking/valid.json'
def test_T033_izhikevich_regular_spiking_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert len(r['spikes'][0])==f['expected_spike_count'];assert r['manifest']['config']['model']=='izhikevich'
