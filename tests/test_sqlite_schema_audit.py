import json
import hashlib
import sqlite3
import subprocess
import sys
from contextlib import closing

import pytest

from neurosim.sqlite_schema_audit import audit_database
from neurosim.workbench.store import SCHEMA_DDL, Store


FIXTURES = "tests/fixtures/omega/T008-sqlite-schema-compatibility-audit"


def build_fixture(path, name):
    fixture = json.load(open(f"{FIXTURES}/{name}.json", encoding="utf-8"))
    with closing(sqlite3.connect(path)) as db:
        for statement in fixture["ddl"]:
            db.execute(statement)
        db.commit()
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
    with closing(sqlite3.connect(path)) as db:
        for statement in SCHEMA_DDL:
            db.execute(statement)
        db.commit()
    sidecar = tmp_path / "offline.db-wal"
    sidecar.write_bytes(b"")
    with pytest.raises(ValueError, match="WAL sidecars"):
        audit_database(path)


def test_column_metadata_mismatch_is_reported_without_modification(tmp_path):
    path = tmp_path / "different-default.db"
    with closing(sqlite3.connect(path)) as db:
        db.execute("CREATE TABLE jobs (id TEXT PRIMARY KEY, progress REAL DEFAULT 1)")
        db.execute("CREATE TABLE exhibition (slot INTEGER PRIMARY KEY, job_id TEXT, reference_id TEXT)")
        db.commit()
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    report = audit_database(path)
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    assert report["compatible"] is False
    assert report["differences"]["mismatched_columns"]["jobs"]["progress"]["actual"]["default"] == "1"
    assert before == after


def test_audit_closes_database_file(tmp_path):
    path = tmp_path / "close.db"
    build_fixture(path, "valid")
    audit_database(path)
    path.unlink()
    assert not path.exists()
