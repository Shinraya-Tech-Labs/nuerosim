"""Read-only projections of persisted results. No regenerated connectivity."""


def topology(result, offset, limit):
    config = result["manifest"]["config"]
    cable = config["model"] == "cable"
    n = len(result["voltage"])
    n_exc = n - round(n * config["inhibitory_fraction"])
    nodes = [
        {
            "id": i,
            "kind": "compartment" if cable else "neuron",
            "type": "passive"
            if cable
            else ("excitatory" if i < n_exc else "inhibitory"),
            "spike_count": len(result["spikes"][i]),
        }
        for i in range(n)
    ]
    if cable:
        edges = [
            {
                "id": i,
                "source": i,
                "target": i + 1,
                "type": "axial",
                "weight": config["parameters"]["axial"],
                "delay_ms": 0,
                "directed": False,
            }
            for i in range(n - 1)
        ]
    else:
        edges = [
            {
                "id": i,
                "source": edge[0],
                "target": edge[1],
                "type": "inhibitory" if edge[2] else "excitatory",
                "weight": config["weight"],
                "delay_ms": result["effective_delay_ms"],
                "directed": True,
            }
            for i, edge in enumerate(result["edges"])
        ]
    return {
        "nodes": nodes,
        "edges": edges[offset : offset + limit],
        "offset": offset,
        "total_edges": len(edges),
        "next_offset": offset + limit if offset + limit < len(edges) else None,
        "weight_unit": "mS/cm^2",
        "coordinates": "not recorded; display layout is illustrative",
        "model": config["model"],
        "duration_ms": config["duration"],
        "dt_ms": config["dt"],
        "config_sha256": result["manifest"]["config_sha256"],
    }


def activity(result, offset, limit):
    events = sorted((t, i) for i, train in enumerate(result["spikes"]) for t in train)
    return {
        "events": [
            {"time_ms": t, "neuron_id": i} for t, i in events[offset : offset + limit]
        ],
        "total_events": len(events),
        "offset": offset,
        "next_offset": offset + limit if offset + limit < len(events) else None,
        "time_unit": "ms",
        "source": "recorded threshold crossings",
    }


def voltage(result, neuron, offset, limit):
    if neuron >= len(result["voltage"]):
        raise ValueError("neuron/compartment ID outside recorded range")
    total = len(result["t"])
    return {
        "neuron_id": neuron,
        "t": result["t"][offset : offset + limit],
        "voltage": result["voltage"][neuron][offset : offset + limit],
        "offset": offset,
        "total_samples": total,
        "next_offset": offset + limit if offset + limit < total else None,
        "time_unit": "ms",
        "voltage_unit": "mV",
    }
