# T005 — Scientific units audit

## Purpose

Check the workbench's declared manifest units and the dimensional arithmetic used for mean firing rate in a saved simulation result. This is a narrow consistency audit, not a general unit system.

## Contract

- **Input:** a result mapping with `manifest.units`, `manifest.config.duration` (ms), `manifest.config.n` (neurons), `spikes` (per-neuron spike times in ms), and `mean_rate_hz` (Hz).
- **Output:** deterministic JSON with pass status, the checked unit declarations, and the recomputed mean rate in Hz.
- **Units checked:** time `ms`, voltage `mV`, current density `uA/cm^2`, conductance density `mS/cm^2`, capacitance density `uF/cm^2`; spike times and duration are milliseconds; mean rate is spikes per neuron per second.
- **Arithmetic:** `mean_rate_hz = total_spikes / n / (duration_ms / 1000)`. Require positive duration, positive neuron count, one spike train per neuron, finite spike times within `[0, duration_ms]`, and agreement with the stored rate at `rel_tol=1e-12`, `abs_tol=1e-12` to allow double-precision rounding only.
- **Acceptance example:** two spikes, one neuron, and 1000 ms duration recompute to 2 Hz.
- **Errors:** reject missing or mismatched unit declarations, malformed result shape, non-finite/out-of-range spike times, invalid duration/count, or inconsistent stored rate; never relabel or silently convert result data.
- **Exclusions:** this audit does not validate model equations, parameter units beyond the manifest's declared categories, biological calibration, or whether a simulation is scientifically appropriate. It does not claim full dimensional analysis.
