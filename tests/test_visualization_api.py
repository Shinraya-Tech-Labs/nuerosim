import time

from fastapi.testclient import TestClient
from neurosim.workbench.api import create_app
from neurosim.workbench.config import Experiment, Pulse
from neurosim.workbench.engine import simulate


def saved(client, config):
    job = client.post("/experiments", json=config.model_dump()).json()
    for _ in range(500):
        state = client.get(f"/experiments/{job['id']}").json()
        if state["status"] in ("completed", "failed", "cancelled"):
            break
        time.sleep(0.02)
    assert state["status"] == "completed", state
    return job["id"], client.get(f"/experiments/{job['id']}/results").json()


def test_topology_and_chunks_exactly_match_saved_output(tmp_path):
    with TestClient(create_app(tmp_path / "views.db")) as c:
        jid, result = saved(
            c,
            Experiment(
                model="lif",
                n=8,
                probability=0.5,
                duration=20,
                pulses=[Pulse(start=0, stop=20, amplitude=3)],
            ),
        )
        edges = []
        offset = 0
        while offset is not None:
            page = c.get(f"/experiments/{jid}/topology?offset={offset}&limit=3").json()
            edges.extend(page["edges"])
            offset = page["next_offset"]
        assert [
            [e["source"], e["target"], e["type"] == "inhibitory"] for e in edges
        ] == result["edges"]
        assert all(e["weight"] == 0.05 and e["delay_ms"] == 1 for e in edges)
        assert len(page["nodes"]) == 8
        events = c.get(f"/experiments/{jid}/activity").json()["events"]
        assert [(e["time_ms"], e["neuron_id"]) for e in events] == sorted(
            (t, i) for i, s in enumerate(result["spikes"]) for t in s
        )
        times, values = [], []
        offset = 0
        while offset is not None:
            page = c.get(
                f"/experiments/{jid}/voltage?neuron=0&offset={offset}&limit=13"
            ).json()
            times.extend(page["t"])
            values.extend(page["voltage"])
            offset = page["next_offset"]
        assert times == result["t"] and values == result["voltage"][0]
        assert c.get(f"/experiments/{jid}/voltage?neuron=8").status_code == 409
        assert c.get(f"/experiments/{jid}/activity?limit=999999").status_code == 422
        assert c.get(f"/experiments/{jid}/topology?offset=-1").status_code == 422


def test_cable_edges_describe_actual_chain(tmp_path):
    with TestClient(create_app(tmp_path / "cable.db")) as c:
        jid, _ = saved(c, Experiment(model="cable", n=3, duration=1, pulses=[]))
        data = c.get(f"/experiments/{jid}/topology").json()
        assert [(e["source"], e["target"]) for e in data["edges"]] == [(0, 1), (1, 2)]
        assert all(e["type"] == "axial" and not e["directed"] for e in data["edges"])
        assert all(n["kind"] == "compartment" for n in data["nodes"])


def test_exports_have_fixed_metadata_and_repeatable_bytes():
    import io
    import zipfile

    from neurosim.workbench.api import export_zip

    result = simulate(Experiment(model="lif", duration=1, pulses=[]))
    first = export_zip(result)
    assert first == export_zip(result)
    with zipfile.ZipFile(io.BytesIO(first)) as archive:
        assert all(i.date_time == (1980, 1, 1, 0, 0, 0) for i in archive.infolist())
