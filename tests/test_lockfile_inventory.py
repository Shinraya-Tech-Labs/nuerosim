import json
from pathlib import Path

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
