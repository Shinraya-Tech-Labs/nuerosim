"""Current-clamp pulse protocol constructors returning validated Pulse models."""

import math

from .workbench.config import Pulse


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


def _pulse(start, stop, amplitude, target):
    start = _number(start, "start_ms")
    stop = _number(stop, "stop_ms")
    amplitude = _number(amplitude, "amplitude_uA_cm2")
    if start < 0 or stop <= start:
        raise ValueError("pulse requires start_ms >= 0 and stop_ms > start_ms")
    if isinstance(target, bool) or not isinstance(target, int) or target < 0:
        raise ValueError("target must be a non-negative integer")
    if not -100 <= amplitude <= 100:
        raise ValueError("amplitude_uA_cm2 must be between -100 and 100")
    return Pulse(start=start, stop=stop, amplitude=amplitude, target=target)


def single_step(start_ms, stop_ms, amplitude_uA_cm2, target=0):
    """Create one rectangular current step."""
    return _pulse(start_ms, stop_ms, amplitude_uA_cm2, target)


def pulse_train(start_ms, width_ms, interval_ms, count, amplitude_uA_cm2, target=0):
    """Create equally spaced rectangular pulses; interval is start-to-start."""
    start = _number(start_ms, "start_ms")
    width = _number(width_ms, "width_ms")
    interval = _number(interval_ms, "interval_ms")
    if start < 0 or width <= 0:
        raise ValueError("start_ms must be non-negative and width_ms positive")
    if interval < width:
        raise ValueError("pulse train interval must be at least its width")
    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 128:
        raise ValueError("pulse train count must be between 1 and 128")
    return [
        _pulse(start + index * interval, start + index * interval + width, amplitude_uA_cm2, target)
        for index in range(count)
    ]


def biphasic(start_ms, phase_width_ms, amplitude_uA_cm2, target=0):
    """Create equal-width opposite phases with zero ideal integrated charge."""
    start = _number(start_ms, "start_ms")
    width = _number(phase_width_ms, "phase_width_ms")
    amplitude = _number(amplitude_uA_cm2, "amplitude_uA_cm2")
    if start < 0 or width <= 0:
        raise ValueError("start_ms must be non-negative and phase_width_ms positive")
    if not -100 <= amplitude <= 100:
        raise ValueError("amplitude_uA_cm2 must be between -100 and 100")
    return [
        _pulse(start, start + width, amplitude, target),
        _pulse(start + width, start + 2 * width, -amplitude, target),
    ]
