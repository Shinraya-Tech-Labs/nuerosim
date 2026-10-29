# SQLite schema compatibility audit

Run the audit on an existing, offline, checkpointed workbench database:

```sh
PYTHONPATH=python python -m neurosim.sqlite_schema_audit path/to/workbench.db
```

The tool reports whether table and column structure matches the current `Store` schema, along with actual counts and any missing, unexpected, or metadata-mismatched tables and columns. It checks names, declared types, nullability, defaults, and primary-key position.

The database must have no `-wal` or `-shm` sidecar. Make an offline checkpointed copy before auditing a database that may be in use. The audit rejects missing paths and invalid SQLite files with a nonzero exit status. It opens the target in immutable read-only mode and does not initialize or migrate it.

This is a structural check; it does not inspect rows, `CHECK` constraints, indexes, triggers, WAL health, or migration compatibility.

## Verification checklist

- [x] Accept a database initialized by `Store`.
- [x] Identify a missing required table and column.
- [x] Compare column metadata and verify the input remains unchanged.
- [x] Reject missing paths and WAL sidecars without creating files.
- [x] Expose deterministic JSON through the module CLI.

See the [contract](contracts/T008-sqlite-schema-compatibility-audit.md) and [validation evidence](evidence/T008-sqlite-schema-compatibility-audit.md).
