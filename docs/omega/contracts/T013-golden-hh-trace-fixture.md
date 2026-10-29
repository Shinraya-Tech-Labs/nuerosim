# T013 — golden HH trace fixture

## Purpose

Compare selected Hodgkin–Huxley voltage samples against an independently integrated adaptive DOP853 reference for a fixed constant-current experiment.

## Contract

- **Input:** JSON fixture with a valid HH `Experiment` configuration, strictly increasing sample times in milliseconds, reference voltages in millivolts, and an absolute tolerance in millivolts.
- **Output:** JSON with pass/fail, sample count, maximum absolute voltage error (mV), per-sample errors, and reference label.
- **Units:** time is ms; voltage/error/tolerance are mV.
- **Acceptance example:** the 20 ms, 0.025 ms fixed-step HH profile sampled every 5 ms agrees with the DOP853 reference within 0.02 mV.
- **Errors:** reject missing fields, invalid/non-HH configs, mismatched/unsorted sample arrays, nonfinite values, nonpositive tolerance, or sample times absent from the saved trace.
- **Scientific scope:** the reference uses the classic four-state HH equations, standard initial gating values, constant 10 µA/cm² current, and DOP853 with `rtol=1e-11`, `atol=1e-12`.
- **Exclusions:** sparse agreement does not establish all-time error bounds, parameter inference, biological validity of the classic model, or correctness under other solvers/configurations.
