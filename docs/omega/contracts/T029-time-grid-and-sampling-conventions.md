# T029 — time grid and sampling conventions

Audit production time endpoints, recording stride, and final-sample inclusion.

- Input: validated experiment with duration, dt, and record_every in ms/steps.
- Output: expected and actual recording indices/times, max time-grid error, final-time inclusion.
- Example: duration=1 ms, dt=.025 ms, record_every=4 gives samples 0,.1,…,1 ms (41 integration steps; final endpoint included).
- Reject duration/dt not integral, invalid stride or unsupported units through Experiment validation.
- Scope: verifies sampled time conventions; no claim about integration accuracy between samples.
