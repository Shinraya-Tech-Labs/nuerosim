# Web visualization validation report — 2026-10-27

The visualization redesign leaves the CPU simulation equations unchanged. The
Python source suite passed **22 tests** with `PYTHONPATH=python`; this setting
ensures pytest imports the repository source instead of a stale installed copy.
Coverage includes persisted topology, edge signs/weights/delays, spike ordering,
voltage page concatenation, passive cable adjacency, request limits and
repeatable exports. One Starlette/httpx deprecation warning remains.

Frontend validation includes a strict TypeScript production build, six Vitest
projection tests and four Playwright end-to-end cases. The browser tests run
real CPU experiments through isolated API and Next.js servers. They check saved
topology, recorded spikes and voltage, synchronized playback, reload,
comparison/export, renderer selection and fallback, SWC handling and mobile
layout. The added exhibition case executes HH, seeded LIF network and paired
LIF runs, checks current metadata and recorded events, verifies the trace
overlay, and captures a 1366×768 presentation view. The benchmark case has 512
neurons and 20,786 persisted edges. Results and screenshots are stored in
`docs/validation/`.

The current renderer benchmark is a headless Chromium run at 1440×1000. This
environment has no usable WebGPU adapter and uses software WebGL; the active
backend was **WebGL2**. Three samples were collected per fixed renderer/budget
configuration. The adaptive case was sampled after lowering the displayed edge
count in response to low frame rate.

| Requested mode            | Visible edges | Median measured FPS | Frame interval p95 (observed) | Draw calls | JS heap |
| ------------------------- | ------------: | ------------------: | ----------------------------: | ---------: | ------: |
| Auto (WebGPU unavailable) |         2,048 |                12.3 |                  83.0–319.5 ms |          2 |  38 MiB |
| Auto (WebGPU unavailable) |        20,786 |                 2.0 |                440.9–587.4 ms |          2 |  38 MiB |
| WebGL2                    |         2,048 |                12.0 |                188.4–201.7 ms |          2 |  38 MiB |
| WebGL2                    |        20,786 |                 2.1 |                501.8–596.6 ms |          2 |  38 MiB |
| WebGL2 adaptive           |         7,680 |    2.5 (one sample) |                      442.7 ms |          2 |  38 MiB |

These measurements do **not** meet the smooth-interaction target for 512 neurons
in this headless software-rendering environment. Adaptive density reduces the
visible lines but did not reach 24 FPS in the observed sample. The two display
budgets, 2,048 and full topology, therefore expose a real clarity/performance
trade-off. The benchmark records Chromium's exposed JavaScript heap estimate,
not total process or GPU memory. It does not measure the host's integrated GPU
or establish performance on consumer hardware.

WebGPU selection is implemented behind `navigator.gpu` and adapter detection;
there is no WebGPU validation result because this browser supplied no usable
adapter. Explicit WebGL2 and the 2D fallback were exercised in browser tests.
No physical GPU comparison, GPU-memory measurement, or WebGPU speedup is claimed.
The screenshot captures and raw benchmark are [in the validation directory](validation/),
including the [1366×768 guided workspace](validation/exhibition-workspace.png).

Npm's audit found no known vulnerabilities in 201 locked dependency entries.
Python dependency consistency passed and pip-audit found no known issue in the
installed dependencies; it cannot audit the local `neurosim` package because it
is not published on PyPI. License metadata was checked for the locked frontend
dependencies, but the repository itself has no project license, so distribution
approval remains unresolved. Docker was not built or run locally because the
Docker daemon was unavailable. CI has not run remotely. This validation run did
not create a release or deployment; the version remains development-only.
