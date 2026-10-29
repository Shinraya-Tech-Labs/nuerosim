# T014 — golden LIF trace fixture

## Purpose

Compare saved voltages from a single-neuron subthreshold LIF run against its closed-form RC membrane solution under constant current.

## Contract

- **Input:** JSON fixture with valid single-neuron LIF config, sample times in milliseconds, reference voltages in millivolts, positive tolerance in millivolts, and explicit units.
- **Output:** JSON pass/fail, sample count, maximum and per-sample absolute errors, and the actual experiment manifest.
- **Units:** time is ms; voltage and tolerance are mV.
- **Acceptance example:** for rest −65 mV, membrane time constant 20 ms, and 0.2 µA/cm² input over 20 ms, `V(t) = -65 + 4(1 - exp(-t/20))` at 5 ms intervals; require max error ≤1e−9 mV.
- **Errors:** reject invalid units/config/model, non-finite or mismatched reference arrays, unsorted or off-grid times, and nonpositive tolerance.
- **Scientific scope:** this closed-form comparison applies to the stated subthreshold LIF parameterization and constant-current interval only.
- **Exclusions:** it does not validate spike/reset dynamics, other parameterizations, population statistics, or biological adequacy of LIF.
