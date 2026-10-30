import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from neurosim.workbench.config import Experiment

FIX=Path(__file__).parent/'fixtures/omega/T030-solver-selection-ux'

def test_T030_solver_selection_ux_unit():
    fixture=json.loads((FIX/'valid.json').read_text())
    assert fixture['default']=='rk4'
    assert Experiment(solver='rk4',model='lif',pulses=[]).solver=='rk4'
    assert Experiment(solver='euler',model='lif',pulses=[]).solver=='euler'

def test_invalid_solver_fixture_rejected():
    fixture=json.loads((FIX/'invalid.json').read_text())
    with pytest.raises(ValidationError,match='rk4'):
        Experiment(solver=fixture['solver'])

def test_hh_euler_dt_limit_is_enforced():
    with pytest.raises(ValidationError,match='HH Euler requires dt'):
        Experiment(model='hh',solver='euler',dt=.025)
