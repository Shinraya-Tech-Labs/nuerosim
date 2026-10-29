# T022 validation evidence

- **Code revision:** `872e01a` (audit implementation; focused checks subsequently run at `5e178a2`).
- **Environment:** Windows 11, Python 3.14.2, NumPy 2.4.2.
- **Command:** `PYTHONPATH=python python -m pytest tests/test_hh_reference.py -q` — 7 passed in 0.78 s.
- **CLI:** valid reference fixture returned exit 0 and `passed: true`; invalid 37°C fixture is rejected.
- **Reference point:** 6.3°C and −65 mV; all six rates match the classic equations' independently calculated expected values exactly at float64 output precision. The three steady gates are m=0.05293248525724958, h=0.5961207535084603, n=0.3176769140606974.
- **Initialization cross-check:** production `initial_state` gates match the independently calculated rate-ratio gates with maximum absolute difference 0.0; maximum fixture rate/gate errors are 0.0 at tolerance 1e−12.
- **Limit:** this checks code equations and initialization only. It does not establish biological validity or temperature-dependent kinetics.
