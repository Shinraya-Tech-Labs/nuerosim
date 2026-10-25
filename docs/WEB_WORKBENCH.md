# Web neuroscience workspace

The Next.js application in `web/` consumes the supported CPU API. The original
FastAPI workbench remains available at port 8000. No simulation equations were
replaced for this visualization upgrade.

## Local development

Install Python as documented in the root README, then start `neurosim serve`.
In another terminal, using Node 22 and npm:

```sh
cd web
npm ci
npm run dev
```

Open http://127.0.0.1:3000. Windows PowerShell can use `npm.cmd` if its execution
policy prevents running `npm.ps1`. Select a completed experiment or expand
**New simulation**, edit the validated JSON and run a CPU simulation.
Jobs are persisted and polled every 1.5 seconds; cancel and reproduce use the
existing backend. The URL identifies the experiment for reload and sharing
within the same local installation. Playback restarts at zero on reload.

`NEUROSIM_API_URL` defaults to `http://127.0.0.1:8000`. Set it **before building**
if changing the backend; Next rewrites are embedded during build. It is a
server-side deployment setting, never a user-controlled URL. Production local
use: `npm run build` then `npm start`. Both servers bind localhost by default.
This remains a single-user application without authentication; remote hosting
needs a separately reviewed authenticated reverse proxy.

## Data contract and interpretation

- `/experiments/{id}/topology?offset=0&limit=4096` returns all node metadata and
  a page of saved edges. Edge IDs are their persisted array indices. Uniform
  weights come from the saved manifest and delay from the actual effective
  integration delay. Cable edges represent undirected adjacent compartments,
  not chemical synapses. Units: mS/cm² and ms.
- `/experiments/{id}/activity?offset=0&limit=20000` returns sorted recorded
  threshold crossings, ordered by time then neuron ID; no regenerated events.
- `/experiments/{id}/voltage?neuron=0&offset=0&limit=5000` returns saved times
  and mV samples for one neuron or cable compartment.
- Each page includes `next_offset`, or null when complete. Negative offsets
  and excessive page sizes fail validation. Incomplete jobs have no result.
- Paging bounds HTTP responses. Storage still decompresses the full bounded
  result blob on every request; this is not an out-of-core data service.

Network layouts are deterministic display coordinates, not anatomy. Excitatory
edges are orange; inhibitory edges cyan; axial links gray. Lines do not depict
axons, lengths, conduction velocity or measured propagation. Select a neuron
with the mouse or dropdown, orbit with drag, zoom with scroll and pan with
right drag. Filters and budgets operate on the saved edges in stable order.
The default edge budget is 2,048; increase it to inspect all saved edges. When
over budget, evenly spaced eligible edges are selected deterministically;
no synthetic edges are added. The rendered/total counts expose omissions.

The renderer selector reports the initialized backend. Auto mode requests a
WebGPU adapter and uses Three.js `WebGPURenderer` when available; otherwise it
uses direct WebGL2. WebGL2 can also be selected explicitly. If WebGL2 cannot
initialize, the application switches to batched 2D SVG. The connection-density
selector and adaptive-density toggle limit display work; adaptive mode lowers
the visible edge budget when measured FPS is below 24. This changes only the
rendered subset, never the saved topology or simulation data.

Playback advances a shared simulation-time cursor at the chosen ms/second.
White nodes indicate recorded spikes in the inclusive trailing 1 ms display
window. This persistence is only a display effect. The raster, voltage and
rate cursors share the same time. Population rate uses all loaded events,
50 equal-width bins, normalized by neuron count and bin duration in seconds.
The last bin includes an event exactly at simulation end. Short bins may give
large rates and must not be interpreted as sustained single-neuron firing.

Limits: 512 network nodes, 32,768 saved edges, 200,000 loaded spike events.
Exceeding the playback event budget gives an explicit error; export remains
available. Raster draws the first 20,000 sorted events and labels the count.
Voltage display uses a stride to limit points to approximately 4,000; peaks
between displayed samples can be missed. ZIP contains the complete saved data.
Comparison overlays the same numeric neuron ID from another experiment; this
does not assert equivalent models, parameters, or biological correspondence.

SWC import validates one rooted acyclic tree, finite coordinates and positive
radii, at most 500 KB / 5,000 points. Its geometry uses SWC coordinates (assumed
µm); marker size is for display and the inspector reports exact radius. No
voltage is assigned to uploaded SWC: the engine has no SWC-to-compartment map.
Imported morphology is a session-local view, not a saved electrical model.

## Testing and measurement

```sh
python -m pytest tests -q
cd web
npm ci
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

E2E starts isolated local servers on 8011/3011 using
`neurosim-data/web-e2e-redesign.db`, executes real simulations, then checks topology,
playback/reload, plotting and SWC import. Default Python is the root `.venv`;
override `NEUROSIM_TEST_PYTHON` for another installed interpreter. Test database
is separate from user experiments; repeated runs accumulate test jobs subject
to the 500-job store bound.

The renderer benchmark uses a real seeded 512-node experiment with 20,786 saved
edges, and records 2,048-edge, full-topology and adaptive cases for auto and
explicit WebGL2 modes. It records the actual renderer, browser version, FPS,
p95 frame interval, draw calls and exposed JS heap. Heap is not total process or
GPU memory. Headless software-rendering results do not establish consumer GPU
performance. See `validation/web-render-benchmark-redesign.json` for samples.

Docker packaging is provided as an optional Compose profile:
`docker compose --profile web up --build`. Its local runtime gate remains blocked
until the Docker daemon is available; it is not a validated deployment claim.

## Release limitations

This is an unreleased local application. CUDA/MPI validation, Docker runtime
validation and broad device/browser coverage are not implied by frontend tests.
The repository license is still unresolved; dependency license metadata and
packaged license files are inventoried separately. A successful build or
benchmark does not satisfy the remaining release gates.
