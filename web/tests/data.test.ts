import { describe, it, expect } from "vitest";
import {
  positions,
  visibleEdges,
  activeAt,
  edgePositions,
  rates,
} from "../lib/data";
describe("scientific display projections", () => {
  it("builds each segment from the saved source and target coordinates", () => {
    const coordinates: [number, number, number][] = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ];
    expect(edgePositions(edges, coordinates)).toEqual([
      1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3,
    ]);
  });
  it("normalizes spike count by population and time, including endpoint spikes", () => {
    const bins = rates(
      [
        { neuron_id: 0, time_ms: 0 },
        { neuron_id: 1, time_ms: 10 },
      ],
      10,
      2,
      2,
    );
    expect(bins.map((b) => b.hz)).toEqual([100, 100]);
  });
  it("bounds display without creating edges", () => {
    expect(visibleEdges(edges, 3, 0, "all", 0, null, 1)).toEqual([]);
    expect(visibleEdges(edges, 3, 1, "all", 0, null, 1)).toEqual([edges[0]]);
    expect(visibleEdges(edges, 3, 2, "all", 0, 2, 1)).toEqual([edges[1]]);
  });
  const edges = [
    {
      id: 0,
      source: 0,
      target: 1,
      type: "excitatory",
      weight: 0.05,
      delay_ms: 1,
      directed: true,
    },
    {
      id: 1,
      source: 2,
      target: 0,
      type: "inhibitory",
      weight: 0.05,
      delay_ms: 1,
      directed: true,
    },
  ];
  it("preserves saved edge identity and endpoints across filters", () => {
    expect(visibleEdges(edges, 3, 10, "all", 0, null, 1)).toEqual(edges);
    expect(visibleEdges(edges, 3, 10, "inhibitory", 0, null, 1)).toEqual([
      edges[1],
    ]);
    expect(visibleEdges(edges, 2, 10, "all", 0, null, 1)).toEqual([edges[0]]);
    expect(visibleEdges(edges, 3, 10, "all", 0.1, null, 1)).toEqual([]);
  });
  it("provides deterministic finite coordinates without changing connectivity", () => {
    expect(positions(2, "columns")).toEqual([
      [-3, 0, 0],
      [3, 0, 0],
    ]);
    for (const layout of ["columns", "sphere", "grid"] as const) {
      expect(positions(512, layout)).toEqual(positions(512, layout));
      expect(positions(512, layout).flat().every(Number.isFinite)).toBe(true);
    }
  });
  it("highlights only recorded spikes at or before the cursor", () => {
    const events = [
      { time_ms: 2, neuron_id: 0 },
      { time_ms: 5, neuron_id: 1 },
    ];
    expect([...activeAt(events, 1)]).toEqual([]);
    expect([...activeAt(events, 2)]).toEqual([0]);
    expect([...activeAt(events, 4)]).toEqual([]);
    expect([...activeAt(events, 5)]).toEqual([1]);
    expect([...activeAt(events, 2)]).toEqual([0]);
  });
});
