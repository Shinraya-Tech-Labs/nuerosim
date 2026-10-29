import json
from pathlib import Path

import pytest

from neurosim.stimuli import biphasic, pulse_train, single_step
from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate


VALID = Path("tests/fixtures/omega/T017-stimulus-pulse-waveform-library/valid.json")
INVALID = Path("tests/fixtures/omega/T017-stimulus-pulse-waveform-library/invalid.json")


def test_T017_stimulus_pulse_waveform_library_unit():
    fixture = json.loads(VALID.read_text(encoding="utf-8"))
    train = [p.model_dump() for p in pulse_train(**fixture["train"])]
    phases = [p.model_dump() for p in biphasic(**fixture["biphasic"])]
    assert train == fixture["expected_train"]
    assert phases == fixture["expected_biphasic"]
    charge = sum(pulse["amplitude"] * (pulse["stop"] - pulse["start"]) for pulse in phases)
    assert charge == fixture["expected_net_charge_uA_ms_cm2"] == 0


def test_invalid_overlap_fixture_is_rejected():
    fixture = json.loads(INVALID.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        pulse_train(
            fixture["start_ms"],
            fixture["width_ms"],
            fixture["interval_ms"],
            fixture["count"],
            fixture["amplitude_uA_cm2"],
        )


@pytest.mark.parametrize(
    ("args", "message"),
    [
        ((-1, 1, 2, 1, 1), "start_ms must be non-negative"),
        ((0, 1, 2, 0, 1), "count must be between 1 and 128"),
        ((0, 1, 2, 129, 1), "count must be between 1 and 128"),
        ((0, 1, 2, 1, 101), "amplitude_uA_cm2 must be between"),
        ((0, float("nan"), 2, 1, 1), "width_ms must be a finite number"),
    ],
)
def test_train_boundaries_are_rejected(args, message):
    with pytest.raises(ValueError, match=message):
        pulse_train(*args)


def test_single_step_and_touching_intervals_are_valid():
    step = single_step(0, 1, -2, target=1)
    train = pulse_train(0, 1, 1, 2, 2)
    assert (step.start, step.stop, step.amplitude, step.target) == (0, 1, -2, 1)
    assert [(pulse.start, pulse.stop) for pulse in train] == [(0, 1), (1, 2)]


def test_biphasic_and_pulse_argument_limits():
    with pytest.raises(ValueError, match="phase_width_ms positive"):
        biphasic(0, 0, 1)
    with pytest.raises(ValueError, match="target must be a non-negative integer"):
        single_step(0, 1, 1, target=True)
    with pytest.raises(ValueError, match="count must be between 1 and 128"):
        pulse_train(0, 1, 1, True, 1)
    with pytest.raises(ValueError, match="start_ms must be a finite number"):
        single_step(True, 1, 1)


def test_generated_train_drives_real_experiment():
    pulses = pulse_train(0, 1, 3, 3, 2)
    config = Experiment(model="lif", duration=20, pulses=pulses, record_every=40)
    result = simulate(config)
    baseline = simulate(config.model_copy(update={"pulses": []}))
    assert result["manifest"]["config"]["pulses"] == [p.model_dump() for p in pulses]
    assert result["voltage"] != baseline["voltage"]
