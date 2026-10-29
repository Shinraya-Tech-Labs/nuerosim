# T009 — UI renderer contract audit

## Purpose

Verify the renderer selection and failure behavior exposed by the 3D workbench UI without claiming hardware performance or scientific validity from rendering output.

## Contract

- **Input:** browser runtime with the workbench loaded; controllable renderer capabilities and WebGL context creation for deterministic boundary checks.
- **Output:** active renderer label, whether the 3D scene or 2D fallback is active, and whether selection/fallback actions remain usable.
- **Units:** no scientific units; viewport dimensions are CSS pixels and frame metrics are frames/second and milliseconds.
- **Selection:** auto mode requests a WebGPU adapter when `navigator.gpu` is available, initializes WebGPU when supported, and otherwise uses WebGL2. Explicit WebGL2 mode must label the backend. A WebGL2 creation/context failure must switch to the supported 2D view.
- **Acceptance examples:** auto mode without WebGPU reports WebGL2; explicit WebGL2 reports WebGL2; unavailable WebGL2 activates 2D fallback and leaves the workspace operable.
- **Errors:** renderer initialization or context-loss failures are surfaced through the fallback UI; no false WebGPU label is permitted.
- **Evidence:** browser test outcomes and the actual initialized renderer label. Performance values are environment-specific and not acceptance thresholds.
- **Exclusions:** this audit does not establish WebGPU behavior on physical hardware, GPU performance, visual/scientific correctness of the scene, accessibility of all controls, or support for every browser/device.
