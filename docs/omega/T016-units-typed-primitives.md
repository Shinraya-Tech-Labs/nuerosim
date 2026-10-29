# Typed unit primitives

Convert supported quantities explicitly and use the typed rate helper:

```python
from neurosim.units import Quantity, Unit, mean_population_rate

duration = Quantity(1000, Unit.MILLISECOND).to(Unit.SECOND)
rate = mean_population_rate(2, 1, duration)
print(duration.value, duration.unit.symbol)  # 1.0 s
print(rate.value, rate.unit.symbol)          # 2.0 Hz
```

The supported units and conversion scales are in `neurosim.units`. Cross-dimension conversions, nonfinite values, and invalid counts/durations raise `ValueError`. The existing `neurosim.units_audit` command exercises these primitives against workbench result JSON without changing the stored schema.

See the [contract](contracts/T016-units-typed-primitives.md) and [validation evidence](evidence/T016-units-typed-primitives.md).
