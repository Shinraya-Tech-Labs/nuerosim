# T016 validation evidence

## Conversion and real-result integration

At code revision `31812b1`, the fixture checks conversions across the supported dimensions: 1000 ms → 1 s, 1 V → 1000 mV, 1 mA/cm² → 1000 µA/cm², 1 S/cm² → 1000 mS/cm², 1 F/cm² → 1,000,000 µF/cm², and 1 kHz → 1000 Hz. The population-rate example computes 2 spikes / 1 neuron / 1 second as **2 Hz**.

The existing scientific units audit now uses `Quantity` to convert manifest duration from ms to s and compute the stored mean rate. A real LIF run produced a rate matching the typed result. The focused unit and integration tests passed (15 passed).

## Limits

These are runtime wrappers and explicit conversions; stored experiment/API values remain ordinary numeric fields in ms and mV. The primitives do not implement general dimensional algebra or prove static type safety.
