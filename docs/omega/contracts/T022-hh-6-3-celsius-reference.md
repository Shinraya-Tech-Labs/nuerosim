# T022 — HH 6.3°C reference

## Purpose

Audit the classic Hodgkin–Huxley rate values and steady-state gates at −65 mV under the model's fixed 6.3°C parameterization.

## Contract

- **Input:** reference temperature (must be 6.3°C), membrane voltage in mV, positive numerical tolerance, and explicit units.
- **Output:** six alpha/beta rates in ms⁻¹, three steady-state gate values, production initial-state gate values, maximum absolute gate discrepancy, and pass/fail.
- **Units:** voltage mV, temperature °C, rate ms⁻¹; gates are dimensionless probabilities in [0,1].
- **Acceptance example:** at −65 mV, steady gates are `m∞≈0.052932485257`, `h∞≈0.596120753508`, `n∞≈0.317676914061`; production initialization agrees within `1e-12`.
- **Errors:** reject temperatures other than 6.3°C (no temperature scaling is implemented), unsupported units, nonfinite voltages, and nonpositive tolerance.
- **Reference:** alpha/beta expressions in the classic 1952 HH formulation with the project’s canonical conductance/reversal constants.
- **Exclusions:** this is a code-level reference check, not a comparison to biological recordings, temperature adaptation, or model validation.
