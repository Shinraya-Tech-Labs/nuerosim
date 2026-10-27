import { test, expect } from "@playwright/test";

test("saved exhibition order, navigation, and paired reload", async ({
  page,
  request,
}) => {
  test.setTimeout(120000);
  async function run(name: string, config: Record<string, unknown>) {
    const response = await request.post("/api/experiments", {
      data: { name, ...config },
    });
    expect(response.status()).toBe(202);
    const id = (await response.json()).id as string;
    await expect
      .poll(
        async () =>
          (await (await request.get(`/api/experiments/${id}`)).json()).status,
      )
      .toBe("completed");
    return id;
  }
  const first = await run("EX 01 — Two Connected Neurons", {
    model: "lif",
    n: 2,
    probability: 0.5,
    inhibitory_fraction: 0,
    weight: 0.5,
    seed: 2,
    duration: 20,
    pulses: [{ target: 0, start: 0, stop: 20, amplitude: 20 }],
  });
  const second = await run("EX 02 — Full Neural Network", {
    model: "lif",
    n: 32,
    probability: 0.1,
    duration: 1,
    pulses: [],
  });
  const third = await run("EX 03 — Hodgkin–Huxley Action Potential", {
    model: "hh",
    n: 1,
    duration: 50,
    dt: 0.025,
    pulses: [{ target: 0, start: 10, stop: 40, amplitude: 10 }],
  });
  const pulse = (amplitude: number) => ({
    model: "lif",
    n: 1,
    duration: 50,
    dt: 0.025,
    probability: 0,
    pulses: [{ target: 0, start: 10, stop: 40, amplitude }],
  });
  const reference = await run(
    "EX 04 — Stimulus Comparison · 8 µA/cm²",
    pulse(8),
  );
  const changed = await run(
    "EX 04 — Stimulus Comparison · 12 µA/cm²",
    pulse(12),
  );
  for (const [slot, job_id, reference_id] of [
    [1, first, null],
    [2, second, null],
    [3, third, null],
    [4, changed, reference],
  ] as const) {
    expect(
      (
        await request.post(`/api/exhibition/${slot}`, {
          data: { job_id, reference_id },
        })
      ).ok(),
    ).toBeTruthy();
  }
  const saved = await (
    await request.get("/api/experiments/" + first + "/topology")
  ).json();
  expect(saved.nodes).toHaveLength(2);
  expect(saved.edges).toHaveLength(1);
  expect(saved.edges[0]).toMatchObject({
    source: 0,
    target: 1,
    type: "excitatory",
  });
  await page.goto("/");
  await expect(page.getByTestId("counts")).toHaveText(
    "2 / 2 neurons · 1 / 1 lines",
  );
  const picker = page.getByLabel("Saved experiment");
  await expect(picker.locator("optgroup").first()).toHaveAttribute(
    "label",
    "EXHIBITION EXPERIMENTS",
  );
  await expect(picker.locator("optgroup").first().locator("option")).toHaveText(
    [
      "EX 01 — Two Connected Neurons",
      "EX 02 — Full Neural Network",
      "EX 03 — Hodgkin–Huxley Action Potential",
      "EX 04 — Stimulus Comparison",
    ],
  );
  await expect(page.getByTestId("performance")).toContainText("FPS");
  await page.screenshot({ path: "../docs/validation/exhibition-history.png" });
  await page.getByRole("button", { name: /Next: EX 02/ }).click();
  await expect(page.getByTestId("counts")).toContainText("32 / 32 neurons");
  await picker.selectOption(third);
  await expect(page.getByTestId("voltage-path")).toBeVisible();
  await picker.selectOption(changed);
  await expect(
    page.getByText(`Comparing neuron 0 from ${reference.slice(0, 8)}`),
  ).toBeVisible();
  await page.locator(".analysis-dock").screenshot({
    path: "../docs/validation/exhibition-comparison.png",
  });
  await page.reload();
  await expect(picker).toHaveValue(changed);
  await expect(
    page.getByText(`Comparing neuron 0 from ${reference.slice(0, 8)}`),
  ).toBeVisible();
});
