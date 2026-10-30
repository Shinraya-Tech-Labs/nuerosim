# NeuroSim v0.2.0 browser integration results

The browser integration suite exercised the local Next.js workbench against a
real FastAPI service and SQLite job store on **2026-10-30**.

## Checks

- `npm test` — 6 Vitest tests passed.
- `npx tsc --noEmit --project tsconfig.e2e.json` — passed.
- `npx prettier --check tests/e2e/connectivity.spec.ts` — passed.
- `$env:NEUROSIM_TEST_PYTHON='python'; npm run test:e2e` — 6 Playwright tests
  passed in 1.7 minutes.

The browser suite submitted real simulations and checked job validation,
recorded topology and traces, event playback, saved comparisons after reload,
SVG export, the `neurosim-results.zip` browser download, valid and invalid SWC
imports, a 512-neuron rendering profile, the WebGL2-to-2D fallback, and mobile
layout. The ZIP download check verifies its filename, local-file ZIP signature,
and payload size; the Python API integration test verifies the archive entries.

## Evidence

The Playwright run refreshed screenshots for the 3D workbench, mobile layout,
renderer fallback, network profile, exhibition history, and comparison view in
[`docs/validation/`](validation/). Its measured renderer observations are in
[`web-render-benchmark-redesign.json`](validation/web-render-benchmark-redesign.json).
The measurement is from headless Chromium with software WebGL on the recorded
host. It is a reproducible browser profile, not a physical-GPU performance
claim.

## Reproduce

From the repository root on Windows:

```powershell
cd web
$env:NEUROSIM_TEST_PYTHON='python'
npm test
npx tsc --noEmit --project tsconfig.e2e.json
npx prettier --check tests/e2e/connectivity.spec.ts
npm run test:e2e
```

CI runs the same Playwright suite with Chromium installed and uploads the web
and exhibition screenshots, browser benchmark JSON, and Playwright test
results.
