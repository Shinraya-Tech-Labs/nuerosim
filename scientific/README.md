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
