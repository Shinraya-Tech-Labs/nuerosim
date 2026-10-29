# Dependency lockfile inventory

From the repository root, print lockfile hashes for a Git commit:

```sh
PYTHONPATH=python python -m neurosim.lockfile_inventory [revision]
```

The revision defaults to `HEAD`. Output contains the resolved SHA, lockfile count, and each recognized tracked lockfile's path, byte size, and SHA-256. The command reads Git blobs, so uncommitted edits do not affect the result. It recognizes names ending in `.lock` and `package-lock.json`; `pyproject.toml` and `package.json` are manifests and are not included.

An unresolved revision or unreadable lockfile exits with status 2 and an error on stderr. An empty result means no recognized lockfiles exist at that commit. The report does not install dependencies, check registry availability, or prove the lockfiles are complete. In particular, the current Python runtime snapshot notes that Linux Docker validation is pending; no full environment or scientific reproducibility claim is made.

## Verification checklist

- [x] Repeat the same revision and compare normalized JSON.
- [x] Compare every reported size and SHA-256 with the corresponding `git show` blob.
- [x] Check an unresolved revision and a zero-byte lockfile.
- [x] Confirm dependency manifests are excluded.

See the [contract](contracts/T002-environment-reproducibility-lockfile-inventory.md) and [validation evidence](evidence/T002-environment-reproducibility-lockfile-inventory.md).
