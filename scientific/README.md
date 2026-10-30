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
