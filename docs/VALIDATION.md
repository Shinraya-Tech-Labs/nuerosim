# Validation and release evidence

## Current v0.2.0 candidate record — 2026-10-31

The release branch is `codex/neurosim-v020-release`. These results describe
specific checks and revisions; they are not a statement that a public release
is ready.

| Area | Verified result | Evidence |
|---|---|---|
| Scientific workbench baseline | 628 Python tests passed in the post-T210 remediation baseline; focused scientific reference and convergence suites and seven independent reference comparisons passed. | [`POST_T210_VALIDATION_RESULTS.md`](omega/POST_T210_VALIDATION_RESULTS.md), [`V020_PROGRESS.md`](omega/V020_PROGRESS.md), [`scientific/results/`](../scientific/results/) |
| Benchmark | Eleven CPU workloads ran for five measured repetitions after warm-up; output hashes matched within each workload. The report verifier and focused harness tests passed. | [`BENCHMARK_RESULTS.md`](BENCHMARK_RESULTS.md), [`v020-run-004.json`](../benchmarks/results/v020-run-004.json) |
| API and lifecycle | 35 focused API, worker, SQLite backup/restore, restart, pagination, and cancellation tests passed. Hosted CPU and web workflows passed on the publication revision. | [`V020_PROGRESS.md`](omega/V020_PROGRESS.md), [`test_release_reliability.py`](../tests/test_release_reliability.py) |
| Browser workbench | Six Playwright end-to-end tests passed, including real simulation submission, reload/comparison, SVG and ZIP downloads, SWC import, 512-neuron rendering, fallback, and mobile layout. | [`WEB_INTEGRATION_VALIDATION.md`](WEB_INTEGRATION_VALIDATION.md), [`validation/`](validation/) |
| Hosted CI for CP12 | CPU run 41122970088 was queued and web run 41122970014 was in progress when CP12 was recorded. Check the run pages for the latest state. | [CPU run](https://github.com/sreerevanth/nuerosim/actions/runs/41122970088), [web run](https://github.com/sreerevanth/nuerosim/actions/runs/41122970014) |
| Docker deployment | A clean Compose image build and authenticated full-stack smoke passed in hosted CI run 41115307566. The local Docker daemon is unavailable on the recording host, so no local image startup is claimed. | [Docker CI run](https://github.com/sreerevanth/nuerosim/actions/runs/41115307566), [`DEPLOYMENT.md`](DEPLOYMENT.md) |
| Security | Historical candidate scans recorded no known vulnerabilities in the audited Python runtime and production npm dependency sets. CP14 must rerun the current dependency scans and release gates. | [`POST_T210_VALIDATION_RESULTS.md`](omega/POST_T210_VALIDATION_RESULTS.md), [`V020_PROGRESS.md`](omega/V020_PROGRESS.md) |
| Release blockers | License ownership/terms are unconfirmed; CP12 hosted checks and CP14 release review remain incomplete. No v0.2.0 tag or release is authorized by these results. | [`ARCHITECTURE.md`](ARCHITECTURE.md), [`V020_PROGRESS.md`](omega/V020_PROGRESS.md) |

Run the Python tests from the repository root with `PYTHONPATH=python` so the
checkout, rather than an older installed package, is exercised. Exact commands,
reports, host details, and remaining limitations are recorded in the linked
evidence files and the persistent commit-point ledger.

## Historical baseline — 2026-10-19

The table below records the earlier pre-remediation state and should be read as
a dated snapshot, not the current candidate status.

This record separates the supported CPU workbench from preserved legacy research.
No release has been tagged, deployed or published.

|Gate|Observed result|
|---|---|
|Original full pytest|Collection failed: two package imports; with PYTHONPATH, missing reconstruction module|
|Original unit file|29 passed, 9 failed, 90 warnings, 29.62 s (baseline)|
|CPU workbench + targeted legacy regressions|19 passed, 1 dependency deprecation warning in 14.33 s from the installed wheel; see `validation/cpu-tests.txt`|
|HH adaptive reference|Max voltage error .006001657 mV at .025 ms; .000305376 mV at .0125 ms; refinement ratio 19.653|
|Packaging|Wheel built and installed into clean .venv; test imports use installed package|
|Dependencies|pip check passed; initial pip audit found vulnerable bundled pip 25.3; upgraded isolated environment to 26.2.1; re-audit found no known vulnerabilities|
|Source security|Bandit on supported workbench: zero findings; this is not a security certification or a clean bill for legacy modules|
|Browser|Real HH submission, completed voltage/raster/rate display, history selection, comparison (two voltage series), SWC (three branch segments), SVG download verified|
|HTTP process|Real Uvicorn job created, executed and retrieved by scripts/smoke_http.py|
|Final network UI run|8 HH neurons, 11 realized synapses, 2 spikes, mean population rate 5 Hz over 50 ms; completed in 3.194 s including worker progress callbacks; four plot types rendered|
|Compose configuration|docker compose config --quiet succeeded|
|Docker execution|Blocked: installed Desktop was started, but Linux engine pipe remained unavailable|
|CUDA|Blocked: nvcc/nvidia-smi unavailable on PATH; no kernel execution or speedup validation|
|MPI|Blocked: MPI launcher unavailable; original implementation unvalidated|
|Remote CI|Workflow added for Windows/Linux Python 3.11–3.14; not run remotely in this session|
|Release|Blocked by Docker/CI gates and absent license confirmation; development version only|

## Test interpretation

The default suite is in `tests/`. It exercises real equations, SQLite, background
threads and HTTP integration; no fake simulation runner is substituted. The
failure tests deliberately corrupt a stored configuration or exceed a real
synapse-resource limit, rather than pretending a simulation succeeded.
It covers running and queued cancellation, retry ancestry, persistent results,
restart interruption, exclusive database ownership, quota enforcement, manifest
environment checks and CLI manifest round-tripping. One dependency deprecation
warning from Starlette's httpx TestClient may appear; no warning is suppressed.

The original root tests remain available and have not been rewritten to greenwash
invalid assumptions. Most of their scientific engine is unsupported. The old
API returned in-memory data and cannot be made compatible with persistent jobs
by merely changing imports. The new `/experiments` API is an explicit replacement.

## CPU benchmark

`scripts/benchmark_cpu.py` runs three actual serial repeats per case and records
all durations, connectivity, spike counts, manifests and environment. See
`validation/cpu-benchmark.json` for exact values. Windows 11, Python 3.14.2,
AMD64 Family 25 Model 80. Installed-wheel medians observed in this session:

|Model|Size|Biological duration|Median wall time|
|---|---:|---:|---:|
|HH|1 neuron|50 ms|1.487 s|
|LIF network|128 neurons / 313 edges|100 ms|1.128 s|
|LIF network|512 neurons / 5182 edges|100 ms|1.807 s|

dt=.025 ms, recording stride 10, probability .02 for networks, seed 42.
All repeated voltage arrays were identical within each case. The host was shared
with other development activity; these are reference observations, not stable
performance guarantees. Timing covers simulation and result construction, not API
queue latency, storage, browser rendering or cold dependency import. GPU numerical
differences and speedups are **not measured**.

## Re-running

```sh
python -m build --wheel
python -m pip install --force-reinstall --no-deps dist/neurosim-0.2.0.dev0-py3-none-any.whl
python -m pytest tests -q -s
python -m pip check
python -m pip_audit
python scripts/benchmark_cpu.py
docker compose up --build --wait
python scripts/smoke_http.py
```

Use an isolated environment with the dev dependencies installed. The source tree
must not be added to PYTHONPATH for an installed-wheel verification. Raw reports
and a real workbench screenshot are retained under `docs/validation/`.
