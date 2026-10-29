import json
from pathlib import Path

import pytest

from neurosim.units import Quantity, Unit, mean_population_rate


FIXTURE = Path("tests/fixtures/omega/T016-units-typed-primitives/valid.json")
INVALID = Path("tests/fixtures/omega/T016-units-typed-primitives/invalid.json")


def test_T016_units_typed_primitives_unit():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for conversion in fixture["conversions"]:
        source = Quantity(conversion["value"], Unit.from_symbol(conversion["from"]))
        converted = source.to(Unit.from_symbol(conversion["to"]))
        assert converted.value == conversion["expected"]
    rate = fixture["mean_rate"]
    result = mean_population_rate(
        rate["spikes"],
        rate["neurons"],
        Quantity(rate["duration"], Unit.from_symbol(rate["duration_unit"])),
    )
    assert result.unit is Unit.HERTZ
    assert result.value == rate["expected_hz"] == 2


def test_invalid_cross_dimension_conversion_fixture():
    fixture = json.loads(INVALID.read_text(encoding="utf-8"))
    value = Quantity(fixture["value"], Unit.from_symbol(fixture["from"]))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        value.to(Unit.from_symbol(fixture["to"]))


@pytest.mark.parametrize("value", [True, float("nan"), float("inf")])
def test_invalid_quantity_values_are_rejected(value):
    with pytest.raises(ValueError, match="finite number"):
        Quantity(value, Unit.MILLISECOND)


def test_zero_identity_and_overflow_boundaries():
    assert Quantity(0, Unit.MILLISECOND).to(Unit.SECOND).value == 0
    with pytest.raises(ValueError, match="finite number"):
        Quantity(1e308, Unit.SECOND).to(Unit.MILLISECOND)
    with pytest.raises(ValueError, match="unsupported unit"):
        Unit.from_symbol("fortnight")


@pytest.mark.parametrize(
    ("spikes", "neurons", "duration", "message"),
    [
        (-1, 1, Quantity(1, Unit.SECOND), "spikes must be"),
        (1, 0, Quantity(1, Unit.SECOND), "neurons must be"),
        (1, 1, Quantity(0, Unit.SECOND), "duration must be positive"),
        (1, 1, Quantity(1, Unit.VOLT), "duration must be a time Quantity"),
    ],
)
def test_mean_rate_rejects_invalid_dimensions_or_counts(spikes, neurons, duration, message):
    with pytest.raises(ValueError, match=message):
        mean_population_rate(spikes, neurons, duration)
