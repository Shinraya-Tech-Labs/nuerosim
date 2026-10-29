import json
import sqlite3
import subprocess
import sys

import pytest

from neurosim.sqlite_schema_audit import audit_database
from neurosim.workbench.store import SCHEMA_DDL, Store


FIXTURES = "tests/fixtures/omega/T008-sqlite-schema-compatibility-audit"


def build_fixture(path, name):
    fixture = json.load(open(f"{FIXTURES}/{name}.json", encoding="utf-8"))
    with sqlite3.connect(path) as db:
        for statement in fixture["ddl"]:
            db.execute(statement)
    return fixture


def test_valid_fixture_matches_store_schema(tmp_path):
    path = tmp_path / "valid.db"
    build_fixture(path, "valid")
    report = audit_database(path)
    assert report["compatible"] is True
    assert (report["table_count"], report["column_count"]) == (2, 12)
    assert report["tables"] == ["exhibition", "jobs"]
    assert not any(report["differences"].values())


def test_incompatible_fixture_names_missing_schema(tmp_path):
    path = tmp_path / "invalid.db"
    build_fixture(path, "invalid")
    report = audit_database(path)
    assert report["compatible"] is False
    assert report["differences"]["missing_tables"] == ["exhibition"]
    assert report["differences"]["missing_columns"] == {"jobs": ["result"]}


def test_audit_store_database_and_cli(tmp_path):
    path = tmp_path / "store.db"
    Store(path)
    report = audit_database(path)
    assert report["compatible"] is True
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.sqlite_schema_audit", str(path)],
        capture_output=True,
        text=True,
        check=True,
        env={**__import__("os").environ, "PYTHONPATH": "python"},
    )
    assert json.loads(result.stdout)["compatible"] is True


def test_missing_database_is_not_created(tmp_path):
    path = tmp_path / "missing.db"
    with pytest.raises(ValueError, match="does not exist"):
        audit_database(path)
    assert not path.exists()


def test_wal_sidecars_are_rejected_without_opening_database(tmp_path):
    path = tmp_path / "offline.db"
    with sqlite3.connect(path) as db:
        for statement in SCHEMA_DDL:
            db.execute(statement)
    sidecar = tmp_path / "offline.db-wal"
    sidecar.write_bytes(b"")
    with pytest.raises(ValueError, match="WAL sidecars"):
        audit_database(path)
