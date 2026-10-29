# T015 validation evidence

## Day 01 baseline gate

At tested code revision `91231ea64f4cb4455cb7ee808f1f05b1e785fdd6` on Windows 11 / Python 3.14.2, all four required local checks passed:

- Python suite: 107 passed in 21.91 s.
- Web unit suite: 6 passed.
- Next.js production build and TypeScript: passed.
- Playwright E2E: 6 passed in 1.4 min, including the 512-neuron renderer benchmark and the new renderer fallback audit.

The signoff command reported `baseline_gate_passed: true` with 4/4 local checks passed. The E2E run regenerated nine tracked validation artifacts; those files were restored. After publication, both GitHub Actions workflows passed on checkpoint `1c9e3ca827519366181afd1f54839818bb5660b8` (CPU run `40925897619`, web run `40925897526`). The signoff record now lists two accepted risks: physical WebGPU and Docker runtime remain unverified.

## Scientific reference fixtures

- HH against independent DOP853: five samples, maximum error `5.6051e-6 mV` against `0.02 mV` tolerance; 2 spikes.
- Subthreshold LIF against its closed-form RC solution: five samples, maximum error `2.13e-14 mV` against `1e-9 mV` tolerance; 0 spikes.
- CPU HH benchmark: two runs at `0.821412 s` and `0.738805 s`, with identical saved voltage, spikes, and connectivity.

## Accepted residual risks

Physical WebGPU behavior/performance, hosted GitHub Actions results, and Docker runtime were not established by the local Day 01 gate. Details and supporting evidence are recorded in `.omega/day01-signoff.json`.
