"""Inventory hashes for recognized lockfiles in a Git commit."""

import hashlib
import json
import subprocess
import sys
from pathlib import PurePosixPath

from neurosim.repo_inventory import inventory as tracked_tree_inventory


def is_lockfile(path: str) -> bool:
    name = PurePosixPath(path).name
    return name.endswith(".lock") or name == "package-lock.json"


def summarize_blobs(blobs: dict[str, bytes], revision: str) -> dict[str, object]:
    lockfiles = [
        {
            "path": path,
            "size_bytes": len(contents),
            "sha256": hashlib.sha256(contents).hexdigest(),
        }
        for path, contents in sorted(blobs.items())
        if is_lockfile(path)
    ]
    return {
        "revision": revision,
        "lockfile_count": len(lockfiles),
        "lockfiles": lockfiles,
    }


def inventory(revision: str = "HEAD") -> dict[str, object]:
    tree = tracked_tree_inventory(revision)
    blobs = {}
    for path in tree["paths"]:
        if is_lockfile(path):
            try:
                blob = subprocess.run(
                    ["git", "show", f"{tree['revision']}:{path}"],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                raise ValueError(f"unable to read tracked lockfile: {path}") from None
            blobs[path] = blob.stdout
    return summarize_blobs(blobs, tree["revision"])


def main() -> None:
    revision = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    try:
        result = inventory(revision)
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"lockfile inventory: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    json.dump(result, sys.stdout, indent=2, sort_keys=True, ensure_ascii=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
