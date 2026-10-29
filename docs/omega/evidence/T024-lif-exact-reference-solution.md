# T024 validation evidence

- **Code revision:** `6a85c48` (exact reference implementation; focused tests run at `acfcfb1`).
- **Environment:** Windows 11, Python 3.14.2, NumPy 2.4.2; production backend `cpu-float64`.
- **Command:** `PYTHONPATH=python python -m pytest tests/test_lif_exact_reference.py -q` — 5 passed in 1.29 s.
- **CLI/persistence:** valid fixture passes and `--output` writes the exact and production traces with the production manifest.
- **Reference:** rest −65 mV, tau 20 ms, capacitance 1 µF/cm², 0.5 µA/cm² pulse on [5,15) ms. Closed form gives −61.06530659712634 mV at 15 ms and −61.9356576966961 mV at 20 ms.
- **Numerical comparison:** production RK4 final sample −61.935657696696126 mV; max absolute error over all recorded samples is below the fixture tolerance 1e−8 mV.
- **Negative case:** a pulse that reaches threshold is rejected before reporting an exact subthreshold comparison.
- **Limit:** reset discontinuities, threshold crossing, multi-neuron/network coupling, and biological validation are excluded.
