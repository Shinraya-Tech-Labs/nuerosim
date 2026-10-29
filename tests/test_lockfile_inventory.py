import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from neurosim.lockfile_inventory import summarize_blobs


def test_T002_environment_reproducibility_lockfile_inventory_unit():
    fixture = json.loads(
        Path(
            "tests/fixtures/omega/T002-environment-reproducibility-lockfile-inventory/valid.json"
        ).read_text(encoding="utf-8")
    )
    blobs = {item["path"]: item["contents"].encode("utf-8") for item in fixture["blobs"]}

    assert summarize_blobs(blobs, fixture["revision"]) == fixture["expected"]


def test_T002_environment_reproducibility_lockfile_inventory_empty_blob_boundary():
    assert summarize_blobs({"requirements-empty.lock": b""}, "empty-blob") == {
        "revision": "empty-blob",
        "lockfile_count": 1,
        "lockfiles": [
            {
                "path": "requirements-empty.lock",
                "size_bytes": 0,
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            }
        ],
    }


def test_T002_environment_reproducibility_lockfile_inventory_cli_integration():
    root = Path(__file__).resolve().parents[1]
    env = os.environ | {"PYTHONPATH": str(root / "python")}
    valid = subprocess.run(
        [sys.executable, "-m", "neurosim.lockfile_inventory", "HEAD"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert valid.returncode == 0, valid.stderr
    output = json.loads(valid.stdout)
    for record in output["lockfiles"]:
        blob = subprocess.run(
            ["git", "show", f"{output['revision']}:{record['path']}"],
            cwd=root,
            capture_output=True,
            check=True,
        ).stdout
        assert record["size_bytes"] == len(blob)
        assert record["sha256"] == hashlib.sha256(blob).hexdigest()
    assert output["lockfile_count"] == len(output["lockfiles"])

    fixture = json.loads(
        (
            root
            / "tests/fixtures/omega/T002-environment-reproducibility-lockfile-inventory/invalid.json"
        ).read_text(encoding="utf-8")
    )
    invalid = subprocess.run(
        [sys.executable, "-m", "neurosim.lockfile_inventory", fixture["revision"]],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert invalid.returncode == 2
    assert fixture["expected_error"] in invalid.stderr
