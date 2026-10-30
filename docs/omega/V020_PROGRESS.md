# NeuroSim v0.2.0 release execution ledger

Release branch: `codex/neurosim-v020-release`  
Verified base: `ea4d43239bc7deb343e112eab413770eddc52165`  
PR #11: merged to `main` at `ea4d43239bc7deb343e112eab413770eddc52165` on 2026-10-30.  
Starting validation environment: Windows 11, Python 3.14.2, Node 22.23.0,
Docker CLI 29.3.1, Docker Compose 5.1.1.

## Commit point status

| Point | Status | Commit | Summary |
|---|---|---|---|
| CP01 | Complete | `5dbe7d49f702e06e5edbc1e17587fcf0a9906679` | Verified merge/base and captured baseline suite. |
| CP02 | Complete; daemon build deferred to CP03 CI | `7c2d883c2e992018836a13443ffbdb8a3377faa9` | Improved container health ordering and Next.js runtime token proxy. |
| CP03 | Complete | `57051899`, `5fc38b70`, `21139cef` | Clean Docker build and full-stack lifecycle smoke verified in hosted CI. |
| CP04 | Complete | `97c37038b0cfc2b1fa7ef04f318cb4f77ec74b3c` | Reproducible eight-case suite, two matching raw runs, hosted science artifact. |
| CP05 | Complete | `767d52c44f39dc49565c389f0312fb0e0229ce73` | Hodgkin-Huxley stimulus-response and DOP853 convergence evidence. |
| CP06 | Complete | `2d91981eb14190ff26f211083a4807d6934570a4` | LIF analytic periods and LIF/AdEx stimulus response. |
| CP07 | Complete | `df4e3dd` | Cable DOP853 trajectory check and seeded-network invariants. |
| CP08 | Complete | `927a929345aa2025286c5243608f40c0d05d1dc3` | Seven-reference report with unit-separated errors and convergence orders. |
| CP09 | Complete | `60c00909ef07a97f5c0267db52047f68aaaf750e` | Isolated benchmark harness, peak RSS, phase metrics, and 11 workloads. |
| CP10 | Hosted CPU and web checks pass | `59bb8de51b3b0be45d6aa65a75e3845108db463c` | Captured five-repeat measurements for all 11 workloads with stable cross-platform provenance. |
| CP11 | Complete; hosted CPU and web checks pass | `134c10cee0a45e531d43b6112a7f03fec507d305` | API, worker, storage, and lifecycle integration verification. |
| CP12 | Complete; hosted checks pass | `a4b5e1bafd6fcec7c6db0f86f92f8616b78072bc` | Browser workbench, rendering, persistence, and export integration. |
| CP13 | Complete; hosted checks pass | `8687dc53a97bdc58b1d85f92cf8447e47f2dc82e` | Verified capabilities, deployment, and limitations docs. |
| CP14 | Complete; technical gates pass, publication blocked by license | `f3516e820836bf29a9a55401d7796cefef0e9dc0` | Full regression, CI, security, and release-gate review. |
| CP15 | Prohibited pending license confirmation | — | Version, annotated tag, and GitHub release only after all gates pass. |

## CP01 — Establish v0.2.0 baseline

- Commit point ID: CP01.
- Commit SHA: recorded in CP02 ledger update after this commit exists.
- Files changed: `docs/omega/V020_PROGRESS.md`.
- Implementation: confirmed PR #11 is merged; verified merge commit and that
  remediation commits `d5166adc69aa5eb71ab18da7b7df50a575987250` and
  `fa1991a6b63bc047a101cf0b72a10ecc943a20ee` are ancestors of `main`; created
  this release branch from the merged main SHA.
- Tests: `$env:PYTHONPATH='python'; python -m pytest tests -q` — 628 passed in
  93.63 seconds.
- Pass/fail: PASS.
- Evidence: PR #11 merge commit; baseline command output in execution record;
  `docs/omega/POST_T210_VALIDATION_RESULTS.md`.
- Remaining issues: Docker daemon runtime status and all release validation are
  still pending. Existing user edit to `web/next-env.d.ts` is preserved.
- Push status: pending initial release-branch push.

## CP02 — Docker configuration and build fixes

- Commit point ID: CP02.
- Commit SHA: recorded in CP03 ledger update after this commit exists.
- Files changed: `Dockerfile.api`, `docker-compose.yml`, `web/middleware.ts`
  (replaced by `web/proxy.ts`).
- Implementation: Compose explicitly builds the web proxy against the internal
  API URL, waits for API health before web startup, and health-checks the web
  service. API image health check now allows startup time and retries. Next.js
  16 proxy convention ensures the bearer token is read on the server at runtime.
- Tests: `docker compose -p neurosim-v020 config --quiet` — PASS;
  `cd web; npm test` — 6 passed;
  `cd web; npm run build` — PASS including TypeScript.
- Docker build: attempted `docker compose -p neurosim-v020 build` — BLOCKED,
  Docker daemon unavailable at `npipe:////./pipe/dockerDesktopLinuxEngine`.
- Pass/fail: configuration/build changes PASS; real image build deferred to
  daemon-enabled CP03 CI.
- Evidence: Compose config output; frontend test/build outputs;
  `docs/omega/POST_T210_VALIDATION_RESULTS.md` for earlier host details.
- Remaining issues: full image build and runtime stack tests required in CP03.
- Push status: CP02 push result recorded in CP03 ledger update.

## CP03 — Docker full-stack runtime and lifecycle verification

- Commit point ID: CP03.
- Commit SHAs: `57051899f2e23f37c96aa1c495bc8c6c2eb68f86`,
  `5fc38b70eed68fbeb562d6f6f6fa0e403b2d48de`,
  `21139cef0ca2d43158ba310e95717055153b532e`.
- Files changed: `.github/workflows/cpu.yml`, `.github/workflows/web.yml`,
  `scripts/smoke_docker_stack.py`, `web/tsconfig.json`,
  `web/tsconfig.e2e.json`, and this ledger.
- Implementation: the daemon-enabled workflow builds and starts the clean API
  plus web stack, waits for health checks, exercises direct API rejection and
  authenticated web proxy access, runs a simulation, retrieves results, retries,
  cancels a running simulation, restarts the API and verifies persisted results,
  captures service logs, then removes only the CI-scoped Compose volume.
- Local checks: `python -m py_compile scripts/smoke_docker_stack.py` — PASS;
  `python -m ruff check scripts/smoke_docker_stack.py` — PASS;
  `docker compose -p neurosim-v020-ci --profile web config --quiet` — PASS.
- Docker runtime: local daemon unavailable (`dockerDesktopLinuxEngine` named
  pipe missing); verified on hosted GitHub Actions Ubuntu runner instead.
- Hosted CI: first candidate run `41113922670` failed at Ruff in Ubuntu/Python
  3.12 after the Python suite passed; matrix fail-fast cancelled remaining jobs.
  The runner selected different ambient lint rules than this host. The lint
  command is isolated with explicit E4/E7/E9/F selection and matrix fail-fast
  is disabled. The first Docker build exposed E2E specs importing test fixtures
  omitted by the production image. Production type-checking now excludes those
  specs while web CI separately type-checks them against fixtures.
- Hosted Docker: PASS in [CI run 41115307566](https://github.com/sreerevanth/nuerosim/actions/runs/41115307566),
  Docker Engine 29.4.2 / Compose 5.1.3 on Linux amd64. Clean compose teardown
  ran before and after. Both images built, health checks passed, and the smoke
  verified unauthenticated API rejection, authenticated Next proxy access,
  simulation create/results, retry, running cancellation, API restart, and
  persisted results. Exact smoke output and service logs are in the run log.
- Web workflow: PASS in [run 41115307664](https://github.com/sreerevanth/nuerosim/actions/runs/41115307664),
  including frontend tests, production build, and Chromium Playwright E2E.
- Pass/fail: PASS; the initially failed Docker build was fixed and the clean
  full-stack lifecycle run passed.
- Remaining issues: none for CP03; continue broader reliability coverage in
  CP11 and final regression in CP14.
- Push status: all CP03 commits are pushed; branch was at `21139cef` during
  verification.

### CP03 repair — separate production and browser E2E type checking

- Files changed: `web/tsconfig.json`, `web/tsconfig.e2e.json`,
  `.github/workflows/web.yml`.
- Implementation: production Next.js type-check excludes Playwright specs that
  import repository-level fixture files unavailable in the production image;
  web CI now separately type-checks those specs and fixture imports with Node
  types before building the app.
- Tests/commands: `cd web; npx tsc --noEmit --project tsconfig.e2e.json` — PASS;
  `cd web; npm run build` — PASS; Docker Compose config — PASS.
- Docker check: resolved by successful build and smoke in CI run 41115307566.
- Evidence: web CI run 41115307664 passed its new E2E TypeScript check, app
  build, and browser tests.
- Remaining issues: none for CP03.

## CP04 — Scientific validation framework and experiment configurations

- Commit point ID: CP04.
- Commit SHA: `97c37038b0cfc2b1fa7ef04f318cb4f77ec74b3c`.
- Files changed: `.github/workflows/cpu.yml`,
  `scripts/run_scientific_validation.py`,
  `tests/test_scientific_validation_runner.py`, `scientific/README.md`,
  `scientific/experiments/v020-core.json`, and two run directories under
  `scientific/results/`.
- Implementation: strict schema/version and unique safe-ID checks; eight
  bounded HH, LIF, AdEx, cable, and seeded-network experiment definitions;
  complete execution manifests and raw traces; deterministic output hashes;
  suite-config SHA-256; wall time and software/platform metadata; refuses to
  overwrite non-empty evidence. CI runs the suite on Ubuntu/Python 3.12 and
  uploads the raw artifacts.
- Tests/commands: `$env:PYTHONPATH='python'; python -m pytest tests/test_scientific_validation_runner.py tests/test_science.py tests/test_hh_reference.py tests/test_lif_exact_reference.py tests/test_adaptive_reference.py tests/test_rk4_convergence.py tests/test_euler_convergence.py tests/test_current_balance.py tests/test_adex_threshold_audit.py -q` — 60 passed;
  `$env:PYTHONPATH='python'; python -m pytest tests/test_scientific_validation_runner.py -q` — 3 passed;
  isolated Ruff E4/E7/E9/F on the runner and test — PASS; standalone suite
  command — PASS for both recorded runs.
- Reproducibility: all 8 `scientific_outputs_sha256` values match between
  `scientific/results/v020-core-run-001/` and `run-002/`;
  suite SHA-256 `c6b0d60281ecd6879cae1f71781ae03b4baed6fadbbc28fbd6e8039325b2f43f`.
- Pass/fail: PASS locally and in hosted CI [run 41116118687](https://github.com/sreerevanth/nuerosim/actions/runs/41116118687).
  Ubuntu/Python 3.12 ran the suite and uploaded `scientific-validation-results`;
  all eight Python matrix jobs, dependency audit, Docker, and web workflows
  passed.
- Evidence: `scientific/results/v020-core-run-001/summary.json`,
  `scientific/results/v020-core-run-002/summary.json`, and per-experiment JSON
  traces in both directories. Hosted artifact upload is added to CPU CI.
- Remaining issues: model-specific tests/references were added in CP05–CP08;
  full release documentation is consolidated in CP13.
- Push status: pushed to `origin/codex/neurosim-v020-release`; verified remote SHA
  `97c37038b0cfc2b1fa7ef04f318cb4f77ec74b3c`.

## CP05 — Hodgkin–Huxley validation

- Commit point ID: CP05.
- Commit SHA: `767d52c44f39dc49565c389f0312fb0e0229ce73`.
- Files changed: `tests/test_science.py`, `scientific/README.md`,
  `.github/workflows/cpu.yml`, and this ledger.
- Implementation: added a stimulus-response regression across 0, 2, 5, and
  10 uA/cm^2; checks spike count and peak voltage rise monotonically without
  inventing exact spike counts. Documented the classical 6.3 °C equations,
  defaults, initial gate state, RK4 step, applied current, and independent
  adaptive-reference method.
- Tests/commands: `python -m pytest tests/test_science.py::test_hh_rate_limits_and_rest tests/test_science.py::test_hh_stimulus_intensity_increases_spike_response tests/test_science.py::test_hh_reference_convergence tests/test_hh_reference.py -q -s` — 10 passed;
  observed maximum voltage errors at `dt=0.025/0.0125 ms` were
  `0.006001657/0.000305376 mV`, a `19.653x` refinement; isolated Ruff on
  `tests/test_science.py` — PASS.
- Reference basis: Hodgkin & Huxley, 1952,
  [DOI 10.1113/jphysiol.1952.sp004764](https://doi.org/10.1113/jphysiol.1952.sp004764);
  independent scalar equations integrated by SciPy DOP853 at `rtol=1e-11`,
  `atol=1e-12`.
- Evidence: `scientific/results/v020-core-run-002/hh_current_clamp.json`;
  stdout from the focused convergence test; `scientific/README.md`.
- Pass/fail: focused checks, full CPU matrix, and web workflow PASS in
  [CPU run 41116458456](https://github.com/sreerevanth/nuerosim/actions/runs/41116458456)
  and [web run 41116458540](https://github.com/sreerevanth/nuerosim/actions/runs/41116458540).
- Remaining issues: LIF/AdEx checks were completed in CP06 and cross-model
  reference/convergence results in CP08.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA verified
  at `767d52c44f39dc49565c389f0312fb0e0229ce73`.

## CP06 — LIF and AdEx validation

- Commit point ID: CP06.
- Commit SHA: `2d91981eb14190ff26f211083a4807d6934570a4`.
- Files changed: `tests/test_science.py`, `scientific/README.md`,
  and this ledger.
- Implementation: parameterized the LIF analytic inter-spike period check at
  three current levels; added monotonic firing-rate checks for LIF and AdEx;
  documented equations, defaults, initial values, solver, operating currents,
  AdEx cutoff/reset rule, and numerical reference tolerances.
- Tests/commands: `$env:PYTHONPATH='python'; python -m pytest tests/test_science.py::test_lif_analytic_subthreshold tests/test_science.py::test_lif_spike_period_and_refractory tests/test_science.py::test_lif_increasing_current_increases_firing_rate tests/test_science.py::test_adex_subthreshold_reference_and_adaptation tests/test_science.py::test_adex_increasing_current_increases_mean_firing_rate tests/test_adaptive_reference.py tests/test_lif_exact_reference.py -q` — 22 passed; isolated Ruff E4/E7/E9/F on `tests/test_science.py` — PASS.
- Outcomes: LIF firing rates at 1/2/4 uA/cm^2 were 30/80/160 Hz over 100 ms;
  AdEx rates at 0.3/1/2/4 uA/cm^2 were 0/15/50/100 Hz over 200 ms. Existing
  exact LIF and independent AdEx DOP853 comparisons passed.
- Evidence: `scientific/results/v020-core-run-002/lif_subthreshold.json`,
  `lif_spike_train.json`, `adex_subthreshold.json`, `adex_adaptation.json`,
  and the LIF/AdEx sections of `scientific/README.md`.
- Pass/fail: local focused validation PASS; CPU and web workflows PASS in
  [run 41116806224](https://github.com/sreerevanth/nuerosim/actions/runs/41116806224)
  and [run 41116806300](https://github.com/sreerevanth/nuerosim/actions/runs/41116806300).
- Remaining issues: passive cable/network validation was completed in CP07;
  combined reference results are captured in CP08.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA verified at
  `2d91981eb14190ff26f211083a4807d6934570a4`.

## CP07 — Passive cable and seeded network validation

- Commit point ID: CP07.
- Commit SHA: `df4e3ddf1acd72d05def26ca876ef1052a880259`.
- Files changed: `tests/test_science.py`, `scientific/README.md`,
  and this ledger.
- Implementation: compare the actual cable solver's full three-compartment
  trajectory against a separately integrated DOP853 system; strengthen network
  same-seed checks to include spikes and prohibit self-edges; document sealed
  cable assumptions, units, defaults, network seed, connectivity, synaptic
  decay, and implementation size limits.
- Tests/commands: `$env:PYTHONPATH='python'; python -m pytest tests/test_science.py::test_cable_production_trajectory_matches_dop853_reference tests/test_science.py::test_passive_cable_conservation_and_decay tests/test_science.py::test_network_seed_inhibition_and_recording tests/test_current_balance.py -q -s` — 7 passed; Ruff E4/E7/E9/F on `tests/test_science.py` — PASS.
- Outcome: cable maximum absolute voltage error against DOP853 was
  `8.467822e-10 mV` (required below `1e-7 mV`); exact deterministic network
  traces and changed-seed topology checks passed.
- Reference basis: SciPy DOP853 high-accuracy reference for the explicit
  passive chain ODE; Rall (1959),
  [DOI 10.1016/0014-4886(59)90046-9](https://doi.org/10.1016/0014-4886(59)90046-9)
  for passive cable context.
- Evidence: `scientific/results/v020-core-run-002/cable_charge.json`,
  `network_seeded.json`, and `scientific/README.md`.
- Pass/fail: local focused validation PASS; all CPU matrix/Docker jobs PASS in
  [run 41117106783](https://github.com/sreerevanth/nuerosim/actions/runs/41117106783)
  and web workflow PASS in [run 41117106807](https://github.com/sreerevanth/nuerosim/actions/runs/41117106807).
- Remaining issues: none for CP07; aggregated reference report is in CP08.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA verified at
  `df4e3ddf1acd72d05def26ca876ef1052a880259`.

## CP08 — Independent reference comparisons and convergence

- Commit point ID: CP08.
- Commit SHA: `927a929345aa2025286c5243608f40c0d05d1dc3`.
- Files changed: `scripts/run_reference_validation.py`,
  `tests/test_reference_validation_runner.py`, `.github/workflows/cpu.yml`,
  `scientific/README.md`, `scientific/results/v020-reference-comparisons-002.json`,
  and this ledger.
- Implementation: aggregates seven reference checks into a reproducible JSON
  report with input fixture SHA-256s, reference methods, physical units,
  measured errors, limits, and Python/NumPy/SciPy/platform metadata. Covers
  published HH rates/gates, exact LIF voltage, HH DOP853 sensitivity, RK4 and
  Euler convergence orders, independent AdEx state comparison, and independent
  passive-cable trajectory comparison. Reports AdEx voltage and adaptation
  errors with separate dimensional tolerances. CPU CI runs and uploads this
  report with raw simulation traces.
- Tests/commands: `$env:PYTHONPATH='python'; python -m pytest tests/test_science.py tests/test_hh_reference.py tests/test_lif_exact_reference.py tests/test_adaptive_reference.py tests/test_rk4_convergence.py tests/test_euler_convergence.py tests/test_current_balance.py tests/test_reference_validation_runner.py tests/test_scientific_validation_runner.py -q` — 63 passed; `$env:PYTHONPATH='python'; python scripts/run_reference_validation.py --output scientific/results/v020-reference-comparisons-002.json` — 7/7 passed; `python -m ruff check --isolated --select E4,E7,E9,F scripts/run_reference_validation.py tests/test_reference_validation_runner.py` — PASS.
- Outcomes: LIF analytic max error `7.105427e-14 mV`; HH observed RK4/Euler
  orders `4.296705/0.996244`; AdEx max voltage/adaptation errors
  `6.309619e-12 mV / 3.756717e-14 uA/cm^2`; cable max trajectory error
  `8.467822e-10 mV`; all within recorded limits.
- Evidence: `scientific/results/v020-reference-comparisons-002.json` and the
  methodology/results sections in `scientific/README.md`.
- Pass/fail: local reference/convergence suite PASS; Ubuntu/Python 3.12 science
  report and web workflow PASS in [CPU run 41117788665](https://github.com/sreerevanth/nuerosim/actions/runs/41117788665)
  and [web run 41117788680](https://github.com/sreerevanth/nuerosim/actions/runs/41117788680).
  Docker build/runtime and all matrix jobs in the CPU run PASS.
- Remaining issues: benchmark methodology and measured benchmark results in
  CP09–CP10; broader documentation consolidated in CP13.
- Push status: pushed to `origin/codex/neurosim-v020-release`;
  remote branch is `codex/neurosim-v020-release` at
  `927a929345aa2025286c5243608f40c0d05d1dc3`.

## CP09 — Benchmark harness and measurement methodology

- Commit point ID: CP09.
- Commit SHA: recorded in CP10 ledger update after this commit exists.
- Files changed: `benchmarks/v020-workloads.json`,
  `scripts/run_release_benchmarks.py`, `tests/test_release_benchmarks.py`,
  `docs/BENCHMARK_METHODOLOGY.md`, `.github/workflows/cpu.yml`, and this ledger.
- Implementation: 11 representative CPU workloads across HH/LIF/AdEx, seeded
  network size/connectivity, duration, and result handling; one discarded
  warm-up and five measured repetitions by default; each sample runs in a fresh
  subprocess. Separately measures setup, simulation, JSON encode/decode,
  process peak RSS and incremental RSS; emits raw samples plus mean, median,
  sample standard deviation, p95, min, and max. Records hardware, OS, versions,
  thread environment, workload config, source revision, and input/runner hashes.
- Tests/commands: `$env:PYTHONPATH='python'; python -m pytest tests/test_release_benchmarks.py -q` — 3 passed; `python -m ruff check --isolated --select E4,E7,E9,F scripts/run_release_benchmarks.py tests/test_release_benchmarks.py` — PASS; `python -m py_compile scripts/run_release_benchmarks.py` — PASS; `$env:PYTHONPATH='python'; python -c "import json; from pathlib import Path; from scripts.run_release_benchmarks import _validate_document; d=json.loads(Path('benchmarks/v020-workloads.json').read_text()); print(_validate_document(d)); print('workloads',len(d['workloads']))"` — warm-up/repetition policy valid; 11 workloads accepted.
- Failure fixed: the first Windows run showed that `GetProcessMemoryInfo` used
  an implicit 32-bit handle signature. Explicit Win32 function prototypes fixed
  it; the complete focused test rerun passed.
- Pass/fail: harness unit tests, configuration validation, Ubuntu CPU matrix,
  Docker build/runtime smoke, and web workflow PASS in [CPU run 41118478729](https://github.com/sreerevanth/nuerosim/actions/runs/41118478729)
  and [web run 41118478731](https://github.com/sreerevanth/nuerosim/actions/runs/41118478731).
- Evidence: `docs/BENCHMARK_METHODOLOGY.md`,
  `benchmarks/v020-workloads.json`, and `tests/test_release_benchmarks.py`.
- Remaining issues: actual benchmark execution and raw measurements are
  captured in CP10.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA
  verified at `60c00909ef07a97f5c0267db52047f68aaaf750e`.

## CP10 — Execute benchmarks and publish measured results

- Commit point ID: CP10.
- Commit SHA: `0717caff6f10ecf9368b920c314b2af3d985f8f7`.
- Corrective commit SHA: `26f52904b368a99dfd7a8e26130c4a426dce11f8`.
- Stable artifact writer commit SHA: `89f9745a87dd01bf54f554d739cec74175becddc`.
- Results publication commit SHA: `59bb8de51b3b0be45d6aa65a75e3845108db463c`.
- Files changed: `benchmarks/results/v020-run-004.json` (captured raw samples
  and aggregates), `docs/BENCHMARK_RESULTS.md`,
  `docs/BENCHMARK_METHODOLOGY.md`, `scripts/run_release_benchmarks.py`,
  `scripts/verify_release_benchmark_report.py`,
  `tests/test_benchmark_report.py`, `tests/test_release_benchmarks.py`,
  `.gitattributes`, and this ledger. The tracked run-001 report was removed after CI exposed
  checkout-dependent raw-byte hashes; local draft runs 002 and 003 were
  replaced by the LF-stable run 004.
- Implementation: ran the configured 11 CPU workloads with one discarded
  warm-up and five fresh-process repetitions each. Every workload produced the
  same deterministic output SHA across its repetitions. Published the measured
  timing, result-size, and incremental RSS summaries with host metadata and
  clear scope limits. Added a report verifier that recomputes summaries from
  raw samples and checks canonicalized config and runner hashes. Canonical
  sorted-key JSON and LF-normalized source/output make hashes stable across
  Windows and Unix checkouts.
- Tests/commands: `$env:PYTHONPATH='python'; python scripts/run_release_benchmarks.py --config benchmarks/v020-workloads.json --output benchmarks/results/v020-run-004.json` — 11 workloads, 5 repetitions each, PASS; `python scripts/verify_release_benchmark_report.py --report benchmarks/results/v020-run-004.json` — PASS; `$env:PYTHONPATH='python'; python -m pytest tests/test_benchmark_report.py tests/test_release_benchmarks.py -q` — 7 passed; `python -m ruff check --isolated --select E4,E7,E9,F scripts/run_release_benchmarks.py tests/test_release_benchmarks.py scripts/verify_release_benchmark_report.py tests/test_benchmark_report.py` — PASS; `python -m py_compile scripts/run_release_benchmarks.py tests/test_release_benchmarks.py scripts/verify_release_benchmark_report.py tests/test_benchmark_report.py` — PASS.
- Failure fixed: CPU run 41119339102 and the CP11 workflow at 41119716700
  rejected the earlier run on Windows because the config hash included
  checkout-specific line endings. The harness now hashes canonical JSON, and
  regression tests verify LF/CRLF config and runner inputs and LF output bytes.
  Hosted validation for the corrected code is still pending.
- Outcome: simulation median ranged from 0.237 s (`lif-network-8-p50-30ms`)
  to 4.727 s (`lif-long-1000ms`). The 64-cell 200 ms serialization workload
  produced a 1,501,263-byte JSON result with 35.424 ms median encoding,
  26.921 ms median decoding, and 20.82 MiB incremental peak RSS. These are
  single-host serial CPU measurements, not throughput claims.
- Evidence: `benchmarks/results/v020-run-004.json` (SHA-256
  `72b27b56508b92e8aefd072375b928170e9f4b2b3315ad29afa8d93655a040bf`),
  `docs/BENCHMARK_RESULTS.md`, and `docs/BENCHMARK_METHODOLOGY.md`.
- Pass/fail: corrected benchmark execution, LF/CRLF hash regression, stable
  report-byte regression, report verification, and focused tests PASS; hosted
  CPU [run 41122245333](https://github.com/sreerevanth/nuerosim/actions/runs/41122245333)
  and web [run 41122245338](https://github.com/sreerevanth/nuerosim/actions/runs/41122245338)
  both passed on the report publication head.
- Remaining issues: no benchmark-specific blocker remains. This benchmark does
  not measure API queuing, concurrent users, or deployment storage; lifecycle
  and storage behavior is covered separately in CP11.
- Push status: all CP10 work pushed to
  `origin/codex/neurosim-v020-release`; remote SHA verified at
  `59bb8de51b3b0be45d6aa65a75e3845108db463c`.

## CP11 — API, worker, storage, and lifecycle integration

- Commit point ID: CP11.
- Commit SHA: `134c10cee0a45e531d43b6112a7f03fec507d305`.
- Files changed: `tests/test_release_reliability.py` and this ledger.
- Implementation: added an end-to-end large-result check using the production
  64-cell workload shape. It verifies API result retrieval, history limit
  validation, online SQLite backup while the application is open, restore,
  API restart, manifest retention, and full result equality after recovery.
  Added endpoint-level activity pagination checks and verified that closing an
  active worker cancels promptly, releases the database lock, and allows a
  replacement worker to acquire it. Existing API tests cover auth/read-only
  modes, queue limits, retries, failures, cancellation, and interrupted-job
  recovery.
- Tests/commands: `$env:PYTHONPATH='python'; python -m pytest tests/test_release_reliability.py tests/test_api.py tests/test_visualization_api.py tests/test_post_t210_remediation.py -q` — 35 passed in 6.94 seconds; `python -m ruff check --isolated --select E4,E7,E9,F tests/test_release_reliability.py` — PASS; `python -m py_compile tests/test_release_reliability.py` — PASS.
- Failure fixed: the initial shutdown-test fixture exceeded the simulator's
  10-million neuron-step input cap. Reduced the test to 200 neurons so the
  long-running job stays inside supported limits and can exercise shutdown.
- Evidence: `tests/test_release_reliability.py`,
  `tests/test_api.py`, `tests/test_visualization_api.py`, and
  `tests/test_post_t210_remediation.py`.
- Pass/fail: focused local integration suite PASS. The hosted CPU matrix and
  web integration workflow, including this test file, passed together on the
  later publication head in runs
  [41122245333](https://github.com/sreerevanth/nuerosim/actions/runs/41122245333)
  and [41122245338](https://github.com/sreerevanth/nuerosim/actions/runs/41122245338).
  Earlier Windows failures on runs 41119716700 and
  41119717047 were caused by the now-fixed CP10 line-ending hash defect.
- Remaining issues: full regression and security/release gate review are CP14.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA
  verified at `134c10cee0a45e531d43b6112a7f03fec507d305`.

## CP12 — Frontend, browser, and export integration

- Commit point ID: CP12.
- Commit SHA: `a4b5e1bafd6fcec7c6db0f86f92f8616b78072bc`.
- Files changed: `.github/workflows/web.yml`,
  `web/tests/e2e/connectivity.spec.ts`, refreshed screenshots and measured
  browser results in `docs/validation/`,
  `docs/WEB_INTEGRATION_VALIDATION.md`, and this ledger.
- Implementation: extended the real browser workbench flow to follow the
  completed simulation's **Export data** link, assert the downloaded filename
  is `neurosim-results.zip`, and verify the ZIP local-file signature and
  non-trivial payload size. The Python API integration test separately checks
  the archive's expected member files. The e2e suite also covered invalid and
  valid experiment forms, seeded demonstrations, saved topology and reload,
  paired comparison persistence, SVG download, valid/invalid SWC import,
  responsive layout, 512-neuron rendering, WebGL2/2D fallback, and renderer
  performance reporting. Updated CI artifact paths to retain the actual
  redesign benchmark JSON and exhibition screenshots produced by these tests.
- Tests/commands: `npm test` — 6 passed; `npx tsc --noEmit --project tsconfig.e2e.json` — PASS; `npx prettier --check tests/e2e/connectivity.spec.ts` — PASS; `$env:NEUROSIM_TEST_PYTHON='python'; npm run test:e2e` — 6 passed in 1.7 minutes, including the ZIP download assertion.
- Outcome: actual browser downloads, saved results, comparison and reload,
  renderer fallback, and mobile layout all passed. The measured renderer
  profile and screenshots were refreshed by the passing browser run.
- Evidence: `docs/WEB_INTEGRATION_VALIDATION.md`,
  `docs/validation/web-3d-redesign.png`,
  `docs/validation/web-mobile-redesign.png`,
  `docs/validation/web-fallback-redesign.png`,
  `docs/validation/web-network-512-auto.png`,
  `docs/validation/web-network-512-redesign.png`, the exhibition screenshots,
  and `docs/validation/web-render-benchmark-redesign.json`.
- Pass/fail: all focused local browser and frontend checks PASS. Hosted CPU
  [run 41122970088](https://github.com/sreerevanth/nuerosim/actions/runs/41122970088)
  and web [run 41122970014](https://github.com/sreerevanth/nuerosim/actions/runs/41122970014)
  both passed on this commit.
- Remaining issues: full regression and security/release gate review are CP14.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA
  verified at `a4b5e1bafd6fcec7c6db0f86f92f8616b78072bc`.

## CP13 — Documentation, deployment, and limitations

- Commit point ID: CP13.
- Commit SHA: `8687dc53a97bdc58b1d85f92cf8447e47f2dc82e`.
- Files changed: `docs/DEPLOYMENT.md`, `docs/VALIDATION.md`, `README.md`, and
  this ledger.
- Implementation: added Compose instructions for API-only and full web startup,
  generated bearer-token setup, loopback binding, health checks, SQLite volume
  retention and online backup, and data-preserving shutdown. Documented the
  reverse-proxy trust boundary, absent accounts/TLS/rotation, local-only SQLite
  constraints, supported scientific bounds, unsupported CUDA/MPI, renderer
  measurement limits, and unresolved licensing. Linked the deployment guide
  from the README and refreshed the validation index with dated CP10–CP12
  evidence and unresolved release gates.
- Tests/commands (all PASS):

  ```powershell
  python -c "from pathlib import Path; fs=[Path('README.md'),Path('docs/DEPLOYMENT.md'),Path('docs/VALIDATION.md'),Path('docs/WEB_INTEGRATION_VALIDATION.md')]; links=[(f,u.split(')',1)[0]) for f in fs for u in f.read_text(encoding='utf-8').split('](')[1:]]; bad=[(str(f),u) for f,u in links if not u.startswith(('http://','https://','mailto:','#')) and u.split('#',1)[0] and not (f.parent/u.split('#',1)[0]).exists()]; print('Markdown local links: PASS' if not bad else bad); assert not bad"
  python -c "import yaml; files=['docker-compose.yml','.github/workflows/cpu.yml','.github/workflows/web.yml']; [yaml.safe_load(open(f, encoding='utf-8')) for f in files]; print('YAML parse: PASS (3 files)')"
  $env:NEUROSIM_AUTH_TOKEN='neurosim-documentation-validation-token'; docker compose config --quiet
  git diff --check
  ```

  The local Docker daemon remains unavailable, so no local image startup was
  claimed.
- Outcome: deployment and validation guidance now describes verified behavior,
  accurately distinguishes prior hosted Docker smoke evidence from local
  runtime availability, and keeps license and release gates visible.
- Evidence: `docs/DEPLOYMENT.md`, `docs/VALIDATION.md`,
  `docs/omega/POST_T210_REMAINING_LIMITATIONS.md`, and CP10/CP11/CP12 records
  above.
- Pass/fail: documentation links, Compose configuration, YAML parsing, and
  whitespace checks PASS. CP13 CPU run
  [41123539549](https://github.com/sreerevanth/nuerosim/actions/runs/41123539549)
  and web run
  [41123539587](https://github.com/sreerevanth/nuerosim/actions/runs/41123539587)
  subsequently passed, including hosted Docker and browser checks.
- Remaining issues: confirmed license terms remain an explicit release gate;
  full regression, current security scans, and release review are CP14.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA
  verified at `8687dc53a97bdc58b1d85f92cf8447e47f2dc82e`.

## CP14 — Full regression, CI, security, and release-gate review

- Commit point ID: CP14.
- Commit SHA: `f3516e820836bf29a9a55401d7796cefef0e9dc0` (recorded in this
  closure update because a commit cannot contain its own SHA).
- Files changed: `docs/RELEASE_GATE.md`, `docs/VALIDATION.md`, `README.md`,
  and this ledger.
- Implementation: reviewed the full test suite in both the checkout and a
  clean installed-wheel environment; reconciled the Windows/Linux workflow
  matrix, Docker lifecycle smoke, browser checks, science/reference validation,
  and current dependency audits. Confirmed version metadata remains
  `0.2.0.dev0`, no v0.2.0 tag/release exists, and the repository has no
  `LICENSE*` or `COPYING*` file or license declaration in `pyproject.toml`.
- Tests/commands:

  ```powershell
  $env:PYTHONPATH='python'; python -m pytest tests -q
  python -m build --wheel
  $releaseVenv='C:\Users\sreer_mg\AppData\Local\Temp\neurosim-cp14-f910d9a120f24883bb2b927241566334'
  python -m venv $releaseVenv
  & "$releaseVenv\Scripts\python.exe" -m pip install '.[dev]'
  $wheel=(Get-ChildItem dist\neurosim-0.2.0.dev0-*.whl | Select-Object -First 1).FullName
  & "$releaseVenv\Scripts\python.exe" -m pip install --force-reinstall --no-deps $wheel
  & "$releaseVenv\Scripts\python.exe" -m pip check
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  & "$releaseVenv\Scripts\python.exe" -m pytest tests -q
  python -m pip_audit -r requirements-runtime.lock
  # From web/:
  npm audit --audit-level=high
  npm test
  npx tsc --noEmit --project tsconfig.e2e.json
  npm run build
  # From repository root, local link check for README and release guides:
  python -c "from pathlib import Path; fs=[Path('README.md'),Path('docs/DEPLOYMENT.md'),Path('docs/VALIDATION.md'),Path('docs/WEB_INTEGRATION_VALIDATION.md'),Path('docs/RELEASE_GATE.md')]; links=[(f,u.split(')',1)[0]) for f in fs for u in f.read_text(encoding='utf-8').split('](')[1:]]; bad=[(str(f),u) for f,u in links if not u.startswith(('http://','https://','mailto:','#')) and u.split('#',1)[0] and not (f.parent/u.split('#',1)[0]).exists()]; print('Markdown local links: PASS' if not bad else bad); assert not bad"
  git diff --check
  ```

  Checkout suite: 649 passed in 130.61 s. Clean installed-wheel suite: 649
  passed in 113.96 s with one upstream Starlette/httpx deprecation warning;
  clean environment `pip check` found no broken requirements. Wheel build,
  runtime audit, npm audit (0 vulnerabilities), six frontend tests, TypeScript,
  and production build passed. A `pip check` in the shared global Python
  environment reported conflicts in unrelated `fastmcp`/`python-dotenv` and
  `yfinance`/`curl-cffi` packages; the fresh project environment is clean.
- Hosted checks: CPU run
  [41123539549](https://github.com/sreerevanth/nuerosim/actions/runs/41123539549)
  passed all eight Windows/Linux Python versions, dependency audit, scientific
  and reference validation, and the Docker image/full-stack lifecycle smoke.
  Web run
  [41123539587](https://github.com/sreerevanth/nuerosim/actions/runs/41123539587)
  passed npm audit, unit tests, e2e typecheck, production build, and all six
  Chromium end-to-end tests.
- Outcome: all technical regression, security-dependency, scientific,
  cross-platform, browser, and hosted Docker gates passed. CP15 cannot run:
  license ownership and terms are unconfirmed, which is an explicit release
  blocker in the repository's release contract.
- Evidence: `docs/RELEASE_GATE.md`, `docs/VALIDATION.md`,
  `docs/omega/POST_T210_VALIDATION_RESULTS.md`, and the linked hosted workflow
  runs above.
- Pass/fail: technical gates PASS; publication gate BLOCKED by unresolved
  licensing. The local Docker daemon was unavailable, while the hosted Docker
  build and runtime check passed.
- Remaining issues: resolve and document the project license before any v0.2.0
  tag or GitHub release. Keep version `0.2.0.dev0` until then.
- Push status: CP14 report commit pushed to
  `origin/codex/neurosim-v020-release`; remote SHA verified at
  `f3516e820836bf29a9a55401d7796cefef0e9dc0`.
