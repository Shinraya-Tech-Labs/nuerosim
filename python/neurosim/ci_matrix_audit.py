"""Summarize declared platform and runtime matrices in GitHub Actions YAML."""

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on optional extra
    yaml = None


RUNTIME_AXES = {"python", "python-version", "node", "node-version"}


def _load_workflow(path):
    if yaml is None:
        raise ValueError("PyYAML is required; install the optional legacy extra")
    try:
        document = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read workflow {path}: {exc}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("jobs"), dict):
        raise ValueError(f"workflow {path} must contain a jobs mapping")
    return document


def _strings(value, label):
    values = value if isinstance(value, list) else [value]
    if not values or any(not isinstance(item, (str, int, float)) for item in values):
        raise ValueError(f"{label} must be a scalar or a non-empty scalar list")
    return [str(item) for item in values]


def audit_workflow(path):
    document = _load_workflow(path)
    records = []
    for job_id, job in sorted(document["jobs"].items()):
        if not isinstance(job, dict):
            raise ValueError(f"workflow {path} job {job_id} must be a mapping")
        strategy = job.get("strategy", {})
        if not isinstance(strategy, dict):
            raise ValueError(f"workflow {path} job {job_id} strategy must be a mapping")
        matrix = strategy.get("matrix", {})
        if not isinstance(matrix, dict):
            raise ValueError(f"workflow {path} job {job_id} matrix must be a mapping")
        axes = {}
        for axis, values in sorted(matrix.items()):
            if axis in {"include", "exclude"}:
                continue
            if not isinstance(values, list):
                raise ValueError(f"matrix axis {axis} must be a non-empty list")
            axes[axis] = _strings(values, f"matrix axis {axis}")
        runs_on = _strings(job["runs-on"], "runs-on") if "runs-on" in job else []
        matrix_platforms = axes.get("os", [])
        platforms = sorted(set(matrix_platforms or [v for v in runs_on if "${{" not in v]))
        runtime_axes = {
            axis.removesuffix("-version"): values
            for axis, values in axes.items()
            if axis in RUNTIME_AXES
        }
        steps = job.get("steps", [])
        if not isinstance(steps, list):
            raise ValueError(f"workflow {path} job {job_id} steps must be a list")
        for step in steps:
            if not isinstance(step, dict) or not isinstance(step.get("with", {}), dict):
                continue
            action = step.get("uses", "")
            action_inputs = step.get("with", {})
            if "setup-python" in action and "python" not in runtime_axes:
                version = action_inputs.get("python-version")
                if isinstance(version, (str, int, float)) and "${{" not in str(version):
                    runtime_axes["python"] = [str(version)]
            if "setup-node" in action and "node" not in runtime_axes:
                version = action_inputs.get("node-version")
                if isinstance(version, (str, int, float)) and "${{" not in str(version):
                    runtime_axes["node"] = [str(version)]
        runtime_axes = dict(sorted(runtime_axes.items()))
        combination_count = math.prod(len(values) for values in axes.values())
        records.append(
            {
                "job": str(job_id),
                "runs_on": runs_on,
                "platforms": platforms,
                "runtime_axes": runtime_axes,
                "matrix_combinations": combination_count,
            }
        )
    return {
        "workflow": str(path),
        "job_count": len(records),
        "matrix_combinations": sum(record["matrix_combinations"] for record in records),
        "jobs": records,
    }


def audit_workflows(paths):
    reports = [audit_workflow(path) for path in sorted(map(str, paths))]
    return {
        "workflows": reports,
        "job_count": sum(report["job_count"] for report in reports),
        "matrix_combinations": sum(report["matrix_combinations"] for report in reports),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", nargs="+", help="GitHub Actions workflow YAML file(s)")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(audit_workflows(args.workflow), sort_keys=True, indent=2))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
