"use client";
import { useState, useMemo, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import { api } from "../lib/data";
import Fallback from "./Fallback";
import type { SceneProps } from "./Scene";
const Scene = dynamic(() => import("./Scene"), { ssr: false });
type Point = {
  id: number;
  type: number;
  x: number;
  y: number;
  z: number;
  radius: number;
  parent: number;
};
export default function Morphology({ fallback }: { fallback: boolean }) {
  const [points, setPoints] = useState<Point[]>([]),
    [name, setName] = useState(""),
    [error, setError] = useState(""),
    [loading, setLoading] = useState(false),
    [selected, setSelected] = useState(0),
    [force2d, setForce2d] = useState(false);
  const generation = useRef(0);
  useEffect(
    () => () => {
      generation.current++;
    },
    [],
  );
  const geometry = useMemo(() => {
    const index = new Map(points.map((p, i) => [p.id, i]));
    const min = [0, 1, 2].map((axis) =>
        Math.min(...points.map((p) => [p.x, p.y, p.z][axis])),
      ),
      max = [0, 1, 2].map((axis) =>
        Math.max(...points.map((p) => [p.x, p.y, p.z][axis])),
      );
    const extent = Math.max(1, ...max.map((v, i) => v - min[i]));
    return {
      nodes: points.map((p, i) => ({
        id: i,
        kind: "SWC point",
        type: "passive",
        spike_count: 0,
      })),
      edges: points.flatMap((p, i) =>
        p.parent === -1
          ? []
          : [
              {
                id: i,
                source: index.get(p.parent)!,
                target: i,
                type: "axial",
                weight: 0,
                delay_ms: 0,
                directed: false,
              },
            ],
      ),
      positions: points.map(
        (p) =>
          [p.x, p.y, p.z].map(
            (v, i) => ((v - (min[i] + max[i]) / 2) * 18) / extent,
          ) as [number, number, number],
      ),
      min,
      max,
    };
  }, [points]);
  async function load(file?: File) {
    if (!file) return;
    const request = ++generation.current;
    setLoading(true);
    setError("");
    setPoints([]);
    try {
      if (file.size > 500000) throw new Error("SWC limit: 500 KB");
      const response = await api<{ points: Point[] }>("/morphology", {
        method: "POST",
        body: JSON.stringify({ text: await file.text() }),
      });
      if (request !== generation.current) return;
      setPoints(response.points);
      setName(file.name);
      setSelected(0);
    } catch (e) {
      if (request === generation.current) setError(String(e));
    } finally {
      if (request === generation.current) setLoading(false);
    }
  }
  const p = points[selected];
  const props: SceneProps = {
    ...geometry,
    selected,
    onSelect: setSelected,
    onHover: () => {},
    active: new Set(),
    rendererMode: "webgl2",
    onRenderer: () => {},
    focusToken: 0,
    onFailure: () => setForce2d(true),
    onMetrics: () => {},
  };
  return (
    <article className="morphology">
      <h2>Morphology explorer</h2>
      <p>
        Import a rooted SWC tree (≤5,000 points). Positions preserve SWC
        geometry; point markers have a fixed display radius. Exact radii are
        shown in the inspector. No voltage coloring: uploaded SWC points have no
        correspondence to simulated compartments.
      </p>
      <label>
        SWC file
        <input
          type="file"
          accept=".swc,text/plain"
          onChange={(e) => load(e.target.files?.[0])}
        />
      </label>
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
      {loading && <p>Validating morphology…</p>}
      {points.length > 0 && (
        <>
          <p data-testid="morphology-count">
            {name} · {points.length} points · {geometry.edges.length} parent
            links
          </p>
          <label>
            SWC point
            <select
              value={selected}
              onChange={(e) => setSelected(Number(e.target.value))}
            >
              {points.map((p, i) => (
                <option value={i} key={p.id}>
                  {p.id} · type {p.type}
                </option>
              ))}
            </select>
          </label>
          <p>
            ID {p.id} · parent {p.parent} · ({p.x}, {p.y}, {p.z}) µm · radius{" "}
            {p.radius} µm
          </p>
          <div className="viewport morphology-view">
            {fallback || force2d ? (
              <Fallback {...props} />
            ) : (
              <Scene {...props} />
            )}
          </div>
        </>
      )}
    </article>
  );
}
