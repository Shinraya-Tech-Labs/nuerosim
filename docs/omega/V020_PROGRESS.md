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
| CP02 | Complete; daemon build deferred to CP03 CI | SHA recorded in CP03 ledger update | Improved container health ordering and Next.js runtime token proxy. |
| CP03 | Pending | — | Full stack runtime, persistence, and lifecycle verification. |
| CP04 | Pending | — | Scientific validation framework and machine-readable configurations. |
| CP05 | Pending | — | Hodgkin-Huxley validation. |
| CP06 | Pending | — | LIF and AdEx validation. |
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
