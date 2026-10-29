# T013 validation evidence

## Trace comparison

At code revision `457cb35`, the fixture audit ran the actual CPU float64 HH engine for a single neuron, 20 ms duration, 0.025 ms timestep, and constant 10 µA/cm² current. At saved times 0, 5, 10, 15, and 20 ms, the largest absolute voltage difference from the independent DOP853 reference was **0.000005606 mV**, within the fixture tolerance of **0.02 mV**. The run recorded 2 spikes and returned config/engine provenance hashes in its manifest.

The focused test file passed (8 passed), including invalid units, unequal arrays, unsorted/off-grid times, nonpositive tolerance, and a deliberately perturbed reference that correctly fails the tolerance check. Environment: Windows 11, Python 3.14.2, NumPy 2.4.2.

## Limits

Only five voltage samples for one current-clamp configuration are checked. This does not establish full-trace bounds or validate other HH parameters, solvers, or biological models.
