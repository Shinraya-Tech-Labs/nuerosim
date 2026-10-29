# T025 — AdEx threshold dynamics

## Purpose

Audit the production AdEx solver's documented numerical threshold `threshold + 5*Delta`, spike timestamps, and reset behavior under a deterministic current pulse.

## Contract

- **Input:** one validated AdEx `Experiment`, explicit units, expected spike count/times, and a positive timing tolerance.
- **Units:** time ms; voltage mV; current density µA/cm²; `threshold` and `Delta` mV.
- **Output:** numerical cutoff voltage, production spike times/count and intervals, final voltage, manifest, and acceptance status.
- **Acceptance example:** threshold −50 mV and Delta 2 mV gives a numerical cutoff of −40 mV. With `a=b=0`, 50 µA/cm² on [1,10) ms, duration 20 ms and dt 0.025 ms, production spike times are 1.5, 4.0, 6.5 and 9.0 ms.
- **Errors:** reject non-AdEx or multi-neuron experiments, invalid units/tolerance, and a fixture whose expected spike count/times differ beyond tolerance.
- **Exclusions:** the cutoff is a numerical stabilization choice, not a biological firing threshold. This check does not establish universal spike timing accuracy or model validity.
