"""Audit default values against numeric bounds in Pydantic JSON Schema."""

import json
import math
import sys

from neurosim.workbench.config import Experiment

BOUND_KEYS = ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum")


def _finite_number(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number")
    try:
        number = float(value)
    except OverflowError:
        raise ValueError(f"{label} must be a finite number") from None
    if not math.isfinite(number):
        raise ValueError(f"{label} must be a finite number")
    return number


def audit_schema(schema: dict) -> dict[str, object]:
    if not isinstance(schema, dict):
        raise ValueError("schema must be an object")
    definitions = schema.get("$defs", {})
    if not isinstance(definitions, dict):
        raise ValueError("schema $defs must be an object")
    models = [("Experiment", schema), *sorted(definitions.items())]
    bounds = []
    for model_name, model in models:
        if not isinstance(model, dict) or not isinstance(model.get("properties", {}), dict):
            raise ValueError(f"{model_name} properties must be an object")
        for field, spec in sorted(model.get("properties", {}).items()):
            if not isinstance(spec, dict):
                raise ValueError(f"{model_name}.{field} schema must be an object")
            if spec.get("type") not in ("number", "integer"):
                continue
            constraints = {key: spec[key] for key in BOUND_KEYS if key in spec}
            if not constraints:
                continue
            default = _finite_number(spec.get("default"), f"{model_name}.{field} default")
            numeric_bounds = {
                key: _finite_number(value, f"{model_name}.{field} {key}")
                for key, value in constraints.items()
            }
            if (
                ("minimum" in numeric_bounds and default < numeric_bounds["minimum"])
                or ("maximum" in numeric_bounds and default > numeric_bounds["maximum"])
                or (
                    "exclusiveMinimum" in numeric_bounds
                    and default <= numeric_bounds["exclusiveMinimum"]
                )
                or (
                    "exclusiveMaximum" in numeric_bounds
                    and default >= numeric_bounds["exclusiveMaximum"]
                )
            ):
                raise ValueError(f"{model_name}.{field} default is outside declared bounds")
            bounds.append(
                {"model": model_name, "field": field, "default": spec["default"], **constraints}
            )
    return {"status": "pass", "field_count": len(bounds), "bounds": bounds}


def main() -> None:
    try:
        report = audit_schema(Experiment.model_json_schema())
        output = json.dumps(report, indent=2, sort_keys=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        print(f"parameter bounds audit: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
