# T017 — stimulus pulse waveform library

## Purpose

Generate common current-clamp pulse protocols as existing validated `Pulse` objects for use in `Experiment` configurations.

## Contract

- **Inputs:** times/durations in milliseconds, amplitude in µA/cm², non-negative integer target, and integer train count.
- **Outputs:** ordered `Pulse` objects with absolute start/stop times and signed amplitudes.
- **Library protocols:** single rectangular step; equally spaced, non-overlapping pulse train; two-phase equal-duration biphasic pulse with opposite amplitudes and zero ideal net charge.
- **Acceptance examples:** a three-pulse train with 1 ms width and 3 ms interval starts at 0, 3, and 6 ms; a ±2 µA/cm², 1 ms/phase biphasic waveform has ideal net charge 0 µA·ms/cm².
- **Errors:** reject non-finite/negative times, nonpositive widths/intervals/counts, overlapping trains, invalid target/amplitude, and trains above the 128-pulse `Experiment` limit.
- **Integration:** outputs use the existing `Pulse` model and can be passed directly into real `Experiment` simulations.
- **Exclusions:** these are current commands, not measured delivered electrode currents; ideal charge balance ignores electrode impedance, hardware limits, and biological effects.
