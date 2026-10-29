# T019 validation evidence

## RK4 refinement result

At code revision `a8fb0f7`, a real HH constant-current run was compared with the independent DOP853 reference. RK4 at **0.025 ms** had maximum sampled voltage error **0.006001657 mV**; at **0.0125 ms**, error was **0.000305376 mV**. Halving the timestep reduced error by a factor of **19.653366**, for observed order **4.296705**, within the declared `[3.5, 4.6]` range.

The combined RK4/Euler convergence tests passed (18 passed). Environment: Windows 11, Python 3.14.2, NumPy 2.4.2. Both timestep runs include actual Experiment manifests.

## Limits

This supports near-fourth-order convergence for one smooth constant-current HH trace. It does not establish order across spike events, discontinuities, other configurations, or biological validity.
