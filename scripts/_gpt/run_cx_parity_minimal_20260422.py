#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON = "/home/qiaosir/miniconda3/envs/LLM/bin/python"
WARM_START = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"

RUNS = [
    {
        "tag": "j1d_historical_auto",
        "protected_group": "mlp",
        "protected_nl_ltp": "1.0",
        "protected_nl_ltd": "-1.0",
        "use_second_order_ste": True,
        "delta_g_eff": "-1.0",
        "second_order_alpha": "1.0",
    },
    {
        "tag": "j1d_literal_zero",
        "protected_group": "mlp",
        "protected_nl_ltp": "1.0",
        "protected_nl_ltd": "-1.0",
        "use_second_order_ste": True,
        "delta_g_eff": "0.0",
        "second_order_alpha": "1.0",
    },
    {
        "tag": "mlp_noso2_fixed",
        "protected_group": "mlp",
        "protected_nl_ltp": "1.0",
        "protected_nl_ltd": "-1.0",
        "use_second_order_ste": False,
        "delta_g_eff": None,
        "second_order_alpha": None,
    },
    {
        "tag": "all_so2_auto",
        "protected_group": "all",
        "protected_nl_ltp": "1.0",
        "protected_nl_ltd": "-1.0",
        "use_second_order_ste": True,
        "delta_g_eff": "-1.0",
        "second_order_alpha": "1.0",
    },
]


def run_cmd(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def load_json(path: Path):
    payload = json.loads(path.read_text())
    if isinstance(payload, list):
        return payload[0]
    return payload


def main() -> None:
    report_dir = REPO_ROOT / "report_md" / "_gpt"
    json_dir = report_dir / "json_gpt"
    csv_dir = report_dir / "csv_gpt"
    log_dir = REPO_ROOT / "logs" / "_gpt"
    ckpt_root = REPO_ROOT / "checkpoints" / "_gpt" / "cx_parity_minimal"
    for p in (report_dir, json_dir, csv_dir, log_dir, ckpt_root):
        p.mkdir(parents=True, exist_ok=True)

    aggregate = {
        "stage": "cx_parity_minimal_20260422",
        "warm_start_from": WARM_START,
        "runs": {},
    }

    for spec in RUNS:
        tag = spec["tag"]
        suffix = f"_{tag}"
        save_dir = ckpt_root / tag
        save_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"cx_parity_{tag}.log"
        json_path = json_dir / f"cx_parity_{tag}.json"
        csv_path = csv_dir / f"cx_parity_{tag}.csv"
        md_path = report_dir / f"cx_parity_{tag}.md"

        cmd = [
            PYTHON,
            "scripts/_gpt/run_tinyvit_groupwise_nl_comp.py",
            "--protected-group", spec["protected_group"],
            "--protected-nl-ltp", spec["protected_nl_ltp"],
            "--protected-nl-ltd", spec["protected_nl_ltd"],
            "--name-suffix", suffix,
            "--mode", "train",
            "--dataset", "cifar10",
            "--experiments", "V4",
            "--epochs", "1",
            "--batch-size", "64",
            "--num-workers", "0",
            "--device", "cuda",
            "--amp",
            "--nl-ltp", "2.0",
            "--nl-ltd", "-2.0",
            "--warm-start-from", WARM_START,
            "--save-dir", str(save_dir),
            "--log-interval", "1",
            "--log-path", str(log_path),
            "--results-json-path", str(json_path),
            "--results-csv-path", str(csv_path),
            "--results-md-path", str(md_path),
        ]
        if spec["use_second_order_ste"]:
            cmd.append("--use-second-order-ste")
            cmd.extend(["--delta-g-eff", spec["delta_g_eff"]])
            cmd.extend(["--second-order-alpha", spec["second_order_alpha"]])

        run_cmd(cmd)
        row = load_json(json_path)
        aggregate["runs"][tag] = {
            "protected_group": spec["protected_group"],
            "use_second_order_ste": spec["use_second_order_ste"],
            "delta_g_eff": spec["delta_g_eff"],
            "second_order_alpha": spec["second_order_alpha"],
            "best_test_acc": row.get("best_test_acc"),
            "best_epoch": row.get("best_epoch"),
            "final_train_acc": row.get("final_train_acc"),
            "final_test_acc": row.get("final_test_acc"),
            "checkpoint_path": row.get("checkpoint_path"),
            "log_path": str(log_path),
            "results_json_path": str(json_path),
        }

    out_json = json_dir / "cx_parity_minimal_20260422.json"
    out_md = report_dir / "CODEX_CX_PARITY_MINIMAL_20260422.md"
    out_json.write_text(json.dumps(aggregate, indent=2), encoding="utf-8")

    lines = [
        "# CX Minimal Parity Probes (2026-04-22)",
        "",
        f"- Warm-start: `{WARM_START}`",
        "- Mode: 1 epoch source-domain parity probes under fixed code",
        "",
        "| tag | group | SO2 | delta_g_eff | alpha | train_acc | test_acc | best_epoch |",
        "|:--|:--|:--:|:--:|:--:|--:|--:|--:|",
    ]
    for tag, row in aggregate["runs"].items():
        lines.append(
            f"| {tag} | {row['protected_group']} | {'Y' if row['use_second_order_ste'] else 'N'} | {row['delta_g_eff']} | {row['second_order_alpha']} | {row['final_train_acc']:.2f} | {row['final_test_acc']:.2f} | {row['best_epoch']} |"
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Parity minimal complete. Summary written to {out_json}")


if __name__ == "__main__":
    main()
