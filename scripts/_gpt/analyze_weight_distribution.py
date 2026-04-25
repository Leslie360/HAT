#!/usr/bin/env python3
"""Compare standard-HAT vs Ensemble-HAT checkpoint weight distributions.

The script loads two checkpoints, computes per-layer histogram summaries and
spectral norms, saves summary plots, and exports a JSON report. Imports for
``torch``/``numpy``/``matplotlib`` are deferred so ``--self-check`` remains
usable in a lightweight shell.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_STANDARD_CKPT = ROOT / "checkpoints" / "V4_hybrid_standard_noise_hat_best.pt"
DEFAULT_ENSEMBLE_CKPT = ROOT / "checkpoints" / "_ensemble" / "V4_hybrid_standard_noise_hat_best.pt"
DEFAULT_R1_GATE_CKPT = (
    ROOT / "checkpoints" / "_gpt" / "r1_clean_anchor" / "V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt"
)
DEFAULT_OUTPUT_DIR = ROOT / "report_md" / "_gpt" / "weight_distribution"
DEFAULT_JSON_OUT = ROOT / "report_md" / "_gpt" / "json_gpt" / "weight_distribution_comparison.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sanitize_layer_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return cleaned.replace(".", "_")


def js_divergence_from_counts(counts_a: Iterable[float], counts_b: Iterable[float]) -> float:
    vec_a = [float(x) for x in counts_a]
    vec_b = [float(x) for x in counts_b]
    total_a = sum(vec_a)
    total_b = sum(vec_b)
    if total_a <= 0 or total_b <= 0:
        return 0.0
    probs_a = [value / total_a for value in vec_a]
    probs_b = [value / total_b for value in vec_b]
    midpoint = [(a + b) / 2.0 for a, b in zip(probs_a, probs_b)]

    def kl_div(p_vec, q_vec) -> float:
        total = 0.0
        for p_val, q_val in zip(p_vec, q_vec):
            if p_val <= 0.0 or q_val <= 0.0:
                continue
            total += p_val * math.log(p_val / q_val, 2.0)
        return total

    return 0.5 * (kl_div(probs_a, midpoint) + kl_div(probs_b, midpoint))


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def require_stack():
    try:
        import numpy as np
        import torch
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - runtime dependency guard
        raise RuntimeError(
            "analyze_weight_distribution.py requires numpy, torch, and matplotlib."
        ) from exc
    return np, torch, plt


def load_checkpoint(path: Path):
    np, torch, _ = require_stack()
    del np
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    state_dict = checkpoint.get("model_state_dict", checkpoint)
    metadata = {
        "checkpoint_path": str(path),
        "best_acc": checkpoint.get("best_acc"),
        "epoch": checkpoint.get("epoch"),
        "best_epoch": checkpoint.get("best_epoch"),
        "dataset": checkpoint.get("dataset"),
        "num_classes": checkpoint.get("num_classes"),
        "experiment_name": (checkpoint.get("exp_cfg") or {}).get("name"),
    }
    return checkpoint, state_dict, metadata


def select_weight_tensors(state_dict) -> Dict[str, object]:
    selected = {}
    for name, tensor in state_dict.items():
        if not name.endswith("weight"):
            continue
        if not hasattr(tensor, "dtype") or not hasattr(tensor, "ndim"):
            continue
        if tensor.ndim < 2:
            continue
        if not tensor.is_floating_point():
            continue
        selected[name] = tensor.detach().cpu().float()
    return selected


def tensor_to_matrix(tensor):
    if tensor.ndim == 2:
        return tensor
    return tensor.reshape(tensor.shape[0], -1)


def tensor_stats(tensor, torch_mod) -> dict:
    flat = tensor.reshape(-1)
    matrix = tensor_to_matrix(tensor)
    spectral_norm = torch_mod.linalg.matrix_norm(matrix, ord=2).item()
    fro_norm = torch_mod.linalg.norm(flat).item()
    return {
        "shape": list(tensor.shape),
        "numel": int(flat.numel()),
        "mean": float(flat.mean().item()),
        "std": float(flat.std(unbiased=False).item()),
        "min": float(flat.min().item()),
        "max": float(flat.max().item()),
        "fro_norm": float(fro_norm),
        "spectral_norm": float(spectral_norm),
    }


def build_layer_row(name: str, standard_tensor, ensemble_tensor, bins: int):
    np, torch, _ = require_stack()

    standard_np = standard_tensor.reshape(-1).numpy()
    ensemble_np = ensemble_tensor.reshape(-1).numpy()
    combined = np.concatenate([standard_np, ensemble_np])
    edges = np.histogram_bin_edges(combined, bins=bins)
    hist_standard, _ = np.histogram(standard_np, bins=edges)
    hist_ensemble, _ = np.histogram(ensemble_np, bins=edges)

    standard_flat = standard_tensor.reshape(-1)
    ensemble_flat = ensemble_tensor.reshape(-1)
    cosine_similarity = torch.dot(standard_flat, ensemble_flat) / (
        torch.linalg.norm(standard_flat) * torch.linalg.norm(ensemble_flat) + 1e-12
    )
    l2_distance = torch.linalg.norm(standard_flat - ensemble_flat).item()

    standard_stats = tensor_stats(standard_tensor, torch)
    ensemble_stats = tensor_stats(ensemble_tensor, torch)
    js_divergence = js_divergence_from_counts(hist_standard.tolist(), hist_ensemble.tolist())

    return {
        "layer": name,
        "sanitized_layer": sanitize_layer_name(name),
        "standard": standard_stats,
        "ensemble": ensemble_stats,
        "comparison": {
            "l2_distance": float(l2_distance),
            "cosine_similarity": float(cosine_similarity.item()),
            "mean_delta": float(ensemble_stats["mean"] - standard_stats["mean"]),
            "std_delta": float(ensemble_stats["std"] - standard_stats["std"]),
            "spectral_norm_delta": float(
                ensemble_stats["spectral_norm"] - standard_stats["spectral_norm"]
            ),
            "js_divergence": float(js_divergence),
        },
        "histogram": {
            "bin_edges": [float(x) for x in edges.tolist()],
            "standard_counts": [int(x) for x in hist_standard.tolist()],
            "ensemble_counts": [int(x) for x in hist_ensemble.tolist()],
        },
    }


def plot_global_histogram(output_path: Path, standard_weights, ensemble_weights, bins: int, label_a: str, label_b: str) -> None:
    np, _, plt = require_stack()
    ensure_parent(output_path)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(standard_weights, bins=bins, alpha=0.55, density=True, label=label_a)
    ax.hist(ensemble_weights, bins=bins, alpha=0.55, density=True, label=label_b)
    ax.set_title("Global Weight Histogram")
    ax.set_xlabel("Weight value")
    ax.set_ylabel("Density")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    del np


def plot_top_spectral_norms(output_path: Path, rows: List[dict], top_k: int, label_a: str, label_b: str) -> None:
    _, _, plt = require_stack()
    ensure_parent(output_path)
    chosen = sorted(
        rows,
        key=lambda row: abs(row["comparison"]["spectral_norm_delta"]),
        reverse=True,
    )[:top_k]
    labels = [row["layer"] for row in chosen]
    standard_vals = [row["standard"]["spectral_norm"] for row in chosen]
    ensemble_vals = [row["ensemble"]["spectral_norm"] for row in chosen]
    positions = list(range(len(chosen)))

    fig_height = max(5.0, 0.35 * len(chosen))
    fig, ax = plt.subplots(figsize=(11, fig_height))
    ax.barh([pos - 0.2 for pos in positions], standard_vals, height=0.38, label=label_a)
    ax.barh([pos + 0.2 for pos in positions], ensemble_vals, height=0.38, label=label_b)
    ax.set_yticks(positions)
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Spectral norm")
    ax.set_title(f"Top {len(chosen)} Layers by Spectral-Norm Shift")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_top_js_divergence(output_path: Path, rows: List[dict], top_k: int) -> None:
    _, _, plt = require_stack()
    ensure_parent(output_path)
    chosen = sorted(rows, key=lambda row: row["comparison"]["js_divergence"], reverse=True)[:top_k]
    labels = [row["layer"] for row in chosen]
    values = [row["comparison"]["js_divergence"] for row in chosen]

    fig_height = max(5.0, 0.35 * len(chosen))
    fig, ax = plt.subplots(figsize=(11, fig_height))
    ax.barh(list(range(len(chosen))), values, color="#4C78A8")
    ax.set_yticks(list(range(len(chosen))))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("JS divergence")
    ax.set_title(f"Top {len(chosen)} Layers by Histogram Divergence")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_top_layer_histograms(output_dir: Path, rows: List[dict], top_k: int, label_a: str, label_b: str) -> List[str]:
    _, _, plt = require_stack()
    output_dir.mkdir(parents=True, exist_ok=True)
    chosen = sorted(rows, key=lambda row: row["comparison"]["js_divergence"], reverse=True)[:top_k]
    saved = []
    for row in chosen:
        edges = row["histogram"]["bin_edges"]
        left_edges = edges[:-1]
        standard_counts = row["histogram"]["standard_counts"]
        ensemble_counts = row["histogram"]["ensemble_counts"]
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.step(left_edges, standard_counts, where="post", label=label_a)
        ax.step(left_edges, ensemble_counts, where="post", label=label_b)
        ax.set_title(f"{row['layer']} histogram")
        ax.set_xlabel("Weight value")
        ax.set_ylabel("Count")
        ax.legend()
        fig.tight_layout()
        out_path = output_dir / f"{row['sanitized_layer']}.png"
        fig.savefig(out_path, dpi=180)
        plt.close(fig)
        saved.append(str(out_path))
    return saved


def run_analysis(args) -> dict:
    np, _, _ = require_stack()

    if not args.force and not args.r1_gate_checkpoint.exists():
        raise FileNotFoundError(
            f"R1 gate checkpoint missing: {args.r1_gate_checkpoint}. "
            "Use --force to bypass the gate."
        )

    _, standard_state_dict, standard_meta = load_checkpoint(args.standard_checkpoint)
    _, ensemble_state_dict, ensemble_meta = load_checkpoint(args.ensemble_checkpoint)

    standard_weights = select_weight_tensors(standard_state_dict)
    ensemble_weights = select_weight_tensors(ensemble_state_dict)
    shared_layers = sorted(
        name
        for name in standard_weights.keys() & ensemble_weights.keys()
        if tuple(standard_weights[name].shape) == tuple(ensemble_weights[name].shape)
    )
    if not shared_layers:
        raise RuntimeError("No shared weight tensors with matching shapes were found.")

    rows = [build_layer_row(name, standard_weights[name], ensemble_weights[name], args.bins) for name in shared_layers]
    all_standard = np.concatenate([standard_weights[name].reshape(-1).numpy() for name in shared_layers])
    all_ensemble = np.concatenate([ensemble_weights[name].reshape(-1).numpy() for name in shared_layers])

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    global_hist_path = output_dir / "global_weight_histogram.png"
    spectral_path = output_dir / "spectral_norm_top_layers.png"
    js_path = output_dir / "histogram_divergence_top_layers.png"
    per_layer_dir = output_dir / "top_layer_histograms"

    label_a = "standard_hat"
    label_b = "ensemble_hat"
    plot_global_histogram(global_hist_path, all_standard, all_ensemble, args.bins, label_a, label_b)
    plot_top_spectral_norms(spectral_path, rows, args.top_k, label_a, label_b)
    plot_top_js_divergence(js_path, rows, args.top_k)
    per_layer_paths = plot_top_layer_histograms(per_layer_dir, rows, args.top_k, label_a, label_b)

    top_js = sorted(rows, key=lambda row: row["comparison"]["js_divergence"], reverse=True)[: args.top_k]
    top_spectral = sorted(
        rows,
        key=lambda row: abs(row["comparison"]["spectral_norm_delta"]),
        reverse=True,
    )[: args.top_k]

    result = {
        "experiment": "weight_distribution_comparison",
        "generated_at": now_iso(),
        "gated_by_r1_checkpoint": str(args.r1_gate_checkpoint),
        "gate_passed": args.force or args.r1_gate_checkpoint.exists(),
        "standard_checkpoint": standard_meta,
        "ensemble_checkpoint": ensemble_meta,
        "layer_count": len(rows),
        "missing_in_standard": sorted(name for name in ensemble_weights.keys() - standard_weights.keys()),
        "missing_in_ensemble": sorted(name for name in standard_weights.keys() - ensemble_weights.keys()),
        "summary": {
            "global_standard_mean": float(all_standard.mean()),
            "global_ensemble_mean": float(all_ensemble.mean()),
            "global_standard_std": float(all_standard.std()),
            "global_ensemble_std": float(all_ensemble.std()),
            "top_js_layers": [
                {"layer": row["layer"], "js_divergence": row["comparison"]["js_divergence"]}
                for row in top_js
            ],
            "top_spectral_shift_layers": [
                {
                    "layer": row["layer"],
                    "spectral_norm_delta": row["comparison"]["spectral_norm_delta"],
                }
                for row in top_spectral
            ],
        },
        "plots": {
            "global_histogram": str(global_hist_path),
            "spectral_norms": str(spectral_path),
            "histogram_divergence": str(js_path),
            "top_layer_histograms": per_layer_paths,
        },
        "layers": rows,
    }
    ensure_parent(args.json_out)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def run_self_check() -> None:
    assert sanitize_layer_name("blocks.0.attn.qkv.weight") == "blocks_0_attn_qkv_weight"
    first = js_divergence_from_counts([1, 3, 2], [1, 3, 2])
    second = js_divergence_from_counts([1, 0, 5], [2, 4, 0])
    mirror = js_divergence_from_counts([2, 4, 0], [1, 0, 5])
    assert abs(first) < 1e-12
    assert second >= 0.0
    assert abs(second - mirror) < 1e-12
    print("analyze_weight_distribution.py self-check passed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--standard-checkpoint", type=Path, default=DEFAULT_STANDARD_CKPT)
    parser.add_argument("--ensemble-checkpoint", type=Path, default=DEFAULT_ENSEMBLE_CKPT)
    parser.add_argument("--r1-gate-checkpoint", type=Path, default=DEFAULT_R1_GATE_CKPT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--bins", type=int, default=80)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--force", action="store_true", help="Bypass the R1 checkpoint gate.")
    parser.add_argument("--self-check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_check:
        run_self_check()
        return
    result = run_analysis(args)
    print(f"Wrote JSON report to {args.json_out}")
    print(f"Saved plots under {args.output_dir}")
    print(
        "Top JS-divergence layer: "
        f"{result['summary']['top_js_layers'][0]['layer']}"
        if result["summary"]["top_js_layers"]
        else "No layers analyzed."
    )


if __name__ == "__main__":
    main()
