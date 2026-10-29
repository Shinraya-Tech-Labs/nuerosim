"""Small runtime-checked quantities for the documented workbench units."""

from dataclasses import dataclass
from enum import Enum
import math


class Unit(Enum):
    SECOND = ("s", "time", 1.0)
    MILLISECOND = ("ms", "time", 1e-3)
    VOLT = ("V", "voltage", 1.0)
    MILLIVOLT = ("mV", "voltage", 1e-3)
    MILLIAMP_PER_CM2 = ("mA/cm^2", "current_density", 1000.0)
    MICROAMP_PER_CM2 = ("uA/cm^2", "current_density", 1.0)
    SIEMENS_PER_CM2 = ("S/cm^2", "conductance_density", 1000.0)
    MILLISIEMENS_PER_CM2 = ("mS/cm^2", "conductance_density", 1.0)
    FARAD_PER_CM2 = ("F/cm^2", "capacitance_density", 1e6)
    MICROFARAD_PER_CM2 = ("uF/cm^2", "capacitance_density", 1.0)
    HERTZ = ("Hz", "frequency", 1.0)
    KILOHERTZ = ("kHz", "frequency", 1000.0)

    def __init__(self, symbol, dimension, scale):
        self.symbol = symbol
        self.dimension = dimension
        self.scale = scale

    @classmethod
    def from_symbol(cls, symbol):
        for unit in cls:
            if unit.symbol == symbol:
                return unit
        raise ValueError(f"unsupported unit: {symbol}")


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: Unit

    def __post_init__(self):
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise ValueError("quantity value must be a finite number")
        if not math.isfinite(self.value):
            raise ValueError("quantity value must be a finite number")
        if not isinstance(self.unit, Unit):
            raise ValueError("quantity unit must be a Unit")
        object.__setattr__(self, "value", float(self.value))

    def to(self, target):
        if not isinstance(target, Unit):
            raise ValueError("target unit must be a Unit")
        if self.unit.dimension != target.dimension:
            raise ValueError(
                f"cannot convert {self.unit.dimension} to {target.dimension}"
            )
        return Quantity(self.value * self.unit.scale / target.scale, target)


def mean_population_rate(spikes, neurons, duration):
    if isinstance(spikes, bool) or not isinstance(spikes, int) or spikes < 0:
        raise ValueError("spikes must be a non-negative integer")
    if isinstance(neurons, bool) or not isinstance(neurons, int) or neurons <= 0:
        raise ValueError("neurons must be a positive integer")
    if not isinstance(duration, Quantity) or duration.unit.dimension != "time":
        raise ValueError("duration must be a time Quantity")
    seconds = duration.to(Unit.SECOND).value
    if seconds <= 0:
        raise ValueError("duration must be positive")
    return Quantity(spikes / neurons / seconds, Unit.HERTZ)
