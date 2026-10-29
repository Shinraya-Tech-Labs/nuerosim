# T020 validation evidence

## Reference precision and RK4 comparison

At code revision `87d723d`, the fixed 20 ms HH experiment was sampled every 0.1 ms (201 samples). DOP853 at `rtol=1e-8`, voltage `atol=1e-10 mV` differed from `rtol=1e-11`, voltage `atol=1e-13 mV` by at most **9.9613e-6 mV**. Production RK4 at 0.025 ms differed from the tighter reference by at most **0.00571947 mV**. Both values were within their 0.001 mV and 0.02 mV limits, respectively.

The focused test file passed (10 passed). Environment: Windows 11, Python 3.14.2, NumPy 2.4.2. The result includes the actual RK4 manifest; adaptive tolerances are recorded separately for voltage and the reference uses fixed `1e-12` absolute tolerance for gating states.

## Limits

This checks reference tolerance sensitivity and RK4 error for one smooth constant-current trace. It does not generalize to discontinuous stimuli, other parameter sets, or biological validity.
