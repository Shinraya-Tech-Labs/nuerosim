"""Read-only inventory of paths tracked by a Git commit."""

import json
import subprocess
import sys
from collections import Counter
from pathlib import PurePosixPath


def summarize_paths(paths: list[str], revision: str) -> dict[str, object]:
    paths = sorted(paths)
    return {
        "revision": revision,
        "tracked_files": len(paths),
        "by_top_level": dict(
            sorted(Counter(path.split("/", 1)[0] if "/" in path else "." for path in paths).items())
        ),
        "by_extension": dict(
            sorted(Counter(PurePosixPath(path).suffix for path in paths).items())
        ),
        "paths": paths,
    }


def inventory(revision: str = "HEAD") -> dict[str, object]:
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if resolved.returncode:
        raise ValueError("revision must resolve to a commit")

    tree = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "-z", resolved.stdout.strip()],
        check=True,
        capture_output=True,
    )
    paths = tree.stdout.decode("utf-8", errors="surrogateescape").rstrip("\0").split("\0")
    if paths == [""]:
        paths = []
    return summarize_paths(paths, resolved.stdout.strip())


def main() -> None:
    revision = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    try:
        result = inventory(revision)
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"repo inventory: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    json.dump(result, sys.stdout, indent=2, sort_keys=True, ensure_ascii=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
