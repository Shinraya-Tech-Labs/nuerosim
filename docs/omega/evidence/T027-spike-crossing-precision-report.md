# T027 validation evidence

- Code revision: `12b0d3a`; focused test suite passed 4 tests (Windows/Python 3.14.2/NumPy 2.4.2).
- HH fixture: dt=0.025 ms, every step recorded; two upward 0 mV crossings are interpolated from production voltage samples.
- Endpoint times: 11.925 and 26.825 ms. Linear estimates: 11.901300985428811 and 26.822719207241708 ms. Both offsets lie within one dt.
- Limit: linear interpolation over one numerical step is an estimate, not a continuous-time exact solution.
