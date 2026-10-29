# T029 validation evidence

- Code: `python/neurosim/time_grid_audit.py`; environment Windows 11, Python 3.14.2, NumPy 2.4.2.
- Focused command: `PYTHONPATH=python python -m pytest tests/test_time_grid_audit.py -q` — 3 passed.
- One millisecond at dt=0.025 ms produced 41 integration steps and 11 recorded samples at indices 0,4,…,40, including the final 1 ms endpoint.
- Reported maximum grid error is below 1e−12 ms. This checks sampling convention, not solver accuracy.
