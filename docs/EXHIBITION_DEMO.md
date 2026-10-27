# NeuroSim exhibition demo

This runbook uses the local CPU engine and persisted experiment API. The three
guided actions in the workspace submit ordinary validated experiments; they do
not load prewritten results. Their configurations are recorded in each saved
manifest. Allow a few minutes for the first frontend build on a slow disk.

## First-time Windows setup

Requirements: Python 3.11+, Node.js 22+, npm, and Git. The repository is named
`nuerosim` on GitHub.

```powershell
git clone https://github.com/Shinraya-Tech-Labs/nuerosim.git
Set-Location nuerosim
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
cd web
npm ci
Set-Location ..
```

Keep two PowerShell terminals open. Terminal 1 starts the real API and CPU job
worker:

```powershell
Set-Location .\nuerosim
.\.venv\Scripts\Activate.ps1
neurosim serve
```

Terminal 2 starts the Next.js workbench:

```powershell
Set-Location .\nuerosim\web
npm run dev
```

Open <http://127.0.0.1:3000>. API health is at
<http://127.0.0.1:8000/health>; interactive API docs are at
<http://127.0.0.1:8000/docs>. The application is single-user and local. Keep
both servers on loopback.

## Offline-day checklist

- Complete the setup above while internet access is available; `npm ci` and
  Python package installation need the package cache or network on first use.
- Keep the repository, `.venv`, and `web/node_modules` on the demo machine.
- Start both servers once before the audience arrives and confirm `/health`.
- The workbench uses no hosted fonts, images, login, or cloud API. Browser
  package installation and first build are not offline if dependencies are
  missing.
- Save any important experiments through the UI export link. The default local
  SQLite data lives under `neurosim-data`; set `NEUROSIM_DB` before starting the
  API to choose another database file.

## Recovery

- **Port 3000 busy:** in Terminal 2 run `npm run dev -- --port 3001`, then open
  <http://127.0.0.1:3001>.
- **Port 8000 busy:** stop the other process if appropriate. Otherwise start
  the API on another loopback port with
  `python -m uvicorn neurosim.workbench.api:app --host 127.0.0.1 --port 8001`.
  Before starting Next.js, set `$env:NEUROSIM_API_URL='http://127.0.0.1:8001'`.
- **Python import or command failure:** activate `.venv`, return to the repo
  root, and run `python -m pip install -e '.[dev]'`. Use `python -m uvicorn ...`
  as shown above if the `neurosim` script is not on PATH.
- **npm dependency failure:** from `web`, run `npm ci` with access to the
  package cache or registry. Do not update package versions during setup.
- **API unavailable in UI:** check Terminal 1 and open `/health`; confirm the
  UI rewrite points to the same API port. Look for the UI's API error state.
- **Slow 3D view:** use the viewport controls to select a lower edge budget or
  2D fallback. The 512-neuron case has 20,786 saved connections; the view is
  bounded to 2,048 by default. This does not reduce the saved scientific data.
- **Renderer unavailable:** check the renderer badge. Auto mode tries WebGPU
  only when supported, then WebGL2; failure falls back to 2D canvas. Do not
  interpret node placement or animated highlights as anatomy or propagation.
- **No saved runs:** start a guided experiment; successful results persist in
  SQLite. If changing `NEUROSIM_DB`, use the same path on every API restart.
- **Return to last known good source:** `git log --oneline` to identify the
  desired commit, then create a recovery branch with
  `git switch -c recovery/<name> <commit>`. Do not reset a branch with local
  changes.

## Three-minute demonstration

### 30-second introduction

“NeuroSim is a local, reproducible workbench for bounded neuron and network
experiments. The browser is showing topology and activity saved by the CPU
simulation service. Each run carries its configuration and random seed. The
network layout is a visual aid rather than anatomy; the plots and spike events
come from the saved simulation.”

### Timed sequence

| Time | Action and narration |
| --- | --- |
| 0:00–0:20 | Open the workbench. Point out the active renderer badge, experiment history, and empty-state HH action. Explain that the service and SQLite database run locally. |
| 0:20–0:55 | Click **01 · HH single-neuron firing**. Wait for completion. Expand **CONFIGURED CURRENT INPUT** and show the configured pulse, then inspect the recorded voltage trace and spike raster. The displayed pulse is configuration metadata, not a measured input trace. |
| 0:55–1:35 | Click **02 · Seeded LIF network**. Inspect the saved 128-neuron topology and recorded excitatory/inhibitory edges. Press play and scrub the timeline; voltage, raster, rate, and node highlighting follow recorded timestamps. |
| 1:35–2:15 | Select a neuron and inspect its saved connections. Change the connection filter or edge budget. Explain that coordinates are deterministic layout coordinates, not physical positions or axons. |
| 2:15–2:45 | Click **03 · Compare 8 vs 12 µA/cm²**. It executes two separately persisted LIF experiments, with the pulse amplitude as the changed input. Wait for both jobs and point to the overlaid recorded voltage traces. Describe only the observed traces. |
| 2:45–3:00 | Show the manifest seed/configuration or export a completed result. State limitations: bounded CPU simulations, single-user local service, and no clinical or anatomical claim. |

The guided configurations are named “Exhibition · HH current clamp”,
“Exhibition · seeded LIF network”, and “Exhibition · LIF pulse 8/12 µA/cm²”.
Their settings are respectively: HH, one neuron, 50 ms, `dt=0.025 ms`, seed 42,
10 µA/cm² over `[10,40)` ms; LIF, 128 neurons, connection probability 0.08,
seed 42, 30 ms, with 16 neurons receiving 20 µA/cm² over `[0,30)` ms; and two
single-neuron LIF runs, 50 ms, `dt=0.025 ms`, seed 42, with the one changed
parameter set to 8 or 12 µA/cm² over `[10,40)` ms. They create real jobs.
Expected output types are recorded voltage, spike events, saved topology,
metadata, and derived population-rate bins; counts below are from actual runs,
not values hardcoded into the visualization.

## Judge questions

1. **Are these measurements from a brain?** No. They are numerical outputs of
   documented simplified models; no experimental dataset is shown.
2. **Is the 3D arrangement anatomical?** No. It is a deterministic illustrative
   layout. Saved directed edges are genuine model connectivity.
3. **What makes a run reproducible?** The manifest records parameters, seed,
   input pulses, configuration hash, saved connectivity, and software metadata.
4. **Does playback invent spikes?** No. Highlights are derived from saved spike
   timestamps and the selected simulation time.
5. **What do orange and cyan mean?** Saved excitatory and inhibitory synapse
   classes, respectively.
6. **Why do traces jump at spikes?** LIF uses a threshold/reset rule and the
   solver's threshold events are quantized to the integration timestep.
7. **What is the comparison changing?** The guided comparison changes only the
   configured LIF input pulse amplitude; both jobs are independently run.
8. **Does the cable use the uploaded SWC geometry?** No. The bounded passive
   cable is a chain of equal compartments. SWC import is a morphology display.
9. **Does this run on a GPU?** The scientific jobs use the CPU. Renderer badge
   reports the browser renderer; GPU acceleration of the simulation is not
   claimed.
10. **Can it model a whole brain or clinical physiology?** No. The engine is
    resource-bounded and has not been clinically validated.

## Verification and rehearsal record

Last source baseline before this exhibition change: commit `458c99b` on branch
`codex/neurosim-research-readme`. The exhibition work is on branch
`exhibition-2026-10-28`. Latest observed upstream CPU and web CI workflows passed
at `69a258c` on 2026-10-27; that CI result does not validate this local change.

Local results on 2026-10-27: Python `pytest tests -q` passed **22 tests** with
one Starlette/httpx deprecation warning; `npm test` passed **6 tests**;
`npm run build` passed its production compilation and TypeScript checks;
`npm run test:e2e` passed **4/4** including the 512-neuron benchmark. The guided
browser test also passed on a separate clean run. One real seeded-network run
recorded 128 neurons, 1,276 saved edges and 1,284 spike events; the result is
stored by that test run rather than hardcoded in the UI. The latest benchmark
sampled the active renderer as WebGL2, with no usable WebGPU adapter. It measured
median 12.0 FPS at 2,048 edges and 2.1 FPS at all 20,786 edges; the environment
is headless and does not measure exhibition-hardware performance. The real
1366×768 screenshot is `docs/validation/exhibition-workspace.png`.

See `docs/validation/web-render-benchmark-redesign.json` and
`docs/WEB_VALIDATION_REPORT.md` for renderer context and raw samples.
Exhibition-device performance and WebGPU performance are unmeasured. No
speedup is claimed.

### Presenter dry run — manually tick only after rehearsal

- [ ] Start API and UI from a fresh login.
- [ ] Confirm health endpoint and renderer badge.
- [ ] Run HH; inspect voltage, raster, and configured pulse metadata.
- [ ] Run seeded network; verify topology, playback, and synchronized plots.
- [ ] Run the two-parameter comparison; confirm both jobs complete and overlay.
- [ ] Pause, scrub, resume, select a neuron, and export results.
- [ ] Refresh and reopen a completed run from history.
- [ ] Confirm 1366×768 layout and test a narrow viewport.
- [ ] Check the 2D fallback on a browser/device without usable WebGL2.
- [ ] Disconnect internet and verify the prepared machine still runs locally.
