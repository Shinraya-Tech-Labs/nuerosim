import { expect, test } from "@playwright/test";
import valid from "../../../tests/fixtures/omega/T009-ui-renderer-contract-audit/valid.json" with {
  type: "json",
};
import invalid from "../../../tests/fixtures/omega/T009-ui-renderer-contract-audit/invalid.json" with {
  type: "json",
};

test("T009 UI renderer contract selects WebGL2 and falls back to 2D", async ({
  page,
  request,
}) => {
  test.setTimeout(120000);
  const created = await request.post("/api/experiments", {
    data: { model: "lif", n: 2, duration: 1, probability: 0, pulses: [] },
  });
  expect(created.status()).toBe(202);
  const job = await created.json();
  await expect
    .poll(
      async () =>
        (await (await request.get(`/api/experiments/${job.id}`)).json()).status,
    )
    .toBe("completed");

  await page.goto(`/?experiment=${job.id}`);
  await expect(page.locator("canvas")).toBeVisible();
  await expect(page.locator(".renderer-badge")).toContainText(
    valid.expected.renderer_label_contains,
  );
  await page.getByLabel("Rendering backend").selectOption("webgl2");
  await expect(page.locator(".renderer-badge")).toContainText("WebGL2");
  await page.getByLabel("Rendering backend").selectOption("auto");
  await expect(page.locator(".renderer-badge")).toContainText("WebGL2");

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
  await expect(page.locator(".renderer-badge")).toContainText(
    invalid.expected.renderer_label_contains,
  );
});
