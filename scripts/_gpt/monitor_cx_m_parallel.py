#!/usr/bin/env python3
"""Monitor local CX-M parallel training sessions and write a compact JSON status."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path


TASKS = {
    "cx_m1": {
        "session": "cx_m1_{timestamp}",
        "log": "logs/_gpt/cx_m1_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m1_fresh_eval.json",
    },
    "cx_m2": {
        "session": "cx_m2_{timestamp}",
        "log": "logs/_gpt/cx_m2_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m2_fresh_eval.json",
    },
    "cx_m3": {
        "session": "cx_m3_{timestamp}",
        "log": "logs/_gpt/cx_m3_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m3_fresh_eval.json",
    },
    "cx_m4": {
        "session": "cx_m4_{timestamp}",
        "log": "logs/_gpt/cx_m4_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m4_fresh_eval.json",
    },
    "cx_m5": {
        "session": "cx_m5_{timestamp}",
        "log": "logs/_gpt/cx_m5_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m5_fresh_eval.json",
    },
    "cx_m6": {
        "session": "cx_m6_{timestamp}",
        "log": "logs/_gpt/cx_m6_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m6_fresh_eval.json",
    },
    "cx_m7": {
        "session": "cx_m7_{timestamp}",
        "log": "logs/_gpt/cx_m7_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m7_fresh_eval.json",
    },
    "cx_m8": {
        "session": "cx_m8_{timestamp}",
        "log": "logs/_gpt/cx_m8_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m8_fresh_eval.json",
    },
    "cx_m9": {
        "session": "cx_m9_{timestamp}",
        "log": "logs/_gpt/cx_m9_{timestamp}.log",
        "fresh_json": "report_md/_gpt/json_gpt/cx_m9_fresh_eval.json",
    },
}

EPOCH_RE = re.compile(
    r"Epoch\s+(?P<epoch>\d+)/(?P<epochs>\d+):\s+"
    r"train_loss=(?P<train_loss>[-+0-9.]+),\s+"
    r"train_acc=(?P<train_acc>[-+0-9.]+)%,\s+"
    r"test_acc=(?P<test_acc>[-+0-9.]+)%.*best=(?P<best>[-+0-9.]+)%"
)


def run_text(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def tmux_session_exists(session: str) -> bool:
    return subprocess.run(
        ["tmux", "has-session", "-t", session],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def gpu_snapshot() -> dict:
    out = run_text([
        "nvidia-smi",
        "--query-gpu=index,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits",
    ])
    if not out:
        return {"available": False}
    row = out.splitlines()[0].split(",")
    return {
        "available": True,
        "index": int(row[0].strip()),
        "memory_used_mib": int(row[1].strip()),
        "memory_total_mib": int(row[2].strip()),
        "utilization_gpu_pct": int(row[3].strip()),
    }


def latest_epoch(log_path: Path) -> dict | None:
    if not log_path.exists():
        return None
    latest = None
    try:
        for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = EPOCH_RE.search(line)
            if match:
                latest = {
                    "line": line,
                    "epoch": int(match.group("epoch")),
                    "epochs": int(match.group("epochs")),
                    "train_loss": float(match.group("train_loss")),
                    "train_acc": float(match.group("train_acc")),
                    "test_acc": float(match.group("test_acc")),
                    "best": float(match.group("best")),
                }
    except OSError:
        return None
    return latest


def build_status(timestamp: str, low_util_streak: int) -> tuple[dict, int]:
    gpu = gpu_snapshot()
    tasks = {}
    any_active = False
    any_incomplete = False

    for task, template in TASKS.items():
        session = template["session"].format(timestamp=timestamp)
        log_path = Path(template["log"].format(timestamp=timestamp))
        fresh_path = Path(template["fresh_json"])
        active = tmux_session_exists(session)
        fresh_done = fresh_path.exists()
        any_active = any_active or active
        any_incomplete = any_incomplete or not fresh_done
        tasks[task] = {
            "session": session,
            "active": active,
            "log": str(log_path),
            "fresh_json": str(fresh_path),
            "fresh_done": fresh_done,
            "latest_epoch": latest_epoch(log_path),
        }

    util = gpu.get("utilization_gpu_pct", 0) if gpu.get("available") else 0
    if any_active and util < 15:
        low_util_streak += 1
    else:
        low_util_streak = 0

    warnings = []
    if low_util_streak >= 5:
        warnings.append("GPU utilization below 15% for five consecutive polls while sessions are active")
    if not any_active and any_incomplete:
        warnings.append("No active CX-M tmux sessions, but at least one fresh JSON is missing")

    status = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "run_timestamp": timestamp,
        "gpu": gpu,
        "tasks": tasks,
        "warnings": warnings,
    }
    return status, low_util_streak


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/cx_m_parallel_monitor.json")
    parser.add_argument("--log-out", default="logs/_gpt/cx_m_parallel_monitor.log")
    args = parser.parse_args()

    json_path = Path(args.json_out)
    log_path = Path(args.log_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    low_util_streak = 0
    with log_path.open("a", encoding="utf-8") as log_fh:
        while True:
            status, low_util_streak = build_status(args.timestamp, low_util_streak)
            json_path.write_text(json.dumps(status, indent=2), encoding="utf-8")
            gpu = status["gpu"]
            util = gpu.get("utilization_gpu_pct", "NA")
            mem = f"{gpu.get('memory_used_mib', 'NA')}/{gpu.get('memory_total_mib', 'NA')}"
            latest = {
                name: (task["latest_epoch"] or {}).get("epoch")
                for name, task in status["tasks"].items()
            }
            log_fh.write(
                f"{status['timestamp']} gpu_util={util} mem={mem} "
                f"epochs={latest} warnings={status['warnings']}\n"
            )
            log_fh.flush()
            time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
