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
