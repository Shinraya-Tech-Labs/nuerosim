# T018 validation evidence

## Euler refinement result

At code revision `7a80211`, a real HH constant-current run was compared with an independent DOP853 reference. Forward Euler at **0.005 ms** had maximum sampled voltage error **2.633780 mV**; at **0.0025 ms**, error was **1.320323 mV**. Halving the timestep reduced error by a factor of **1.994800**, for observed order **0.996244**, within the first-order acceptance range `[0.7, 1.3]`.

The focused test file passed (9 passed). Environment: Windows 11, Python 3.14.2, NumPy 2.4.2. Both reports include the actual `Experiment` manifests.

## Limits

This supports first-order convergence for one smooth constant-current HH trace. It does not establish stability/accuracy under other inputs, across discontinuities, or for other models.
