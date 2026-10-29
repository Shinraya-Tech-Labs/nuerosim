# T027 — spike crossing precision report

## Purpose

Quantify HH 0 mV spike-time grid quantization using linear interpolation between consecutive production voltage samples.

## Contract

- **Input:** one validated, single-neuron HH `Experiment` with `record_every=1` and explicit units.
- **Units:** time ms, voltage mV, current density µA/cm².
- **Output:** each production endpoint spike time, interpolated 0 mV crossing time, endpoint-minus-crossing offset, dt bound, and manifest.
- **Acceptance example:** dt 0.025 ms and `record_every=1` yield crossing offsets in [0,0.025] ms for upward crossings.
- **Errors:** reject other models, multiple neurons, downsampled voltage traces, invalid units and traces without a bracketing upward crossing.
- **Exclusions:** linear interpolation estimates crossing within each step; it is not an exact continuous-time solution or an accuracy claim for all timesteps/models.
