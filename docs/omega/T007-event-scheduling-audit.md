# Event scheduling audit

Run the audit on a workbench result JSON file:

```sh
PYTHONPATH=python python -m neurosim.event_schedule results.json
```

For a ZIP export, extract its `results.json` member first. The audit checks that the manifest declares milliseconds and that `effective_delay_ms` matches the engine's timestep rounding rule. It reports the requested delay, timestep, integer delay steps, effective delay, and rounding amount. Derived millisecond values are rounded to 12 decimal places for display.

An invalid manifest/config or inconsistent saved delay exits nonzero with an error. The engine applies arrivals at step start and schedules outgoing events from spike time plus effective delay; the audit checks the delay arithmetic only. It does not verify each event, synaptic weight or response magnitude, and it makes no biological claim.

## Verification checklist

- [x] Check the off-grid 1.01 ms / 0.025 ms example (41 steps, 1.025 ms).
- [x] Reject an effective delay shorter than requested.
- [x] Check minimum grid-aligned delay and zero rounding.
- [x] Audit a real simulation result and verify target response after arrival.

See the [contract](contracts/T007-event-scheduling-audit.md) and [validation evidence](evidence/T007-event-scheduling-audit.md).
