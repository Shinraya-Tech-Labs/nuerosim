# T001 — Repository tree provenance inventory

## Purpose

Provide a reproducible, read-only inventory of the repository tree at a named Git revision. The inventory describes what Git tracks and the repository metadata available at that revision; it is an audit aid, not proof of ownership or authorship.

## Contract

- **Input:** a Git repository and a commit-ish that resolves to a commit. A working-tree mode may be added only if it labels staged, unstaged, and untracked files separately.
- **Output:** deterministic JSON tied to the resolved commit SHA, containing sorted tracked paths and summary counts grouped by top-level directory and file extension. Missing extensions use the empty string.
- **Units:** file counts are integer counts of Git-tracked paths; sizes, if later added, must be bytes. No biological or performance units apply.
- **Defaults:** inventory `HEAD`; include every path returned by Git at that revision, including dotfiles; sort paths lexically using `/` separators.
- **Errors:** fail with a nonzero status and a clear message if the repository or revision cannot be resolved. Do not silently fall back to the live working tree.
- **Acceptance example:** the same repository revision produces byte-equivalent normalized JSON on repeated runs; the output's path list length equals its reported tracked-file count.
- **Exclusions:** this inventory does not establish license rights, contributor identity, upstream origin, scientific validity, data quality, or whether generated/binary files should be distributed. Git history and configured remotes are recorded as metadata only and are not independently verified claims.

## Verification

The implementation must be read-only and use Git's tracked tree as its source of truth. Check a valid revision, an invalid revision, deterministic ordering, and the count/path consistency. Document limitations where Git metadata is absent or incomplete.
