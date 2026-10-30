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
| CP05 | Pushed; hosted CI pending | `767d52c44f39dc49565c389f0312fb0e0229ce73` | Hodgkin-Huxley stimulus-response and DOP853 convergence evidence. |
| CP06 | Implemented; commit SHA recorded in CP07 ledger update | Pending this commit | LIF analytic periods and LIF/AdEx stimulus response. |
| CP07 | Pending | — | Passive cable and seeded network validation. |
| CP08 | Pending | — | Independent references and convergence studies. |
| CP09 | Pending | — | Reproducible benchmark harness and methodology. |
| CP10 | Pending | — | Benchmark runs, raw measurements, and results. |
| CP11 | Pending | — | API, worker, storage, and lifecycle integration. |
| CP12 | Pending | — | Frontend, browser, and export integration. |
| CP13 | Pending | — | Verified capabilities, deployment, and limitations docs. |
| CP14 | Pending | — | Full regression, CI, security, and release-gate review. |
| CP15 | Pending | — | Version, annotated tag, and GitHub release (only if all gates pass). |

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
- Remaining issues: model-specific equation/parameter/tolerance writeups and
  deeper validation additions continue in CP05–CP08 and CP13.
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
- Pass/fail: focused model checks PASS; CPU [run 41116458456](https://github.com/sreerevanth/nuerosim/actions/runs/41116458456)
  and web CI [run 41116458540](https://github.com/sreerevanth/nuerosim/actions/runs/41116458540)
  are still running.
- Remaining issues: LIF/AdEx checks in CP06 and cross-model reference/convergence
  summary in CP08.
- Push status: pushed to `origin/codex/neurosim-v020-release`; remote SHA verified
  at `767d52c44f39dc49565c389f0312fb0e0229ce73`.

## CP06 — LIF and AdEx validation

- Commit point ID: CP06.
- Commit SHA: recorded in CP07 ledger update after this commit exists.
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
- Pass/fail: local focused validation PASS; hosted CI will run on this commit.
- Remaining issues: passive cable/network validation in CP07; combined
  independent reference and convergence report in CP08.
- Push status: pending commit and push.
