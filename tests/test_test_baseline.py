import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.test_baseline import capture_baseline


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T011-test-baseline-capture"


def test_valid_fixture_captures_successful_command():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    command = [sys.executable, *fixture["command"][1:]]
    report = capture_baseline(command, cwd=ROOT, timeout=fixture["timeout_seconds"])
    expected = fixture["expected"]
    assert report["exit_code"] == expected["exit_code"]
    assert report["stdout_tail"] == expected["stdout_tail"]
    assert report["timed_out"] is expected["timed_out"]
    assert report["git_revision"]


def test_invalid_fixture_rejects_empty_command():
    fixture = json.loads((FIXTURES / "invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        capture_baseline(fixture["command"], timeout=fixture["timeout_seconds"])


def test_nonzero_exit_and_output_tail_are_preserved():
    report = capture_baseline(
        [sys.executable, "-c", "import sys; sys.stdout.write('x'*100); sys.exit(7)"],
        cwd=ROOT,
        output_limit=20,
    )
    assert report["exit_code"] == 7
    assert report["stdout_tail"] == "x" * 20
    assert report["stderr_tail"] == ""


def test_timeout_is_recorded_and_process_stopped():
    report = capture_baseline(
        [sys.executable, "-c", "import time; time.sleep(2)"], cwd=ROOT, timeout=1
    )
    assert report["timed_out"] is True
    assert report["exit_code"] == 124


def test_invalid_timeout_and_working_directory_are_rejected(tmp_path):
    with pytest.raises(ValueError, match="timeout must be"):
        capture_baseline([sys.executable, "-c", "pass"], timeout=0)
    with pytest.raises(ValueError, match="working directory does not exist"):
        capture_baseline([sys.executable, "-c", "pass"], cwd=tmp_path / "missing")


def test_zero_output_limit_returns_empty_tail():
    report = capture_baseline(
        [sys.executable, "-c", "print('discarded')"], cwd=ROOT, output_limit=0
    )
    assert report["stdout_tail"] == ""


def test_cli_emits_baseline_json():
    env = {**os.environ, "PYTHONPATH": "python"}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "neurosim.test_baseline",
            "--cwd",
            str(ROOT),
            "--",
            sys.executable,
            "-c",
            "import sys; sys.stdout.write('cli-ok')",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["exit_code"] == 0
    assert report["stdout_tail"] == "cli-ok"
