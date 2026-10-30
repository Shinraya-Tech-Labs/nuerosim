import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T036-morris-lecar/valid.json'
def test_T036_morris_lecar_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert len(r['spikes'][0])==f['expected_spike_count'];assert all(map(lambda x: x==x,r['voltage'][0]));assert r['manifest']['config']['model']=='morris_lecar'
