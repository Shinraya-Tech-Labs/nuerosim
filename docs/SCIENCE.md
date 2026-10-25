# Scientific model contract

The supported implementation is `neurosim.workbench`. It is an educational and
numerical experimentation platform, not a validated model of a human cell type,
brain circuit, molecular dynamics or clinical physiology. The original L5/PV,
calcium, plasticity, reconstruction, CUDA and MPI prototypes are retained but
are not used by the workbench. Separating the execution path prevents the known
legacy numerical defects from contaminating new validation.

## Units and models

Time: ms; voltage: mV; current density: microamp/cm²; conductance density:
mS/cm²; capacitance density: microfarad/cm². All neurons within a network share
one model and parameter set. `initial_voltage` sets every compartment/neuron;
HH gates start at their steady-state values and AdEx adaptation starts at zero.

HH implements `C dV/dt = I - gNa*m³*h*(V-ENa) - gK*n⁴*(V-EK) - gL*(V-EL)`
and the classic alpha/beta equations at **6.3 °C**, with singularity limits at
-40 and -55 mV. Conductances are configurable. No temperature scaling or
changing ion concentrations is claimed. A spike is an upward crossing of 0 mV.
The independent scalar DOP853 reference tests use default HH parameters and
constant 10 microamp/cm² stimulation; they validate equation implementation,
not agreement with a measured biological preparation.
See [NEURON HH documentation](https://neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/mechanisms/mech.html).

LIF implements `dV/dt = (rest-V)/tau_m + I/C`, followed by a reset at threshold
and an absolute refractory interval. HH conductance/reversal parameters do not
affect LIF. Subthreshold trajectories and regular spike intervals are compared
with analytic solutions.

AdEx adds `Delta/tau_m * exp((V-threshold)/Delta) - w/C` to LIF voltage and
`dw/dt = (a*(V-rest)-w)/tau_w`, with `w += b` at a spike. The numerical cutoff is
`threshold+5*Delta`; the exponential argument is capped there during RK stages.
Reset discontinuities and grid spike timing limit accuracy near firing even
with RK4. Adaptation continues during refractory periods while voltage is held
at reset. This cutoff variant is tested for subthreshold agreement and adaptation,
not for exhaustive firing-pattern equivalence.
See [Brette and Gerstner's AdEx description](https://www.scholarpedia.org/article/Adaptive_exponential_integrate-and-fire_model).

The cable is a **passive sealed chain of 1–32 equal-area compartments** with
equal capacitance and symmetric adjacent coupling. `C dV_i/dt = I_i -
gL*(V_i-EL) + axial*sum(V_j-V_i)`. Each edge carries opposite currents,
preserving total capacitive charge without leak/input. It is not an SWC-derived
active dendrite model; no geometry-dependent resistivity, calcium or soma/AIS
specialization is represented. `n` denotes compartments for this model.

## Inputs and synapses

Pulses add together and use half-open intervals `[start,stop)` on the timestep
grid. Amplitude is current **density**, not nA or total microamps. Arbitrary
Python functions and uploaded code are not accepted by the API.

Random directed connectivity uses NumPy's seeded generator, excludes self-edges,
and is stored explicitly in results. The last `round(n*inhibitory_fraction)`
neurons are inhibitory. A presynaptic spike increases the target conductance by
`weight` exactly once. Excitatory reversal is 0 mV; inhibitory reversal is -80 mV.
Both use `dg/dt=-g/tau_syn`, evaluated analytically at RK stages. Delay rounds
up to an integer number of timesteps, recorded as `effective_delay_ms`.
Events arrive at the start of a step after their recorded spike time plus delay.
No plasticity, stochastic channel noise, mixed cell-type populations or
double-exponential receptor kinetics is claimed.

## Integration and bounds

Float64 forward Euler and explicit RK4 are supported. Default dt=.025 ms;
HH Euler requires <=.005 ms. RK4 is fourth order only on smooth portions of the
trajectory. Current discontinuities align to the grid; threshold/reset events
are grid-quantized (timing uncertainty at least one dt). Decrease dt and compare
results for each scientific use, especially near threshold. Allowed parameter
ranges are resource/sanity constraints, **not a stability proof** for every
parameter combination. Non-finite states and out-of-range HH gates fail the job;
HH gates are not clipped to conceal instability.

Limits: 512 neurons, 2000 ms, 10 million neuron-steps, one million recorded
voltage values, 128 pulses, 32768 realized synapses and one million pending
events. Synapse/event limits fail jobs explicitly if exceeded.
Recording includes t=0 and the exact final time,
even when the recording stride does not divide the step count. Spikes are
recorded at every step independently of voltage recording stride. Firing-rate
bins span the actual duration and use actual bin widths, including silent
neurons in the denominator. Results use `[0,duration]` for recorded spikes.

## Reproducibility and validation scope

Exports include full configuration, seed, connectivity, units, version, engine
source hash, configuration hash, NumPy/Python/platform and outputs. Re-running
with the same environment is deterministic; cross-version/platform bitwise
identity is not guaranteed. Pin the environment and preserve the wheel for
archival work. A configuration hash identifies the full manifest configuration,
including experiment name; it is not an output checksum.

Tests cover HH rest, rate singularities, spike count/peak and timestep convergence
against an independent adaptive solver; analytic LIF; subthreshold AdEx and
adaptation; conservative cable coupling; input validation; deterministic networks;
synapse sign, onset delay and first-step amplitude. These do not establish
parameter-fitting quality, physiological accuracy of arbitrary networks, or
CUDA/MPI correctness. The raw legacy test failures remain in validation records.
