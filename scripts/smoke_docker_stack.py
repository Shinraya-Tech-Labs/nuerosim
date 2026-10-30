"""Exercise the authenticated Compose stack through both API entry points."""

import json
import os
import subprocess
import time
import urllib.error
import urllib.request


TOKEN = os.environ["NEUROSIM_AUTH_TOKEN"]
API = os.environ.get("NEUROSIM_API_URL", "http://127.0.0.1:8000")
WEB = os.environ.get("NEUROSIM_WEB_URL", "http://127.0.0.1:3000")
PROJECT = os.environ.get("NEUROSIM_COMPOSE_PROJECT", "neurosim-v020-ci")


def request(base, path, body=None, *, auth=True):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(base + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)


def wait_for_job(job_id, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        job = request(WEB, f"/api/experiments/{job_id}")
        if job["status"] in {"completed", "failed", "cancelled"}:
            return job
        time.sleep(0.1)
    raise TimeoutError(f"job {job_id} did not finish")


def main():
    assert request(API, "/health", auth=False)["status"] == "ok"
    try:
        request(API, "/defaults", auth=False)
    except urllib.error.HTTPError as error:
        assert error.code == 401
    else:
        raise AssertionError("unauthenticated API request was accepted")

    # This URL reaches FastAPI through the Next.js proxy and verifies its bearer injection.
    assert request(WEB, "/api/health")["status"] == "ok"
    assert "model" in request(WEB, "/api/defaults")

    first = request(
        WEB,
        "/api/experiments",
        {"name": "Docker smoke", "model": "lif", "duration": 1, "pulses": []},
    )
    assert wait_for_job(first["id"])["status"] == "completed"
    result = request(WEB, f"/api/experiments/{first['id']}/results")
    assert result["manifest"]["config"]["name"] == "Docker smoke"

    retry = request(WEB, f"/api/experiments/{first['id']}/retry", {})
    assert retry["parent_id"] == first["id"]
    assert wait_for_job(retry["id"])["status"] == "completed"

    long_job = request(
        WEB,
        "/api/experiments",
        {
            "name": "Docker cancellation smoke",
            "model": "lif",
            "n": 512,
            "duration": 488,
            "record_every": 1000,
            "pulses": [],
        },
    )
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        state = request(WEB, f"/api/experiments/{long_job['id']}")["status"]
        if state == "running":
            break
        if state in {"failed", "completed", "cancelled"}:
            raise AssertionError(f"job ended before running cancellation test: {state}")
        time.sleep(0.25)
    else:
        raise TimeoutError("long smoke job never entered running state")
    request(WEB, f"/api/experiments/{long_job['id']}/cancel", {})
    assert wait_for_job(long_job["id"])["status"] == "cancelled"

    subprocess.run(
        ["docker", "compose", "-p", PROJECT, "--profile", "web", "restart", "neurosim"],
        check=True,
        env=os.environ.copy(),
        timeout=60,
    )
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        try:
            if request(API, "/health", auth=False)["status"] == "ok":
                break
        except (OSError, urllib.error.URLError):
            time.sleep(1)
    else:
        raise TimeoutError("API did not become healthy after restart")
    persisted = request(WEB, f"/api/experiments/{retry['id']}")
    assert persisted["status"] == "completed"
    assert request(WEB, f"/api/experiments/{retry['id']}/results")["manifest"]
    print("Docker stack passed auth, proxy, execution, result, retry, cancellation, and restart persistence checks")


if __name__ == "__main__":
    main()
