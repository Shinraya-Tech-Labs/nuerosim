"""Read-only structural audit for workbench SQLite databases."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .workbench.store import create_schema


def schema_signature(db):
    tables = {}
    names = sorted(
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    )
    for name in names:
        quoted = '"' + name.replace('"', '""') + '"'
        tables[name] = {
            row[1]: {
                "type": (row[2] or "").upper(),
                "notnull": bool(row[3]),
                "default": row[4],
                "primary_key": row[5],
            }
            for row in db.execute(f"PRAGMA table_info({quoted})")
        }
    return tables


def compare_schemas(actual, expected):
    missing_tables = sorted(expected.keys() - actual.keys())
    unexpected_tables = sorted(actual.keys() - expected.keys())
    missing_columns = {}
    unexpected_columns = {}
    mismatched_columns = {}
    for table in sorted(actual.keys() & expected.keys()):
        actual_cols, expected_cols = actual[table], expected[table]
        missing = sorted(expected_cols.keys() - actual_cols.keys())
        unexpected = sorted(actual_cols.keys() - expected_cols.keys())
        mismatch = {
            column: {"actual": actual_cols[column], "expected": expected_cols[column]}
            for column in sorted(actual_cols.keys() & expected_cols.keys())
            if actual_cols[column] != expected_cols[column]
        }
        if missing:
            missing_columns[table] = missing
        if unexpected:
            unexpected_columns[table] = unexpected
        if mismatch:
            mismatched_columns[table] = mismatch
    return {
        "missing_tables": missing_tables,
        "unexpected_tables": unexpected_tables,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "mismatched_columns": mismatched_columns,
    }


def audit_database(path):
    path = Path(path).resolve()
    if not path.is_file():
        raise ValueError(f"database does not exist or is not a file: {path}")
    sidecars = [Path(str(path) + suffix) for suffix in ("-wal", "-shm")]
    if any(sidecar.exists() for sidecar in sidecars):
        raise ValueError("database has WAL sidecars; audit an offline checkpointed copy")
    try:
        with sqlite3.connect(":memory:") as reference:
            create_schema(reference)
            expected = schema_signature(reference)
        uri = path.as_uri() + "?mode=ro&immutable=1"
        with sqlite3.connect(uri, uri=True) as actual_db:
            actual = schema_signature(actual_db)
    except sqlite3.Error as exc:
        raise ValueError(f"cannot read SQLite schema: {exc}") from exc
    differences = compare_schemas(actual, expected)
    return {
        "compatible": not any(differences.values()),
        "table_count": len(actual),
        "column_count": sum(map(len, actual.values())),
        "tables": sorted(actual),
        "differences": differences,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", help="existing offline SQLite database")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(audit_database(args.database), sort_keys=True, indent=2))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
