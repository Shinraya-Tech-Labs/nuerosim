import json
import subprocess
import sys
import zipfile


def test_cli_manifest_reproduction(tmp_path):
    config = tmp_path / "input.json"
    config.write_text(json.dumps({"model": "lif", "duration": 10, "pulses": []}))
    first = tmp_path / "first.zip"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "neurosim.workbench.cli",
            "simulate",
            str(config),
            "--output",
            str(first),
        ],
        check=True,
        capture_output=True,
    )
    with zipfile.ZipFile(first) as z:
        expected = json.loads(z.read("results.json"))
        config.write_bytes(z.read("manifest.json"))
    second = tmp_path / "second.zip"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "neurosim.workbench.cli",
            "simulate",
            str(config),
            "--output",
            str(second),
        ],
        check=True,
        capture_output=True,
    )
    with zipfile.ZipFile(second) as z:
        actual = json.loads(z.read("results.json"))
    assert expected["voltage"] == actual["voltage"]
    assert expected["manifest"] == actual["manifest"]
