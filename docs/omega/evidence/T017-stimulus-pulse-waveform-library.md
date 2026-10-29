# T017 validation evidence

## Protocol values and simulation integration

At code revision `614dce2`, a three-pulse train generated `[0,1)`, `[3,4)`, and `[6,7)` ms intervals at 2 µA/cm². Its three pulses appeared unchanged in the real LIF experiment manifest. The run ended at **−62.35056 mV** versus **−65 mV** with no pulses, and produced zero spikes. A 1 ms/phase ±2 µA/cm² biphasic command had ideal net charge **0 µA·ms/cm²**.

The focused test file passed (10 passed), covering exact protocol values, ideal charge balance, real simulation integration, overlap rejection, pulse count/amplitude bounds, and invalid arguments. Environment: Windows 11, Python 3.14.2.

## Limits

Charge balance is an ideal command calculation. The library does not model electrode impedance, hardware delivery, or biological response beyond passing `Pulse` objects to the existing simulator.
