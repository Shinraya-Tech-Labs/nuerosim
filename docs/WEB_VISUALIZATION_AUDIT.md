# Web visualization audit — 2026-10-20

The existing supported workbench is a single HTML page served by FastAPI. It
renders SVG plots and an adjacency scatterplot, not a 3D scene. The existing
CPU engine, SQLite job lifecycle, original UI and export routes will remain.

Saved results contain `edges: [source, target, inhibitory][]`, `spikes: number[][]`
(ms by neuron), `t: number[]` (recorded ms), and `voltage: number[][]` (mV by
neuron/compartment). Connectivity is actually sampled during simulation and
persisted. Weight is uniform and comes from the saved manifest; effective delay
is stored in results. There are no measured 3D positions, synaptic geometries,
per-edge currents or recorded propagation trajectories. Layout coordinates must
be labeled illustrative. Spike flashes may use recorded times only.

The cable model stores compartment voltage but has no SWC ID mapping. Uploaded
SWC therefore must not receive voltage colors from unrelated network results.
The SWC route already validates parent links, cycles and finite coordinates.

Result retrieval decompresses one JSON blob. The added topology, activity and
voltage routes provide bounded response pages without changing the stored
scientific schema. Server decompression remains a limitation; these are not
streaming storage. Existing polling reflects real execution; WebSockets were
unnecessary.

## Renderer architecture and current validation

The dashboard is a local Next.js workbench with a large 3D viewport, collapsible
experiment rail, contextual neuron inspector, recorded-time transport, and a
scrollable analysis dock. The mobile rail starts collapsed below 900 px. Controls
operate on saved experiments and recorded backend outputs; screenshot evidence
is in `validation/web-3d-redesign.png`, `validation/web-mobile-redesign.png`,
`validation/web-fallback-redesign.png`, and the 512-neuron network captures.

Renderer selection checks `navigator.gpu` and requests an adapter when
available. It uses Three.js `WebGPURenderer` only when an adapter is available,
labels the initialized backend, and uses direct WebGL2 otherwise. WebGL2 can
also be selected explicitly. If WebGL2 creation fails, the error boundary
switches to the batched SVG 2D view. Headless Chromium in this run did not expose
a WebGPU adapter, so WebGPU rendering was **not validated**; auto mode used
direct WebGL2. The runtime test verifies the active label and fallback behavior.

Node markers are instanced, and eligible persisted edges are batched in a
line-segment geometry with a configurable display budget. Three layouts are
deterministic display arrangements only. Recorded spikes drive playback, not
random visual events. Uploaded SWC files receive no voltage coloring because
their points are not mapped to simulated compartments.

## Implementation gates

1. **Complete:** add topology pages and verify each edge against persisted
   results. The React Three Fiber view uses deterministic display layouts,
   instanced nodes and batched lines.
2. **Complete:** add timestamp playback, selected-neuron traces, synchronized
   raster and voltage cursors; test scrub and experiment reload.
3. **Complete:** add rooted SWC morphology viewing, metadata, budgets and 2D
   fallback; uploaded morphology carries no unrelated voltage.
4. **Complete for local validation:** Python, frontend build/unit tests, and
   real-server Chromium flows pass. Current 512-node measurements are in
   `validation/web-render-benchmark-redesign.json`. Headless software rendering
   is slow at full topology; consumer-GPU performance and WebGPU remain
   unverified. Docker and remote CI are not locally verified. No release or
   push; project licensing remains unresolved.

Rendering follows R3F's documented instancing/batching guidance:
https://r3f.docs.pmnd.rs/advanced/scaling-performance
Next.js rewrites proxy same-origin `/api` to local FastAPI:
https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites

See [`WEB_VALIDATION_REPORT.md`](WEB_VALIDATION_REPORT.md) for measured results
and remaining blockers. Renderer integration follows the official
[Three.js WebGPURenderer](https://threejs.org/docs/pages/WebGPURenderer.html)
and [React Three Fiber Canvas](https://r3f.docs.pmnd.rs/api/canvas)
documentation.
