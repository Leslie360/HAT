#!/usr/bin/env python3
"""Re-evaluate the paper-locked standard V4 checkpoint on fresh instances without AMP.

This is a narrow recovery script for the Round I C-1 integrity check. It keeps the
paper-locked checkpoint and protocol (10 fresh D2D instances x 5 MC evaluations per
instance), but forces the inference-only path implemented in
`run_fresh_instance_cadence_control.evaluate_fresh_instances`, which already evaluates
with `amp_enabled=False`.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import sys

import torch

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from repo_bootstrap import ensure_repo_root
from run_fresh_instance_cadence_control import FIXED_CKPT, evaluate_fresh_instances

ensure_repo_root()


def build_markdown(result: dict, json_path: str) -> str:
    lines = [
        "# Standard-HAT Fresh-Instance Re-evaluation (`--no-amp`)",
        "",
        f"- Generated: `{datetime.now().isoformat()}`",
        f"- Checkpoint: `{result['checkpoint_path']}`",
        f"- Protocol: `{result['fresh_instances']} fresh D2D instances x {result['mc_runs_per_instance']} MC evaluations per instance`",
        f"- Output JSON: `{json_path}`",
        "",
        "| Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) | Best epoch |",
        "|--:|--:|--:|--:|",
        f"| {result['train_best_acc']:.2f} | {result['cross_instance_mean']:.2f} | {result['cross_instance_std']:.2f} | {result['train_best_epoch']} |",
        "",
        "## Instance means",
        "",
        "| Instance | Seed | Mean acc (%) | Within-instance std (%) |",
        "|:--|--:|--:|--:|",
    ]
    for row in result["instances"]:
        lines.append(
            f"| {row['instance_index'] + 1} | {row['seed']} | {row['test_acc_mean']:.2f} | {row['test_acc_std']:.2f} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--fresh-instances", type=int, default=10)
    parser.add_argument("--eval-runs", type=int, default=5)
    parser.add_argument(
        "--json-path",
        default="report_md/_gpt/json_gpt/fresh_instance_eval_v4_standard_noamp.json",
    )
    parser.add_argument(
        "--md-path",
        default="report_md/_gpt/fresh_instance_eval_v4_standard_noamp.md",
    )
    args = parser.parse_args()

    result = evaluate_fresh_instances(
        checkpoint_path=FIXED_CKPT,
        device=args.device,
        fresh_instances=args.fresh_instances,
        eval_runs=args.eval_runs,
        data_root=args.data_root,
        num_workers=args.num_workers,
    )

    payload = {
        "generated_at": datetime.now().isoformat(),
        "protocol": (
            f"{args.fresh_instances} fresh D2D instances x {args.eval_runs} MC evaluations "
            "per instance on the paper-locked Tiny-ViT V4 standard-HAT checkpoint"
        ),
        "result": result,
    }

    json_path = Path(args.json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_path = Path(args.md_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(build_markdown(result, str(json_path)), encoding="utf-8")

    print(json.dumps(
        {
            "json_path": str(json_path),
            "md_path": str(md_path),
            "cross_instance_mean": result["cross_instance_mean"],
            "cross_instance_std": result["cross_instance_std"],
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
