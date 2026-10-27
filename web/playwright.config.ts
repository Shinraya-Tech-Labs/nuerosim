import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/e2e",
  workers: 1,
  expect: { timeout: 30000 },
  use: {
    baseURL: "http://127.0.0.1:3011",
    viewport: { width: 1440, height: 1000 },
  },
  webServer: [
    {
      command: `${process.env.NEUROSIM_TEST_PYTHON || (process.platform === "win32" ? "..\\.venv\\Scripts\\python.exe" : "../.venv/bin/python")} -m uvicorn neurosim.workbench.api:app --host 127.0.0.1 --port 8011`,
      url: "http://127.0.0.1:8011/health",
      env: {
        PYTHONPATH: "../python",
        NEUROSIM_DB: `../neurosim-data/web-e2e-${Date.now()}.db`,
      },
      reuseExistingServer: false,
      timeout: 30000,
    },
    {
      command: "npm run dev -- --port 3011",
      url: "http://127.0.0.1:3011",
      env: {
        NEUROSIM_API_URL: "http://127.0.0.1:8011",
        NEXT_DIST_DIR: ".next-e2e",
        NEXT_TELEMETRY_DISABLED: "1",
      },
      reuseExistingServer: false,
      timeout: 240000,
    },
  ],
  timeout: 60000,
});
