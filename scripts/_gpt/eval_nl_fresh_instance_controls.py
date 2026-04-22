#!/usr/bin/env python3
"""Evaluate fresh-instance transfer for severe-NL mitigation checkpoints."""

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
from run_fresh_instance_cadence_control import evaluate_fresh_instances

ensure_repo_root()


DEFAULT_CHECKPOINTS = {
    "mlp": "checkpoints/_gpt/nl_mitigation/v4_nl2_mlp_linear_comp/V4_hybrid_standard_noise_hat_nl2_mlp_linear_comp_best.pt",
    "qkv": "checkpoints/_gpt/nl_mitigation/v4_nl2_qkv_linear_comp/V4_hybrid_standard_noise_hat_nl2_qkv_linear_comp_best.pt",
    "all": "checkpoints/_gpt/nl_mitigation/v4_nl2_all_linear_comp/V4_hybrid_standard_noise_hat_nl2_all_linear_comp_best.pt",
}


def build_markdown(summary: dict) -> str:
    lines = [
        "# Fresh-Instance NL Mitigation Controls",
        "",
        f"- Generated: `{summary['generated_at']}`",
        f"- Protocol: `{summary['protocol']}`",
        "",
        "| Condition | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |",
        "|:--|--:|--:|--:|",
    ]
    for key in ["mlp", "qkv", "all"]:
        if key not in summary["results"]:
            continue
        row = summary["results"][key]
        lines.append(
            f"| {key} | {row['train_best_acc']:.2f} | {row['cross_instance_mean']:.2f} | {row['cross_instance_std']:.2f} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "- `mlp` tests whether protecting only the MLP analog path restores cross-instance robustness under severe nonlinear write.",
        "- `qkv` is the negative control against the MLP-localization hypothesis.",
        "- `all` is the upper-bound control that linearizes every analog block while keeping the severe-NL global setting elsewhere in the recipe.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--fresh-instances", type=int, default=10)
    parser.add_argument("--eval-runs", type=int, default=5)
    parser.add_argument(
        "--lanes",
        nargs="+",
        choices=sorted(DEFAULT_CHECKPOINTS.keys()),
        default=["mlp", "qkv", "all"],
        help="Subset of mitigation lanes to evaluate.",
    )
    parser.add_argument(
        "--json-path",
        default="report_md/_gpt/json_gpt/nl_fresh_instance_controls_20260418.json",
    )
    parser.add_argument(
        "--md-path",
        default="report_md/_gpt/NL_FRESH_INSTANCE_CONTROLS_20260418.md",
    )
    args = parser.parse_args()

    results = {}
    for key in args.lanes:
        ckpt = DEFAULT_CHECKPOINTS[key]
        results[key] = evaluate_fresh_instances(
            checkpoint_path=ckpt,
            device=args.device,
            fresh_instances=args.fresh_instances,
            eval_runs=args.eval_runs,
            data_root=args.data_root,
            num_workers=args.num_workers,
        )

    summary = {
        "generated_at": datetime.now().isoformat(),
        "protocol": (
            f"{args.fresh_instances} fresh D2D instances x {args.eval_runs} MC evaluations "
            f"per instance on CIFAR-10 Tiny-ViT V4 severe-NL mitigation checkpoints"
        ),
        "results": results,
    }

    json_path = Path(args.json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md_path = Path(args.md_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(build_markdown(summary), encoding="utf-8")

    print(
        json.dumps(
            {
                "json_path": str(json_path),
                "md_path": str(md_path),
                **{
                    f"{key}_mean": value["cross_instance_mean"]
                    for key, value in results.items()
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
