"""Strict SWC viewer input. Morphology is not a fitted electrical model."""

import math


def parse_swc(text):
    points = {}
    if len(text) > 500_000:
        raise ValueError("SWC exceeds 500 KB")
    for line_number, line in enumerate(text.splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) != 7:
            raise ValueError(f"line {line_number}: expected 7 fields")
        nid, kind = int(fields[0]), int(fields[1])
        x, y, z, r = map(float, fields[2:6])
        parent = int(fields[6])
        if (
            nid <= 0
            or nid in points
            or kind not in range(8)
            or r <= 0
            or not all(math.isfinite(v) and abs(v) < 1e6 for v in (x, y, z, r))
        ):
            raise ValueError(f"line {line_number}: invalid or duplicate point")
        points[nid] = {
            "id": nid,
            "type": kind,
            "x": x,
            "y": y,
            "z": z,
            "radius": r,
            "parent": parent,
        }
        if len(points) > 5000:
            raise ValueError("limit: 5000 SWC points")
    if not points or sum(p["parent"] == -1 for p in points.values()) != 1:
        raise ValueError("SWC must have exactly one root")
    visited = set()
    for nid in points:
        path = set()
        while nid != -1 and nid not in visited:
            if nid not in points or nid in path:
                raise ValueError("missing parent or cycle")
            path.add(nid)
            nid = points[nid]["parent"]
        visited.update(path)
    return list(points.values())
