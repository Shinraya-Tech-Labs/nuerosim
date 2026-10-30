import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
F=Path(__file__).parent/'fixtures/omega/T037-adaptive-lif-baseline-refinement/valid.json'
def test_T037_adaptive_lif_baseline_refinement_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert len(r['spikes'][0])==0;assert r['manifest']['config']['parameters']['noise_std']==0
