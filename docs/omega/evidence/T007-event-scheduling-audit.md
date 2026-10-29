# T007 validation evidence

## Numeric cross-check and environment

At code revision `6b8f4f359659646464b5a2da8ec203ce8886338d`, a real two-neuron LIF run requested a **2.01 ms** delay at **0.025 ms** timestep. The shared engine rule produced **81 steps**, **2.025 ms** effective delay, and **0.015 ms** rounding. The audit matched the saved result. The source neuron produced 3 spikes in the 25 ms run.

The focused audit tests passed (5 passed); the existing event integration tests also passed (2 passed). Environment: Windows 11, Python 3.14.2. The boundary test covers one minimum grid-aligned timestep with zero rounding.

## Limits

The audit checks delay arithmetic and the test checks one arrival path. It does not validate every queued event, synaptic weight, receptor effect, or biological interpretation.
