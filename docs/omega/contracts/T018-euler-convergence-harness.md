# T018 — Euler convergence harness

## Purpose

Measure fixed-step forward Euler convergence for a classic HH constant-current trace against an independent adaptive DOP853 reference.

## Contract

- **Input:** duration in ms, two decreasing Euler timesteps in ms, and constant current in µA/cm². Timesteps must satisfy the configured HH Euler bound (`dt <= 0.005 ms`) and exactly divide the duration.
- **Output:** JSON containing each timestep, maximum absolute sampled voltage error in mV, coarse/fine error ratio, observed order `log2(ratio)`, and pass/fail.
- **Units:** time/dt in ms, voltage and error in mV, order is dimensionless.
- **Reference:** classic four-state HH equations at standard initial gating values, integrated by DOP853 (`rtol=1e-11`, `atol=1e-12`) under constant input.
- **Acceptance example:** forward Euler is first order; halving dt should reduce global maximum voltage error by approximately 2, with observed order in `[0.7, 1.3]`.
- **Errors:** reject unsupported timesteps, duration grids, current values, or a reference error that does not decrease under refinement.
- **Exclusions:** this does not establish Euler stability/accuracy outside this trajectory, across discontinuous protocols, or biological validity.
