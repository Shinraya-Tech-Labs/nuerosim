"""CLI uses exactly the same validation and engine as the workbench."""

import argparse
import json
from pathlib import Path

from .config import Experiment
from .engine import simulate


def main():
    parser = argparse.ArgumentParser(description="NeuroSim CPU experiments")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("serve", help="local workbench at http://127.0.0.1:8000")
    run = sub.add_parser("simulate", help="run a config or exported manifest")
    run.add_argument("config", type=Path)
    run.add_argument("--output", type=Path, default=Path("results/run.zip"))
    sub.add_parser("example", help="print a complete default JSON configuration")
    args = parser.parse_args()
    if args.command == "serve":
        from .api import serve

        serve()
    elif args.command == "example":
        print(Experiment().model_dump_json(indent=2))
    else:
        from .api import export_zip

        raw = json.loads(args.config.read_text(encoding="utf-8-sig"))
        config = Experiment.model_validate(raw.get("config", raw))
        result = simulate(config)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(export_zip(result))
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "spikes": sum(map(len, result["spikes"])),
                    "wall_time_s": result["wall_time_s"],
                }
            )
        )


if __name__ == "__main__":
    main()
