import { test, expect } from "@playwright/test";
import { writeFileSync } from "node:fs";

test("profile the 512-neuron network at balanced and full edge density", async ({
  page,
  request,
  browser,
}, testInfo) => {
  test.setTimeout(300000);
  const response = await request.post("/api/experiments", {
    data: {
      name: "Redesign renderer benchmark 512",
      model: "lif",
      n: 512,
      probability: 0.08,
      duration: 1,
      pulses: [],
      seed: 42,
    },
  });
  expect(response.status()).toBe(202);
  const job = await response.json();
  await expect
    .poll(
      async () =>
        (await (await request.get(`/api/experiments/${job.id}`)).json()).status,
      { timeout: 90000 },
    )
    .toBe("completed");
  const topology = await (
    await request.get(`/api/experiments/${job.id}/topology`)
  ).json();
  await page.goto(`/?experiment=${job.id}`);
  await expect(page.getByTestId("counts")).toContainText("512 / 512 neurons");
  await expect(page.locator(".renderer-badge")).toContainText(/WebGPU|WebGL2/);

  const measurements = [];
  for (const mode of ["auto", "webgl2"]) {
    await page.getByLabel("Rendering backend").selectOption(mode);
    await expect(page.locator(".renderer-badge")).toContainText(
      /WebGPU|WebGL2/,
    );
    for (const budget of [2048, 32768]) {
      await page.getByLabel("Edge display budget").selectOption(String(budget));
      const shown = Math.min(budget, topology.total_edges);
      await expect(page.getByTestId("counts")).toContainText(
        `${shown.toLocaleString()} / ${topology.total_edges.toLocaleString()} lines`,
      );
      await page.waitForTimeout(1800);
      const samples = [];
      for (let i = 0; i < 3; i++) {
        samples.push(await page.getByTestId("performance").textContent());
        if (i < 2) await page.waitForTimeout(1100);
      }
      measurements.push({
        neurons: topology.nodes.length,
        savedEdges: topology.total_edges,
        visibleEdges: shown,
        edgeBudget: budget,
        config_sha256: topology.config_sha256,
        requestedRenderer: mode,
        activeRenderer: await page.locator(".renderer-badge").textContent(),
        samples,
      });
      if (budget === 2048 && mode === "auto")
        await page.screenshot({
          path: "../docs/validation/web-network-512-auto.png",
        });
      if (budget === 32768 && mode === "webgl2")
        await page.screenshot({
          path: "../docs/validation/web-network-512-redesign.png",
        });
    }
  }
  await page.getByLabel("Toggle adaptive density").click();
  const visibleCount = async () => {
    const text = (await page.getByTestId("counts").textContent()) || "";
    const match = text.match(/·\s*([\d,]+) \/ [\d,]+ lines/);
    return match ? Number(match[1].replaceAll(",", "")) : topology.total_edges;
  };
  await expect
    .poll(visibleCount, { timeout: 30000 })
    .toBeLessThan(topology.total_edges);
  await page.waitForTimeout(3500);
  measurements.push({
    neurons: topology.nodes.length,
    savedEdges: topology.total_edges,
    visibleEdges: await visibleCount(),
    edgeBudget: "adaptive",
    requestedRenderer: "webgl2",
    activeRenderer: await page.locator(".renderer-badge").textContent(),
    samples: [await page.getByTestId("performance").textContent()],
  });
  writeFileSync(
    "../docs/validation/web-render-benchmark-redesign.json",
    JSON.stringify(
      {
        date: new Date().toISOString(),
        browser: browser.version(),
        environment:
          "Headless Chromium, local Next development server, 1440×1000. Renderer is read from Three.js's initialized backend; JS heap and frame metrics are reported when the browser exposes them. No physical GPU result is implied.",
        measurements,
      },
      null,
      2,
    ),
  );
});
