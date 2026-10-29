# T026 validation evidence

- **Code revision:** `dbff942` (audit implementation; focused checks at `5b115ff`).
- **Environment:** Windows 11, Python 3.14.2, NumPy 2.4.2; production backend `cpu-float64`.
- **Command:** `PYTHONPATH=python python -m pytest tests/test_refractory_audit.py -q` — 4 passed in 1.40 s.
- **Reference run:** LIF dt 0.025 ms, refractory 2 ms, 20 µA/cm² pulse on [0,20) ms; first spike at 0.775 ms and subsequent intervals are 2.775 ms.
- **Schedule check:** minimum observed interval 2.775 ms exceeds the configured refractory period; 2 ms corresponds to 80 integration steps. Persisted output includes all spike intervals and the production manifest.
- **Limit:** intervals also include the time needed to recharge to threshold; this audit checks the refractory lower bound, not exact spike-time accuracy.
