"""Read-only map of supported and explicitly legacy project boundaries."""

import json
import subprocess
import sys
import tomllib

from neurosim.repo_inventory import inventory as tracked_tree_inventory


def parse_project_scripts(contents: str) -> dict[str, str]:
    try:
        project = tomllib.loads(contents).get("project", {})
    except tomllib.TOMLDecodeError:
        raise ValueError("pyproject.toml must contain valid TOML") from None
    scripts = project.get("scripts", {}) if isinstance(project, dict) else None
    if not isinstance(scripts, dict) or not all(
        isinstance(name, str) and isinstance(target, str) for name, target in scripts.items()
    ):
        raise ValueError("project.scripts must be a table of string targets")
    return scripts


def summarize_boundaries(
    paths: list[str], project_scripts: dict[str, str], revision: str
) -> dict[str, object]:
    legacy_modules = sorted(
        path
        for path in paths
        if path.startswith("python/neurosim/legacy_") and path.endswith(".py")
    )
    archived_files = sorted(path for path in paths if path.startswith("docs/legacy/"))
    entry_points = {"neurosim.workbench": {}, "neurosim.legacy": {}, "other": {}}
    for name, target in sorted(project_scripts.items()):
        boundary = next(
            (
                prefix
                for prefix in ("neurosim.workbench", "neurosim.legacy")
                if target == prefix or target.startswith(prefix + ".")
            ),
            "other",
        )
        entry_points[boundary][name] = target
    return {
        "revision": revision,
        "legacy_modules": legacy_modules,
        "archived_legacy_files": archived_files,
        "entry_points": entry_points,
        "legacy_module_count": len(legacy_modules),
        "archived_file_count": len(archived_files),
        "entry_point_count": len(project_scripts),
    }


def inventory(revision: str = "HEAD") -> dict[str, object]:
    tree = tracked_tree_inventory(revision)
    try:
        manifest = subprocess.run(
            ["git", "show", f"{tree['revision']}:pyproject.toml"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        raise ValueError("pyproject.toml is missing or unreadable at this revision") from None
    try:
        contents = manifest.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("pyproject.toml must be UTF-8") from None
    scripts = parse_project_scripts(contents)
    return summarize_boundaries(tree["paths"], scripts, tree["revision"])


def main() -> None:
    revision = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    try:
        result = inventory(revision)
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"legacy boundary map: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    json.dump(result, sys.stdout, indent=2, sort_keys=True, ensure_ascii=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
