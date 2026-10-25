import { test, expect } from "@playwright/test";
test("real saved topology renders, filters, and reloads", async ({
  page,
  request,
}) => {
  test.setTimeout(120000);
  const created = await request.post("/api/experiments", {
    data: {
      model: "lif",
      n: 32,
      probability: 0.25,
      duration: 2,
      pulses: [{ start: 0, stop: 2, amplitude: 20, target: 0 }],
    },
  });
  expect(created.status()).toBe(202);
  const job = await created.json();
  await expect
    .poll(
      async () =>
        (await (await request.get(`/api/experiments/${job.id}`)).json()).status,
    )
    .toBe("completed");
  const topology = await (
    await request.get(`/api/experiments/${job.id}/topology`)
  ).json();
  await page.goto(`/?experiment=${job.id}`);
  await expect(page.getByTestId("counts")).toHaveText(
    `32 / 32 neurons · ${topology.total_edges} / ${topology.total_edges} lines`,
  );
  await expect(page.locator("canvas")).toBeVisible();
  await expect(page.getByText(/WebGPU|WebGL2/).first()).toBeVisible();
  const result = await (
    await request.get(`/api/experiments/${job.id}/results`)
  ).json();
  const eventCount = result.spikes.flat().length;
  expect(eventCount).toBeGreaterThan(0);
  await expect(page.getByTestId("event-count")).toHaveText(
    `${eventCount} SPIKES`,
  );
  await expect(page.getByTestId("voltage-path")).toHaveAttribute(
    "d",
    new RegExp(`^M50,${140 - (result.voltage[0][0] + 80) * 0.8}`),
  );
  const spike = result.spikes[0][0];
  await page.getByLabel("Simulation timeline").fill(String(spike));
  await expect(page.getByTestId("cursor-time")).toHaveText(
    `${spike.toFixed(3)} ms`,
  );
  await expect(page.getByTestId("plot-cursor")).toHaveAttribute(
    "x1",
    String(50 + (spike / 2) * 900),
  );
  const raster = await page.getByTestId("raster-path").getAttribute("d");
  await page.getByLabel("Rendering backend").selectOption("webgl2");
  await expect(page.locator(".renderer-badge")).toContainText("WebGL2");
  await page.getByLabel("Rendering backend").selectOption("auto");
  await expect(page.locator(".renderer-badge")).toContainText(/WebGPU|WebGL2/);
  await page
    .getByLabel(
      "Interactive 3D neural connectivity view. Use arrow keys to select neurons.",
    )
    .focus();
  await page.keyboard.press("ArrowRight");
  await expect(page.getByLabel("Selected neuron", { exact: true })).toHaveValue(
    "1",
  );
  await page.getByLabel("Selected neuron", { exact: true }).selectOption("0");
  await page.screenshot({
    path: "../docs/validation/web-3d-redesign.png",
  });
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(
    page.getByRole("button", { name: "Expand experiment sidebar" }),
  ).toBeVisible();
  await expect(page.locator("canvas")).toBeVisible();
  await page.screenshot({
    path: "../docs/validation/web-mobile-redesign.png",
  });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page
    .getByRole("region", { name: "Neural network workspace" })
    .getByLabel("Connection type", { exact: true })
    .selectOption("inhibitory");
  await expect(page.getByTestId("counts")).toContainText(
    `${topology.edges.filter((e: { type: string }) => e.type === "inhibitory").length} / ${topology.total_edges} lines`,
  );
  await page.reload();
  await expect(page.getByTestId("counts")).toHaveText(
    `32 / 32 neurons · ${topology.total_edges} / ${topology.total_edges} lines`,
  );
  await expect(page.getByTestId("cursor-time")).toHaveText("0.000 ms");
  await expect(page.getByTestId("raster-path")).toHaveAttribute("d", raster!);
  await page.getByLabel("Simulation timeline").fill(String(spike));
  await expect(page.getByTestId("plot-cursor")).toHaveAttribute(
    "x1",
    String(50 + (spike / 2) * 900),
  );
  await page.getByLabel("Playback speed").selectOption("100");
  await page.getByLabel("Play recorded activity").click();
  await expect(page.getByTestId("cursor-time")).toHaveText("2.000 ms");
  const other = await (
    await request.post("/api/experiments", {
      data: { model: "lif", duration: 1, pulses: [], initial_voltage: -60 },
    })
  ).json();
  await expect
    .poll(
      async () =>
        (await (await request.get(`/api/experiments/${other.id}`)).json())
          .status,
    )
    .toBe("completed");
  await expect(
    page
      .getByLabel("Comparison experiment")
      .locator(`option[value="${other.id}"]`),
  ).toBeAttached();
  await page.getByLabel("Comparison experiment").selectOption(other.id);
  await expect(page.getByTestId("comparison-path")).toHaveAttribute(
    "d",
    /^M50,124 /,
  );
  const exportEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export plots as SVG" }).click();
  const download = await exportEvent;
  expect(download.suggestedFilename()).toBe("neurosim-signals.svg");
  await download.saveAs("../docs/validation/neurosim-signals.svg");
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (
      this: HTMLCanvasElement,
      type: string,
      ...args: unknown[]
    ) {
      if (type.startsWith("webgl")) return null;
      return Reflect.apply(original, this, [type, ...args]);
    } as typeof original;
  });
  await page.reload();
  await expect(
    page.getByRole("img", { name: "2D network connectivity" }),
  ).toBeVisible();
  await page.getByLabel("SWC file").setInputFiles("../examples/branched.swc");
  await expect(page.getByTestId("morphology-count")).toContainText(
    "parent links",
  );
  await page.screenshot({
    path: "../docs/validation/web-fallback-redesign.png",
  });
});

test("configuration submits a real job and reports validation failures", async ({
  page,
}) => {
  test.setTimeout(120000);
  await page.goto("/");
  await page.getByText("New simulation", { exact: true }).click();
  await page.getByLabel("Experiment configuration").fill('{"model":"invalid"}');
  await page.getByRole("button", { name: "Run CPU simulation" }).click();
  await expect(page.locator("main [role=alert]")).toContainText("422");
  await page.getByLabel("Experiment configuration").fill(
    JSON.stringify({
      model: "lif",
      n: 2,
      duration: 1,
      pulses: [],
      probability: 0,
    }),
  );
  await page.getByRole("button", { name: "Run CPU simulation" }).click();
  await expect(page.getByTestId("counts")).toHaveText(
    "2 / 2 neurons · 0 / 0 lines",
  );
  await page.getByLabel("SWC file").setInputFiles({
    name: "invalid.swc",
    mimeType: "text/plain",
    buffer: Buffer.from("1 1 0 0 0 -1 -1"),
  });
  await expect(page.locator("main [role=alert]")).toContainText("invalid");
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(
    page.getByRole("button", { name: "Expand experiment sidebar" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "LIF NETWORK" }),
  ).toBeVisible();
});
