# T002 — Environment reproducibility lockfile inventory

## Purpose

Record which dependency lockfiles are present at a Git revision and identify their exact contents with SHA-256. This is an inventory, not a claim that the environment is fully reproducible.

## Contract

- **Input:** a Git repository and a revision that resolves to a commit; default to `HEAD`.
- **Lockfile scope:** recognized tracked lockfiles only: basenames ending in `.lock`, plus `package-lock.json`. At this revision the known files are `requirements-runtime.lock` and `web/package-lock.json`. `pyproject.toml` and `web/package.json` are dependency manifests, not lockfiles.
- **Output:** deterministic JSON containing the resolved commit SHA and each sorted lockfile's repository-relative path, byte length, and SHA-256. Include the total lockfile count. Read blob contents from the selected Git tree, not the current working copy.
- **Units:** byte lengths are non-negative integer bytes; lockfile count is an integer; hashes are lowercase 64-character SHA-256 hex strings.
- **Defaults:** include only files recognized as lockfiles and tracked at the selected revision. Report zero if none are present; do not silently substitute a manifest.
- **Errors:** an unresolvable revision or Git read error exits nonzero with a concise message.
- **Acceptance example:** repeated runs against one commit produce identical normalized JSON, and each reported size and hash matches the corresponding blob in that commit.
- **Exclusions:** the inventory does not resolve dependencies, prove registry availability, validate platform coverage, or establish that a lockfile is complete. `requirements-runtime.lock` is a pinned runtime snapshot; its header says Linux Docker validation is pending. No environment equivalence or scientific reproducibility claim follows from its presence.
