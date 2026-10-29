"use client";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import {
  Component,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  type ReactNode,
} from "react";
import type { OrbitControls as OrbitControlsImpl } from "three-stdlib";
import type { WebGPURendererParameters } from "three/webgpu";
import { edgePositions, type Edge, type Node } from "../lib/data";
export type SceneProps = {
  nodes: Node[];
  edges: Edge[];
  positions: [number, number, number][];
  selected: number;
  onSelect: (id: number) => void;
  onHover: (id: number | null) => void;
  active: Set<number>;
  onFailure: () => void;
  onMetrics: (s: string) => void;
  rendererMode: "auto" | "webgl2";
  onRenderer: (s: string) => void;
  focusToken: number;
};
function colorFor(node: Node, selected: number, active: Set<number>) {
  return active.has(node.id)
    ? "#ffffff"
    : node.id === selected
      ? "#ffe287"
      : node.type === "inhibitory"
        ? "#4dcbd7"
        : "#ed883c";
}
function Geometry(p: SceneProps) {
  const mesh = useRef<THREE.InstancedMesh>(null),
    controls = useRef<OrbitControlsImpl>(null),
    focus = useRef<{ target: THREE.Vector3; camera: THREE.Vector3 } | null>(
      null,
    ),
    styles = useRef(new Map<number, string>()),
    initialized = useRef<{
      nodes: Node[];
      positions: [number, number, number][];
    } | null>(null);
  const lines = useMemo(() => {
    const points = edgePositions(p.edges, p.positions),
      colors: number[] = [];
    for (const edge of p.edges) {
      const connected =
        edge.source === p.selected || edge.target === p.selected;
      const c = new THREE.Color(
        connected
          ? "#ffe0a3"
          : edge.type === "inhibitory"
            ? "#4dcbd7"
            : edge.type === "axial"
              ? "#b4b9ca"
              : "#ed883c",
      );
      if (!connected) c.multiplyScalar(0.55);
      colors.push(c.r, c.g, c.b, c.r, c.g, c.b);
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute(
      "position",
      new THREE.Float32BufferAttribute(points, 3),
    );
    geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    return geometry;
  }, [p.edges, p.positions, p.selected]);
  const arrow = useMemo(() => {
    if (p.nodes.length !== 2 || p.edges.length !== 1) return null;
    const edge = p.edges[0],
      source = new THREE.Vector3(...p.positions[edge.source]),
      target = new THREE.Vector3(...p.positions[edge.target]),
      direction = target.clone().sub(source).normalize();
    return {
      position: target.addScaledVector(direction, -0.65),
      rotation: new THREE.Quaternion().setFromUnitVectors(
        new THREE.Vector3(0, 1, 0),
        direction,
      ),
    };
  }, [p.nodes.length, p.edges, p.positions]);
  useEffect(() => () => lines.dispose(), [lines]);
  useEffect(() => {
    if (!mesh.current) return;
    const changed =
      initialized.current?.nodes !== p.nodes ||
      initialized.current?.positions !== p.positions;
    const matrix = new THREE.Matrix4();
    p.nodes.forEach((node, index) => {
      if (changed) {
        matrix.makeTranslation(...p.positions[node.id]);
        mesh.current!.setMatrixAt(index, matrix);
      }
      const color = colorFor(node, p.selected, p.active);
      if (styles.current.get(node.id) !== color) {
        mesh.current!.setColorAt(index, new THREE.Color(color));
        styles.current.set(node.id, color);
      }
    });
    if (changed) {
      mesh.current.instanceMatrix.needsUpdate = true;
      mesh.current.computeBoundingSphere();
      initialized.current = { nodes: p.nodes, positions: p.positions };
      styles.current.clear();
      p.nodes.forEach((node) =>
        styles.current.set(node.id, colorFor(node, p.selected, p.active)),
      );
    }
    if (mesh.current.instanceColor)
      mesh.current.instanceColor.needsUpdate = true;
  }, [p.nodes, p.positions, p.selected, p.active]);
  useEffect(() => {
    if (p.focusToken === 0 || !p.positions[p.selected]) return;
    const target = new THREE.Vector3(...p.positions[p.selected]);
    focus.current = {
      target,
      camera: target.clone().add(new THREE.Vector3(0, 2.5, 18)),
    };
  }, [p.focusToken]);
  const metrics = useRef({ start: 0, frames: 0, intervals: [] as number[] });
  useFrame(({ gl, clock }, delta) => {
    const m = metrics.current;
    m.frames++;
    m.intervals.push(delta * 1000);
    const now = clock.elapsedTime;
    if (now - m.start >= 1) {
      const sorted = m.intervals.sort((a, b) => a - b);
      const memory = (
        performance as Performance & { memory?: { usedJSHeapSize: number } }
      ).memory;
      p.onMetrics(
        `${(m.frames / (now - m.start)).toFixed(1)} FPS · p95 ${sorted[Math.floor(sorted.length * 0.95)]?.toFixed(1) ?? "—"} ms · ${gl.info.render.calls} draw calls · JS heap ${memory ? (memory.usedJSHeapSize / 1048576).toFixed(0) + " MiB" : "unavailable"}`,
      );
      m.start = now;
      m.frames = 0;
      m.intervals = [];
    }
    if (focus.current && controls.current) {
      const alpha = 1 - Math.exp(-6 * Math.max(delta, 0));
      controls.current.target.lerp(focus.current.target, alpha);
      controls.current.object.position.lerp(focus.current.camera, alpha);
      controls.current.update();
      if (
        controls.current.target.distanceTo(focus.current.target) < 0.02 &&
        controls.current.object.position.distanceTo(focus.current.camera) < 0.05
      )
        focus.current = null;
    }
  });
  return (
    <>
      {arrow && (
        <mesh position={arrow.position} quaternion={arrow.rotation}>
          <coneGeometry args={[0.28, 0.6, 12]} />
          <meshBasicMaterial color="#ffe0a3" />
        </mesh>
      )}
      <lineSegments geometry={lines}>
        <lineBasicMaterial
          vertexColors
          transparent
          opacity={
            p.edges.length === 1
              ? 0.9
              : Math.min(0.32, 8 / Math.sqrt(Math.max(1, p.edges.length)))
          }
          depthWrite={false}
        />
      </lineSegments>
      <instancedMesh
        ref={mesh}
        args={[undefined, undefined, p.nodes.length]}
        onClick={(e) => {
          e.stopPropagation();
          if (e.instanceId !== undefined) p.onSelect(p.nodes[e.instanceId].id);
        }}
        onPointerMove={(e) => {
          e.stopPropagation();
          if (e.instanceId !== undefined) p.onHover(p.nodes[e.instanceId].id);
        }}
        onPointerOut={() => p.onHover(null)}
      >
        <sphereGeometry
          args={[
            p.nodes.length === 2
              ? 0.5
              : Math.min(0.12, 24 / Math.max(1, p.nodes.length)),
            8,
            6,
          ]}
        />
        <meshBasicMaterial />
      </instancedMesh>
      <OrbitControls ref={controls} makeDefault enableDamping />
    </>
  );
}
class RendererBoundary extends Component<
  { children: ReactNode; onFailure: () => void },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch() {
    this.props.onFailure();
  }
  render() {
    return this.state.failed ? (
      <p className="renderer-error">Starting compatible renderer…</p>
    ) : (
      this.props.children
    );
  }
}
export default function Scene(p: SceneProps) {
  const currentRendererMode = useRef(p.rendererMode);
  currentRendererMode.current = p.rendererMode;
  const webgpuFactory = useCallback(
    async (props: THREE.WebGLRendererParameters) => {
      const useWebGL2 = () => {
        p.onRenderer("WebGL2 · WebGPU unavailable");
        return new THREE.WebGLRenderer(props);
      };
      if (!navigator.gpu) return useWebGL2();
      const adapter = await navigator.gpu.requestAdapter();
      if (!adapter) return useWebGL2();
      const { WebGPURenderer } = await import("three/webgpu");
      const renderer = new WebGPURenderer(
        props as unknown as WebGPURendererParameters,
      );
      await renderer.init();
      const backend = renderer.backend as typeof renderer.backend & {
        isWebGPUBackend?: boolean;
      };
      p.onRenderer(
        backend.isWebGPUBackend ? "WebGPU" : "WebGL2 · WebGPU fallback",
      );
      return renderer as unknown as THREE.WebGLRenderer;
    },
    [p.onRenderer],
  );
  return (
    <RendererBoundary key={p.rendererMode} onFailure={p.onFailure}>
      <Canvas
        key={p.rendererMode}
        gl={p.rendererMode === "auto" ? webgpuFactory : undefined}
        camera={{ position: [3, 4, 27], fov: 48 }}
        dpr={[1, 1.5]}
        onCreated={({ gl }) => {
          if (!("isWebGPURenderer" in gl) && p.rendererMode === "webgl2")
            p.onRenderer("WebGL2");
          const mode = p.rendererMode;
          gl.domElement.addEventListener(
            "webglcontextlost",
            () => {
              if (currentRendererMode.current === mode) p.onFailure();
            },
            { once: true },
          );
        }}
        fallback={
          <p className="renderer-error">WebGL2 is unavailable. Switch to 2D.</p>
        }
      >
        <Geometry {...p} />
      </Canvas>
    </RendererBoundary>
  );
}
