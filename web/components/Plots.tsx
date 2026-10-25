"use client";
import { useRef, useMemo } from "react";
import { rates, type Event, type Trace } from "../lib/data";
export function downloadSvg(svg: SVGSVGElement | null, name: string) {
  if (!svg) return;
  const copy = svg.cloneNode(true) as SVGSVGElement;
  copy.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  copy.setAttribute(
    "style",
    "background:#101722;color:#aab7c9;font:12px Arial",
  );
  const url = URL.createObjectURL(
    new Blob([new XMLSerializer().serializeToString(copy)], {
      type: "image/svg+xml",
    }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export default function Plots({
  events,
  trace,
  comparison,
  time,
  duration,
  n,
  selected,
}: {
  events: Event[];
  trace: Trace | null;
  comparison: Trace | null;
  time: number;
  duration: number;
  n: number;
  selected: number;
}) {
  const ref = useRef<SVGSVGElement>(null);
  const x = (t: number) => 50 + (t / duration) * 900;
  const bins = useMemo(() => rates(events, duration, n), [events, duration, n]);
  const maxRate = Math.max(1, ...bins.map((b) => b.hz));
  const path = (data: Trace) => {
    const stride = Math.max(1, Math.ceil(data.t.length / 4000));
    return data.t
      .map((t, i) =>
        i % stride === 0 || i === data.t.length - 1
          ? `${i === 0 ? "M" : "L"}${x(t)},${140 - (data.voltage[i] + 80) * 0.8}`
          : "",
      )
      .join(" ");
  };
  const shown = useMemo(() => events.slice(0, 20000), [events]);
  const tracePath = useMemo(
    () => (trace ? path(trace) : undefined),
    [trace, duration],
  );
  const comparisonPath = useMemo(
    () => (comparison ? path(comparison) : undefined),
    [comparison, duration],
  );
  return (
    <article className="plots">
      <h2>Recorded signals · neuron / compartment {selected}</h2>
      {!trace && (
        <p>
          Waiting for selected voltage trace. Any retrieval failure is reported
          above.
        </p>
      )}
      <p>
        Voltage: display stride ≈4,000 points; full data in ZIP. Raster: first{" "}
        {shown.length} / {events.length} events. Rate: all events, 50 equal
        bins, population-normalized Hz. Trace scale −80 to +60 mV; out-of-range
        values are clipped.
      </p>
      <svg
        ref={ref}
        viewBox="0 0 1000 440"
        role="img"
        aria-label="Synchronized voltage, raster and rate plots"
      >
        <defs>
          <clipPath id="trace-area">
            <rect x="50" y="28" width="900" height="112" />
          </clipPath>
        </defs>
        <g fill="#aab7c9" fontSize="12">
          <text x="8" y="24">
            mV
          </text>
          <text x="8" y="145">
            −80
          </text>
          <text x="8" y="40">
            +60
          </text>
          <text x="8" y="185">
            ID
          </text>
          <text x="8" y="325">
            Hz
          </text>
          <text x="50" y="430">
            0 ms
          </text>
          <text x="900" y="430">
            {duration} ms
          </text>
          <text x="55" y="325">
            scale top {maxRate.toFixed(1)} Hz
          </text>
        </g>
        <g stroke="#303d50">
          <path d="M50 145H950 M50 290H950 M50 410H950" />
        </g>
        <g clipPath="url(#trace-area)">
          {trace && (
            <path
              data-testid="voltage-path"
              d={tracePath}
              fill="none"
              stroke="#ed883c"
              strokeWidth="1.4"
            />
          )}
          {comparison && (
            <path
              data-testid="comparison-path"
              d={comparisonPath}
              fill="none"
              stroke="#4dcbd7"
            />
          )}
        </g>
        <path
          data-testid="raster-path"
          d={shown
            .map(
              (e) =>
                `M${x(e.time_ms)},${180 + (e.neuron_id / Math.max(1, n - 1)) * 100}v3`,
            )
            .join(" ")}
          stroke="#b2bed1"
        />
        <path
          d={bins
            .map(
              (b, i) =>
                `${i === 0 ? "M" : "L"}${x(b.t)},${405 - (b.hz / maxRate) * 70}`,
            )
            .join(" ")}
          stroke="#8eb9ac"
          fill="none"
        />
        <line
          data-testid="plot-cursor"
          x1={x(time)}
          x2={x(time)}
          y1="28"
          y2="410"
          stroke="#ffffff"
          strokeDasharray="3 4"
        />
      </svg>
      <button onClick={() => downloadSvg(ref.current, "neurosim-signals.svg")}>
        Export plots as SVG
      </button>
    </article>
  );
}
