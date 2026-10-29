export type Node = {
  id: number;
  kind: string;
  type: string;
  spike_count: number;
};
export type Edge = {
  id: number;
  source: number;
  target: number;
  type: string;
  weight: number;
  delay_ms: number;
  directed: boolean;
};
export type Topology = {
  nodes: Node[];
  edges: Edge[];
  total_edges: number;
  model: string;
  duration_ms: number;
  dt_ms: number;
  config_sha256: string;
};
export type Event = { time_ms: number; neuron_id: number };
export type Trace = { t: number[]; voltage: number[] };
export async function activity(
  id: string,
  signal: AbortSignal,
): Promise<Event[]> {
  let offset: number | null = 0;
  const events: Event[] = [];
  while (offset !== null) {
    const page: {
      events: Event[];
      next_offset: number | null;
      total_events: number;
    } = await api(`/experiments/${id}/activity?offset=${offset}`, { signal });
    if (page.total_events > 200000)
      throw new Error(
        "Playback budget: more than 200,000 spikes. Export the full data or record a shorter experiment.",
      );
    events.push(...page.events);
    offset = page.next_offset;
  }
  return events;
}
export async function trace(
  id: string,
  neuron: number,
  signal: AbortSignal,
): Promise<Trace> {
  let offset: number | null = 0;
  const result: Trace = { t: [], voltage: [] };
  while (offset !== null) {
    const page: Trace & { next_offset: number | null } = await api(
      `/experiments/${id}/voltage?neuron=${neuron}&offset=${offset}`,
      { signal },
    );
    result.t.push(...page.t);
    result.voltage.push(...page.voltage);
    offset = page.next_offset;
  }
  return result;
}
export function rates(events: Event[], duration: number, n: number, bins = 50) {
  const counts = Array.from({ length: bins }, () => 0);
  for (const e of events)
    counts[Math.min(bins - 1, Math.floor((e.time_ms / duration) * bins))]++;
  return counts.map((count, i) => ({
    t: ((i + 0.5) * duration) / bins,
    hz: count / n / (duration / bins / 1000),
  }));
}
export type Job = {
  id: string;
  status: string;
  progress: number;
  error: string | null;
  manifest: {
    config: Record<string, unknown> & { pulses?: Pulse[] };
    config_sha256: string;
  };
};
export type ExhibitionEntry = {
  slot: number;
  job_id: string;
  reference_id: string | null;
};
export type Pulse = {
  target: number;
  start: number;
  stop: number;
  amplitude: number;
};
export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    cache: "no-store",
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok)
    throw new Error(`${response.status}: ${await response.text()}`);
  return response.json();
}
export async function topology(
  id: string,
  signal: AbortSignal,
): Promise<Topology> {
  let offset: number | null = 0,
    first: Topology | undefined;
  const edges: Edge[] = [];
  while (offset !== null) {
    const page: Topology & { next_offset: number | null } = await api(
      `/experiments/${id}/topology?offset=${offset}`,
      { signal },
    );
    first ??= page;
    edges.push(...page.edges);
    offset = page.next_offset;
  }
  return { ...first!, edges };
}
export type Layout = "columns" | "sphere" | "grid";
export function positions(
  count: number,
  layout: Layout,
): [number, number, number][] {
  if (count === 2 && layout === "columns")
    return [
      [-3, 0, 0],
      [3, 0, 0],
    ];
  return Array.from({ length: count }, (_, i) => {
    if (layout === "sphere") {
      const y = 1 - (2 * (i + 0.5)) / count;
      const r = Math.sqrt(1 - y * y);
      const angle = i * Math.PI * (3 - Math.sqrt(5));
      return [r * Math.cos(angle) * 9, y * 9, r * Math.sin(angle) * 9];
    }
    if (layout === "grid") {
      const side = Math.ceil(Math.sqrt(count));
      return [
        (((i % side) - (side - 1) / 2) * 18) / side,
        ((Math.floor(i / side) - (side - 1) / 2) * 18) / side,
        0,
      ];
    }
    const rows = Math.ceil(count / 4);
    return [
      ((i % 4) - 1.5) * 4,
      ((Math.floor(i / 4) - (rows - 1) / 2) * 18) / rows,
      (i % 2) * 2 - 1,
    ];
  });
}
export function visibleEdges(
  edges: Edge[],
  nodeBudget: number,
  edgeBudget: number,
  type: string,
  minimum: number,
  selected: number | null,
  stride: number,
) {
  const eligible = edges
    .filter(
      (e) =>
        e.source < nodeBudget &&
        e.target < nodeBudget &&
        (type === "all" || e.type === type) &&
        e.weight >= minimum &&
        (selected === null || e.source === selected || e.target === selected),
    )
    .filter((_, i) => i % stride === 0);
  if (eligible.length <= edgeBudget) return eligible;
  return Array.from(
    { length: edgeBudget },
    (_, i) => eligible[Math.floor((i * eligible.length) / edgeBudget)],
  );
}
export function edgePositions(
  edges: Edge[],
  coordinates: [number, number, number][],
) {
  return edges.flatMap((e) => [
    ...coordinates[e.source],
    ...coordinates[e.target],
  ]);
}
export function activeAt(
  events: Event[],
  time: number,
  window = 1,
): Set<number> {
  let lo = 0,
    hi = events.length;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (events[mid].time_ms < time - window) lo = mid + 1;
    else hi = mid;
  }
  const active = new Set<number>();
  for (let i = lo; i < events.length && events[i].time_ms <= time; i++)
    active.add(events[i].neuron_id);
  return active;
}
