# Day 01 — Baseline and scientific contract

**Status:** complete. **Tested code revision:** `91231ea64f4cb4455cb7ee808f1f05b1e785fdd6`. **Branch:** `exhibition-2026-10-28`.

## Work delivered

| Package | Delivered capability |
|---|---|
| T001 | Read-only repository tree provenance inventory |
| T002 | Git-tree lockfile size and SHA-256 inventory |
| T003 | Legacy module/archive and project-entrypoint boundary map |
| T004 | Deterministic FastAPI OpenAPI contract snapshot |
| T005 | Scientific units and population-rate audit |
| T006 | Pydantic parameter-bound/default audit |
| T007 | Event delay rounding and saved schedule audit, sharing engine timing logic |
| T008 | Immutable read-only SQLite schema compatibility check for offline databases |
| T009 | Browser renderer selection and interactive 2D fallback contract audit |
| T010 | GitHub Actions runner/runtime matrix inventory |
| T011 | Shell-free test command baseline capture with bounded output and timeout |
| T012 | Repeatable seeded CPU benchmark profiles and median/reproducibility report |
| T013 | HH trace comparison against independent DOP853 samples |
| T014 | Subthreshold LIF trace comparison against the closed-form RC response |
| T015 | Required-check signoff and explicitly dispositioned residual-risk register |

Detailed contracts and per-package evidence are linked from each `docs/omega/Tnnn-*.md` page. Overall baseline record: [.omega/day01-signoff.json](../../.omega/day01-signoff.json).

## Verification gate

- Python: `python -m pytest tests -q` — **107 passed** in 21.91 seconds.
- Web unit tests: `npm test` — **6 passed**.
- Web build: `npm run build` — Next.js production build and TypeScript passed.
- Browser E2E: `npm run test:e2e` — **6 passed** in 1.4 minutes, including the 512-neuron renderer benchmark.
- Baseline signoff: **4/4 required checks passed**, with 3 accepted residual risks.
- Scientific reference checks: HH maximum sampled error `5.6051e-6 mV` (tolerance `0.02 mV`); subthreshold LIF maximum sampled error `2.13e-14 mV` (tolerance `1e-9 mV`).
- CPU HH benchmark: 2 runs, `0.821412 s` and `0.738805 s`, median `0.780109 s`; saved voltage, spikes, and connectivity were identical.

E2E regenerated nine tracked screenshots/benchmark files. They were restored to their pre-run versions after verification; the worktree was clean at the gate. WebGPU was unavailable in headless Chromium, which used WebGL2 and the tested 2D fallback.

## Risks and limits

The baseline is local to Windows 11 / Python 3.14.2 and the recorded web toolchain. Physical WebGPU behavior/performance, hosted GitHub Actions results, and Docker runtime were not established in this gate. These are documented as accepted residual risks in the signoff record; acceptance does not constitute release approval. The HH fixture samples five times from one configuration; the LIF fixture covers one subthreshold case only. CPU benchmark timings are host/load-dependent observations.

## Commit and delivery counts

From base `5416e0f87040924e68ebd47eea332d0e98fd1dc2` through completion of Day 01, **149 authored substantive commits** were recorded on this feature branch. **Pushed: 0; merged: 0; default-branch/graph-eligible: 0.** This is **1 below** the document's 150-commit target; no empty or artificial commits were added. No release or merge is claimed.

## Next execution point

`.omega/state.json` advances to **T016/U01 — units typed primitives**, Day 02. Per the continuous-execution instruction, work proceeds to the next bucket without waiting for a calendar change.
