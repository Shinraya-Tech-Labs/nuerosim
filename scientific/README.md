# Reproducible scientific experiment records

`experiments/v020-core.json` defines bounded workbench runs for the supported
HH, LIF, AdEx, passive cable, and seeded network paths. Each entry includes the
full model configuration, purpose, units (at suite level), and links to tests
that independently check the relevant equations or invariants.

Run the suite from the repository root:

```powershell
$env:PYTHONPATH = 'python'
python scripts/run_scientific_validation.py --config scientific/experiments/v020-core.json --output-dir scientific/results/v020-core-reproduction-003
```

The runner refuses to write into a non-empty output directory. Each experiment
artifact records the complete execution manifest, raw trajectories/spikes/
connectivity, a SHA-256 over deterministic scientific outputs, and measured
wall time separately. Summary metadata records the Python, NumPy, and platform
environment and the SHA-256 of the exact suite configuration. Experiment IDs
are checked as safe filenames before output is written. The committed
`results/v020-core-run-001` and `results/v020-core-run-002` records are two
independent runs; all eight scientific output hashes match. Run 002 also records
the suite configuration hash. Wall-clock values can vary. The runner refuses
to overwrite evidence, so choose a new empty output directory for each run.

## Hodgkin–Huxley validation

The single-compartment model implements the classical sodium, potassium, and
leak-current equations:

```text
Cm dV/dt = I - gNa m^3 h (V - ENa) - gK n^4 (V - EK) - gL (V - EL)
dx/dt = alpha_x(V) (1 - x) - beta_x(V) x, x in {m, h, n}
```

The rate equations are the squid giant-axon formulation at 6.3 °C. Defaults
are `Cm=1 uF/cm^2`, `gNa=120 mS/cm^2`, `gK=36 mS/cm^2`,
`gL=0.3 mS/cm^2`, `ENa=50 mV`, `EK=-77 mV`, and `EL=-54.387 mV`.
Voltage starts at `-65 mV`; the three gates start at their steady-state values
at that voltage. The production solver is fixed-step RK4, with `dt=0.025 ms`
for the core suite. The response check applies constant 0, 2, 5, and
10 `uA/cm^2` current for 20 ms. It checks nondecreasing spike count and peak
voltage as drive increases, plus a quiescent no-drive baseline.

`tests/test_science.py::test_hh_reference_convergence` independently encodes
the scalar equations and compares production RK4 with SciPy's adaptive DOP853
solution (`rtol=1e-11`, `atol=1e-12`). The maximum voltage error must remain
below 0.02 mV; halving the production step must reduce error by at least 8x.
These bounds are comfortably above the measured reference error yet strict
enough to reject drift beyond the RK4 refinement envelope. On this host,
maximum errors at 0.025 and 0.0125 ms were 0.006001657 and 0.000305376 mV
(19.653x refinement). This is a numerical solver comparison, not a comparison
against new biological data.

The model equations and rate form are based on Hodgkin and Huxley's primary
paper: [A quantitative description of membrane current and its application to
conduction and excitation in nerve (1952)](https://doi.org/10.1113/jphysiol.1952.sp004764).

## LIF and AdEx validation

For LIF, the implemented subthreshold equation is
`dV/dt = (Vrest - V)/tau_m + I/Cm`, with threshold/reset and a fixed refractory
interval. Defaults are `Vrest=-65 mV`, `Vthreshold=-50 mV`, `Vreset=-65 mV`,
`tau_m=20 ms`, `Cm=1 uF/cm^2`, and `refractory=2 ms`; the initial voltage is
`-65 mV`. The production method is RK4 at `dt=0.025 ms`. With constant input,
the voltage has the analytic exponential solution and the inter-spike period
is `-tau_m*ln(1 - (Vthreshold - Vreset)/(I*tau_m)) + refractory`. Tests compare
the recorded subthreshold trajectory to the analytic curve and check the
derived period at 1, 2, and 4 `uA/cm^2`. Separate checks require firing rate to
increase with those current levels. The recorded 100 ms runs produced 30, 80,
and 160 Hz, respectively.

AdEx uses
`dV/dt = (Vrest-V)/tau_m + I/Cm + Delta_T/tau_m*exp((V-Vthreshold)/Delta_T) - w/Cm`
and `dw/dt = (a*(V-Vrest)-w)/tau_w`. Defaults are `Delta_T=2 mV`,
`tau_w=100 ms`, `a=0.02 mS/cm^2`, and `b=0.1 uA/cm^2`, with `w(0)=0` and
`V(0)=-65 mV`. For numerical stability, the production implementation caps
the exponential at `threshold + 5*Delta_T`; a spike resets voltage to `-65 mV`
and increments adaptation by `b`. The single-neuron tests use RK4 at
`dt=0.025 ms`. A 0.3 `uA/cm^2`, 20 ms subthreshold trace is compared at the
endpoint against a separately written SciPy DOP853 system (`rtol=1e-10`,
`atol=1e-12`) with `1e-7` absolute tolerance. Sustained 2 `uA/cm^2` input
checks adaptation by requiring successive inter-spike intervals to lengthen;
0.3, 1, 2, and 4 `uA/cm^2` checks increasing mean firing rate. The recorded
200 ms runs produced 0, 15, 50, and 100 Hz, respectively.

The AdEx form follows Brette and Gerstner, [Adaptive exponential
integrate-and-fire model as an effective description of neuronal activity
(2005)](https://doi.org/10.1152/jn.00686.2005). The comparisons here establish
implementation and numerical consistency for these fixtures; they do not
validate the defaults against a particular biological cell recording.
