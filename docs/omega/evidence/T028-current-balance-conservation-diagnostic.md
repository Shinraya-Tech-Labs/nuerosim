# T028 validation evidence

- **Code revision:** `7e04e18`; focused checks at the completed T028 test commit.
- **Environment:** Windows 11, Python 3.14.2, NumPy 2.4.2.
- **Command:** `PYTHONPATH=python python -m pytest tests/test_current_balance.py -q` — 4 passed in 1.58 s.
- **Reference:** cable voltages [−65,−55,−75] mV with axial=0.1 mS/cm² produced [1,−3,2] µA/cm². The fsum net is exactly 0.
- **Limit:** this audits the production cable axial-current helper only; membrane leak and external currents need not conserve charge.
