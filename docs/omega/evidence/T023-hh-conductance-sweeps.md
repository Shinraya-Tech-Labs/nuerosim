# T023 validation evidence

- **Code revision:** `405acd8` (sweep mechanism; focused checks run at `16d194d`).
- **Environment:** Windows 11, Python 3.14.2, NumPy 2.4.2; production backend `cpu-float64`.
- **Command:** `PYTHONPATH=python python -m pytest tests/test_hh_conductance_sweep.py -q` — 5 passed in 5.95 s.
- **CLI:** valid fixture returned exit 0. `--output` persisted the JSON report, including each production manifest and its swept `g_na` value.
- **Sweep:** 50 ms, 0.025 ms RK4, 10 µA/cm² from 10–40 ms; `g_na` 60/120/180 mS/cm² produced 1/2/3 spikes at 12.65 ms; 11.925/26.825 ms; and 11.675/25.025/38.15 ms, respectively.
- **Final voltages:** −65.63596520061942, −65.44700087955275, and −68.23661771872393 mV; all match the checked-in fixture within 1e−9 mV.
- **Limit:** this is a small deterministic sensitivity example. Spike-count trends depend on the fixed experiment and are not a universal biological or monotonicity claim.
