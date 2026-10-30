# T040 — stochastic LIF seeded noise

Add reproducible Gaussian current noise controlled by Experiment.seed and Parameters.noise_std. A fixed seed must produce identical traces and manifests; different seeds may differ. Noise is current density with a per-step standard deviation scaled by sqrt(dt). This is a seeded numerical perturbation, not a calibrated channel-noise model.
