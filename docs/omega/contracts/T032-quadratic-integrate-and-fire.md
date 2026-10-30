# T032 — quadratic integrate-and-fire

The workbench QIF variant integrates `dV/dt=(V-rest)(V-threshold)/tau_m + I/cm` with configured reset and absolute refractory scheduling. Units are mV, ms and µA/cm². The numerical spike event is an upward crossing of configured threshold. This parameterized implementation is not a canonical dimensionless QIF fit and does not establish biological fidelity.
