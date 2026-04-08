#!/usr/bin/env python3
"""Watch a running sweep process and append a completion note to GPT sync files."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def load_rows(json_path: Path, model: str, experiment: str, sweep_type: str) -> list[dict]:
    if not json_path.exists():
        return []
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    rows = payload.get("results", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return []
    return [
        row for row in rows
        if row.get("model") == model
        and row.get("experiment") == experiment
        and row.get("sweep_type") == sweep_type
    ]


def append_block(path: Path, text: str):
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n" + text)


def main():
    parser = argparse.ArgumentParser(description="Watch a sweep PID and update GPT coordination docs on completion.")
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--log-path", type=str, required=True)
    parser.add_argument("--json-path", type=str, required=True)
    parser.add_argument("--repo-root", type=str, default="/home/qiaosir/projects/compute_vit")
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--experiment", type=str, required=True)
    parser.add_argument("--sweep-type", type=str, default="noise")
    parser.add_argument("--poll-seconds", type=int, default=30)
    args = parser.parse_args()

    log_path = Path(args.log_path)
    json_path = Path(args.json_path)
    repo = Path(args.repo_root)

    while pid_alive(args.pid):
        time.sleep(max(5, args.poll_seconds))

    status = "success" if log_path.exists() and "Merged rows written:" in log_path.read_text(encoding="utf-8", errors="ignore") else "stopped"
    rows = load_rows(json_path, args.model, args.experiment, args.sweep_type)
    ts = time.strftime("%Y-%m-%d %H:%M")

    summary_lines = []
    if rows:
        best = max(rows, key=lambda r: float(r.get("test_acc_mean", -1.0)))
        worst = min(rows, key=lambda r: float(r.get("test_acc_mean", 1e9)))
        summary_lines.append(f"- rows available: `{len(rows)}`")
        summary_lines.append(
            f"- best point: sigma_c2c={best.get('sigma_c2c')}, sigma_d2d={best.get('sigma_d2d')}, acc={float(best.get('test_acc_mean')):.2f}%"
        )
        summary_lines.append(
            f"- worst point: sigma_c2c={worst.get('sigma_c2c')}, sigma_d2d={worst.get('sigma_d2d')}, acc={float(worst.get('test_acc_mean')):.2f}%"
        )
    else:
        summary_lines.append("- final JSON rows were not found; inspect the sweep log directly.")

    block = "\n".join([
        f"## [Codex] {ts}",
        "### Topic",
        f"- {args.model} {args.experiment} {args.sweep_type} sweep watcher",
        "",
        "### Status",
        f"- watcher observed completion status: `{status}`",
        *summary_lines,
        "",
        "### Evidence",
        f"- `{log_path}`",
        f"- `{json_path}`",
        "",
        "### Next",
        "- Claude can read this block directly from AGENT_SYNC_gpt.md.",
        "" ,
    ])

    for rel in (
        "report_md/_gpt/AGENT_SYNC_gpt.md",
        "report_md/_gpt/LLM_HANDOFF_gpt.md",
        "report_md/_gpt/LLM_CHANGELOG_gpt.md",
    ):
        append_block(repo / rel, block)


if __name__ == "__main__":
    main()
