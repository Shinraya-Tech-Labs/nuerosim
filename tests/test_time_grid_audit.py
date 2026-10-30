import json, os, subprocess, sys
from pathlib import Path
import pytest
from neurosim.time_grid_audit import audit
ROOT=Path(__file__).resolve().parents[1]; FIX=ROOT/'tests/fixtures/omega/T029-time-grid-and-sampling-conventions'
def test_T029_time_grid_and_sampling_conventions_unit():
 f=json.loads((FIX/'valid.json').read_text());r=audit(f['experiment']);assert r['passed'];assert r['final_time_included'];assert len(r['times_ms'])==11;assert r['max_grid_error_ms']<1e-12
def test_nonintegral_duration_fixture_is_rejected():
 f=json.loads((FIX/'invalid.json').read_text())
 from neurosim.workbench.config import Experiment
 with pytest.raises(Exception,match=f['expected_error']): Experiment.model_validate(f['experiment'])
def test_cli_runs_fixture(tmp_path):
 out=tmp_path/'grid.json'; subprocess.run([sys.executable,'-m','neurosim.time_grid_audit',str(FIX/'valid.json'),'--output',str(out)],cwd=ROOT,env={**os.environ,'PYTHONPATH':'python'},check=True,capture_output=True,text=True);assert json.loads(out.read_text())['passed']
