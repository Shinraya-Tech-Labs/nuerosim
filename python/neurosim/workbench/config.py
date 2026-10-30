"""Strict bounded manifests. Model quantities use membrane density units."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid", allow_inf_nan=False, validate_default=True
    )


class Pulse(StrictModel):
    target: int = Field(0, ge=0)
    start: float = Field(10, ge=0)
    stop: float = Field(40, gt=0)
    amplitude: float = Field(10, ge=-100, le=100)


class Parameters(StrictModel):
    cm: float = Field(1, ge=0.5, le=2)
    g_na: float = Field(120, ge=0, le=240)
    g_k: float = Field(36, ge=0, le=72)
    g_leak: float = Field(0.3, ge=0, le=1)
    e_na: float = Field(50, ge=20, le=70)
    e_k: float = Field(-77, ge=-100, le=-60)
    e_leak: float = Field(-54.387, ge=-80, le=-40)
    tau_m: float = Field(20, ge=5, le=100)
    rest: float = Field(-65, ge=-80, le=-55)
    reset: float = Field(-65, ge=-80, le=-55)
    threshold: float = Field(-50, ge=-54, le=-40)
    refractory: float = Field(2, ge=0, le=20)
    delta_t: float = Field(2, ge=1, le=5)
    tau_w: float = Field(100, ge=10, le=1000)
    a: float = Field(0.02, ge=0, le=0.2)
    b: float = Field(0.1, ge=0, le=2)
    axial: float = Field(0.1, ge=0, le=1)
    izh_a: float = Field(0.02, ge=0, le=1)
    izh_b: float = Field(0.2, ge=0, le=1)
    izh_c: float = Field(-65, ge=-100, le=-40)
    izh_d: float = Field(8, ge=-20, le=50)
    fhn_epsilon: float = Field(0.08, gt=0, le=1)
    fhn_beta: float = Field(0.7, ge=0, le=2)
    fhn_gamma: float = Field(0.8, ge=0, le=2)
    noise_std: float = Field(0, ge=0, le=100)


class Experiment(StrictModel):
    name: str = Field("Current clamp", min_length=1, max_length=120)
    model: Literal["hh", "lif", "adex", "eif", "qif", "izhikevich", "fhn", "morris_lecar", "cable"] = "hh"
    solver: Literal["rk4", "euler"] = "rk4"
    duration: float = Field(50, gt=0, le=2000)
    dt: float = Field(0.025, ge=0.001, le=0.025)
    record_every: int = Field(4, ge=1, le=1000)
    n: int = Field(1, ge=1, le=512)
    seed: int = Field(42, ge=0, le=2**32 - 1)
    probability: float = Field(0, ge=0, le=1)
    inhibitory_fraction: float = Field(0.2, ge=0, le=1)
    weight: float = Field(0.05, ge=0, le=0.5)
    delay: float = Field(1, ge=0.025, le=20)
    tau_syn: float = Field(5, ge=1, le=50)
    initial_voltage: float = Field(-65, ge=-80, le=-55)
    pulses: list[Pulse] = Field(default_factory=lambda: [Pulse()], max_length=128)
    parameters: Parameters = Field(default_factory=Parameters)

    @model_validator(mode="after")
    def check_budget(self):
        steps = round(self.duration / self.dt)
        if abs(steps * self.dt - self.duration) > 1e-8:
            raise ValueError("duration must be an integer multiple of dt")
        if steps * self.n > 10_000_000:
            raise ValueError("limit: 10 million neuron-steps")
        if (steps // self.record_every + 2) * self.n > 1_000_000:
            raise ValueError("limit: one million recorded voltage values")
        if self.model == "cable" and (self.n > 32 or self.probability != 0):
            raise ValueError("passive cable: 1..32 equal compartments, no synapses")
        if self.model == "hh" and self.solver == "euler" and self.dt > 0.005:
            raise ValueError("HH Euler requires dt <= .005 ms")
        for pulse in self.pulses:
            if (
                pulse.target >= self.n
                or not 0 <= pulse.start < pulse.stop <= self.duration
            ):
                raise ValueError("invalid pulse target or interval")
            if any(
                abs(t / self.dt - round(t / self.dt)) > 1e-7
                for t in (pulse.start, pulse.stop)
            ):
                raise ValueError("pulse boundaries must align with dt")
        return self
