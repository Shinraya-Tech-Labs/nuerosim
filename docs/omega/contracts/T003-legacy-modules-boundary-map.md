# T003 — Legacy modules boundary map

## Purpose

Produce a reproducible map separating the supported workbench entry points from explicitly legacy-named Python modules and archived `docs/legacy` files at a Git revision.

## Contract

- **Input:** a Git repository and a revision resolving to a commit; default to `HEAD`.
- **Scope:** tracked paths matching `python/neurosim/legacy_*.py`, all tracked paths under `docs/legacy/`, and the `project.scripts` table in that revision's `pyproject.toml`.
- **Output:** deterministic JSON with the resolved commit SHA, sorted legacy module paths, sorted archived legacy document paths, and the project's registered console entry points grouped by target boundary (`neurosim.workbench`, `neurosim.legacy`, or other). Include integer path counts.
- **Units:** counts are Git-tracked paths or registered entry points, not runtime call counts.
- **Defaults:** read all source metadata from the selected commit tree. Do not use the current working copy as a fallback.
- **Errors:** unresolved revisions, missing/unreadable `pyproject.toml`, or malformed TOML return a nonzero status with a concise error.
- **Acceptance example:** the current `python/neurosim/legacy_cli.py` is listed as a legacy-named module; `docs/legacy/` files are listed as archived material; `neurosim` and `neurosim-serve` point to `neurosim.workbench` targets.
- **Exclusions:** this naming and entry-point map is not a dynamic import/call graph and cannot detect legacy code under other names, transitive use, scientific validity, or deletion safety. The legacy CLI module is not assumed to be publicly registered merely because it exists.
