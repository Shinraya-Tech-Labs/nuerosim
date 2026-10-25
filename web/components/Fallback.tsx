import type { SceneProps } from "./Scene";
export default function Fallback(p: SceneProps) {
  const xy = (id: number) => [
    400 + p.positions[id][0] * 25,
    290 - p.positions[id][1] * 25,
  ];
  return (
    <svg viewBox="0 0 800 580" role="img" aria-label="2D network connectivity">
      {["excitatory", "inhibitory", "axial"].map((type) => (
        <path
          key={type}
          d={p.edges
            .filter((e) => e.type === type)
            .map((e) => {
              const a = xy(e.source),
                b = xy(e.target);
              return `M${a[0]},${a[1]}L${b[0]},${b[1]}`;
            })
            .join(" ")}
          fill="none"
          stroke={
            type === "inhibitory"
              ? "#4dcbd7"
              : type === "axial"
                ? "#b4b9ca"
                : "#ed883c"
          }
          opacity=".2"
        />
      ))}
      {p.nodes.map((n) => {
        const [x, y] = xy(n.id);
        return (
          <circle
            key={n.id}
            cx={x}
            cy={y}
            r={n.id === p.selected ? 5 : 3}
            fill={
              p.active.has(n.id)
                ? "white"
                : n.type === "inhibitory"
                  ? "#4dcbd7"
                  : "#ed883c"
            }
            onClick={() => p.onSelect(n.id)}
            onMouseEnter={() => p.onHover(n.id)}
            onMouseLeave={() => p.onHover(null)}
          >
            <title>Neuron {n.id}</title>
          </circle>
        );
      })}
    </svg>
  );
}
