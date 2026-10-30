# T030 — solver selection UX

Add an explicit solver selector to the validated CPU experiment editor. Solver names match the `Experiment` schema: RK4 and forward Euler. Selection updates the JSON configuration submitted to the existing experiment API; no numerical behavior is inferred from labels.

- Input/output: `solver` is `rk4` or `euler`; dt remains in ms and model-specific bounds remain enforced by the backend.
- Default: RK4 when no solver is present.
- Invalid JSON cannot be safely edited by the control and produces a visible error; the textarea remains available for direct editing.
- This control selects an integrator; it does not claim one solver is universally more accurate or appropriate.
