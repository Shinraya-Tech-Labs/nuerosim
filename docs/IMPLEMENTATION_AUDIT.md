# Implementation audit

Audited 2026-10-19, Windows, Python 3.14.2. Starting commit:
`4616fa7d48234bcc13372ec796498339337a23a2`. The local origin is
`sreerevanth/nuerosim`, whereas the requested repository is
`Shinraya-Tech-Labs/nuerosim`. Work applies to this supplied checkout; no remote
was changed and nothing was published.

## Baseline evidence

`python -m pytest -q`: zero tests collected, two import errors (`neurosim`).
With `PYTHONPATH=python`, collection still fails on
`neurosim.reconstruction.ingestion`, which actually lives in `python/pipeline`.
Raw follow-up outputs are retained in `docs/validation/`.

The isolated original unit file ran with `PYTHONPATH=python`: **29 passed,
9 failed, 90 warnings in 29.62 s**. The full original suite never completed
collection. These are baseline results, not the status of the new workbench.

## Findings and priority

|Priority|Evidence|Remediation|
|---|---|---|
|P0|pyproject uses nonexistent `setuptools.backends.legacy:build`; mandatory NEURON/MPI/VTK dependencies; testpaths points to absent tests directory|Use setuptools.build_meta and CPU dependencies; test installed wheel|
|P0|engine.rk4_step reads axial current from original state at all stages, never advances synapses/time/spike detection|Provide tested CPU solver with explicit state and event ordering; preserve legacy code pending repair|
|P0|neuron._axial_currents multiplies mV/ohm by 1e-3 instead of 1e3 for microamps|Do not use legacy cable results as evidence; add conservative passive cable reference|
|P0|RecordingBuffer._last_rec is shared by all neurons, skipping every neuron after first; time labels precede integrated state; final values NaN|Record initial and end-of-step states consistently for every neuron|
|P0|37 C Q10 speeds HH gates ~29-fold; explicit dt .025 and high AIS conductance unstable; tests inject 5 microamps into a tiny soma|Bound model parameters/timestep and validate classic HH at 6.3 C; distinguish current density from total current|
|P0|API stores jobs only in dictionaries; missing reconstruction import; neuron_ids ignored; synchronous CPU work inside async runner; no cancel/retry/persistence|Replace public execution path with validated manifests, SQLite jobs and actual background worker|
|P0|pickle.load on checkpoint path; Celery SLURM script interpolates unvalidated config; GPU task executes CPU engine then labels result cuda|Keep unsupported paths out of application; do not accept pickle uploads; reject unavailable backends|
|P1|Synapse normalization wrong, unstable Euler decay, weight multiplied twice by pipeline/event path|Use exact exponential conductance decay and one event weight application|
|P1|Diffusion guard alpha<=.5 is incorrect for 2-D five-point stencil; np.roll is periodic despite zero-flux comment; clipping hides loss|Correct stencil boundary and positivity condition, add mass tests|
|P1|SWC reader silently skips malformed rows; split compartments attach as siblings; missing/cyclic parents unvalidated|Strict bounded SWC parser for viewing; do not claim SWC electrophysiology reconstruction validated|
|P1|CMake references absent cpp/, cmake/, tests/cpp; CUDA language enabled even with ENABLE_CUDA=OFF|Archive unsupported build recipe; CPU Python package independent|
|P1|All Docker recipes copy nonexistent services/configs/scripts or cpp; Compose references nonexistent docker/ directory and viz image|Single CPU service with persistent volume and non-root user|
|P1|neurosim-ci.yml is at root (not an Actions workflow); references absent tests/scripts; auto-publishes images; security scan nonblocking|Supported CPU CI in .github/workflows; no publishing|
|P1|README advertises molecular accuracy, production HPC, brain atlas, NeuroML/NWB and directories absent from checkout; LICENSE absent|Replace with measured capabilities and explicit limitations; clarify licensing before release|
|P2|distributed.py consumes spike history, wrong incoming lookup and placeholder weight*spike_time; nonblocking communication lacks reliable receive completion|MPI blocked pending real runtime and serial equivalence tests|
|P2|hh_cuda.cu is standalone, float32 gate clipping, no tested binding; no nvcc/nvidia-smi found|CUDA validation blocked, no speedup claim|
|P2|optimization.py claims GPFA/VAE but dispatches PCA/ICA/UMAP; CLI imports nonexistent ml module; silent fallbacks change algorithms|Preserve research code; exclude unvalidated optimization from supported commands|
|P2|dashboard loads HDF5 only; statistics use a time window without filtering spikes; standalone launcher duplicates science and installs dependencies at runtime|Workbench must use same backend and manifests as CLI|
|P2|tracked __pycache__, empty 3.8 and pytest artifacts|Remove generated artifacts and ignore future caches|

## Inspected scope

All tracked source areas: models (channels, neuron, plasticity), simulation
(engine, distributed, optimization), analysis, reconstruction/ingestion,
API/Celery, visualization, CLI and standalone launcher. Reviewed the two original
test files, pyproject, CMake, three Dockerfiles, Compose, Kubernetes manifest,
root CI YAML, experiment YAML, README and technical documentation. Existing
channel equations, analysis utilities, reconstruction and experimental models
are retained. Empty package initializers do not repair misplaced modules.

## Incremental gates

1. Audit and CPU packaging: installation, import and baseline evidence.
2. Scientific baseline: HH reference/convergence, LIF analytic solution,
   AdEx subthreshold/adaptation, reproducibility, synapse sign/delay,
   passive cable conservation, strict input/resource bounds.
3. Persistent experiments: real execution, cancellation, retry lineage,
   failure/restart recovery, immutable manifests, export and API integration.
4. Workbench: configuration, polling, plots, history/comparison, SWC display,
   export; verify browser interactions against real results.
5. Release: clean wheel install, supported test suite, dependency/security scan,
   measured CPU benchmark, Docker smoke and CI across supported systems.
   No versioned release until gates pass. Legacy scientific failures remain
   visible and are not evidence that the replacement path is validated.

## Implemented remediation

The supported `neurosim.workbench` path now has CPU packaging, strict manifests,
four bounded models, deterministic synaptic networks, numerical references,
SQLite execution/history/recovery/cancellation/retry, JSON/CSV ZIP exports,
same-origin workbench and SWC viewing. Original source is preserved. The legacy
axial conversion and diffusion stencil/positivity/boundary defects have targeted
repairs and regression tests; this does not validate the rest of the legacy engine.
Old build/deployment recipes were moved to `docs/legacy`, tracked caches removed,
and actual CPU CI added without release/publish actions. The public legacy API
and CLI entry paths now forward to the supported workbench.

See `VALIDATION.md` for measured gates and remaining blockers. No CUDA/MPI test,
Docker runtime test or remote CI run is represented as passing.
