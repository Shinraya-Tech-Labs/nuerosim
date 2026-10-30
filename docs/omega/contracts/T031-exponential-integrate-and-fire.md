# T031 — exponential integrate-and-fire

Add the EIF voltage equation to the production workbench: LIF leak/current terms plus the existing capped exponential `Delta/tau_m * exp((V-threshold)/Delta)`. Threshold is the reset threshold; the numerical exponential cutoff is threshold+5 Delta. Parameters use mV, ms, µA/cm² and µF/cm². Deterministic pulses run through the usual Experiment and result manifest. This model is a numerical EIF variant, not a biological fit.
