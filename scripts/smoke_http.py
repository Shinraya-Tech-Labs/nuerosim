"""Real job smoke test against localhost; suitable for Docker CI."""

import json
import time
import urllib.request


def request(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        "http://127.0.0.1:8000" + path,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.load(response)


job = request(
    "/experiments", {"name": "HTTP smoke", "model": "lif", "duration": 10, "pulses": []}
)
deadline = time.monotonic() + 30
while time.monotonic() < deadline:
    status = request("/experiments/" + job["id"])
    if status["status"] in ("failed", "cancelled"):
        raise RuntimeError(status)
    if status["status"] == "completed":
        result = request("/experiments/" + job["id"] + "/results")
        assert result["voltage"][0][-1] == -65
        print("Real HTTP experiment completed and retrieved")
        break
    time.sleep(0.1)
else:
    raise TimeoutError("simulation did not finish")
