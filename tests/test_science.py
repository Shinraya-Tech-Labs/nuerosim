import numpy as np
import pytest
from scipy.integrate import solve_ivp

from neurosim.workbench.config import Experiment, Parameters, Pulse
from neurosim.workbench.engine import (
    Cancelled,
    cable_current,
    derivative,
    initial_state,
    rates,
    simulate,
)


def test_hh_rate_limits_and_rest():
    assert rates(np.array([-40.0]))[0][0] == 1
    assert rates(np.array([-55.0]))[4][0] == 0.1
    r = simulate(Experiment(pulses=[]))
    assert max(abs(np.array(r["voltage"])[0] + 65)) < 0.1
    assert r["spikes"] == [[]]
    assert np.all(
        (np.array(r["final_state"])[1:4] >= 0) & (np.array(r["final_state"])[1:4] <= 1)
    )


def test_hh_stimulus_intensity_increases_spike_response():
    responses = []
    for amplitude in (0, 2, 5, 10):
        result = simulate(
            Experiment(
                duration=20,
                dt=0.025,
                record_every=1,
                pulses=[Pulse(start=0, stop=20, amplitude=amplitude)],
            )
        )
        responses.append((len(result["spikes"][0]), max(result["voltage"][0])))

    spike_counts = [count for count, _ in responses]
    peak_voltages = [peak for _, peak in responses]
    assert spike_counts == sorted(spike_counts)
    assert spike_counts[0] == 0 < spike_counts[-1]
    assert all(left < right for left, right in zip(peak_voltages, peak_voltages[1:]))


def test_hh_reference_convergence():
    # Independent scalar HH equations + adaptive DOP853; constant current avoids
    # discontinuity-related order reduction in this solver comparison.
    def reference(t, y):
        v, m, h, n = y
        am = 1 if abs(v + 40) < 1e-8 else 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))
        an = (
            0.1
            if abs(v + 55) < 1e-8
            else 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))
        )
        return [
            10 - 120 * m**3 * h * (v - 50) - 36 * n**4 * (v + 77) - 0.3 * (v + 54.387),
            am * (1 - m) - 4 * np.exp(-(v + 65) / 18) * m,
            0.07 * np.exp(-(v + 65) / 20) * (1 - h) - h / (1 + np.exp(-(v + 35) / 10)),
            an * (1 - n) - 0.125 * np.exp(-(v + 65) / 80) * n,
        ]

    ref = solve_ivp(
        reference,
        (0, 20),
        [-65, 0.052932485257, 0.596120753508, 0.317676914061],
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
        dense_output=True,
    )
    errors = []
    for dt in [0.025, 0.0125]:
        r = simulate(
            Experiment(
                duration=20, dt=dt, record_every=1, pulses=[Pulse(start=0, stop=20)]
            )
        )
        errors.append(np.max(abs(np.array(r["voltage"])[0] - ref.sol(r["t"])[0])))
        assert len(r["spikes"][0]) == 2
        assert 30 < max(r["voltage"][0]) < 50
    assert errors[0] < 0.02
    assert errors[1] < errors[0] / 8
    print(
        f"HH max voltage errors (mV), dt .025/.0125: {errors}; refinement ratio: {errors[0] / errors[1]:.3f}"
    )


def test_lif_analytic_subthreshold():
    c = Experiment(
        model="lif", duration=20, pulses=[Pulse(start=0, stop=20, amplitude=0.2)]
    )
    r = simulate(c)
    expected = -65 + 4 * (1 - np.exp(-np.array(r["t"]) / 20))
    np.testing.assert_allclose(r["voltage"][0], expected, atol=1e-9)


def test_lif_spike_period_and_refractory():
    r = simulate(
        Experiment(
            model="lif", duration=100, pulses=[Pulse(start=0, stop=100, amplitude=2)]
        )
    )
    period = -20 * np.log(1 - 15 / 40) + 2
    np.testing.assert_allclose(np.diff(r["spikes"][0]), period, atol=0.026)


def test_adex_subthreshold_reference_and_adaptation():
    c = Experiment(
        model="adex", duration=20, pulses=[Pulse(start=0, stop=20, amplitude=0.3)]
    )
    r = simulate(c)

    def f(t, y):
        v, w = y
        return [
            (-65 - v) / 20 + 0.3 + 2 / 20 * np.exp((v + 50) / 2) - w,
            (0.02 * (v + 65) - w) / 100,
        ]

    ref = solve_ivp(f, (0, 20), [-65, 0], rtol=1e-10, atol=1e-12)
    np.testing.assert_allclose(
        np.array(r["final_state"])[[0, 4], 0], ref.y[:, -1], atol=1e-7
    )
    r = simulate(
        Experiment(
            model="adex", duration=200, pulses=[Pulse(start=0, stop=200, amplitude=2)]
        )
    )
    assert len(r["spikes"][0]) > 3
    assert np.diff(r["spikes"][0])[-1] > np.diff(r["spikes"][0])[0]


def test_passive_cable_conservation_and_decay():
    v = np.array([-70.0, -60.0, -50.0])
    assert abs(cable_current(v, 0.1).sum()) < 1e-14
    c = Experiment(
        model="cable", n=3, duration=10, pulses=[], parameters=Parameters(g_leak=0)
    )
    y = initial_state(c)
    y[0] = v
    ref = solve_ivp(
        lambda t, x: cable_current(x, 0.1), (0, 10), v, rtol=1e-10, atol=1e-12
    )
    assert abs(ref.y[:, -1].sum() - v.sum()) < 1e-10
    assert np.ptp(ref.y[:, -1]) < np.ptp(v)
    assert derivative(y, np.zeros(3), np.zeros(3), np.zeros(3), c)[0].sum() == 0
    r = simulate(c)
    np.testing.assert_allclose(r["voltage"], -65)
    driven = simulate(
        Experiment(
            model="cable",
            n=3,
            duration=10,
            parameters=Parameters(g_leak=0),
            pulses=[Pulse(start=0, stop=10, amplitude=1)],
        )
    )
    assert abs(sum(v[-1] for v in driven["voltage"]) - (-195 + 10)) < 1e-9


def test_network_seed_inhibition_and_recording():
    c = Experiment(
        model="lif",
        n=8,
        probability=0.5,
        duration=30,
        pulses=[Pulse(start=0, stop=30, amplitude=3)],
    )
    a, b = simulate(c), simulate(c)
    assert a["voltage"] == b["voltage"] and a["edges"] == b["edges"]
    assert a["edges"] != simulate(c.model_copy(update={"seed": 43}))["edges"]
    assert len(a["voltage"]) == 8 and np.isfinite(a["voltage"]).all()
    state = initial_state(c)
    z = np.zeros(8)
    g = np.ones(8) * 0.1
    base = derivative(state, z, z, z, c)[0]
    assert np.all(derivative(state, z, g, z, c)[0] > base)
    assert np.all(derivative(state, z, z, g, c)[0] < base)


def test_cancel_and_invalid_inputs():
    with pytest.raises(Cancelled):
        simulate(Experiment(), cancelled=lambda: True)
    for kw in (
        {"dt": 0},
        {"duration": float("nan")},
        {"backend": "cuda"},
        {"n": 10000},
        {"model": "cable", "probability": 0.1},
        {"solver": "cn"},
        {"model": "hh", "solver": "euler"},
        {"pulses": [{"target": 3}]},
    ):
        with pytest.raises(ValueError):
            Experiment(**kw)
