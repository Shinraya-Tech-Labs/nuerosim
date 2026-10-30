import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T034-izhikevich-fast-spiking/valid.json'
def test_T034_izhikevich_fast_spiking_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert len(r['spikes'][0])==f['expected_spike_count'];assert r['spikes'][0][1]>r['spikes'][0][0]
