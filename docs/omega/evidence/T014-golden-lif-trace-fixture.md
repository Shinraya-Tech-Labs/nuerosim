# T014 validation evidence

## Analytic trace comparison

At code revision `bb976f4`, the actual single-neuron LIF engine was audited against `V(t) = -65 + 4(1 - exp(-t/20))` mV at 0, 5, 10, 15, and 20 ms. The maximum absolute error was **2.13×10⁻¹⁴ mV**, below the **1×10⁻⁹ mV** tolerance. The run produced zero spikes and returned the config hash `6f5bed5b814502c6b77a662d9e05ce0c84fd104ada46390b11b91abb9f7fbf55`.

The focused test file passed (9 passed), including invalid units, unequal arrays, off-grid/unsorted times, tolerance failure, and a spiking run that violates the subthreshold contract. Environment: Windows 11, Python 3.14.2, NumPy 2.4.2.

## Limits

This checks one subthreshold configuration against an analytic RC response. It does not test LIF spike/reset dynamics or validate the model biologically.
