"""Narrow regression coverage, not endorsement of the entire legacy engine."""

import numpy as np
import pytest
from neurosim.models.plasticity import NeurotransmitterDiffusion
from neurosim.models.neuron import Compartment, CompartmentType, MultiCompartmentNeuron


def test_diffusion_mass_boundary_and_decay():
    d = NeurotransmitterDiffusion(k_clear=0)
    d.release(1, cx=0, cy=0)
    mass = d.total_transmitter()
    d.step()
    assert d.C[-1, -1] == 0  # sealed, not periodic
    for _ in range(100):
        d.step()
    assert np.all(d.C >= 0)
    assert abs(d.total_transmitter() - mass) < 1e-14
    d = NeurotransmitterDiffusion(k_clear=0.1)
    d.release(1)
    mass = d.total_transmitter()
    for _ in range(100):
        d.step()
    assert d.total_transmitter() == pytest.approx(mass * (1 - 0.1 * d.dt) ** 100)
    with pytest.raises(ValueError):
        NeurotransmitterDiffusion(dt=0.002)  # alpha=.32; > .25 even without clearance


def test_legacy_axial_units_and_conservation():
    neuron = MultiCompartmentNeuron(0)
    for i in range(2):
        neuron.add_compartment(
            Compartment(
                i, CompartmentType.SOMA, 20, 20, parent_id=None if i == 0 else 0
            )
        )
    neuron.initialize()
    neuron.V = np.array([-65.0, -55.0])
    currents = neuron._axial_currents()
    assert currents[0] == pytest.approx(10 / neuron.compartments[0].r_axial * 1000)
    assert currents.sum() == 0
