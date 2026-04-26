#!/usr/bin/env python3
"""R10E AIHWKit feasibility probe for the real Tiny-ViT backbone.

This file deliberately does *not* train a toy substitute model.  A previous
draft used a two-layer ``TinyViTDummy`` placeholder, which would have produced
an invalid head-to-head baseline.  R10E must first establish whether AIHWKit can
convert the actual Tiny-ViT operator mix used by the paper.  If conversion is
unsupported, the scientifically honest deliverable is a structured failure
record, not a dummy accuracy number.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def runtime_metadata() -> dict:
    try:
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        commit_hash = None
    try:
        dirty = bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
            ).strip()
        )
    except Exception:
        dirty = None
    return {
        "generated_at": datetime.now().isoformat(),
        "commit_hash": commit_hash,
        "git_worktree_dirty": dirty,
        "python": sys.version,
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
    }


def write_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(path), "status": payload.get("status")}, indent=2))


def count_modules(model: torch.nn.Module) -> dict:
    counts: dict[str, int] = {}
    for module in model.modules():
        name = type(module).__name__
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="report_md/_gpt/json_gpt/r10e_aihwkit_conversion_probe.json",
    )
    parser.add_argument("--num-classes", type=int, default=10)
    args = parser.parse_args()

    out_path = ROOT / args.output
    payload = {
        **runtime_metadata(),
        "task": "R10E AIHWKit real Tiny-ViT conversion feasibility probe",
        "status": None,
        "notes": [
            "No dummy model is trained.",
            "A paper-grade AIHWKit baseline requires successful conversion of the real Tiny-ViT backbone.",
        ],
    }

    try:
        import aihwkit
        from aihwkit.nn.conversion import convert_to_analog
        from aihwkit.simulator.configs import InferenceRPUConfig
    except Exception as exc:  # pragma: no cover - depends on optional env
        payload.update(
            {
                "status": "blocked_aihwkit_import_failed",
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "traceback": traceback.format_exc(limit=8),
            }
        )
        write_report(out_path, payload)
        return

    payload["aihwkit_version"] = getattr(aihwkit, "__version__", "unknown")

    try:
        from train_tinyvit_ensemble import create_tinyvit_model

        model = create_tinyvit_model(num_classes=args.num_classes, pretrained=False)
        payload["source_model_module_counts"] = count_modules(model)

        rpu_config = InferenceRPUConfig()
        # 4-bit-equivalent forward discretization; D2D/C2C semantic parity is
        # not attempted until the real operator conversion succeeds.
        rpu_config.forward.inp_res = 1 / 16
        rpu_config.forward.out_res = 1 / 16

        analog_model = convert_to_analog(model, rpu_config)
        payload["converted_model_module_counts"] = count_modules(analog_model)
        payload["status"] = "conversion_succeeded_training_not_run"
        payload["next_step"] = (
            "Implement a real Tiny-ViT AIHWKit training/evaluation protocol with "
            "documented mapping of D2D/C2C semantics before reporting any accuracy."
        )
    except Exception as exc:  # pragma: no cover - depends on optional env
        payload.update(
            {
                "status": "blocked_real_tinyvit_conversion_failed",
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "traceback": traceback.format_exc(limit=12),
                "paper_safe_interpretation": (
                    "AIHWKit head-to-head accuracy is unavailable because the real "
                    "Tiny-ViT operator mix cannot be converted under this probe. "
                    "This may be cited only as a tooling-coverage limitation, not "
                    "as evidence that the proposed method outperforms AIHWKit."
                ),
            }
        )

    write_report(out_path, payload)


if __name__ == "__main__":
    main()
