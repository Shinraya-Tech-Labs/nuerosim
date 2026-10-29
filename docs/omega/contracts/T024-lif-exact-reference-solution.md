# T024 — LIF exact reference solution

## Purpose

Compare the production LIF integrator with the closed-form solution of its constant-current, piecewise-constant pulse equation.

## Contract

- **Input:** one validated single-neuron LIF `Experiment`, explicit units, and a positive voltage tolerance.
- **Equation:** `dV/dt = (rest - V)/tau_m + I/cm`; current is constant between pulse boundaries and additive across overlapping pulses.
- **Units:** time ms, voltage mV, current density µA/cm², capacitance density µF/cm².
- **Output:** production and exact voltage at each production recording time, maximum absolute error, pass/fail, and the production result manifest.
- **Acceptance example:** `V(0)=-65 mV`, `tau_m=20 ms`, `rest=-65 mV`, `cm=1`, pulse 0.5 µA/cm² on [5,15) ms, gives `V(15)=-61.06530659712634 mV` and `V(20)=-61.9356576966961 mV`.
- **Errors:** reject non-LIF, multi-neuron or synaptic experiments, unsupported units, invalid tolerance, and inputs whose exact trajectory reaches threshold (reset is outside the closed-form scope).
- **Exclusions:** numerical reference for the implemented subthreshold equation only; not a claim about biological fidelity or spike-time accuracy.
