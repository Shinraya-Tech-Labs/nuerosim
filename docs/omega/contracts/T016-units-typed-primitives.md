# T016 — units typed primitives

## Purpose

Provide small runtime-checked quantities for the workbench's documented units, with explicit conversion only between units of the same physical dimension.

## Contract

- **Input:** finite numeric value and a supported `Unit`; booleans, NaN, and infinities are invalid.
- **Output:** immutable `Quantity` retaining its unit; `.to(target_unit)` returns an explicitly converted quantity and rejects cross-dimension conversion.
- **Supported dimensions:** time (s/ms), voltage (V/mV), current density (µA/cm²/mA/cm²), conductance density (mS/cm²/S/cm²), capacitance density (µF/cm²/F/cm²), and frequency (Hz/kHz).
- **Units:** scale factors are exact decimal SI prefixes; values remain floating point. The workbench still stores times in ms and voltages in mV.
- **Acceptance examples:** 1000 ms converts to 1 s; 1 V converts to 1000 mV; 2 spikes / 1 neuron / 1 s returns 2 Hz.
- **Errors:** reject unsupported units, invalid values, mismatched dimensions, negative spike counts, nonpositive neuron counts, and nonpositive duration.
- **Integration:** the existing mean-rate units audit will use the typed time and rate primitive while preserving its JSON schema.
- **Exclusions:** this does not change stored/API values, enforce units statically, add dimensional arithmetic, or validate the biological model.
