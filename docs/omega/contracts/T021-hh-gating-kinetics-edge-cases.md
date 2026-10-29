# T021 — HH gating kinetics edge cases

## Purpose

Audit the classic HH alpha/beta rate functions around their removable singularities and confirm finite, nonnegative rates in declared millivolt inputs.

## Contract

- **Input:** non-empty array of finite membrane voltages in mV.
- **Output:** per-voltage `alpha_m`, `beta_m`, `alpha_h`, `beta_h`, `alpha_n`, `beta_n` values in ms⁻¹; report checks finite/nonnegative rates and removable-singularity limits.
- **Acceptance examples:** `alpha_m(-40 mV)=1 ms⁻¹` and `alpha_n(-55 mV)=0.1 ms⁻¹`; adjacent voltages near those points remain continuous within fixture tolerance.
- **Units:** voltage mV; kinetic rates ms⁻¹.
- **Errors:** reject empty, non-numeric, boolean, or nonfinite voltage inputs and any nonfinite/negative resulting rate.
- **Exclusions:** this verifies arithmetic limits for the classic 6.3°C HH equations only; it does not validate channel kinetics experimentally, temperature scaling, or model suitability.
