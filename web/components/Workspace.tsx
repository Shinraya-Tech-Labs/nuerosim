"use client";
import dynamic from "next/dynamic";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  api,
  topology,
  positions,
  visibleEdges,
  activity,
  trace,
  activeAt,
  type Event,
  type Trace,
  type Topology,
  type Job,
  type Layout,
} from "../lib/data";
import Fallback from "./Fallback";
import Plots from "./Plots";
import Morphology from "./Morphology";
const Scene = dynamic(() => import("./Scene"), {
  ssr: false,
  loading: () => <p>Loading 3D renderer…</p>,
});
const HH_DEMO = {
  name: "Exhibition · HH current clamp",
  model: "hh",
  duration: 50,
  dt: 0.025,
  record_every: 4,
  n: 1,
  seed: 42,
  pulses: [{ target: 0, start: 10, stop: 40, amplitude: 10 }],
};
const NETWORK_DEMO = {
  name: "Exhibition · seeded LIF network",
  model: "lif",
  duration: 30,
  n: 128,
  seed: 42,
  probability: 0.08,
  pulses: Array.from({ length: 16 }, (_, target) => ({
    target,
    start: 0,
    stop: 30,
    amplitude: 20,
  })),
};
const pairedLifDemo = (amplitude: number, label: string) => ({
  name: `Exhibition · LIF pulse ${label} µA/cm²`,
  model: "lif",
  duration: 50,
  dt: 0.025,
  record_every: 4,
  n: 1,
  seed: 42,
  probability: 0,
  pulses: [{ target: 0, start: 10, stop: 40, amplitude }],
});
export default function Workspace() {
  const [jobs, setJobs] = useState<Job[]>([]),
    [id, setId] = useState(""),
    [data, setData] = useState<Topology | null>(null),
    [error, setError] = useState(""),
    [loading, setLoading] = useState(false),
    [config, setConfig] = useState(""),
    [sidebarOpen, setSidebarOpen] = useState(true),
    [rendererMode, setRendererMode] = useState<"auto" | "webgl2">("auto"),
    [rendererLabel, setRendererLabel] = useState("Renderer idle"),
    [focusToken, setFocusToken] = useState(0),
    [adaptive, setAdaptive] = useState(false),
    [busy, setBusy] = useState(false);
  const [presentationMode, setPresentationMode] = useState(false),
    [comparisonPair, setComparisonPair] = useState<{
      referenceId: string;
      changedId: string;
    } | null>(null);
  const [layout, setLayout] = useState<Layout>("columns"),
    [selected, setSelected] = useState(0),
    [hover, setHover] = useState<number | null>(null),
    [type, setType] = useState("all"),
    [minimum, setMinimum] = useState(0),
    [incident, setIncident] = useState(false),
    [nodeBudget, setNodeBudget] = useState(512),
    [edgeBudget, setEdgeBudget] = useState(2048),
    [stride, setStride] = useState(1),
    [adaptiveBudget, setAdaptiveBudget] = useState(2048),
    [fallback, setFallback] = useState(false);
  const metrics = "Measuring rendered frames…";
  const metricsRef = useRef<HTMLSpanElement>(null);
  const [events, setEvents] = useState<Event[]>([]),
    [signal, setSignal] = useState<Trace | null>(null),
    [time, setTime] = useState(0),
    [playing, setPlaying] = useState(false),
    [speed, setSpeed] = useState(10),
    [signalsLoading, setSignalsLoading] = useState(false),
    [eventsLoaded, setEventsLoaded] = useState(false),
    [compare, setCompare] = useState(""),
    [comparison, setComparison] = useState<Trace | null>(null);
  const job = jobs.find((j) => j.id === id);
  const displayEdgeBudget = adaptive
    ? Math.min(edgeBudget, adaptiveBudget)
    : edgeBudget;
  useEffect(() => {
    const q = new URLSearchParams(location.search).get("experiment");
    if (q) setId(q);
    api("/defaults")
      .then((v) => setConfig(JSON.stringify(v, null, 2)))
      .catch((e) => setError(String(e)));
    let alive = true;
    const refresh = () =>
      api<Job[]>("/experiments?limit=500")
        .then((v) => {
          if (alive) setJobs(v);
        })
        .catch((e) => {
          if (alive) setError(String(e));
        });
    refresh();
    const timer = setInterval(refresh, 1500);
    return () => {
      alive = false;
      clearInterval(timer);
    };
  }, []);
  useEffect(() => {
    const collapseOnSmallScreens = () => {
      if (window.innerWidth <= 900) setSidebarOpen(false);
    };
    collapseOnSmallScreens();
    window.addEventListener("resize", collapseOnSmallScreens);
    return () => window.removeEventListener("resize", collapseOnSmallScreens);
  }, []);
  useEffect(() => {
    if (!id || job?.status !== "completed") {
      setData(null);
      return;
    }
    const controller = new AbortController();
    setLoading(true);
    setData(null);
    setError("");
    topology(id, controller.signal)
      .then((v) => {
        setData(v);
        setSelected(0);
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(String(e));
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [id, job?.status]);
  const pos = useMemo(
    () => positions(data?.nodes.length || 0, layout),
    [data?.nodes.length, layout],
  );
  const nodes = useMemo(
    () => data?.nodes.slice(0, nodeBudget) || [],
    [data, nodeBudget],
  );
  const edges = useMemo(
    () =>
      visibleEdges(
        data?.edges || [],
        nodeBudget,
        displayEdgeBudget,
        type,
        minimum,
        incident ? selected : null,
        stride,
      ),
    [
      data,
      nodeBudget,
      displayEdgeBudget,
      type,
      minimum,
      incident,
      selected,
      stride,
    ],
  );
  useEffect(() => {
    setPlaying(false);
    setTime(0);
    setEvents([]);
    setEventsLoaded(false);
    setComparison(null);
    setCompare("");
    if (!data) return;
    const controller = new AbortController();
    setSignalsLoading(true);
    activity(id, controller.signal)
      .then((value) => {
        setEvents(value);
        setEventsLoaded(true);
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(String(e));
      })
      .finally(() => {
        if (!controller.signal.aborted) setSignalsLoading(false);
      });
    return () => controller.abort();
  }, [data, id]);
  useEffect(() => {
    setSignal(null);
    if (!data) return;
    const controller = new AbortController();
    trace(id, selected, controller.signal)
      .then(setSignal)
      .catch((e) => {
        if (!controller.signal.aborted) setError(String(e));
      });
    return () => controller.abort();
  }, [data, id, selected]);
  useEffect(() => {
    setComparison(null);
    if (!compare) return;
    const controller = new AbortController();
    trace(compare, selected, controller.signal)
      .then(setComparison)
      .catch((e) => {
        if (!controller.signal.aborted) setError(`Comparison: ${e}`);
      });
    return () => controller.abort();
  }, [compare, selected]);
  useEffect(() => {
    if (!comparisonPair) return;
    const pair = [comparisonPair.referenceId, comparisonPair.changedId].map(
      (runId) => jobs.find((item) => item.id === runId),
    );
    if (
      pair.some(
        (item) => item?.status === "failed" || item?.status === "cancelled",
      )
    ) {
      setError(
        "A paired comparison run failed or was cancelled. Inspect both jobs in experiment history.",
      );
      setComparisonPair(null);
    } else if (
      pair.every((item) => item?.status === "completed") &&
      (id !== comparisonPair.changedId ||
        data?.config_sha256 === pair[1]?.manifest.config_sha256)
    ) {
      if (id === comparisonPair.changedId)
        setCompare(comparisonPair.referenceId);
      setComparisonPair(null);
    }
  }, [jobs, comparisonPair, id, data]);
  useEffect(() => {
    if (!playing || !data) return;
    let previous = performance.now();
    const timer = setInterval(() => {
      const now = performance.now();
      const delta = ((now - previous) * speed) / 1000;
      previous = now;
      setTime((t) => Math.min(data.duration_ms, t + delta));
    }, 33);
    return () => clearInterval(timer);
  }, [playing, data, speed]);
  useEffect(() => {
    if (data && time >= data.duration_ms) setPlaying(false);
  }, [time, data]);
  const active = useMemo(() => activeAt(events, time), [events, time]);
  useEffect(() => {
    setAdaptiveBudget(edgeBudget);
  }, [edgeBudget]);
  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if (!data || !document.activeElement?.classList.contains("visualization"))
        return;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        setSelected((v) => Math.min(data.nodes.length - 1, v + 1));
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        setSelected((v) => Math.max(0, v - 1));
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [data]);
  function choose(value: string) {
    setId(value);
    history.replaceState(
      null,
      "",
      value ? `?experiment=${encodeURIComponent(value)}` : "/",
    );
  }
  async function run(path = "/experiments", body?: string) {
    setBusy(true);
    setError("");
    try {
      const result = await api<Job>(path, { method: "POST", body });
      setJobs(await api<Job[]>("/experiments?limit=500"));
      choose(result.id);
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }
  async function runComparisonDemo() {
    setBusy(true);
    setError("");
    try {
      const reference = await api<Job>("/experiments", {
        method: "POST",
        body: JSON.stringify(pairedLifDemo(8, "8")),
      });
      const changed = await api<Job>("/experiments", {
        method: "POST",
        body: JSON.stringify(pairedLifDemo(12, "12")),
      });
      setComparisonPair({ referenceId: reference.id, changedId: changed.id });
      choose(changed.id);
      setJobs(await api<Job[]>("/experiments?limit=500"));
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }
  const inspected = data?.nodes[hover ?? selected];
  const props = {
    nodes,
    edges,
    positions: pos,
    selected,
    onSelect: setSelected,
    onHover: setHover,
    active,
    rendererMode,
    onRenderer: setRendererLabel,
    focusToken,
    onFailure: () => {
      if (rendererMode === "auto") {
        setRendererMode("webgl2");
        setRendererLabel("Switching to WebGL2…");
      } else setFallback(true);
    },
    onMetrics: (value: string) => {
      if (metricsRef.current) metricsRef.current.textContent = value;
      const fps = Number.parseFloat(value);
      if (adaptive && Number.isFinite(fps) && fps < 24)
        setAdaptiveBudget((v) =>
          Math.max(256, Math.floor((v * 0.75) / 256) * 256),
        );
    },
  };
  return (
    <main className="app-shell">
      <header className="topbar">
        <button
          className="icon-button sidebar-toggle"
          aria-label={
            sidebarOpen
              ? "Collapse experiment sidebar"
              : "Expand experiment sidebar"
          }
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? "‹" : "☰"}
        </button>
        <div className="brand-mark">
          <span className="brand-glyph">N</span>
          <span>
            NEUROSIM<small>NEURAL DYNAMICS LAB</small>
          </span>
        </div>
        <div className="topbar-divider" />
        <div className="run-title">
          <span className="live-dot" />
          <span>
            {job
              ? `${String(job.manifest.config.name || job.manifest.config.model)} · ${job.status}`
              : "No experiment loaded"}
          </span>
          <small>{job?.id.slice(0, 8) || "LOCAL CPU WORKSPACE"}</small>
        </div>
        <div className="topbar-right">
          <button
            className="subtle-button presentation-toggle"
            aria-label={
              presentationMode
                ? "Exit presentation mode"
                : "Enter presentation mode"
            }
            aria-pressed={presentationMode}
            onClick={() => {
              const enabled = !presentationMode;
              setPresentationMode(enabled);
              setSidebarOpen(!enabled);
            }}
          >
            {presentationMode ? "Exit presentation" : "Presentation"}
          </button>
          <span className="renderer-badge">
            <i />
            {fallback ? "2D canvas" : rendererLabel}
          </span>
          <span className="topbar-separator" />
          <span className="environment-tag">LOCAL · REPRODUCIBLE</span>
        </div>
      </header>
      <div
        className={`workbench ${sidebarOpen ? "with-sidebar" : "sidebar-collapsed"} ${presentationMode ? "presentation" : ""}`}
      >
        {sidebarOpen && (
          <aside className="experiment-rail">
            <div className="rail-heading">
              <span className="eyebrow">WORKSPACE</span>
              <span className="tiny-counter">
                {jobs.length.toString().padStart(2, "0")} RUNS
              </span>
            </div>
            <label className="control-label">
              EXPERIMENT HISTORY
              <select
                aria-label="Saved experiment"
                value={id}
                onChange={(e) => choose(e.target.value)}
              >
                <option value="">Select an experiment…</option>
                {jobs.map((j) => (
                  <option key={j.id} value={j.id}>
                    {j.id.slice(0, 8)} · {j.status}
                  </option>
                ))}
              </select>
            </label>
            {job && (
              <div className="job-card">
                <div className="job-state">
                  <span className={`state-dot ${job.status}`} />
                  <strong>{job.status}</strong>
                  <span>{Math.round(job.progress * 100)}%</span>
                </div>
                <progress value={job.progress} max={1} />
                {job.error && <p className="job-error">{job.error}</p>}
                <details className="job-inputs">
                  <summary>CONFIGURED CURRENT INPUT</summary>
                  {job.manifest.config.pulses?.length ? (
                    job.manifest.config.pulses.map((pulse, index) => (
                      <p key={`${pulse.target}-${index}`}>
                        Neuron {pulse.target}: {pulse.amplitude} µA/cm² · [
                        {pulse.start}, {pulse.stop}) ms
                      </p>
                    ))
                  ) : (
                    <p>No external current pulses configured.</p>
                  )}
                  <small>
                    Configured current density, not a recorded current trace.
                  </small>
                </details>
                <div className="job-actions">
                  {["queued", "running", "cancelling"].includes(job.status) ? (
                    <button
                      className="subtle-button"
                      disabled={busy || job.status === "cancelling"}
                      onClick={() => run(`/experiments/${id}/cancel`)}
                    >
                      Cancel job
                    </button>
                  ) : (
                    <button
                      className="subtle-button"
                      disabled={busy}
                      onClick={() => run(`/experiments/${id}/retry`)}
                    >
                      Reproduce
                    </button>
                  )}
                  {job.status === "completed" && (
                    <a
                      className="download-link"
                      href={`/api/experiments/${id}/export`}
                      download
                    >
                      Export data ↗
                    </a>
                  )}
                </div>
              </div>
            )}
            <section
              className="guided-demos"
              aria-label="Guided demonstrations"
            >
              <span className="eyebrow">GUIDED DEMONSTRATIONS</span>
              <button
                className="subtle-button full-width"
                disabled={busy || comparisonPair !== null}
                onClick={() => run("/experiments", JSON.stringify(HH_DEMO))}
              >
                01 · HH single-neuron firing
              </button>
              <button
                className="subtle-button full-width"
                disabled={busy || comparisonPair !== null}
                onClick={() =>
                  run("/experiments", JSON.stringify(NETWORK_DEMO))
                }
              >
                02 · Seeded LIF network
              </button>
              <button
                className="subtle-button full-width"
                disabled={busy || comparisonPair !== null}
                onClick={runComparisonDemo}
              >
                03 · Compare 8 vs 12 µA/cm²
              </button>
              {comparisonPair && (
                <p className="helper" role="status">
                  Waiting for both recorded LIF runs. Their voltage traces will
                  be compared when complete.
                </p>
              )}
            </section>
            <details className="rail-section">
              <summary>New simulation</summary>
              <p className="helper">
                Validated CPU experiment settings. Configure the model, inputs
                and network in the engine schema.
              </p>
              <textarea
                aria-label="Experiment configuration"
                value={config}
                onChange={(e) => setConfig(e.target.value)}
                spellCheck={false}
              />
              <button
                className="primary-button run-button"
                disabled={busy || !config}
                onClick={() => run("/experiments", config)}
              >
                {busy ? "Submitting…" : "Run CPU simulation"}
              </button>
            </details>
            <div className="rail-section-title">
              <span>DATASET</span>
              <span className="tiny-counter">
                {data ? `${data.nodes.length} NODES` : "—"}
              </span>
            </div>
            {data ? (
              <>
                <label className="control-label">
                  SELECT NEURON
                  <select
                    aria-label="Selected neuron"
                    value={selected}
                    onChange={(e) => setSelected(Number(e.target.value))}
                  >
                    {data.nodes.map((n) => (
                      <option key={n.id} value={n.id}>
                        {String(n.id).padStart(3, "0")} · {n.type}
                      </option>
                    ))}
                  </select>
                </label>
                <button
                  className="subtle-button full-width"
                  onClick={() => setFocusToken((v) => v + 1)}
                >
                  ⌖ &nbsp;Focus selected neuron
                </button>
              </>
            ) : (
              <p className="rail-empty">
                Load a completed experiment to inspect its recorded network.
              </p>
            )}
            <details className="rail-section advanced">
              <summary>Simulation settings</summary>
              <label className="control-label">
                ARRANGEMENT
                <select
                  value={layout}
                  onChange={(e) => setLayout(e.target.value as Layout)}
                >
                  <option value="columns">Depth columns</option>
                  <option value="sphere">Spherical cloud</option>
                  <option value="grid">Planar grid</option>
                </select>
              </label>
              <label className="control-label">
                CONNECTION CLASS
                <select
                  aria-label="Connection type"
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                >
                  <option value="all">All saved connections</option>
                  <option value="excitatory">Excitatory only</option>
                  <option value="inhibitory">Inhibitory only</option>
                  <option value="axial">Axial cable coupling</option>
                </select>
              </label>
              <label className="control-label">
                MINIMUM WEIGHT <output>{minimum.toFixed(2)} mS/cm²</output>
                <input
                  type="range"
                  min="0"
                  max="0.5"
                  step="0.01"
                  value={minimum}
                  onChange={(e) => setMinimum(Number(e.target.value))}
                />
              </label>
              <label className="control-label">
                NODE DISPLAY LIMIT <output>{nodeBudget}</output>
                <input
                  aria-label="Node display budget"
                  type="range"
                  min="1"
                  max="512"
                  step="1"
                  value={nodeBudget}
                  onChange={(e) => setNodeBudget(Number(e.target.value))}
                />
              </label>
              <label className="control-label">
                LINE DETAIL
                <select
                  value={stride}
                  onChange={(e) => setStride(Number(e.target.value))}
                >
                  <option value={1}>All eligible links</option>
                  <option value={2}>Every second eligible link</option>
                  <option value={4}>Every fourth eligible link</option>
                </select>
              </label>
              <label className="toggle-row">
                <input
                  type="checkbox"
                  checked={incident}
                  onChange={(e) => setIncident(e.target.checked)}
                />
                <span>Emphasize selected connections</span>
              </label>
              <label className="toggle-row">
                <input
                  aria-label="Adaptive density"
                  type="checkbox"
                  checked={adaptive}
                  onChange={(e) => setAdaptive(e.target.checked)}
                />
                <span>Reduce density below 24 FPS</span>
              </label>
              <button
                className="subtle-button full-width"
                onClick={() => setEdgeBudget(2048)}
              >
                Reset line density to balanced
              </button>
            </details>
            <details className="rail-section">
              <summary>SWC morphology</summary>
              <Morphology fallback={fallback} />
            </details>
            <details className="rail-section science-guide">
              <summary>How to read the signals</summary>
              <p className="helper">
                Membrane voltage is recorded in mV. A raster marks recorded
                spike times by neuron; population rate is normalized in Hz.
                Excitatory and inhibitory colors label saved synapse classes.
                The 3D positions are illustrative, not anatomy. The manifest
                records the seed and configuration for reruns.
              </p>
            </details>
            <div className="rail-foot">
              <span className="live-dot" />
              Computations remain on this machine
            </div>
          </aside>
        )}
        <section className="studio" aria-label="Neural network workspace">
          {error && (
            <div role="alert" className="error-banner">
              {error}
              <button aria-label="Dismiss error" onClick={() => setError("")}>
                ×
              </button>
            </div>
          )}
          <div
            className="visualization"
            tabIndex={0}
            aria-label="Interactive 3D neural connectivity view. Use arrow keys to select neurons."
          >
            <div className="scene-host">
              {loading ? (
                <div className="scene-state">
                  <span className="loader-mark" />
                  <strong>Retrieving recorded topology</strong>
                  <small>Reading saved connections and spike metadata</small>
                </div>
              ) : data ? (
                <>{fallback ? <Fallback {...props} /> : <Scene {...props} />}</>
              ) : (
                <div className="scene-state">
                  <div className="empty-orbit">◌</div>
                  <span className="eyebrow">NEURAL DYNAMICS / 3D VIEWPORT</span>
                  <h1>
                    {job
                      ? `Simulation ${job.status}`
                      : "A window into the network"}
                  </h1>
                  <p>
                    Choose a completed experiment, or run a CPU simulation to
                    explore its recorded topology and activity.
                  </p>
                  {!job && (
                    <div className="empty-actions">
                      <button
                        className="primary-button"
                        disabled={busy}
                        onClick={() =>
                          run("/experiments", JSON.stringify(HH_DEMO))
                        }
                      >
                        {busy ? "Submitting…" : "Run HH current-clamp demo"}
                      </button>
                      <button
                        className="subtle-button"
                        onClick={() => setSidebarOpen(true)}
                      >
                        Open experiment library
                      </button>
                    </div>
                  )}
                </div>
              )}
              <div className="scene-vignette" />
              <div className="view-heading">
                <div>
                  <span className="eyebrow">CONNECTOME VIEW</span>
                  <h1>
                    {data
                      ? `${data.model.toUpperCase()} NETWORK`
                      : "Network observatory"}
                  </h1>
                  <p>
                    {data
                      ? `${data.duration_ms} ms recorded · Δt ${data.dt_ms} ms · deterministic seed ${job?.manifest.config.seed}`
                      : "SIMULATION TOPOLOGY · RECORDED ACTIVITY"}
                  </p>
                </div>
                <div className="view-stat">
                  <span className="live-dot" />
                  <span>{data ? "SAVED DATA" : "AWAITING DATA"}</span>
                </div>
              </div>
              {data && (
                <div className="floating-tools">
                  <label className="tool-select">
                    LAYOUT
                    <select
                      aria-label="Layout"
                      value={layout}
                      onChange={(e) => setLayout(e.target.value as Layout)}
                    >
                      <option value="columns">Depth columns</option>
                      <option value="sphere">Spherical cloud</option>
                      <option value="grid">Planar grid</option>
                    </select>
                  </label>
                  <label className="tool-select">
                    CONNECTIONS
                    <select
                      aria-label="Connection type"
                      value={type}
                      onChange={(e) => setType(e.target.value)}
                    >
                      <option value="all">All classes</option>
                      <option value="excitatory">Excitatory</option>
                      <option value="inhibitory">Inhibitory</option>
                      <option value="axial">Axial coupling</option>
                    </select>
                  </label>
                  <label className="tool-select">
                    DENSITY
                    <select
                      aria-label="Edge display budget"
                      value={edgeBudget}
                      onChange={(e) => setEdgeBudget(Number(e.target.value))}
                    >
                      <option value={512}>512 lines</option>
                      <option value={2048}>2,048 lines</option>
                      <option value={8192}>8,192 lines</option>
                      <option value={32768}>Full topology</option>
                    </select>
                  </label>
                  <button
                    className={`icon-button ${adaptive ? "tool-active" : ""}`}
                    aria-pressed={adaptive}
                    aria-label="Toggle adaptive density"
                    title="Adaptive density below 24 FPS"
                    onClick={() => setAdaptive(!adaptive)}
                  >
                    ◈
                  </button>
                  <button
                    className="icon-button"
                    aria-label="Focus selected neuron"
                    title="Focus selected neuron"
                    onClick={() => setFocusToken((v) => v + 1)}
                  >
                    ⌖
                  </button>
                  <label className="renderer-select">
                    <span>RENDER</span>
                    <select
                      aria-label="Rendering backend"
                      value={rendererMode}
                      onChange={(e) => {
                        const mode = e.target.value as "auto" | "webgl2";
                        if (mode === rendererMode) return;
                        setRendererMode(mode);
                        setRendererLabel("Initializing renderer…");
                      }}
                    >
                      <option value="auto">Auto · WebGPU first</option>
                      <option value="webgl2">WebGL2</option>
                    </select>
                  </label>
                </div>
              )}
              {data && (
                <div className="connection-legend">
                  <span className="legend-exc">● EXC</span>
                  <span className="legend-inh">● INH</span>
                  <span className="legend-axial">● AXIAL</span>
                </div>
              )}
              {data && (
                <div className="scene-readout">
                  <strong data-testid="counts">
                    {nodes.length} / {data.nodes.length} neurons&nbsp; · &nbsp;
                    {edges.length.toLocaleString()} /{" "}
                    {data.total_edges.toLocaleString()} lines
                  </strong>
                  <small>
                    Illustrative geometry · saved synapses · no measured spatial
                    propagation
                  </small>
                </div>
              )}
              {data && (
                <aside
                  className="inspector"
                  aria-label="Selected neuron inspector"
                >
                  <div className="inspector-title">
                    <div>
                      <span className="eyebrow">INSPECTOR</span>
                      <h2>
                        {hover === null ? "NEURON" : "HOVERED"}{" "}
                        <span>
                          {String(inspected?.id ?? selected).padStart(3, "0")}
                        </span>
                      </h2>
                    </div>
                    <button
                      className="icon-button"
                      aria-label="Focus on neuron"
                      title="Focus selected neuron"
                      onClick={() => setFocusToken((v) => v + 1)}
                    >
                      ⌖
                    </button>
                  </div>
                  <div className="inspector-class">
                    <i
                      className={
                        inspected?.type === "inhibitory"
                          ? "cyan-dot"
                          : "orange-dot"
                      }
                    />
                    {inspected?.type?.toUpperCase()} · {inspected?.kind}
                  </div>
                  <div className="inspector-metrics">
                    <div>
                      <strong>{inspected?.spike_count ?? 0}</strong>
                      <small>RECORDED SPIKES</small>
                    </div>
                    <div>
                      <strong>
                        {
                          data.edges.filter((e) => e.target === inspected?.id)
                            .length
                        }
                      </strong>
                      <small>INPUTS</small>
                    </div>
                    <div>
                      <strong>
                        {
                          data.edges.filter((e) => e.source === inspected?.id)
                            .length
                        }
                      </strong>
                      <small>OUTPUTS</small>
                    </div>
                  </div>
                  {selected >= nodeBudget && (
                    <p className="inspector-note">
                      Neuron lies outside the visible node budget.
                    </p>
                  )}
                  <details className="edge-inspector">
                    <summary>
                      ACTUAL CONNECTIONS{" "}
                      <span>
                        {
                          data.edges.filter(
                            (e) =>
                              e.source === inspected?.id ||
                              e.target === inspected?.id,
                          ).length
                        }
                      </span>
                    </summary>
                    {data.edges
                      .filter(
                        (e) =>
                          e.source === inspected?.id ||
                          e.target === inspected?.id,
                      )
                      .slice(0, 8)
                      .map((e) => (
                        <div className="edge-row" key={e.id}>
                          <span
                            className={
                              e.type === "inhibitory"
                                ? "cyan-dot"
                                : "orange-dot"
                            }
                          />
                          <code>
                            {e.source} {e.directed ? "→" : "↔"} {e.target}
                          </code>
                          <small>{e.weight} mS/cm²</small>
                        </div>
                      ))}
                  </details>
                  <p className="inspector-note">
                    IDs and counts come from the persisted experiment. Display
                    coordinates do not encode anatomy.
                  </p>
                </aside>
              )}
              <div className="viewport-footer">
                <span>
                  DRAG ORBIT <i>·</i> SCROLL ZOOM <i>·</i> RIGHT DRAG PAN{" "}
                  <i>·</i> ← → SELECT
                </span>
                <span data-testid="performance" ref={metricsRef}>
                  {metrics}
                </span>
                <span>
                  {data?.config_sha256.slice(0, 10).toUpperCase() || "NEUROSIM"}
                </span>
              </div>
              {data && (
                <section className="transport" aria-label="Simulation playback">
                  <div className="transport-top">
                    <div className="transport-title">
                      <span className="playhead-mark">
                        {playing ? "Ⅱ" : "▶"}
                      </span>
                      <div>
                        <span className="eyebrow">RECORDED PLAYBACK</span>
                        <strong data-testid="cursor-time">
                          {time.toFixed(3)} <small>ms</small>
                        </strong>
                      </div>
                      <span className="event-pill" data-testid="event-count">
                        {eventsLoaded
                          ? `${events.length} SPIKES`
                          : signalsLoading
                            ? "LOADING"
                            : "UNAVAILABLE"}
                      </span>
                    </div>
                    <div className="transport-actions">
                      <label>
                        SPEED
                        <select
                          aria-label="Playback speed"
                          value={speed}
                          onChange={(e) => setSpeed(Number(e.target.value))}
                        >
                          <option value={1}>1×</option>
                          <option value={10}>10×</option>
                          <option value={50}>50×</option>
                          <option value={100}>100×</option>
                        </select>
                      </label>
                      <button
                        className="play-button"
                        disabled={signalsLoading || !eventsLoaded}
                        onClick={() => {
                          if (time >= data.duration_ms) setTime(0);
                          setPlaying(!playing);
                        }}
                        aria-label={
                          playing ? "Pause playback" : "Play recorded activity"
                        }
                      >
                        {playing ? "Ⅱ" : "▶"}
                      </button>
                    </div>
                  </div>
                  <label className="timeline-label">
                    <span>0 ms</span>
                    <input
                      aria-label="Simulation timeline"
                      type="range"
                      min={0}
                      max={data.duration_ms}
                      step={data.dt_ms}
                      value={time}
                      onChange={(e) => {
                        setPlaying(false);
                        setTime(Number(e.target.value));
                      }}
                    />
                    <span>{data.duration_ms} ms</span>
                  </label>
                  <div className="transport-foot">
                    <span>
                      {signalsLoading
                        ? "Loading recorded timestamps…"
                        : "Node highlights mark recorded threshold crossings within a trailing 1 ms display window."}
                    </span>
                    <span>Δt {data.dt_ms} ms</span>
                  </div>
                </section>
              )}
            </div>
          </div>
          <div className="science-note">
            <span>ⓘ</span> Layout is illustrative. Edges represent saved
            synapses or adjacent cable coupling; they do not encode physical
            distance or propagation.
          </div>
          {data && (
            <section className="analysis-dock">
              <div className="analysis-heading">
                <div>
                  <span className="eyebrow">SIGNALS & MEASUREMENTS</span>
                  <h2>Recorded analysis</h2>
                </div>
                <label className="compare-select">
                  COMPARE
                  <select
                    aria-label="Comparison experiment"
                    value={compare}
                    onChange={(e) => setCompare(e.target.value)}
                  >
                    <option value="">No comparison</option>
                    {jobs
                      .filter((j) => j.status === "completed" && j.id !== id)
                      .map((j) => (
                        <option key={j.id} value={j.id}>
                          {j.id.slice(0, 8)} · {String(j.manifest.config.model)}
                        </option>
                      ))}
                  </select>
                </label>
              </div>
              {comparison && (
                <p className="comparison-note">
                  Comparing neuron {selected} from {compare.slice(0, 8)}. Models
                  and parameters may differ; times share the current experiment
                  axis.
                </p>
              )}
              {eventsLoaded ? (
                <Plots
                  events={events}
                  trace={signal}
                  comparison={comparison}
                  time={time}
                  duration={data.duration_ms}
                  n={data.nodes.length}
                  selected={selected}
                />
              ) : (
                <p>
                  {signalsLoading
                    ? "Loading saved activity…"
                    : "Activity could not be retrieved. Saved data remains available for export."}
                </p>
              )}
            </section>
          )}
        </section>
      </div>
    </main>
  );
}
