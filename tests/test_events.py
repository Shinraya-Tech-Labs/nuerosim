import numpy as np
from neurosim.workbench.config import Experiment, Pulse
from neurosim.workbench.engine import simulate


def test_synaptic_delay_and_weight_once():
    base = dict(
        model="lif",
        n=2,
        duration=25,
        record_every=1,
        probability=1,
        inhibitory_fraction=0,
        delay=2,
        pulses=[Pulse(start=0, stop=25, amplitude=3)],
    )
    result = simulate(Experiment(**base))
    times = np.array(result["t"])
    first_arrival = result["spikes"][0][0] + 2
    voltage = np.array(result["voltage"])[1]
    np.testing.assert_allclose(voltage[times <= first_arrival + 1e-9], -65, atol=1e-10)
    assert voltage[np.searchsorted(times, first_arrival + 0.025)] > -65
    # First step of conductance-driven target response against a scalar reference.
    from scipy.integrate import solve_ivp

    ref = solve_ivp(
        lambda t, v: (-65 - v) / 20 + 0.05 * np.exp(-t / 5) * (0 - v),
        (0, 0.025),
        [-65],
        rtol=1e-12,
        atol=1e-12,
    )
    actual = voltage[np.searchsorted(times, first_arrival + 0.025)]
    np.testing.assert_allclose(actual, ref.y[0, -1], atol=1e-7)
    inhibitory = simulate(Experiment(**{**base, "inhibitory_fraction": 1}))
    assert min(inhibitory["voltage"][1]) < -65


def test_euler_convergence_and_cable_driven_transfer():
    errors = []
    for dt in [0.025, 0.0125]:
        result = simulate(
            Experiment(
                model="lif",
                solver="euler",
                dt=dt,
                duration=10,
                pulses=[Pulse(start=0, stop=10, amplitude=0.2)],
            )
        )
        errors.append(abs(result["voltage"][0][-1] - (-65 + 4 * (1 - np.exp(-0.5)))))
    assert errors[1] < errors[0] * 0.51
    result = simulate(
        Experiment(
            model="cable",
            n=3,
            duration=10,
            pulses=[Pulse(start=0, stop=10, amplitude=1)],
        )
    )
    assert (
        result["voltage"][0][-1] > result["voltage"][1][-1] > result["voltage"][2][-1]
    )
