# T020 — adaptive reference comparisons

## Purpose

Quantify both adaptive-reference tolerance sensitivity and production RK4 error for one fixed HH constant-current experiment.

## Contract

- **Input:** duration (ms), constant current (µA/cm²), fixed-step RK4 dt (ms), saved-sample stride, two ordered DOP853 tolerance pairs, and explicit units.
- **Output:** JSON with maximum DOP853-to-DOP853 voltage difference (mV), maximum RK4-to-tight-DOP853 error (mV), configured tolerance pairs, experiment manifest, and pass/fail.
- **Units:** time/dt in ms; voltage and absolute error in mV; rtol/atol are dimensionless/scaled absolute voltage tolerance.
- **Reference:** classic HH equations with standard initial gating values; each adaptive solve uses dense output at the exact production trace timestamps.
- **Acceptance example:** for the default 20 ms, 10 µA/cm² HH case, loose-vs-tight DOP853 discrepancy is ≤0.001 mV and RK4 error is ≤0.02 mV.
- **Errors:** reject invalid units, nonpositive or unordered solver tolerances, unsupported config, or failed adaptive integration.
- **Exclusions:** one trajectory and tolerance pair do not establish adaptive solver behavior for all models, discontinuities, parameter sets, or biological validity.
