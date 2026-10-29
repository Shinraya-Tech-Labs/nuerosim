# Legacy modules boundary map

Run from the repository root to inspect the supported and explicitly legacy paths at a commit:

```sh
PYTHONPATH=python python -m neurosim.module_boundaries [revision]
```

The revision defaults to `HEAD`. The JSON reports legacy-named Python modules under `python/neurosim/legacy_*.py`, archived files under `docs/legacy/`, and registered console entry points grouped by target (`neurosim.workbench`, `neurosim.legacy`, or `other`). It reads paths and `pyproject.toml` from the Git commit, not from uncommitted files.

The map reflects naming and packaging metadata only. It is not a dynamic import graph and may miss legacy code outside these conventions. It does not establish scientific validity, support status for every importable module, or whether archived files can be deleted. Malformed TOML or an unresolved revision exits nonzero with an explanatory message. No biological claims are made.

## Verification checklist

- [x] Compare path groups with the selected commit tree.
- [x] Compare registered entry points with `project.scripts` in that commit.
- [x] Check malformed TOML and an empty-map boundary.
- [x] Confirm the legacy CLI module is present but is not a registered console entry point.

See the [contract](contracts/T003-legacy-modules-boundary-map.md) and [validation evidence](evidence/T003-legacy-modules-boundary-map.md).
