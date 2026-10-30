import json
import os
import subprocess
import sys
from pathlib import Path


def test_T205_integration_test_full_run_cli_integration():
    fixture = Path("tests/fixtures/omega/T205-integration-test-full-run/valid.json")
    env = os.environ | {"PYTHONPATH": str(Path("python").resolve())}
    run = subprocess.run([sys.executable, "-m", "neurosim.omega_final", "--fixture", str(fixture)], env=env, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout)["task"] == "T205"

