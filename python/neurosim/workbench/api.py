"""Local single-user API. Do not expose without an authenticated reverse proxy."""

import csv
import io
import json
import os
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, Response
from pydantic import Field

from . import views
from .config import Experiment, StrictModel
from .morphology import parse_swc
from .store import Store, Worker


class SWCRequest(StrictModel):
    text: str = Field(max_length=500_000)


class ExhibitionBinding(StrictModel):
    job_id: str = Field(min_length=1)
    reference_id: str | None = None


def export_zip(result):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:

        def write(name, content):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o600 << 16
            archive.writestr(info, content)

        write("manifest.json", json.dumps(result["manifest"], indent=2, sort_keys=True))
        write("results.json", json.dumps(result, allow_nan=False, sort_keys=True))
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow(
            ["time_ms"] + [f"voltage_{i}_mV" for i in range(len(result["voltage"]))]
        )
        writer.writerows(zip(result["t"], *result["voltage"]))
        write("voltage.csv", stream.getvalue())
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow(["neuron_id", "spike_time_ms"])
        writer.writerows(
            (i, t) for i, train in enumerate(result["spikes"]) for t in train
        )
        write("spikes.csv", stream.getvalue())
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow(["source", "target", "inhibitory"])
        writer.writerows(result["edges"])
        write("connectivity.csv", stream.getvalue())
    return output.getvalue()


def create_app(database=None):
    @asynccontextmanager
    async def lifespan(app):
        app.state.store = Store(
            database or os.environ.get("NEUROSIM_DB", "neurosim-data/experiments.db")
        )
        worker = Worker(app.state.store)
        app.state.worker = worker
        try:
            yield
        finally:
            worker.close()

    app = FastAPI(title="NeuroSim CPU Workbench", lifespan=lifespan)

    @app.exception_handler(KeyError)
    async def missing(request, exc):
        return Response(
            '{"detail":"experiment not found"}',
            status_code=404,
            media_type="application/json",
        )

    @app.exception_handler(ValueError)
    async def invalid(request, exc):
        return Response(
            json.dumps({"detail": str(exc)}),
            status_code=409,
            media_type="application/json",
        )

    @app.get("/", response_class=HTMLResponse)
    def index():
        return Path(__file__).with_name("index.html").read_text(encoding="utf-8")

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "backend": "cpu",
            "worker_alive": app.state.worker.thread.is_alive(),
        }

    @app.get("/defaults")
    def defaults():
        return Experiment().model_dump()

    @app.post("/experiments", status_code=202)
    def create(config: Experiment):
        return app.state.store.create(config)

    @app.get("/experiments")
    def history(limit: int = Query(100, ge=1, le=500)):
        return app.state.store.history(limit)

    @app.get("/exhibition")
    def exhibition():
        return app.state.store.exhibition()

    @app.post("/exhibition/{slot}")
    def bind_exhibition(slot: int, binding: ExhibitionBinding):
        return app.state.store.bind_exhibition(
            slot, binding.job_id, binding.reference_id
        )

    @app.get("/experiments/{jid}")
    def get(jid: str):
        return app.state.store.get(jid)

    @app.post("/experiments/{jid}/cancel")
    def cancel(jid: str):
        return app.state.store.cancel(jid)

    @app.post("/experiments/{jid}/retry", status_code=202)
    def retry(jid: str):
        job = app.state.store.get(jid)
        if job["status"] not in ("failed", "cancelled", "completed"):
            raise HTTPException(409, "experiment is still active")
        return app.state.store.create(
            Experiment.model_validate(job["manifest"]["config"]), parent=jid
        )

    @app.delete("/experiments/{jid}", status_code=204)
    def delete(jid: str):
        app.state.store.delete(jid)

    @app.get("/experiments/{jid}/results")
    def results(jid: str):
        return app.state.store.result(jid)

    @app.get("/experiments/{jid}/manifest")
    def get_manifest(jid: str):
        return app.state.store.get(jid)["manifest"]

    @app.get("/experiments/{jid}/topology")
    def topology(
        jid: str, offset: int = Query(0, ge=0), limit: int = Query(4096, ge=1, le=4096)
    ):
        return views.topology(app.state.store.result(jid), offset, limit)

    @app.get("/experiments/{jid}/activity")
    def activity(
        jid: str,
        offset: int = Query(0, ge=0),
        limit: int = Query(20000, ge=1, le=20000),
    ):
        return views.activity(app.state.store.result(jid), offset, limit)

    @app.get("/experiments/{jid}/voltage")
    def voltage(
        jid: str,
        neuron: int = Query(0, ge=0),
        offset: int = Query(0, ge=0),
        limit: int = Query(5000, ge=1, le=5000),
    ):
        return views.voltage(app.state.store.result(jid), neuron, offset, limit)

    @app.get("/experiments/{jid}/export")
    def export(jid: str):
        return Response(
            export_zip(app.state.store.result(jid)),
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="neurosim-results.zip"'
            },
        )

    @app.post("/morphology")
    def morphology(request: SWCRequest):
        try:
            return {"points": parse_swc(request.text)}
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    return app


app = create_app()


def serve():
    import uvicorn

    uvicorn.run("neurosim.workbench.api:app", host="127.0.0.1", port=8000, workers=1)
