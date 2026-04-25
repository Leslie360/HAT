#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON = "/home/qiaosir/miniconda3/envs/LLM/bin/python"

WARM_START = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
ALPHA_VALUES = [0.0, 0.25, 0.5, 0.75, 1.0]
DELTA_G_EFF = 0.15
EPOCHS = 100
BATCH_SIZE = 64
NUM_WORKERS = 0
PIN_MEMORY = "off"
FRESH_INSTANCES = 10
EVAL_RUNS = 5


def run_cmd(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def tag_for(alpha: float) -> str:
    return f"k4_alpha_{alpha:.2f}".replace('.', 'p')


def checkpoint_name(tag: str) -> str:
    return f"V4_hybrid_standard_noise_hat_{tag}_best.pt"


def load_checkpoint_best(checkpoint_path: Path) -> tuple[float | None, int | None]:
    import torch
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    return ckpt.get("best_acc"), ckpt.get("best_epoch", ckpt.get("epoch"))


def main() -> None:
    report_dir = REPO_ROOT / "report_md" / "_gpt"
    json_dir = report_dir / "json_gpt"
    csv_dir = report_dir / "csv_gpt"
    ckpt_root = REPO_ROOT / "checkpoints" / "_gpt" / "cx_k4_alpha"
    report_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    ckpt_root.mkdir(parents=True, exist_ok=True)

    aggregate = {
        "stage": "K4_alpha_continuation",
        "warm_start_from": WARM_START,
        "delta_g_eff": DELTA_G_EFF,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "num_workers": NUM_WORKERS,
        "pin_memory": PIN_MEMORY,
        "fresh_instances": FRESH_INSTANCES,
        "eval_runs": EVAL_RUNS,
        "results": {},
    }

    for alpha in ALPHA_VALUES:
        tag = tag_for(alpha)
        suffix = f"_{tag}"
        save_dir = ckpt_root / tag
        save_dir.mkdir(parents=True, exist_ok=True)

        train_log = REPO_ROOT / "logs" / "_gpt" / f"cx_k4_train_{tag}.log"
        train_json = json_dir / f"cx_k4_train_{tag}.json"
        train_csv = csv_dir / f"cx_k4_train_{tag}.csv"
        train_md = report_dir / f"cx_k4_train_{tag}.md"
        eval_json = json_dir / f"cx_k4_eval_{tag}.json"
        ckpt_path = save_dir / checkpoint_name(tag)

        train_best_acc = None
        train_best_epoch = None

        if not ckpt_path.exists():
            train_cmd = [
                PYTHON,
                "scripts/_gpt/run_tinyvit_groupwise_nl_comp.py",
                "--protected-group", "mlp",
                "--protected-nl-ltp", "1.0",
                "--protected-nl-ltd", "-1.0",
                "--use-second-order-ste",
                "--delta-g-eff", str(DELTA_G_EFF),
                "--second-order-alpha", str(alpha),
                "--name-suffix", suffix,
                "--mode", "train",
                "--dataset", "cifar10",
                "--experiments", "V4",
                "--epochs", str(EPOCHS),
                "--batch-size", str(BATCH_SIZE),
                "--num-workers", str(NUM_WORKERS),
                "--pin-memory", PIN_MEMORY,
                "--device", "cuda",
                "--amp",
                "--nl-ltp", "2.0",
                "--nl-ltd", "-2.0",
                "--warm-start-from", WARM_START,
                "--save-dir", str(save_dir),
                "--log-interval", "5",
                "--log-path", str(train_log),
                "--results-json-path", str(train_json),
                "--results-csv-path", str(train_csv),
                "--results-md-path", str(train_md),
            ]
            run_cmd(train_cmd)

        if train_json.exists():
            payload = json.loads(train_json.read_text())
            row = payload[0] if isinstance(payload, list) and payload else payload
            train_best_acc = row.get("best_test_acc")
            train_best_epoch = row.get("best_epoch")
        elif ckpt_path.exists():
            train_best_acc, train_best_epoch = load_checkpoint_best(ckpt_path)

        if not eval_json.exists():
            eval_cmd = [
                PYTHON,
                "scripts/_gpt/eval_joint_fresh_instance.py",
                "--checkpoint", str(ckpt_path),
                "--device", "cuda",
                "--fresh-instances", str(FRESH_INSTANCES),
                "--eval-runs", str(EVAL_RUNS),
                "--data-root", "./data",
                "--num-workers", "0",
                "--protected-group", "mlp",
                "--protected-nl-ltp", "1.0",
                "--protected-nl-ltd", "-1.0",
                "--use-second-order-ste",
                "--delta-g-eff", str(DELTA_G_EFF),
                "--second-order-alpha", str(alpha),
                "--json-out", str(eval_json),
            ]
            run_cmd(eval_cmd)

        eval_payload = json.loads(eval_json.read_text())
        aggregate["results"][tag] = {
            "second_order_alpha": alpha,
            "delta_g_eff": DELTA_G_EFF,
            "train_best_acc": train_best_acc,
            "train_best_epoch": train_best_epoch,
            "fresh_mean": eval_payload.get("cross_instance_mean"),
            "fresh_std": eval_payload.get("cross_instance_std"),
            "fresh_instances": eval_payload.get("fresh_instances"),
            "mc_runs_per_instance": eval_payload.get("mc_runs_per_instance"),
            "checkpoint_path": str(ckpt_path),
        }

    means = [row["fresh_mean"] for row in aggregate["results"].values() if row.get("fresh_mean") is not None]
    aggregate["best_tag"] = max(aggregate["results"].items(), key=lambda kv: kv[1].get("fresh_mean", float("-inf")))[0]
    aggregate["mean_of_means"] = mean(means) if means else None

    out_json = json_dir / "cx_k4_alpha_continuation.json"
    out_md = report_dir / "CODEX_CX_K4_CONTINUATION_20260422.md"
    out_json.write_text(json.dumps(aggregate, indent=2), encoding="utf-8")

    lines = [
        "# CX-K4 Continuation: second_order_alpha Sweep",
        "",
        f"- Warm-start: `{WARM_START}`",
        f"- delta_g_eff: `{DELTA_G_EFF}`",
        f"- Epochs per run: `{EPOCHS}`",
        f"- Batch size: `{BATCH_SIZE}`",
        f"- Num workers: `{NUM_WORKERS}`",
        f"- Pin memory: `{PIN_MEMORY}`",
        f"- Fresh protocol: `{FRESH_INSTANCES} fresh x {EVAL_RUNS} eval`",
        "",
        "| tag | alpha | train best acc | train best epoch | fresh mean | fresh std |",
        "|:--|--:|--:|--:|--:|--:|",
    ]
    for tag, row in aggregate["results"].items():
        lines.append(
            f"| {tag} | {row['second_order_alpha']:.2f} | {row['train_best_acc'] if row['train_best_acc'] is not None else float('nan'):.2f} | {row['train_best_epoch']} | {row['fresh_mean']:.2f} | {row['fresh_std']:.2f} |"
        )
    lines.extend([
        "",
        f"- Best candidate: `{aggregate['best_tag']}`",
        f"- Aggregate JSON: `{out_json.relative_to(REPO_ROOT)}`",
    ])
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"K4 continuation complete. Summary written to {out_json}")


if __name__ == "__main__":
    main()
