import json
from pathlib import Path
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
import pytest
F=Path(__file__).parent/'fixtures/omega/T032-quadratic-integrate-and-fire/valid.json'
def test_T032_quadratic_integrate_and_fire_unit():
 f=json.loads(F.read_text());r=simulate(Experiment.model_validate(f['experiment']));assert r['spikes'][0]==pytest.approx(f['expected_spikes_ms'],abs=1e-12);assert r['manifest']['config']['model']=='qif'
