# T025 validation evidence

- **Code revision:** `905111b` (audit implementation; focused checks run at `cf9f889`).
- **Environment:** Windows 11, Python 3.14.2, NumPy 2.4.2; production backend `cpu-float64`.
- **Command:** `PYTHONPATH=python python -m pytest tests/test_adex_threshold_audit.py -q` — 5 passed in 1.56 s.
- **Reference run:** threshold −50 mV and Delta 2 mV derive the numerical cutoff −40 mV. With 50 µA/cm² on [1,10) ms and adaptation disabled, production reports spikes at 1.5, 4.0, 6.5, and 9.0 ms.
- **High-drive edge:** a 100 µA/cm² pulse remained finite under the capped exponential and produced four reset events at 1.25, 3.5, 5.75, and 8.0 ms.
- **Integration:** output includes production manifest, spike intervals, count, final voltage, and cutoff; CLI persistence is checked.
- **Limit:** the `threshold+5*Delta` cutoff is numerical stabilization, not a biological threshold. Spike timing depends on this dt/configuration.
