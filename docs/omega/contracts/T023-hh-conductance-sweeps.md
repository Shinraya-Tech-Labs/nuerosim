# T023 — HH conductance sweeps

## Purpose

Run a deterministic sweep of maximal sodium conductance (`g_na`) through the production Hodgkin–Huxley workbench engine, holding every other experiment setting fixed.

## Contract

- **Input:** one validated HH `Experiment` configuration and a strictly increasing list of 2–12 `g_na` values.
- **Units:** `g_na` in mS/cm²; time ms; voltage mV; input current density µA/cm²; spike times ms.
- **Output:** per conductance, production simulator manifest, spike times/count, final voltage, and shared sweep parameters.
- **Acceptance example:** default 50 ms, 0.025 ms RK4 run with a 10 µA/cm² pulse from 10–40 ms and `g_na` values 60, 120, 180 mS/cm² produces respectively 1, 2, 3 spikes.
- **Errors:** reject non-HH configurations, invalid experiment manifests, unsorted/duplicate/out-of-range conductances, invalid units, and sweeps outside the 2–12 point resource bound.
- **Exclusions:** this is a deterministic parameter-sensitivity experiment, not a fit to biological recordings, a universal monotonicity claim, or evidence of physiological validity.
