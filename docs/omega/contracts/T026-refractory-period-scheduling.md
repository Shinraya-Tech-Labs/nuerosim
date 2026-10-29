# T026 — refractory period scheduling

## Purpose

Verify that production LIF/AdEx spike trains respect the configured absolute refractory interval.

## Contract

- **Input:** one validated LIF or AdEx `Experiment` and a numerical interval tolerance.
- **Units:** time and refractory period in ms; voltage mV; current density µA/cm².
- **Output:** production spike times, interspike intervals, configured refractory period, dt-derived step count, manifest, and pass/fail.
- **Acceptance example:** LIF with dt 0.025 ms, refractory 2 ms, rest/reset −65 mV, threshold −50 mV, tau 20 ms, and 20 µA/cm² on [0,20) ms produces first spike at 0.775 ms and 2.775 ms intervals.
- **Errors:** reject other models, multiple neurons, invalid tolerances and malformed configurations.
- **Exclusions:** an interval at least as long as the refractory period validates scheduling only; it does not establish absolute spike timing accuracy or biological validity.
