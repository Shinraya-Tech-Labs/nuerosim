# UI renderer contract audit

Run the browser contract audit from the web project:

```sh
cd web
npx playwright test tests/e2e/renderer-contract.spec.ts
```

The audit creates a real completed LIF experiment, checks auto and explicit WebGL2 labels, then blocks WebGL context creation and checks the accessible 2D fallback and neuron selection. It uses the existing API and UI rather than simulated experiment output.

The contract covers renderer selection and fallback behavior. A passing headless browser test does not establish physical GPU performance, WebGPU behavior, scientific validity of the visualization, or support across every device.

See the [contract](contracts/T009-ui-renderer-contract-audit.md) and [validation evidence](evidence/T009-ui-renderer-contract-audit.md).
