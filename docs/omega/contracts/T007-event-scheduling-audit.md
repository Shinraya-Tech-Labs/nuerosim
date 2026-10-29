# T007 — Event scheduling audit

## Purpose

Check that a saved workbench result's effective synaptic delay matches the engine's timestep rounding rule.

## Contract

- **Input:** a result containing `manifest.config.delay` and `dt` (ms), plus `effective_delay_ms` (ms).
- **Output:** deterministic JSON with pass status, requested delay, timestep, integer delay steps, computed effective delay, and rounding remainder. Derived millisecond values are rounded to 12 decimal places for display.
- **Units:** requested/effective delay and timestep are milliseconds; delay steps are integer timesteps.
- **Rule:** `delay_steps = max(1, ceil(delay_ms / dt_ms - 1e-10))`; effective delay is `delay_steps * dt_ms`. Require the saved result's effective delay to match within `rel_tol=1e-12`, `abs_tol=1e-12`.
- **Ordering context:** the engine applies queued arrivals at step start and enqueues a fired neuron's outgoing events for its recorded spike time plus effective delay. The audit verifies the reported delay arithmetic, not a trace of every event.
- **Acceptance example:** delay 1.01 ms with dt 0.025 ms gives 41 steps and 1.025 ms effective delay.
- **Errors:** reject missing/non-finite/non-positive timing values or an inconsistent saved effective delay.
- **Exclusions:** this does not audit event weights, connectivity, every queue entry, receptor kinetics, or biological validity. It does not prove that a downstream synaptic response has the correct sign or magnitude.
