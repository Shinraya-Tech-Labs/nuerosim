# T028 — current balance conservation diagnostic

## Purpose

Check the passive cable solver's equal-and-opposite axial currents and compare their net current with zero.

## Contract

- **Input:** finite compartment voltages, nonnegative axial coupling, and explicit units.
- **Equation:** edge flow is `axial*(V[i+1]-V[i])`; each edge contributes opposite signs to its two adjacent compartments.
- **Units:** voltage mV; axial coupling mS/cm²; current density µA/cm².
- **Output:** per-compartment axial current vector, net current, and maximum absolute net-balance residual.
- **Acceptance example:** voltages [−65,−55,−75] mV and axial=0.1 mS/cm² produce currents [1,−3,2] µA/cm² and net 0.
- **Errors:** reject non-finite/non-vector voltage, fewer than two compartments, negative coupling, and unsupported units.
- **Exclusions:** checks the discrete axial term only; it does not claim conservation of membrane charge in the presence of leak, input, or integration error.
