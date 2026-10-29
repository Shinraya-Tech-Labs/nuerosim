# Stimulus pulse waveform library

Construct protocols and pass their `Pulse` objects directly to an experiment:

```python
from neurosim.stimuli import biphasic, pulse_train, single_step
from neurosim.workbench.config import Experiment

step = single_step(0, 5, 2)
train = pulse_train(0, 1, 3, 3, 2)
balanced = biphasic(10, 1, 2)
experiment = Experiment(model="lif", duration=20, pulses=train)
```

The library provides a single rectangular step, a non-overlapping train (interval measured start-to-start), and an equal-width biphasic pair. Times use ms and amplitudes µA/cm². The simulator config still enforces timestep alignment, target bounds, and simulation duration.

Biphasic net charge is zero only for the ideal requested waveform; this does not describe electrode delivery or guarantee a biological effect. See the [contract](contracts/T017-stimulus-pulse-waveform-library.md) and [validation evidence](evidence/T017-stimulus-pulse-waveform-library.md).
