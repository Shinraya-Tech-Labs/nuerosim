import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T039-passive-rc-neuron/valid.json'
def test_T039_passive_rc_neuron_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert r['manifest']['config']['model']=='cable';assert r['final_state'][0][0]<-50
