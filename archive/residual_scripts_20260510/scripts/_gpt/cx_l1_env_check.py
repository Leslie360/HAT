#!/usr/bin/env python3
"""Preflight check for Work 2 CX-L1 LLM KV-cache bring-up.

This script is intentionally download-free. It reports whether the local Python
environment can run HuggingFace LLM inference and whether expected cache paths
already contain model/dataset material.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON = ROOT / "report_md" / "_gpt" / "json_gpt" / "cx_l1_env_preflight.json"

REQUIRED_MODULES = [
    "torch",
    "transformers",
    "datasets",
    "accelerate",
    "evaluate",
    "numpy",
]
OPTIONAL_MODULES = ["sentencepiece", "safetensors", "tokenizers"]
DEFAULT_MODEL_IDS = [
    "TinyLlama/TinyLlama-1.1B-intermediate",
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "gpt2-medium",
]


def module_status(name: str) -> dict:
    try:
        mod = importlib.import_module(name)
        return {"present": True, "version": getattr(mod, "__version__", "unknown")}
    except Exception as exc:
        return {"present": False, "error": f"{type(exc).__name__}: {exc}"}


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=20)
        return proc.returncode, (proc.stdout + proc.stderr).strip()
    except Exception as exc:
        return 999, f"{type(exc).__name__}: {exc}"


def hf_cache_candidates(model_ids: list[str]) -> dict:
    hf_home = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
    hub = hf_home / "hub"
    out = {"hf_home": str(hf_home), "hub_exists": hub.exists(), "models": {}}
    for model_id in model_ids:
        repo_dir = "models--" + model_id.replace("/", "--")
        path = hub / repo_dir
        out["models"][model_id] = {
            "cache_dir": str(path),
            "exists": path.exists(),
            "snapshot_count": len(list((path / "snapshots").glob("*"))) if (path / "snapshots").exists() else 0,
        }
    return out


def gpu_status() -> dict:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return {"nvidia_smi": None, "available": False}
    rc, text = run_cmd([
        nvidia_smi,
        "--query-gpu=index,name,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits",
    ])
    return {"nvidia_smi": nvidia_smi, "returncode": rc, "output": text, "available": rc == 0}


def build_result(args: argparse.Namespace) -> dict:
    required = {name: module_status(name) for name in REQUIRED_MODULES}
    optional = {name: module_status(name) for name in OPTIONAL_MODULES}
    missing_required = [name for name, status in required.items() if not status["present"]]
    result = {
        "experiment": "cx_l1_env_preflight",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "python": sys.executable,
        "python_version": sys.version,
        "platform": platform.platform(),
        "required_modules": required,
        "optional_modules": optional,
        "missing_required": missing_required,
        "hf_cache": hf_cache_candidates(args.model_id),
        "gpu": gpu_status(),
        "download_free": True,
        "ready_for_cx_l1": not missing_required,
        "recommended_install_command": (
            f"{sys.executable} -m pip install transformers datasets accelerate evaluate sentencepiece safetensors"
        ),
        "notes": [
            "Do not launch CX-L1 while Work 1 R2 or other CX-K GPU tasks own the GPU.",
            "If TinyLlama cannot be loaded or baseline perplexity is bad, fall back to gpt2-medium per Claude rule.",
            "This preflight does not download model weights or datasets.",
        ],
    }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--model-id", action="append", default=list(DEFAULT_MODEL_IDS))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = build_result(args)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "json_out": str(args.json_out),
        "ready_for_cx_l1": result["ready_for_cx_l1"],
        "missing_required": result["missing_required"],
        "gpu_available": result["gpu"].get("available"),
    }, indent=2))


if __name__ == "__main__":
    main()
