# T005 validation evidence

## Numeric check and environment

At code revision `6173085353f6ec361d5249e6358c5b46ae439014`, the file-based audit CLI read a deterministic result with 2 spikes, 1 neuron, and 1000 ms duration. It recomputed **2.0 Hz**, matching the independent calculation `2 / 1 / (1000 / 1000)`. The rate comparison uses `rel_tol=1e-12` and `abs_tol=1e-12` for floating-point rounding.

The manifest units matched the declarations in `docs/SCIENCE.md`: time ms, voltage mV, current density uA/cm², conductance density mS/cm², capacitance density uF/cm². The focused tests passed (5 passed), including a real result from `workbench.engine.simulate` and invalid-unit, zero-duration, out-of-range spike, and inconsistent-rate cases. Environment: Windows 11, Python 3.14.2.

## Limits

This verifies the declared unit labels and mean-rate arithmetic only. It is not dimensional analysis of every parameter, a check of model equations, or evidence of biological calibration.
