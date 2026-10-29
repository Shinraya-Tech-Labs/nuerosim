# T006 — Model parameter bounds audit

## Purpose

Report numeric field defaults and declared inclusive/exclusive bounds from the supported workbench Pydantic schema, and verify that each default satisfies those bounds.

## Contract

- **Input:** `Experiment.model_json_schema()` and its named definitions (`$defs`).
- **Scope:** numeric scalar properties with at least one declared `minimum`, `maximum`, `exclusiveMinimum`, or `exclusiveMaximum`; report model and field names, default, and each declared bound verbatim.
- **Output:** deterministic JSON with sorted bound records, count, and pass status. Bound values remain in the field's existing input unit; do not convert or infer units.
- **Defaults:** inspect the top-level Experiment schema and all named definitions, including nested Pulse and Parameters fields. Ignore strings, enums, and fields without numeric bounds.
- **Errors:** reject malformed schema/constraints, non-finite or non-numeric defaults, or defaults outside a declared bound.
- **Acceptance example:** `Experiment.dt` reports default `0.025` with inclusive bounds `0.001`–`0.025` and passes the default check.
- **Exclusions:** Pydantic's JSON Schema does not encode all cross-field validators (for example, duration/timestep divisibility, pulse alignment, or the HH Euler timestep rule). The audit does not evaluate those validators, prove numerical stability, assign biological units, or claim that allowed bounds are biologically calibrated.
