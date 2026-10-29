# LIF exact reference solution

Run the subthreshold exact-reference comparison through the production LIF simulator:

```sh
PYTHONPATH=python python -m neurosim.lif_exact_reference tests/fixtures/omega/T024-lif-exact-reference-solution/valid.json --output lif-reference.json
```

The tool compares exact and production voltages at each recorded time and includes the production manifest in its report. It exits 0 when maximum error and fixture reference values pass, 1 for numeric mismatch, and 2 for invalid input. It accepts one LIF neuron with piecewise constant current pulses and rejects trajectories that reach threshold because reset behavior is outside this exact solution.

See the [contract](contracts/T024-lif-exact-reference-solution.md), [validation evidence](evidence/T024-lif-exact-reference-solution.md), and [Day 02 report](DAY_02_REPORT.md).
