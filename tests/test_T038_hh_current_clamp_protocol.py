import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T038-hh-current-clamp-protocol/valid.json'
def test_T038_hh_current_clamp_protocol_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert len(r['spikes'][0])==2;assert r['manifest']['config']['model']=='hh'
