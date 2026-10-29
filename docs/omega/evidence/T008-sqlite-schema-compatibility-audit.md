# T008 validation evidence

## Schema and behavior

At code revision `d7b0801`, a temporary database initialized by `Store` reported compatible: 2 tables and 12 columns, with no structural differences. A second temporary database from the invalid fixture reported the missing `exhibition` table and `jobs.result` column. The CLI emitted the same deterministic JSON report. Missing paths were rejected without creating a file; WAL sidecars were rejected before opening; a metadata-mismatch database retained the same SHA-256 before and after audit; and the audited database could be deleted immediately after return.

The focused test file passed (7 passed). Five repeated audits of the temporary `Store` database took 43.227, 1.000, 0.896, 0.863, and 0.885 ms; median 0.896 ms after the first call. These measurements include in-process reference schema creation and SQLite connection overhead.

## Limits

This checks table/column shape, declared type, nullability, default, and primary-key position. It does not compare `CHECK` constraints, indexes, triggers, rows, or migrations. Only an offline checkpointed copy without WAL/SHM sidecars is accepted.
