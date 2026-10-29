# T021 validation evidence

## Removable singularity results

At code revision `24835ba`, the audit evaluated all six HH rates at voltages immediately around and exactly at −40 and −55 mV. It measured `alpha_m(-40 mV) = 1 ms⁻¹` and `alpha_n(-55 mV) = 0.1 ms⁻¹`. At ±1e−6 mV around the respective points, maximum deviations from the limits were **5.0e−8 ms⁻¹** and **5.0e−9 ms⁻¹**, both within the **1e−7 ms⁻¹** continuity tolerance. All reported rates were finite and nonnegative.

The focused audit tests passed (9 passed), and the pre-existing real HH rest/rate-limit test also passed. Environment: Windows 11, Python 3.14.2, NumPy 2.4.2.

## Limits

This validates numerical handling of the classic rate equations near two singular voltages. It does not establish measured channel kinetics or temperature scaling.
