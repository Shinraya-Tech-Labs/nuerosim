# T008 — SQLite schema compatibility audit

## Purpose

Check an existing workbench SQLite database against the table and column structure declared by `Store` without opening it for writes or changing its schema.

## Contract

- **Input:** path to an existing SQLite database. The reference schema is created in memory from the same DDL used by `Store` initialization.
- **Output:** deterministic JSON with a compatibility boolean, actual table/column counts, sorted table names, and sorted missing-table/column or unexpected-table/column differences.
- **Units:** table and column counts are non-negative integers. There are no biological units.
- **Comparison:** compare table and column names plus declared type, nullability, default, and primary-key position. Require the current table/column shape exactly; this is a structural compatibility check, not a migration.
- **Side effects:** open the target with SQLite immutable read-only mode. Require an offline database with no `-wal` or `-shm` sidecar; if either exists, reject it and ask the operator to audit an offline checkpointed copy. Never initialize, migrate, repair, checkpoint, vacuum, or rewrite the target database.
- **Errors:** reject missing/unreadable/non-SQLite files with a nonzero status and concise message.
- **Acceptance example:** a database initialized by `Store` reports compatible; a database missing a required column reports incompatible and identifies the difference.
- **Exclusions:** this does not inspect row contents, `CHECK` constraints, indexes, triggers, WAL health, schema history, migration paths, or forward/backward compatibility across application versions. Immutable mode intentionally does not observe concurrent file changes; an offline copy is required.
