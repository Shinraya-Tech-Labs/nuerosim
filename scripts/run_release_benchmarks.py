"""Run isolated, reproducible CPU simulation and result handling benchmarks."""

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate


PHASES = ("setup", "simulation", "serialization", "retrieval")


def _windows_memory_snapshot():
    class ProcessMemoryCounters(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(ProcessMemoryCounters),
        wintypes.DWORD,
    ]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    process = kernel32.GetCurrentProcess()
    if not psapi.GetProcessMemoryInfo(
        process, ctypes.byref(counters), counters.cb
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    return counters.WorkingSetSize, counters.PeakWorkingSetSize


def _memory_snapshot():
    if os.name == "nt":
        return _windows_memory_snapshot()
    import resource

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = int(peak if sys.platform == "darwin" else peak * 1024)
    try:
        with Path("/proc/self/statm").open(encoding="ascii") as stream:
            resident_pages = int(stream.read().split()[1])
        current_bytes = resident_pages * os.sysconf("SC_PAGE_SIZE")
    except (OSError, ValueError, IndexError, AttributeError):
        current_bytes = peak_bytes
    return int(current_bytes), peak_bytes


def _worker(spec):
    baseline_rss, baseline_peak = _memory_snapshot()
    started = time.perf_counter()
    config = Experiment.model_validate(spec["config"])
    setup_s = time.perf_counter() - started
    after_setup = _memory_snapshot()[1]

    started = time.perf_counter()
    result = simulate(config)
    simulation_s = time.perf_counter() - started
    after_simulation = _memory_snapshot()[1]

    started = time.perf_counter()
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)
    serialization_s = time.perf_counter() - started
    after_serialization = _memory_snapshot()[1]

    started = time.perf_counter()
    retrieved = json.loads(payload)
    retrieval_s = time.perf_counter() - started
    _, after_retrieval_peak = _memory_snapshot()
    if retrieved["manifest"]["config_sha256"] != result["manifest"]["config_sha256"]:
        raise AssertionError("serialized result changed its configuration manifest")

    deterministic_output = {
        key: result[key]
        for key in (
            "t",
            "voltage",
            "spikes",
            "edges",
            "rate_time",
            "rate_hz",
            "mean_rate_hz",
            "final_state",
            "effective_delay_ms",
            "activity_events",
        )
    }
    digest = hashlib.sha256(
        json.dumps(
            deterministic_output,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    peaks = [baseline_peak, after_setup, after_simulation, after_serialization, after_retrieval_peak]
    phase_peak = dict(zip((*PHASES, "complete"), peaks[1:]))
    return {
        "setup_s": setup_s,
        "simulation_s": simulation_s,
        "engine_reported_simulation_s": float(result["wall_time_s"]),
        "serialization_s": serialization_s,
        "retrieval_s": retrieval_s,
        "process_baseline_rss_bytes": int(baseline_rss),
        "process_peak_rss_bytes": int(after_retrieval_peak),
        "incremental_peak_rss_bytes": max(0, int(after_retrieval_peak) - int(baseline_rss)),
        "phase_peak_rss_bytes": {key: int(value) for key, value in phase_peak.items()},
        "serialized_result_bytes": len(payload.encode("utf-8")),
        "neuron_count": config.n,
        "time_steps": round(config.duration / config.dt),
        "realized_edge_count": len(result["edges"]),
        "spike_count": sum(map(len, result["spikes"])),
        "output_sha256": digest,
    }


def _worker_main():
    spec = json.load(sys.stdin)
    print(json.dumps(_worker(spec), sort_keys=True, allow_nan=False))


def _validate_document(document):
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("benchmark config must be an object with schema_version=1")
    suite = document.get("suite")
    workloads = document.get("workloads")
    if not isinstance(suite, str) or not suite:
        raise ValueError("suite must be a non-empty string")
    if not isinstance(workloads, list) or not workloads:
        raise ValueError("workloads must be a non-empty list")
    warmups = document.get("warmup_repeats")
    repetitions = document.get("repetitions")
    if isinstance(warmups, bool) or not isinstance(warmups, int) or not 0 <= warmups <= 10:
        raise ValueError("warmup_repeats must be an integer from 0 through 10")
    if isinstance(repetitions, bool) or not isinstance(repetitions, int) or not 3 <= repetitions <= 20:
        raise ValueError("repetitions must be an integer from 3 through 20")
    ids = []
    for workload in workloads:
        if not isinstance(workload, dict):
            raise ValueError("each workload must be an object")
        workload_id = workload.get("id")
        if not isinstance(workload_id, str) or re.fullmatch(r"[a-z0-9][a-z0-9_-]*", workload_id) is None:
            raise ValueError("workload ids must be lowercase filename-safe slugs")
        if not isinstance(workload.get("category"), str) or not workload["category"]:
            raise ValueError(f"{workload_id}: category must be a non-empty string")
        if not isinstance(workload.get("config"), dict):
            raise ValueError(f"{workload_id}: config must be an object")
        Experiment.model_validate(workload["config"])
        ids.append(workload_id)
    if len(ids) != len(set(ids)):
        raise ValueError("workload ids must be unique")
    return warmups, repetitions


def _run_sample(spec):
    completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--worker"],
        input=json.dumps(spec, sort_keys=True),
        capture_output=True,
        check=False,
        text=True,
        timeout=300,
        env=os.environ.copy(),
    )
    if completed.returncode:
        raise RuntimeError(
            f"benchmark worker failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    try:
        sample = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"benchmark worker returned invalid JSON: {completed.stdout[:200]}") from exc
    return sample


def _percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    return float(ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower))


def _summarize(values):
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "sample_stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "p95": _percentile(values, 0.95),
        "min": min(values),
        "max": max(values),
    }


def _cpu_model():
    if os.name == "nt":
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name)",
                ],
                capture_output=True,
                check=True,
                text=True,
                timeout=10,
            )
            if result.stdout.strip():
                return result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    if sys.platform.startswith("linux"):
        try:
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or platform.uname().processor or "unknown"


def _system_memory_bytes():
    if os.name == "nt":
        class MemoryStatusEx(ctypes.Structure):
            _fields_ = [
                ("dwLength", wintypes.DWORD),
                ("dwMemoryLoad", wintypes.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatusEx()
        status.dwLength = ctypes.sizeof(status)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MemoryStatusEx)]
        kernel32.GlobalMemoryStatusEx.restype = wintypes.BOOL
        if kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return int(status.ullTotalPhys)
    if hasattr(os, "sysconf"):
        try:
            return int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"))
        except (ValueError, OSError):
            pass
    return None


def _dependency_versions():
    packages = ("neurosim", "numpy", "scipy", "pydantic", "fastapi")
    versions = {}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def _git_revision(root):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            check=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _benchmark_workload(workload, warmups, repetitions):
    spec = {"id": workload["id"], "config": workload["config"]}
    for _ in range(warmups):
        _run_sample(spec)
    samples = [_run_sample(spec) for _ in range(repetitions)]
    output_hashes = {sample["output_sha256"] for sample in samples}
    if len(output_hashes) != 1:
        raise RuntimeError(f"{workload['id']}: repeated output hashes differ")
    measured = {
        phase: _summarize([sample[f"{phase}_s"] for sample in samples])
        for phase in PHASES
    }
    measured["measured_total"] = _summarize(
        [sum(sample[f"{phase}_s"] for phase in PHASES) for sample in samples]
    )
    return {
        "id": workload["id"],
        "category": workload["category"],
        "config": workload["config"],
        "derived": {
            "neuron_count": samples[0]["neuron_count"],
            "time_steps": samples[0]["time_steps"],
            "neuron_steps": samples[0]["neuron_count"] * samples[0]["time_steps"],
            "realized_edge_count": samples[0]["realized_edge_count"],
            "spike_count": samples[0]["spike_count"],
            "serialized_result_bytes": samples[0]["serialized_result_bytes"],
        },
        "warmup_repeats_discarded": warmups,
        "repetitions": repetitions,
        "identical_output_sha256": next(iter(output_hashes)),
        "repeats_identical": True,
        "phase_summary_seconds": measured,
        "memory_summary_bytes": {
            key: _summarize([float(sample[key]) for sample in samples])
            for key in (
                "process_baseline_rss_bytes",
                "process_peak_rss_bytes",
                "incremental_peak_rss_bytes",
            )
        },
        "sample_records": samples,
    }


def run_benchmarks(config_path, output_path):
    config_path = Path(config_path)
    output_path = Path(output_path)
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite benchmark evidence: {output_path}")
    config_bytes = config_path.read_bytes()
    document = json.loads(config_bytes)
    warmups, repetitions = _validate_document(document)
    canonical_config = json.dumps(
        document, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    canonical_runner = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    results = [
        _benchmark_workload(workload, warmups, repetitions)
        for workload in document["workloads"]
    ]
    report = {
        "schema_version": 1,
        "suite": document["suite"],
        "run_started_utc": datetime.now(timezone.utc).isoformat(),
        "source_revision": _git_revision(config_path.resolve().parents[1]),
        "config_path": config_path.as_posix(),
        "config_sha256": hashlib.sha256(canonical_config).hexdigest(),
        "runner_sha256": hashlib.sha256(canonical_runner).hexdigest(),
        "protocol": {
            "warmup_repeats": warmups,
            "measured_repetitions": repetitions,
            "sample_isolation": "one fresh Python subprocess per warmup or measured sample",
            "timing_clock": "time.perf_counter",
            "serialization": "stdlib json.dumps followed by json.loads in each worker",
            "percentile_method": "linear interpolation; p95 over measured repetitions",
            "rss_scope": "worker process working set peak including imports and result materialization",
        },
        "environment": {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "processor": _cpu_model(),
            "logical_cpu_count": os.cpu_count(),
            "system_memory_bytes": _system_memory_bytes(),
            "python": sys.version.split()[0],
            "dependencies": _dependency_versions(),
            "thread_environment": {
                key: os.environ.get(key)
                for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")
            },
        },
        "benchmarks": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=Path("benchmarks/v020-workloads.json")
    )
    parser.add_argument(
        "--output", type=Path, default=Path("benchmarks/results/v020-run-001.json")
    )
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.worker:
        _worker_main()
        return 0
    try:
        report = run_benchmarks(args.config, args.output)
    except (OSError, ValueError, TypeError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(
        json.dumps(
            {
                "suite": report["suite"],
                "output": str(args.output),
                "workload_count": len(report["benchmarks"]),
                "repetitions": report["protocol"]["measured_repetitions"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
