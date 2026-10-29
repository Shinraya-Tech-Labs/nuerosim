# T019 — RK4 convergence harness

## Purpose

Measure fixed-step RK4 convergence for a classic HH constant-current trace against an independent adaptive DOP853 reference.

## Contract

- **Input:** duration in ms, two decreasing RK4 timesteps in ms, and constant current in µA/cm². Each timestep must divide the duration exactly and obey the supported maximum 0.025 ms.
- **Output:** JSON containing each timestep, maximum absolute sampled voltage error in mV, coarse/fine error ratio, observed order `log2(ratio)`, and pass/fail.
- **Units:** time/dt in ms, voltage/error in mV, order is dimensionless.
- **Reference:** classic four-state HH equations at standard initial gating values, integrated by DOP853 (`rtol=1e-11`, `atol=1e-12`) under constant input.
- **Acceptance example:** RK4 is fourth order on a smooth trace; halving dt should reduce global maximum voltage error by roughly 16, with observed order in `[3.5, 4.6]`.
- **Errors:** reject unsupported timesteps, duration grids, current values, or a reference error that does not decrease under refinement.
- **Exclusions:** this does not establish RK4 order across spike events/discontinuities, stability outside the tested configuration, or biological validity.
