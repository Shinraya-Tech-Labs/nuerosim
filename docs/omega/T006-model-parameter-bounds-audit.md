# Model parameter bounds audit

Run from the repository root:

```sh
PYTHONPATH=python python -m neurosim.parameter_bounds
```

The command reads the Pydantic JSON Schema for the workbench `Experiment` and reports bounded numeric fields from the Experiment model and nested definitions, including `Pulse` and `Parameters`. Each record preserves the declared default and inclusive or exclusive limits in the field's existing input units. The command exits nonzero if a schema is malformed or a default violates its bounds.

This only checks field-level schema defaults. Cross-field validators—such as timestep divisibility, pulse alignment, and the HH Euler timestep restriction—are not represented by the schema scan. Passing this audit does not prove numerical stability, biological calibration, or scientific suitability; the tool does not assign or convert units.

## Verification checklist

- [x] Compare the audit count with bounded numeric properties in the live schema.
- [x] Check an inclusive maximum and an exclusive minimum.
- [x] Reject a default outside its bound.
- [x] Compare CLI output with the actual workbench schema audit.

See the [contract](contracts/T006-model-parameter-bounds-audit.md) and [validation evidence](evidence/T006-model-parameter-bounds-audit.md).
