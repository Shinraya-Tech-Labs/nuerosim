# T006 validation evidence

## Schema cross-check and environment

At revision `ce723a35d4cb70bac5e6f2924d89030044e0fd63`, the CLI audited the installed workbench `Experiment.model_json_schema()` on Windows 11, Python 3.14.2. It reported **32** bounded numeric fields, matching an independent count of numeric properties with declared bounds across the root schema and `$defs`. Every reported default satisfied its declared inclusive/exclusive bounds.

Two representative values:

- `Experiment.dt`: default `0.025`, inclusive bounds `0.001`–`0.025`.
- `Pulse.stop`: default `40`, exclusive minimum `0`.

The focused tests passed (5 passed), including exact inclusive/exclusive edge behavior and the live CLI comparison.

## Limits

The report preserves bounds in each field's input units and does not assign or convert units. JSON Schema omits custom cross-field checks and stability analysis; this audit does not claim biological calibration or safety.
