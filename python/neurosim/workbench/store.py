"""SQLite persistence and one cooperative CPU worker per local application."""

import json
import os
import sqlite3
import threading
import time
import uuid
import zlib
from contextlib import contextmanager
from pathlib import Path

from .config import Experiment
from .engine import Cancelled, manifest, simulate


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("""CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY, created REAL NOT NULL, updated REAL NOT NULL,
                status TEXT NOT NULL, progress REAL NOT NULL DEFAULT 0,
                manifest TEXT NOT NULL, parent_id TEXT, error TEXT, result BLOB)""")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def create(self, config, parent=None):
        jid = str(uuid.uuid4())
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            count = db.execute("SELECT count(*) FROM jobs").fetchone()[0]
            active = db.execute(
                "SELECT count(*) FROM jobs WHERE status IN ('queued','running','cancelling')"
            ).fetchone()[0]
            if count >= 500 or active >= 16:
                raise ValueError(
                    "local storage limit: 500 experiments, 16 active jobs; delete old jobs"
                )
            db.execute(
                "INSERT INTO jobs(id,created,updated,status,manifest,parent_id) VALUES(?,?,?,'queued',?,?)",
                (jid, now, now, json.dumps(manifest(config)), parent),
            )
        return self.get(jid)

    def get(self, jid):
        with self.connection() as db:
            row = db.execute(
                "SELECT id,created,updated,status,progress,manifest,parent_id,error FROM jobs WHERE id=?",
                (jid,),
            ).fetchone()
        if row is None:
            raise KeyError(jid)
        result = dict(row)
        result["manifest"] = json.loads(result["manifest"])
        return result

    def history(self, limit=100):
        with self.connection() as db:
            ids = [
                r[0]
                for r in db.execute(
                    "SELECT id FROM jobs ORDER BY created DESC LIMIT ?", (limit,)
                )
            ]
        return [self.get(jid) for jid in ids]

    def result(self, jid):
        job = self.get(jid)
        if job["status"] != "completed":
            raise ValueError("results available only for completed experiments")
        with self.connection() as db:
            payload = db.execute(
                "SELECT result FROM jobs WHERE id=?", (jid,)
            ).fetchone()[0]
        return json.loads(zlib.decompress(payload))

    def cancel(self, jid):
        self.get(jid)
        with self.connection() as db:
            db.execute(
                """UPDATE jobs SET status=CASE WHEN status='queued' THEN 'cancelled'
                       ELSE 'cancelling' END, updated=? WHERE id=? AND status IN ('queued','running')""",
                (time.time(), jid),
            )
        return self.get(jid)

    def delete(self, jid):
        self.get(jid)
        with self.connection() as db:
            n = db.execute(
                "DELETE FROM jobs WHERE id=? AND status IN ('completed','failed','cancelled')",
                (jid,),
            ).rowcount
        if not n:
            raise ValueError("cancel active experiment before deleting")

    def claim(self):
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id FROM jobs WHERE status='queued' ORDER BY created LIMIT 1"
            ).fetchone()
            if row is None:
                return None
            db.execute(
                "UPDATE jobs SET status='running', updated=? WHERE id=?",
                (time.time(), row[0]),
            )
            return row[0]

    def progress(self, jid, fraction):
        with self.connection() as db:
            db.execute(
                "UPDATE jobs SET progress=?, updated=? WHERE id=? AND status='running'",
                (fraction, time.time(), jid),
            )

    def finish(self, jid, status, result=None, error=None):
        payload = (
            zlib.compress(json.dumps(result, allow_nan=False).encode())
            if result is not None
            else None
        )
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            current = db.execute(
                "SELECT status FROM jobs WHERE id=?", (jid,)
            ).fetchone()[0]
            if current == "cancelling":
                status, payload, error = "cancelled", None, None
            db.execute(
                "UPDATE jobs SET status=?,result=?,error=?,updated=?,progress=CASE WHEN ?='completed' THEN 1 ELSE progress END WHERE id=?",
                (status, payload, error, time.time(), status, jid),
            )


class Worker:
    """Exclusive file lock prevents multiple servers from sharing a job store."""

    def __init__(self, store):
        self.store = store
        self.stop = threading.Event()
        self.lock = open(str(store.path) + ".lock", "a+b")
        try:
            if os.fstat(self.lock.fileno()).st_size == 0:
                self.lock.write(b"0")
                self.lock.flush()
            self.lock.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.lock.close()
            raise RuntimeError(
                "database already owned by another server; use one worker"
            ) from None
        with store.connection() as db:
            db.execute(
                "UPDATE jobs SET status='failed',error='Execution interrupted by process exit; retry from manifest',updated=? WHERE status IN ('running','cancelling')",
                (time.time(),),
            )
        self.thread = threading.Thread(
            target=self.run, name="neurosim-cpu", daemon=True
        )
        self.thread.start()

    def run(self):
        while not self.stop.is_set():
            jid = self.store.claim()
            if jid is None:
                self.stop.wait(0.1)
                continue
            try:
                saved_manifest = self.store.get(jid)["manifest"]
                config = Experiment.model_validate(saved_manifest["config"])
                if saved_manifest != manifest(config):
                    raise ValueError(
                        "execution environment changed since submission; retry to create a new manifest"
                    )
                last_progress = 0.0
                last_cancel = 0.0
                cancel_requested = False

                def progress(fraction):
                    nonlocal last_progress
                    now = time.monotonic()
                    if fraction == 1 or now - last_progress >= 0.25:
                        self.store.progress(jid, fraction)
                        last_progress = now

                def cancelled():
                    nonlocal last_cancel, cancel_requested
                    now = time.monotonic()
                    if now - last_cancel >= 0.05:
                        cancel_requested = self.store.get(jid)["status"] == "cancelling"
                        last_cancel = now
                    return self.stop.is_set() or cancel_requested

                result = simulate(config, progress=progress, cancelled=cancelled)
                self.store.finish(jid, "completed", result)
            except Cancelled:
                self.store.finish(jid, "cancelled")
            except Exception as exc:
                self.store.finish(jid, "failed", error=f"{type(exc).__name__}: {exc}")

    def close(self):
        self.stop.set()
        self.thread.join()
        self.lock.close()
