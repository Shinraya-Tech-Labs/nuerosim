# T009 validation evidence

## Browser contract results

At code revision `e75ac82`, the focused Playwright audit created and loaded a real completed two-neuron LIF experiment. In this headless Chromium environment, auto mode reported WebGL2 because WebGPU was unavailable. Explicit WebGL2 selection also reported WebGL2. After WebGL context creation was denied on reload, the UI rendered the accessible 2D connectivity view, labeled it `2D canvas`, and still allowed neuron selection.

Command: `npx playwright test tests/e2e/renderer-contract.spec.ts` from `web/`. Result: 1 passed in 9.9 seconds. Browser emitted the known Three.js Clock deprecation and WebGL context failure diagnostic used to verify fallback.

## Limits

This validates renderer selection and the WebGL-unavailable fallback in headless Chromium only. It does not validate physical GPU/WebGPU rendering or performance, and it does not assert visual or scientific validity of the rendered layout.
