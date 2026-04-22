#!/usr/bin/env python3
"""Heavy-tailed D2D evaluator stub.

This intentionally mirrors the existing fresh-instance harness interface but leaves the
heavy-tailed sampling function as a TODO. It exists to prove the code path is ready
for a rebuttal-phase implementation if requested.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CKPT = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
DEFAULT_JSON = "report_md/_gpt/json_gpt/heavy_tailed_d2d_stub.json"


def sample_heavy_tailed_d2d_mask(*_args, **_kwargs):
    raise NotImplementedError(
        "TODO: implement heavy-tailed D2D sampling (e.g. Gaussian + truncated log-normal mixture)."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Heavy-tailed D2D evaluator stub")
    parser.add_argument("--checkpoint", default=DEFAULT_CKPT)
    parser.add_argument("--dataset", default="cifar10")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--fresh-instances", type=int, default=10)
    parser.add_argument("--eval-runs", type=int, default=5)
    parser.add_argument("--tail-family", choices=["lognormal", "student_t", "pareto_trunc"], default="lognormal")
    parser.add_argument("--tail-prob", type=float, default=0.03)
    parser.add_argument("--tail-scale", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=20260420)
    parser.add_argument("--output-json", default=DEFAULT_JSON)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    payload = {
        "status": "stub",
        "checkpoint": args.checkpoint,
        "dataset": args.dataset,
        "data_root": args.data_root,
        "device": args.device,
        "fresh_instances": args.fresh_instances,
        "eval_runs": args.eval_runs,
        "tail_family": args.tail_family,
        "tail_prob": args.tail_prob,
        "tail_scale": args.tail_scale,
        "seed": args.seed,
        "todo": "Implement sample_heavy_tailed_d2d_mask() and wire into fresh-instance evaluation harness.",
    }

    output = REPO_ROOT / args.output_json
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return

    sample_heavy_tailed_d2d_mask()


if __name__ == "__main__":
    main()
