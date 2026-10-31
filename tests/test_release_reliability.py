import json
import time

from fastapi.testclient import TestClient

from neurosim.workbench.api import create_app
from neurosim.workbench.config import Experiment, Pulse
from neurosim.workbench.store import Store, Worker


def _wait_for_status(client, job_id, expected, timeout=20):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        job = client.get(f"/experiments/{job_id}").json()
        if job["status"] in {"completed", "cancelled", "failed"}:
            assert job["status"] == expected, job
            return job
        time.sleep(0.02)
    raise AssertionError(f"job {job_id} did not finish within {timeout} seconds")


def test_large_api_result_survives_live_backup_and_restart(tmp_path):
    database = tmp_path / "large-results.db"
    backup = tmp_path / "large-results-backup.db"
    restored_path = tmp_path / "large-results-restored.db"
    config = Experiment(
        model="lif",
        n=64,
        duration=200,
        record_every=4,
        probability=0.1,
        seed=42,
        pulses=[Pulse(target=0, start=0, stop=200, amplitude=3)],
    )

    with TestClient(create_app(database)) as client:
        response = client.post("/experiments", json=config.model_dump())
        assert response.status_code == 202
        job_id = response.json()["id"]
        _wait_for_status(client, job_id, "completed")

        result_response = client.get(f"/experiments/{job_id}/results")
        assert result_response.status_code == 200
        result = result_response.json()
        assert len(json.dumps(result, separators=(",", ":"))) > 1_000_000
        assert result["manifest"]["config"]["n"] == 64

        history = client.get("/experiments?limit=1")
        assert history.status_code == 200
        assert [row["id"] for row in history.json()] == [job_id]
        assert client.get("/experiments?limit=501").status_code == 422

        # Exercise SQLite's online backup API while the service still owns the DB.
        client.app.state.store.backup_to(backup)

    restored = Store(restored_path)
    restored.restore_from(backup)
    assert restored.get(job_id)["status"] == "completed"
    assert restored.result(job_id) == result

    with TestClient(create_app(restored_path)) as restarted:
        assert restarted.get(f"/experiments/{job_id}/results").json() == result
        assert restarted.get(f"/experiments/{job_id}/manifest").json() == result[
            "manifest"
        ]


def test_activity_endpoint_paginates_materialized_events(tmp_path):
    config = Experiment(
        model="lif",
        n=8,
        probability=0.5,
        duration=20,
        record_every=5,
        pulses=[Pulse(start=0, stop=20, amplitude=3)],
    )
    with TestClient(create_app(tmp_path / "activity.db")) as client:
        job = client.post("/experiments", json=config.model_dump()).json()
        _wait_for_status(client, job["id"], "completed")
        baseline = client.get(f"/experiments/{job['id']}/activity").json()
        assert baseline["total_events"] > 2

        events = []
        offset = 0
        while offset is not None:
            page = client.get(
                f"/experiments/{job['id']}/activity?offset={offset}&limit=2"
            ).json()
            assert page["offset"] == offset
            assert page["total_events"] == baseline["total_events"]
            events.extend(page["events"])
            offset = page["next_offset"]

        assert events == baseline["events"]
        assert client.get(
            f"/experiments/{job['id']}/activity?offset=-1"
        ).status_code == 422


def test_worker_shutdown_cancels_active_work_and_releases_database_lock(tmp_path):
    store = Store(tmp_path / "shutdown.db")
    worker = Worker(store)
    job = None
    try:
        job = store.create(
            Experiment(n=200, probability=0.1, duration=1000, record_every=40)
        )
        deadline = time.monotonic() + 5
        while store.get(job["id"])["status"] == "queued" and time.monotonic() < deadline:
            time.sleep(0.01)
        assert store.get(job["id"])["status"] == "running"

        worker.close()
        assert not worker.thread.is_alive()
        assert worker.lock.closed
        assert store.get(job["id"])["status"] == "cancelled"

        replacement = Worker(store)
        replacement.close()
        assert not replacement.thread.is_alive()
    finally:
        if worker.thread.is_alive():
            worker.close()
