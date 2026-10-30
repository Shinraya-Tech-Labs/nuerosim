import json
import os
import subprocess
import sys
from pathlib import Path


def test_T196_documentation_accuracy_crosscheck_cli_integration():
    fixture = Path("tests/fixtures/omega/T196-documentation-accuracy-crosscheck/valid.json")
    env = os.environ | {"PYTHONPATH": str(Path("python").resolve())}
    run = subprocess.run([sys.executable, "-m", "neurosim.omega_final", "--fixture", str(fixture)], env=env, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout)["task"] == "T196"

