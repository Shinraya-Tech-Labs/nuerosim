# Repository tree provenance inventory

Run from the repository root to print a deterministic JSON inventory of a commit's Git-tracked paths:

```sh
PYTHONPATH=python python -m neurosim.repo_inventory [revision]
```

The revision defaults to `HEAD`. The output includes the resolved commit SHA, sorted paths, total tracked path count, counts by top-level directory, and counts by filename extension. Root-level files are grouped under `.`; extensionless files use the empty extension key. The command reads the selected commit tree, so uncommitted and ignored files are excluded.

An unknown revision or Git read error prints a message to stderr and exits nonzero (revision errors use status 2). The inventory is descriptive metadata: it cannot prove ownership, authorship, license rights, scientific validity, or the provenance of ignored/untracked files. It makes no biological claims.

## Verification checklist

- [x] Repeat the same revision and compare normalized JSON.
- [x] Confirm path count and sorted order.
- [x] Check an unresolved revision and an empty-tree summary.
- [x] Cross-check counts against `git ls-tree` and `git ls-files`.

See the [contract](contracts/T001-repo-tree-provenance-inventory.md) and [validation evidence](evidence/T001-repo-tree-provenance-inventory.md).
