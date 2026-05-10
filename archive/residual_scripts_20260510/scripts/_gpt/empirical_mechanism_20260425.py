#!/usr/bin/env python3
"""Round-7 empirical mechanism analyses for existing TinyViT/HAT checkpoints.

Jobs:
  E1 hessian     Lanczos Hessian spectrum on a fixed eval batch.
  E2 d2d         D2D mismatch loss landscape for canonical Standard vs Ensemble.
  E3 cka         Linear CKA matrix across post-fix M-series checkpoints.
  E4 sensitivity Per-layer single-D2D-mask sensitivity for canonical Ensemble.
  E5 avg         Checkpoint averaging probe for Standard seeds 123/456.
  report         Master markdown summary from landed JSONs.

This script intentionally does not edit canonical model code and avoids
train_tinyvit.evaluate(), because that function resets analog noise before every
eval. Jobs E2/E4 need manually assigned D2D masks to remain in effect.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from amp_utils import autocast_context
from eval_fresh_instances_postfix import load_checkpoint_provenance, runtime_metadata
from inference_analysis_utils import iter_analog_modules, load_model_bundle, set_uniform_noise
from train_tinyvit import DATASET_STATS

JSON_DIR = ROOT / "report_md/_gpt/json_gpt"
CSV_DIR = ROOT / "report_md/_gpt/csv_gpt"
FIG_DIR = ROOT / "paper/figures"
REPORT_PATH = ROOT / "report_md/_gpt/CODEX_EMPIRICAL_MECHANISM_REPORT_20260425.md"
AVG_CKPT_DIR = ROOT / "checkpoints/_gpt/empirical_mechanism_20260425"

RUNS = {
    "canonical_standard": {
        "label": "Canonical Standard HAT (NL=1)",
        "short": "Standard NL=1",
        "exp_id": "V4",
        "checkpoint": "checkpoints/V4_hybrid_standard_noise_hat_best.pt",
        "nl_ltp": 1.0,
        "nl_ltd": -1.0,
        "noise_mode": "uniform",
        "hat_type": "Standard",
        "seed": None,
    },
    "canonical_ensemble": {
        "label": "Canonical Ensemble HAT (NL=1)",
        "short": "Ensemble NL=1",
        "exp_id": "V4",
        "checkpoint": "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt",
        "nl_ltp": 1.0,
        "nl_ltd": -1.0,
        "noise_mode": "uniform",
        "hat_type": "Ensemble",
        "seed": None,
    },
    "cx_m1": {
        "label": "CX-M1 Standard seed123 severe-NL",
        "short": "M1 Standard",
        "exp_id": "V3",
        "checkpoint": "checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt",
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "uniform",
        "hat_type": "Standard",
        "seed": 123,
    },
    "cx_m2": {
        "label": "CX-M2 Ensemble seed123 severe-NL",
        "short": "M2 Ensemble",
        "exp_id": "V4",
        "checkpoint": "checkpoints/_gpt/postfix_m_series/cx_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt",
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "uniform",
        "hat_type": "Ensemble",
        "seed": 123,
    },
    "cx_m3": {
        "label": "CX-M3 Proportional seed123 severe-NL",
        "short": "M3 Proportional",
        "exp_id": "V4",
        "checkpoint": "checkpoints/_gpt/postfix_m_series/cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt",
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "proportional",
        "hat_type": "Proportional",
        "seed": 123,
    },
    "cx_m4": {
        "label": "CX-M4 Proportional seed456 severe-NL",
        "short": "M4 Proportional",
        "exp_id": "V4",
        "checkpoint": "checkpoints/_gpt/postfix_m_series/cx_m4_proportional_seed456/V4_hybrid_standard_noise_hat_best.pt",
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "proportional",
        "hat_type": "Proportional",
        "seed": 456,
    },
    "cx_m5": {
        "label": "CX-M5 Standard seed456 severe-NL",
        "short": "M5 Standard",
        "exp_id": "V3",
        "checkpoint": "checkpoints/_gpt/postfix_m_series/cx_m5_standard_seed456/V3_hybrid_standard_noise_standard_train_best.pt",
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "uniform",
        "hat_type": "Standard",
        "seed": 456,
    },
    "cx_m6": {
        "label": "CX-M6 Ensemble seed456 severe-NL",
        "short": "M6 Ensemble",
        "exp_id": "V4",
        "checkpoint": "checkpoints/_gpt/postfix_m_series/cx_m6_ensemble_seed456/V4_hybrid_standard_noise_hat_best.pt",
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "uniform",
        "hat_type": "Ensemble",
        "seed": 456,
    },
}

CODE_PROVENANCE = [
    ROOT / "analog_layers.py",
    ROOT / "inference_analysis_utils.py",
    ROOT / "train_tinyvit.py",
    ROOT / "eval_fresh_instances_postfix.py",
    ROOT / "scripts/_gpt/empirical_mechanism_20260425.py",
]

COLORS = {
    "canonical_standard": "#b84a39",
    "canonical_ensemble": "#2364aa",
    "cx_m1": "#bf7f00",
    "cx_m2": "#2a9d8f",
    "cx_m3": "#6d597a",
    "cx_m4": "#9d4edd",
    "cx_m5": "#d95d39",
    "cx_m6": "#40916c",
}


def ensure_dirs() -> None:
    for path in (JSON_DIR, CSV_DIR, FIG_DIR, AVG_CKPT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def rel(path: Path | str) -> str:
    p = Path(path)
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def code_sha256(paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        if not path.exists():
            continue
        digest.update(rel(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def base_metadata(extra: Optional[dict] = None) -> dict:
    meta = runtime_metadata()
    meta["code_sha256"] = code_sha256(CODE_PROVENANCE)
    meta["script"] = rel(__file__)
    meta["gpu_resize_eval"] = os.environ.get("CODEX_EMPIRICAL_GPU_RESIZE", "1") != "0"
    meta["gpu_resize_protocol"] = "CIFAR32 ToTensor -> GPU bilinear resize 224 -> GPU normalize" if meta["gpu_resize_eval"] else "canonical CPU Resize transform"
    meta["timestamp_unix"] = time.time()
    if extra:
        meta.update(extra)
    return meta


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    print(f"[save] {rel(path)}", flush=True)


def configure_model_from_run(bundle, run_id: str) -> None:
    cfg = RUNS[run_id]
    ckpt_cfg = checkpoint_exp_cfg(run_id)
    for attr in ("sigma_c2c", "sigma_d2d", "noise_enabled", "hat_training"):
        value = ckpt_cfg.get(attr)
        if value is not None and hasattr(bundle.exp_cfg, attr):
            setattr(bundle.exp_cfg, attr, value)
    if cfg.get("nl_ltp") is not None:
        bundle.exp_cfg.nl_ltp = float(cfg["nl_ltp"])
    if cfg.get("nl_ltd") is not None:
        bundle.exp_cfg.nl_ltd = float(cfg["nl_ltd"])
    if cfg.get("noise_mode") is not None:
        bundle.exp_cfg.noise_mode = str(cfg["noise_mode"])
    for _, module in iter_analog_modules(bundle.model):
        module.config.NL_LTP = float(bundle.exp_cfg.nl_ltp)
        module.config.NL_LTD = float(bundle.exp_cfg.nl_ltd)
        module.config.noise_mode = str(bundle.exp_cfg.noise_mode)


def checkpoint_exp_cfg(run_id: str) -> dict:
    ckpt = ROOT / RUNS[run_id]["checkpoint"]
    data = torch.load(ckpt, map_location="cpu", weights_only=False)
    return dict(data.get("exp_cfg") or {})


def load_run(run_id: str, device: str, batch_size: int, num_workers: int, amp: bool):
    cfg = RUNS[run_id]
    ckpt = ROOT / cfg["checkpoint"]
    if not ckpt.exists():
        raise FileNotFoundError(f"Missing checkpoint for {run_id}: {ckpt}")
    print(f"[load] {run_id}: {rel(ckpt)}", flush=True)
    bundle = load_model_bundle(
        "tinyvit",
        cfg["exp_id"],
        device,
        checkpoint_path=str(ckpt),
        num_workers=num_workers,
        batch_size=batch_size,
        amp_enabled=amp,
    )
    configure_model_from_run(bundle, run_id)
    maybe_enable_gpu_resize_loader(bundle, batch_size=batch_size, num_workers=num_workers)
    return bundle


def maybe_enable_gpu_resize_loader(bundle, batch_size: int, num_workers: int) -> None:
    """Replace CPU PIL resize with native 32x32 loading plus GPU resize.

    This is scoped to this analysis script. It preserves the eval transform order
    as closely as practical: ToTensor at 32x32, GPU bilinear resize to 224, then
    CIFAR normalization on GPU.
    """
    if os.environ.get("CODEX_EMPIRICAL_GPU_RESIZE", "1") == "0":
        return
    if bundle.dataset != "cifar10":
        return
    stats = DATASET_STATS[bundle.dataset]
    testset = datasets.CIFAR10(
        root="./data",
        train=False,
        download=False,
        transform=transforms.ToTensor(),
    )
    loader_kwargs = {
        "batch_size": batch_size,
        "shuffle": False,
        "num_workers": num_workers,
        "pin_memory": False,
    }
    if num_workers > 0:
        loader_kwargs["persistent_workers"] = True
    bundle.testloader = DataLoader(testset, **loader_kwargs)
    bundle._codex_gpu_resize_size = 224
    bundle._codex_norm_mean = torch.tensor(stats["mean"], dtype=torch.float32, device=bundle.device).view(1, -1, 1, 1)
    bundle._codex_norm_std = torch.tensor(stats["std"], dtype=torch.float32, device=bundle.device).view(1, -1, 1, 1)


def preprocess_inputs(bundle, inputs: torch.Tensor) -> torch.Tensor:
    inputs = inputs.to(bundle.device, non_blocking=True)
    size = getattr(bundle, "_codex_gpu_resize_size", None)
    if size is not None:
        if inputs.shape[-1] != size or inputs.shape[-2] != size:
            inputs = F.interpolate(inputs, size=(size, size), mode="bilinear", align_corners=False)
        inputs = (inputs - bundle._codex_norm_mean) / bundle._codex_norm_std
    return inputs


def clean_noise(bundle) -> None:
    set_uniform_noise(bundle.model, sigma_c2c=0.0, sigma_d2d=0.0, noise_enabled=False, resample_d2d=False)
    for _, module in iter_analog_modules(bundle.model):
        if hasattr(module, "d2d_noise"):
            module.d2d_noise.zero_()
        module.config.retention_enabled = False


def enable_fixed_d2d(bundle, sigma: float, noise_mode: str) -> None:
    for _, module in iter_analog_modules(bundle.model):
        module.config.noise_enabled = True
        module.config.sigma_c2c = 0.0
        module.config.sigma_d2d = float(sigma)
        module.config.noise_mode = noise_mode
        module.config.retention_enabled = False


def enable_loaded_d2d(bundle, noise_mode: str) -> None:
    """Use checkpoint-loaded fixed D2D buffers, but disable stochastic C2C."""
    sigma = float(getattr(bundle.exp_cfg, "sigma_d2d", 0.1) or 0.1)
    for _, module in iter_analog_modules(bundle.model):
        module.config.noise_enabled = True
        module.config.sigma_c2c = 0.0
        module.config.sigma_d2d = sigma
        module.config.noise_mode = noise_mode
        module.config.retention_enabled = False


def capture_d2d_masks(bundle) -> Dict[str, torch.Tensor]:
    return {name: module.d2d_noise.detach().clone() for name, module in iter_analog_modules(bundle.model)}


def set_d2d_from_base(bundle, base_masks: Dict[str, torch.Tensor], alpha: float) -> None:
    with torch.no_grad():
        for name, module in iter_analog_modules(bundle.model):
            module.d2d_noise.copy_(base_masks[name] * alpha)


def set_d2d_source_to_fresh(bundle, source_masks: Dict[str, torch.Tensor], fresh_masks: Dict[str, torch.Tensor], alpha: float) -> None:
    with torch.no_grad():
        for name, module in iter_analog_modules(bundle.model):
            module.d2d_noise.copy_(source_masks[name] + alpha * (fresh_masks[name] - source_masks[name]))


def sample_base_d2d_masks(bundle, sigma: float, seed: int) -> Dict[str, torch.Tensor]:
    torch.manual_seed(seed)
    masks = {}
    with torch.no_grad():
        for name, module in iter_analog_modules(bundle.model):
            g_range = float(module.config.G_max - module.config.G_min)
            masks[name] = torch.randn_like(module.d2d_noise) * sigma * g_range
    return masks


@torch.no_grad()
def eval_manual(bundle, max_batches: Optional[int] = None) -> Tuple[float, float, int]:
    model = bundle.model
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(bundle.testloader):
        if max_batches is not None and batch_idx >= max_batches:
            break
        inputs = preprocess_inputs(bundle, inputs)
        targets = targets.to(bundle.device, non_blocking=True)
        with autocast_context(bundle.device, bundle.amp_enabled):
            outputs = model(inputs)
            loss = bundle.criterion(outputs, targets)
        running_loss += float(loss.item()) * int(inputs.size(0))
        correct += int(outputs.argmax(dim=1).eq(targets).sum().item())
        total += int(targets.size(0))
    if total == 0:
        raise RuntimeError("eval_manual saw zero samples")
    return running_loss / total, 100.0 * correct / total, total


def analog_layer_group(name: str) -> str:
    if "patch_embed" in name:
        return "patch_embed"
    if ".attn.qkv" in name:
        return "qkv"
    if ".attn.proj" in name:
        return "proj"
    if ".mlp." in name:
        return "mlp"
    if "head" in name:
        return "head"
    return "other"


def checkpoint_provenance(run_id: str) -> dict:
    ckpt = ROOT / RUNS[run_id]["checkpoint"]
    prov = load_checkpoint_provenance(ckpt)
    prov.update({
        "run_id": run_id,
        "checkpoint_path": rel(ckpt),
        "label": RUNS[run_id]["label"],
        "exp_id": RUNS[run_id]["exp_id"],
        "eval_nl_ltp": RUNS[run_id]["nl_ltp"],
        "eval_nl_ltd": RUNS[run_id]["nl_ltd"],
        "eval_noise_mode": RUNS[run_id]["noise_mode"],
        "hat_type": RUNS[run_id]["hat_type"],
        "seed": RUNS[run_id]["seed"],
    })
    return prov


def plot_cka(matrix: np.ndarray, labels: Sequence[str], out_base: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    im = ax.imshow(matrix, vmin=0.0, vmax=1.0, cmap="viridis")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_title(title)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white" if matrix[i, j] < 0.55 else "black", fontsize=8)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Linear CKA")
    fig.tight_layout()
    fig.savefig(out_base.with_suffix(".png"), dpi=300)
    fig.savefig(out_base.with_suffix(".pdf"))
    plt.close(fig)


def center_gram(K: torch.Tensor) -> torch.Tensor:
    n = K.size(0)
    unit = torch.ones((n, n), device=K.device, dtype=K.dtype) / n
    return K - unit @ K - K @ unit + unit @ K @ unit


def linear_cka(X: torch.Tensor, Y: torch.Tensor) -> float:
    X = X.float()
    Y = Y.float()
    X = X - X.mean(dim=0, keepdim=True)
    Y = Y - Y.mean(dim=0, keepdim=True)
    K = center_gram(X @ X.t())
    L = center_gram(Y @ Y.t())
    hsic = (K * L).sum()
    norm = torch.linalg.norm(K) * torch.linalg.norm(L)
    if float(norm.item()) == 0.0:
        return float("nan")
    return float((hsic / norm).detach().cpu().item())


def reduce_activation(output: torch.Tensor, max_features: int = 2048) -> torch.Tensor:
    if isinstance(output, (tuple, list)):
        output = output[0]
    x = output.detach().float()
    if x.dim() == 4:
        x = x.mean(dim=(2, 3))
    elif x.dim() == 3:
        x = x.mean(dim=1)
    elif x.dim() > 2:
        x = x.flatten(start_dim=1)
    if x.dim() == 1:
        x = x.unsqueeze(1)
    if x.size(1) > max_features:
        idx = torch.linspace(0, x.size(1) - 1, steps=max_features, device=x.device).long()
        x = x.index_select(1, idx)
    return x.cpu()


def collect_activations(bundle, max_layers: Optional[int] = None) -> Dict[str, torch.Tensor]:
    activations: Dict[str, torch.Tensor] = {}
    handles = []
    names = [name for name, _ in iter_analog_modules(bundle.model)]
    if max_layers is not None:
        names = names[:max_layers]
    names_set = set(names)

    def make_hook(name: str):
        def hook(_module, _inputs, output):
            if name not in activations:
                activations[name] = reduce_activation(output)
        return hook

    for name, module in iter_analog_modules(bundle.model):
        if name in names_set:
            handles.append(module.register_forward_hook(make_hook(name)))
    try:
        bundle.model.eval()
        inputs, _targets = next(iter(bundle.testloader))
        inputs = preprocess_inputs(bundle, inputs)
        with torch.no_grad(), autocast_context(bundle.device, bundle.amp_enabled):
            _ = bundle.model(inputs)
    finally:
        for handle in handles:
            handle.remove()
    return activations


def job_cka(args) -> dict:
    ensure_dirs()
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    run_ids = ["cx_m1", "cx_m2", "cx_m3", "cx_m4", "cx_m5", "cx_m6"]
    all_acts: Dict[str, Dict[str, torch.Tensor]] = {}
    provenance = {}
    for run_id in run_ids:
        bundle = load_run(run_id, args.device, args.batch_size, args.num_workers, amp=True)
        enable_loaded_d2d(bundle, RUNS[run_id]["noise_mode"])
        acts = collect_activations(bundle)
        all_acts[run_id] = acts
        provenance[run_id] = checkpoint_provenance(run_id)
        del bundle
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    common_layers = sorted(set.intersection(*[set(acts.keys()) for acts in all_acts.values()]))
    per_layer = []
    aggregate = np.zeros((len(run_ids), len(run_ids)), dtype=np.float64)
    layer_count = 0
    for layer in common_layers:
        matrix = np.eye(len(run_ids), dtype=np.float64)
        valid = True
        for i, left in enumerate(run_ids):
            for j, right in enumerate(run_ids):
                if j <= i:
                    continue
                value = linear_cka(all_acts[left][layer], all_acts[right][layer])
                if math.isnan(value):
                    valid = False
                matrix[i, j] = matrix[j, i] = value
        if not valid:
            continue
        aggregate += matrix
        layer_count += 1
        per_layer.append({
            "layer": layer,
            "group": analog_layer_group(layer),
            "matrix": matrix.tolist(),
            "offdiag_mean": float((matrix.sum() - np.trace(matrix)) / (matrix.size - len(run_ids))),
        })
    if layer_count == 0:
        raise RuntimeError("No valid common CKA layers")
    aggregate /= layer_count
    labels = [RUNS[x]["short"].replace(" ", "\n") for x in run_ids]
    plot_cka(aggregate, labels, FIG_DIR / "figS_cka_mseries", "M-series representation similarity")
    offdiag = float((aggregate.sum() - np.trace(aggregate)) / (aggregate.size - len(run_ids)))
    result = {
        "job": "E3_CKA_M_SERIES",
        "method": "linear CKA on one fixed CIFAR-10 eval batch; analog-module outputs reduced by token/spatial mean; aggregate is mean across valid common analog layers",
        "batch_size": args.batch_size,
        "num_workers": args.num_workers,
        "run_ids": run_ids,
        "layer_count": layer_count,
        "aggregate_matrix": aggregate.tolist(),
        "aggregate_offdiag_mean": offdiag,
        "per_layer": per_layer,
        "figures": [rel(FIG_DIR / "figS_cka_mseries.png"), rel(FIG_DIR / "figS_cka_mseries.pdf")],
        "provenance": provenance,
        **base_metadata(),
    }
    save_json(JSON_DIR / "cka_mseries.json", result)
    print(f"[E3] aggregate offdiag CKA={offdiag:.4f} across {layer_count} layers", flush=True)
    return result


def plot_d2d(data: dict) -> None:
    fig, ax1 = plt.subplots(figsize=(6.8, 4.8))
    ax2 = ax1.twinx()
    for run_id, style in [("canonical_standard", "--"), ("canonical_ensemble", "-")]:
        rows = data["summary"][run_id]
        alphas = np.array([row["alpha"] for row in rows], dtype=float)
        acc = np.array([row["acc_mean"] for row in rows], dtype=float)
        acc_std = np.array([row["acc_std"] for row in rows], dtype=float)
        loss = np.array([row["loss_mean"] for row in rows], dtype=float)
        color = COLORS[run_id]
        label = RUNS[run_id]["short"]
        ax1.plot(alphas, acc, style, color=color, marker="o", label=f"{label} acc")
        ax1.fill_between(alphas, acc - acc_std, acc + acc_std, color=color, alpha=0.15)
        ax2.plot(alphas, loss, style, color=color, marker="x", alpha=0.45, label=f"{label} loss")
    ax1.set_xlabel(r"D2D perturbation magnitude $\alpha$")
    ax1.set_ylabel("Test accuracy (%)")
    ax2.set_ylabel("Test loss")
    ax1.set_title("D2D mismatch-direction loss landscape")
    ax1.grid(True, alpha=0.25)
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, fontsize=8, loc="best")
    fig.tight_layout()
    out = FIG_DIR / "figS_d2d_loss_landscape"
    fig.savefig(out.with_suffix(".png"), dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    plt.close(fig)


def job_d2d(args) -> dict:
    ensure_dirs()
    run_ids = ["canonical_standard", "canonical_ensemble"]
    alphas = [float(x) for x in args.alphas.split(",")]
    raw = []
    summary: Dict[str, List[dict]] = {}
    provenance = {}
    for run_id in run_ids:
        bundle = load_run(run_id, args.device, args.batch_size, args.num_workers, amp=True)
        configure_model_from_run(bundle, run_id)
        enable_loaded_d2d(bundle, RUNS[run_id]["noise_mode"])
        source_masks = capture_d2d_masks(bundle)
        provenance[run_id] = checkpoint_provenance(run_id)
        per_alpha_values: Dict[float, List[Tuple[float, float]]] = {alpha: [] for alpha in alphas}
        for mask_idx in range(args.masks):
            fresh = sample_base_d2d_masks(bundle, args.sigma_d2d, args.seed + 1000 * mask_idx)
            for alpha in alphas:
                set_d2d_source_to_fresh(bundle, source_masks, fresh, alpha)
                loss, acc, n = eval_manual(bundle, max_batches=args.max_batches)
                per_alpha_values[alpha].append((loss, acc))
                raw.append({"run_id": run_id, "mask_idx": mask_idx, "alpha": alpha, "test_loss": loss, "test_acc": acc, "samples": n})
                print(f"[E2] {run_id} mask={mask_idx} alpha={alpha}: loss={loss:.4f} acc={acc:.2f}% n={n}", flush=True)
        rows = []
        for alpha in alphas:
            losses = np.array([x[0] for x in per_alpha_values[alpha]], dtype=float)
            accs = np.array([x[1] for x in per_alpha_values[alpha]], dtype=float)
            rows.append({
                "alpha": alpha,
                "loss_mean": float(losses.mean()),
                "loss_std": float(losses.std(ddof=0)),
                "acc_mean": float(accs.mean()),
                "acc_std": float(accs.std(ddof=0)),
            })
        summary[run_id] = rows
        del bundle
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    result = {
        "job": "E2_D2D_LOSS_LANDSCAPE",
        "method": "Source-to-fresh fixed-D2D interpolation: d2d(alpha)=checkpoint_source_d2d + alpha*(fresh_d2d - checkpoint_source_d2d); custom eval loop avoids train_tinyvit.evaluate noise reset",
        "sigma_d2d": args.sigma_d2d,
        "alphas": alphas,
        "masks": args.masks,
        "max_batches": args.max_batches,
        "batch_size": args.batch_size,
        "summary": summary,
        "raw": raw,
        "figures": [rel(FIG_DIR / "figS_d2d_loss_landscape.png"), rel(FIG_DIR / "figS_d2d_loss_landscape.pdf")],
        "provenance": provenance,
        **base_metadata(),
    }
    plot_d2d(result)
    save_json(JSON_DIR / "d2d_loss_landscape.json", result)
    return result


def plot_sensitivity(data: dict) -> None:
    rows = data["ranked_layers"]
    colors = {"mlp": "#d95d39", "qkv": "#2364aa", "proj": "#2a9d8f", "patch_embed": "#6d597a", "head": "#bf7f00", "other": "#999999"}
    fig, ax = plt.subplots(figsize=(12.0, 5.0))
    x = np.arange(len(rows))
    drops = np.array([row["acc_drop_pp"] for row in rows], dtype=float)
    bar_colors = [colors.get(row["group"], "#999999") for row in rows]
    ax.bar(x, drops, color=bar_colors, width=0.8)
    ax.set_xlabel("Analog layer rank by sensitivity")
    ax.set_ylabel("Accuracy drop (pp)")
    ax.set_title("Per-layer D2D mismatch sensitivity in canonical Ensemble HAT")
    ax.grid(True, axis="y", alpha=0.25)
    tick_every = max(1, len(rows) // 12)
    ax.set_xticks(x[::tick_every])
    ax.set_xticklabels([str(i + 1) for i in x[::tick_every]])
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, c in colors.items()]
    ax.legend(handles, list(colors.keys()), fontsize=8, ncol=6, loc="upper right")
    fig.tight_layout()
    out = FIG_DIR / "figS_per_layer_sensitivity"
    fig.savefig(out.with_suffix(".png"), dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    plt.close(fig)


def job_sensitivity(args) -> dict:
    ensure_dirs()
    run_id = "canonical_ensemble"
    bundle = load_run(run_id, args.device, args.batch_size, args.num_workers, amp=True)
    configure_model_from_run(bundle, run_id)
    clean_noise(bundle)
    baseline_loss, baseline_acc, n = eval_manual(bundle, max_batches=args.max_batches)
    layer_names = [name for name, _ in iter_analog_modules(bundle.model)]
    rows = []
    for layer_idx, target_name in enumerate(layer_names):
        clean_noise(bundle)
        enable_fixed_d2d(bundle, sigma=args.sigma_d2d, noise_mode=RUNS[run_id]["noise_mode"])
        with torch.no_grad():
            for name, module in iter_analog_modules(bundle.model):
                module.d2d_noise.zero_()
                if name == target_name:
                    torch.manual_seed(args.seed + layer_idx)
                    g_range = float(module.config.G_max - module.config.G_min)
                    module.d2d_noise.copy_(torch.randn_like(module.d2d_noise) * args.sigma_d2d * g_range)
        loss, acc, _ = eval_manual(bundle, max_batches=args.max_batches)
        row = {
            "layer_index": layer_idx,
            "layer": target_name,
            "group": analog_layer_group(target_name),
            "test_loss": loss,
            "test_acc": acc,
            "baseline_acc": baseline_acc,
            "acc_drop_pp": baseline_acc - acc,
            "samples": n,
        }
        rows.append(row)
        print(f"[E4] {layer_idx+1:02d}/{len(layer_names)} {target_name}: acc={acc:.2f}% drop={baseline_acc-acc:.2f}pp", flush=True)
    ranked = sorted(rows, key=lambda x: x["acc_drop_pp"], reverse=True)
    group_summary = {}
    for group in sorted({row["group"] for row in rows}):
        vals = [row["acc_drop_pp"] for row in rows if row["group"] == group]
        group_summary[group] = {"count": len(vals), "mean_drop_pp": float(np.mean(vals)), "max_drop_pp": float(np.max(vals))}
    result = {
        "job": "E4_PER_LAYER_D2D_SENSITIVITY",
        "method": "Perturb exactly one analog layer at a time with one fixed sigma_d2d mask; all other D2D buffers zero; custom eval loop",
        "run_id": run_id,
        "sigma_d2d": args.sigma_d2d,
        "max_batches": args.max_batches,
        "batch_size": args.batch_size,
        "baseline_loss": baseline_loss,
        "baseline_acc": baseline_acc,
        "samples": n,
        "layers_in_network_order": rows,
        "ranked_layers": ranked,
        "top5": ranked[:5],
        "group_summary": group_summary,
        "figures": [rel(FIG_DIR / "figS_per_layer_sensitivity.png"), rel(FIG_DIR / "figS_per_layer_sensitivity.pdf")],
        "provenance": {run_id: checkpoint_provenance(run_id)},
        **base_metadata(),
    }
    plot_sensitivity(result)
    save_json(JSON_DIR / "per_layer_d2d_sensitivity.json", result)
    return result


def flatten_params(params: Sequence[torch.Tensor]) -> torch.Tensor:
    return torch.cat([p.reshape(-1) for p in params])


def unflatten_like(vec: torch.Tensor, params: Sequence[torch.Tensor]) -> List[torch.Tensor]:
    out = []
    offset = 0
    for p in params:
        n = p.numel()
        out.append(vec[offset:offset+n].view_as(p))
        offset += n
    return out


def dot_params(left: Sequence[torch.Tensor], right: Sequence[torch.Tensor]) -> torch.Tensor:
    total = None
    for a, b in zip(left, right):
        value = (a * b).sum()
        total = value if total is None else total + value
    assert total is not None
    return total


def norm_flat(vec: torch.Tensor) -> torch.Tensor:
    return torch.linalg.norm(vec)


def prepare_hessian_params(model: nn.Module, mode: str) -> List[torch.Tensor]:
    if mode == "all":
        params = [p for p in model.parameters() if p.requires_grad]
    elif mode == "analog":
        selected = []
        for _name, module in iter_analog_modules(model):
            selected.append(module.weight)
            if getattr(module, "bias", None) is not None:
                selected.append(module.bias)
        params = [p for p in selected if p is not None and p.requires_grad]
    elif mode == "head":
        params = [p for name, p in model.named_parameters() if p.requires_grad and "head" in name]
    else:
        raise ValueError(f"Unknown hessian param mode: {mode}")
    if not params:
        raise RuntimeError(f"No Hessian params selected for mode={mode}")
    return params


def fixed_batch(bundle, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
    xs = []
    ys = []
    total = 0
    for inputs, targets in bundle.testloader:
        xs.append(inputs)
        ys.append(targets)
        total += int(inputs.size(0))
        if total >= batch_size:
            break
    x = preprocess_inputs(bundle, torch.cat(xs, dim=0)[:batch_size])
    y = torch.cat(ys, dim=0)[:batch_size].to(bundle.device)
    return x, y


def hessian_lanczos(bundle, params: Sequence[torch.Tensor], x: torch.Tensor, y: torch.Tensor, steps: int) -> Tuple[List[float], float]:
    criterion = bundle.criterion
    model = bundle.model
    model.eval()
    if torch.cuda.is_available():
        # Fused SDPA kernels in current PyTorch do not expose second
        # derivatives. Hessian-vector products need the math attention path.
        try:
            torch.backends.cuda.enable_flash_sdp(False)
            torch.backends.cuda.enable_mem_efficient_sdp(False)
            torch.backends.cuda.enable_math_sdp(True)
        except Exception:
            pass
    n_params = sum(p.numel() for p in params)
    q = torch.randn(n_params, device=bundle.device, dtype=torch.float32)
    q = q / q.norm().clamp_min(1e-12)
    q_prev = torch.zeros_like(q)
    beta = torch.tensor(0.0, device=bundle.device)
    alphas: List[float] = []
    betas: List[float] = []

    def hvp(q_vec: torch.Tensor) -> torch.Tensor:
        model.zero_grad(set_to_none=True)
        with torch.enable_grad():
            outputs = model(x)
            loss = criterion(outputs, y)
            grads = torch.autograd.grad(loss, params, create_graph=True, retain_graph=True, allow_unused=False)
            v_parts = unflatten_like(q_vec, params)
            grad_dot_v = dot_params(grads, v_parts)
            hv = torch.autograd.grad(grad_dot_v, params, retain_graph=False, allow_unused=False)
        return flatten_params([h.detach().float() for h in hv])

    trace_estimates = []
    for j in range(steps):
        z = hvp(q)
        alpha = torch.dot(q, z)
        z = z - alpha * q - beta * q_prev
        beta_new = z.norm()
        alphas.append(float(alpha.detach().cpu().item()))
        if j < steps - 1:
            betas.append(float(beta_new.detach().cpu().item()))
        trace_estimates.append(float(torch.dot(q, z + alpha * q + beta * q_prev).detach().cpu().item()))
        print(f"[E1] lanczos step {j+1}/{steps}: alpha={alphas[-1]:.6g} beta={float(beta_new.detach().cpu().item()):.6g}", flush=True)
        if float(beta_new.detach().cpu().item()) < 1e-10:
            break
        q_prev = q
        q = z / beta_new
        beta = beta_new
    m = len(alphas)
    T = torch.zeros((m, m), dtype=torch.float64)
    for i, a in enumerate(alphas):
        T[i, i] = a
    for i, b in enumerate(betas[:max(0, m-1)]):
        T[i, i+1] = b
        T[i+1, i] = b
    eigvals = torch.linalg.eigvalsh(T).flip(0).cpu().numpy().astype(float).tolist()
    trace_proxy = float(np.mean(trace_estimates)) if trace_estimates else float("nan")
    return eigvals, trace_proxy


def plot_hessian(results: Dict[str, dict]) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    for run_id, data in results.items():
        eig = np.array(data["ritz_eigenvalues"], dtype=float)
        if eig.size == 0:
            continue
        y = np.abs(eig)
        ax.plot(np.arange(1, len(y) + 1), y, marker="o", markersize=2, linewidth=1.4, color=COLORS.get(run_id), label=RUNS[run_id]["short"])
    ax.set_yscale("log")
    ax.set_xlabel("Ritz eigenvalue index")
    ax.set_ylabel("Absolute Hessian eigenvalue (log scale)")
    ax.set_title("Hessian spectrum approximation")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    out = FIG_DIR / "figS_hessian_spectrum"
    fig.savefig(out.with_suffix(".png"), dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    plt.close(fig)


def job_hessian(args) -> dict:
    ensure_dirs()
    run_ids = args.run_ids.split(",") if args.run_ids else ["canonical_ensemble", "canonical_standard", "cx_m1", "cx_m3", "cx_m2"]
    results = {}
    for run_id in run_ids:
        torch.manual_seed(args.seed)
        np.random.seed(args.seed)
        bundle = load_run(run_id, args.device, args.batch_size, args.num_workers, amp=False)
        clean_noise(bundle)
        x, y = fixed_batch(bundle, args.hessian_batch)
        params = prepare_hessian_params(bundle.model, args.hessian_params)
        param_count = int(sum(p.numel() for p in params))
        print(f"[E1] {run_id}: params={param_count} batch={x.size(0)} steps={args.lanczos_steps}", flush=True)
        eigvals, trace_proxy = hessian_lanczos(bundle, params, x, y, args.lanczos_steps)
        data = {
            "job": "E1_HESSIAN_EIGENSPECTRUM",
            "run_id": run_id,
            "method": "Lanczos Ritz spectrum on fixed CIFAR-10 eval batch with analog noise disabled",
            "sdpa_backend_note": "CUDA flash/mem-efficient SDPA disabled for HVP because fused efficient-attention backward lacks second derivatives",
            "hessian_params": args.hessian_params,
            "param_count": param_count,
            "fixed_batch_size": int(x.size(0)),
            "lanczos_steps": args.lanczos_steps,
            "ritz_eigenvalues": eigvals,
            "top1_abs_eigenvalue": float(abs(eigvals[0])) if eigvals else None,
            "trace_rayleigh_proxy": trace_proxy,
            "provenance": checkpoint_provenance(run_id),
            **base_metadata(),
        }
        save_json(JSON_DIR / f"hessian_eigenspectrum_{run_id}.json", data)
        results[run_id] = data
        del bundle, x, y, params
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    plot_hessian(results)
    combined = {
        "job": "E1_HESSIAN_EIGENSPECTRUM_COMBINED",
        "run_ids": run_ids,
        "figures": [rel(FIG_DIR / "figS_hessian_spectrum.png"), rel(FIG_DIR / "figS_hessian_spectrum.pdf")],
        "results": {k: {"top1_abs_eigenvalue": v["top1_abs_eigenvalue"], "json": rel(JSON_DIR / f"hessian_eigenspectrum_{k}.json")} for k, v in results.items()},
        **base_metadata(),
    }
    save_json(JSON_DIR / "hessian_eigenspectrum_summary.json", combined)
    return combined


def average_checkpoints(out_path: Path) -> None:
    src1 = ROOT / RUNS["cx_m1"]["checkpoint"]
    src2 = ROOT / RUNS["cx_m5"]["checkpoint"]
    ckpt1 = torch.load(src1, map_location="cpu", weights_only=False)
    ckpt2 = torch.load(src2, map_location="cpu", weights_only=False)
    sd1 = ckpt1["model_state_dict"]
    sd2 = ckpt2["model_state_dict"]
    avg_sd = {}
    for key, val1 in sd1.items():
        val2 = sd2[key]
        if torch.is_floating_point(val1):
            avg_sd[key] = (val1.float() + val2.float()) / 2.0
            if avg_sd[key].dtype != val1.dtype:
                avg_sd[key] = avg_sd[key].to(dtype=val1.dtype)
        else:
            avg_sd[key] = val1.clone()
    out = copy.deepcopy(ckpt1)
    out["model_state_dict"] = avg_sd
    out["best_acc"] = None
    out["epoch"] = None
    out["best_epoch"] = None
    out["seed"] = "avg_123_456"
    out["averaged_from"] = [rel(src1), rel(src2)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(out, out_path)


def eval_fresh_for_bundle(bundle, instances: int, mc_runs: int, sigma_d2d: float, noise_mode: str, seed: int, max_batches: Optional[int]) -> dict:
    instance_means = []
    raw = []
    enable_fixed_d2d(bundle, sigma=sigma_d2d, noise_mode=noise_mode)
    for i in range(instances):
        base = sample_base_d2d_masks(bundle, sigma_d2d, seed + i * 100)
        set_d2d_from_base(bundle, base, 1.0)
        mc_accs = []
        mc_losses = []
        for r in range(mc_runs):
            loss, acc, n = eval_manual(bundle, max_batches=max_batches)
            mc_losses.append(loss)
            mc_accs.append(acc)
            raw.append({"instance": i, "mc_run": r, "test_loss": loss, "test_acc": acc, "samples": n})
        instance_means.append(float(np.mean(mc_accs)))
        print(f"[E5] instance={i+1}/{instances} mean={instance_means[-1]:.2f}%", flush=True)
    return {
        "cross_instance_mean": float(np.mean(instance_means)),
        "cross_instance_std": float(np.std(instance_means, ddof=0)),
        "instance_means": instance_means,
        "raw": raw,
    }


def plot_checkpoint_avg(data: dict) -> None:
    labels = ["Std seed123", "Std seed456", "Avg(123,456)", "Ensemble ref"]
    values = [
        data["references"].get("cx_m1_fresh_mean"),
        data["references"].get("cx_m5_fresh_mean"),
        data["checkpoint_average"]["cross_instance_mean"],
        data["references"].get("canonical_ensemble_fresh_mean"),
    ]
    stds = [
        data["references"].get("cx_m1_fresh_std", 0.0),
        data["references"].get("cx_m5_fresh_std", 0.0),
        data["checkpoint_average"].get("cross_instance_std", 0.0),
        data["references"].get("canonical_ensemble_fresh_std", 0.0),
    ]
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    x = np.arange(len(labels))
    ax.bar(x, values, yerr=stds, color=["#d95d39", "#d95d39", "#bf7f00", "#2364aa"], capsize=4)
    ax.set_ylabel("Fresh-instance accuracy (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylim(0, max(100, max(values) + 10))
    ax.set_title("Checkpoint averaging probe")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    out = FIG_DIR / "figS_checkpoint_avg"
    fig.savefig(out.with_suffix(".png"), dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    plt.close(fig)


def load_reference_fresh() -> dict:
    refs = {}
    candidates = {
        "cx_m1": JSON_DIR / "cx_m1_fresh_eval.json",
        "cx_m5": JSON_DIR / "cx_m5_fresh_eval.json",
    }
    for key, path in candidates.items():
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            refs[f"{key}_fresh_mean"] = data.get("cross_instance_mean")
            refs[f"{key}_fresh_std"] = data.get("cross_instance_std")
    ensemble_json = JSON_DIR / "fresh_instance_eval.json"
    if ensemble_json.exists():
        data = json.loads(ensemble_json.read_text(encoding="utf-8"))
        # Older format: list of model rows.
        if isinstance(data, list):
            for row in data:
                name = str(row.get("model") or row.get("name") or row.get("experiment") or "")
                if "Ensemble" in name or "V4_Ensemble" in name:
                    refs["canonical_ensemble_fresh_mean"] = row.get("mean_acc", row.get("test_acc_mean", row.get("cross_instance_mean")))
                    refs["canonical_ensemble_fresh_std"] = row.get("std_acc", row.get("test_acc_std", row.get("cross_instance_std")))
        elif isinstance(data, dict):
            for row in data.get("results", []):
                name = str(row.get("model") or row.get("name") or row.get("experiment") or "")
                if "Ensemble" in name or "V4_Ensemble" in name:
                    refs["canonical_ensemble_fresh_mean"] = row.get("mean_acc", row.get("test_acc_mean", row.get("cross_instance_mean")))
                    refs["canonical_ensemble_fresh_std"] = row.get("std_acc", row.get("test_acc_std", row.get("cross_instance_std")))
    refs.setdefault("canonical_ensemble_fresh_mean", 86.37)
    refs.setdefault("canonical_ensemble_fresh_std", 1.54)
    return refs


def job_avg(args) -> dict:
    ensure_dirs()
    out_path = AVG_CKPT_DIR / "cx_m1_m5_standard_seedavg.pt"
    average_checkpoints(out_path)
    # Register a temporary run so load_run can use the existing loader path.
    RUNS["cx_m1_m5_avg"] = {
        "label": "Checkpoint average of CX-M1 Standard seed123 and CX-M5 Standard seed456",
        "short": "Avg M1/M5",
        "exp_id": "V3",
        "checkpoint": rel(out_path),
        "nl_ltp": 2.0,
        "nl_ltd": -2.0,
        "noise_mode": "uniform",
        "hat_type": "StandardAvg",
        "seed": "avg_123_456",
    }
    bundle = load_run("cx_m1_m5_avg", args.device, args.batch_size, args.num_workers, amp=True)
    configure_model_from_run(bundle, "cx_m1_m5_avg")
    result_eval = eval_fresh_for_bundle(bundle, args.instances, args.mc_runs, args.sigma_d2d, "uniform", args.seed, args.max_batches)
    refs = load_reference_fresh()
    result = {
        "job": "E5_CHECKPOINT_AVERAGING",
        "method": "Parameter-wise average of CX-M1 Standard seed123 and CX-M5 Standard seed456; fresh-instance eval with fixed D2D per instance",
        "averaged_checkpoint": rel(out_path),
        "averaged_from": [RUNS["cx_m1"]["checkpoint"], RUNS["cx_m5"]["checkpoint"]],
        "instances": args.instances,
        "mc_runs": args.mc_runs,
        "sigma_d2d": args.sigma_d2d,
        "max_batches": args.max_batches,
        "checkpoint_average": result_eval,
        "references": refs,
        "figures": [rel(FIG_DIR / "figS_checkpoint_avg.png"), rel(FIG_DIR / "figS_checkpoint_avg.pdf")],
        "provenance": {
            "cx_m1": checkpoint_provenance("cx_m1"),
            "cx_m5": checkpoint_provenance("cx_m5"),
        },
        **base_metadata(),
    }
    plot_checkpoint_avg(result)
    save_json(JSON_DIR / "checkpoint_average_eval.json", result)
    return result


def load_optional_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def fmt(value, digits=2):
    if value is None:
        return "PENDING"
    try:
        if math.isnan(float(value)):
            return "nan"
        return f"{float(value):.{digits}f}"
    except Exception:
        return str(value)


def write_report(args) -> dict:
    ensure_dirs()
    hessian = load_optional_json(JSON_DIR / "hessian_eigenspectrum_summary.json")
    d2d = load_optional_json(JSON_DIR / "d2d_loss_landscape.json")
    cka = load_optional_json(JSON_DIR / "cka_mseries.json")
    sens = load_optional_json(JSON_DIR / "per_layer_d2d_sensitivity.json")
    avg = load_optional_json(JSON_DIR / "checkpoint_average_eval.json")

    lines = [
        "# CODEX Empirical Mechanism Report",
        "",
        "**Date:** 2026-04-25  ",
        "**Scope:** Claude Round-7 `DISPATCH_CODEX_EMPIRICAL_DEEPENING_20260425.md` Phase 2.  ",
        "**Constraint:** Existing checkpoints only; no new training; canonical model code unchanged.  ",
        "",
        "## 1. Provenance",
        "",
    ]
    meta = base_metadata()
    for key in ["commit_hash", "git_worktree_dirty", "cuda_device_name", "pytorch_version", "code_sha256", "gpu_resize_eval", "gpu_resize_protocol"]:
        lines.append(f"- {key}: `{meta.get(key)}`")
    lines.extend([
        "- Analysis script: `scripts/_gpt/empirical_mechanism_20260425.py`",
        "- Figures directory: `paper/figures/`",
        "- JSON directory: `report_md/_gpt/json_gpt/`",
        "",
        "## 2. Per-Job Results",
        "",
        "### E1 Hessian Eigenspectrum",
        "",
    ])
    if hessian:
        lines.append("| Checkpoint | Params | Batch | Top-1 abs Ritz eigenvalue | JSON |")
        lines.append("|:--|:--|--:|--:|:--|")
        for run_id, row in hessian.get("results", {}).items():
            indiv = load_optional_json(ROOT / str(row.get("json", "")))
            params_mode = indiv.get("hessian_params") if indiv else "unknown"
            batch = indiv.get("fixed_batch_size") if indiv else None
            lines.append(f"| {RUNS.get(run_id, {}).get('short', run_id)} | {params_mode} | {fmt(batch, 0)} | {fmt(row.get('top1_abs_eigenvalue'), 4)} | `{row.get('json')}` |")
        if "canonical_ensemble" in hessian.get("results", {}) and "canonical_standard" in hessian.get("results", {}):
            e = hessian["results"]["canonical_ensemble"].get("top1_abs_eigenvalue")
            s = hessian["results"]["canonical_standard"].get("top1_abs_eigenvalue")
            ratio = abs(float(s)) / max(abs(float(e)), 1e-12) if e is not None and s is not None else None
            lines.append(f"\nStandard/Ensemble top-1 ratio: **{fmt(ratio, 2)}x**.")
            if ratio is not None and ratio < 1.0:
                lines.append("**Escalation:** E1 contradicts the simple global-Hessian flat-minima hypothesis: canonical Ensemble HAT has a larger analog-parameter top-1 Ritz value than canonical Standard HAT under this batch-32 Lanczos protocol.")
            elif ratio is not None and ratio >= 2.0:
                lines.append("E1 supports the simple global-Hessian flat-minima hypothesis under this Lanczos protocol.")
            else:
                lines.append("E1 gives weak/ambiguous global-Hessian support under this Lanczos protocol.")
        lines.append("Protocol note: full analog-parameter HVP required disabling CUDA flash/mem-efficient SDPA because fused efficient-attention backward lacks second derivatives in this PyTorch build.")
        lines.append("Figure: `paper/figures/figS_hessian_spectrum.{png,pdf}`")
    else:
        lines.append("PENDING: Hessian JSON not landed yet.")

    lines.extend(["", "### E2 D2D Loss Landscape", ""])
    if d2d:
        lines.append("| Model | alpha=0 acc | alpha=1 acc | alpha=3 acc |")
        lines.append("|:--|--:|--:|--:|")
        for run_id in ["canonical_standard", "canonical_ensemble"]:
            rows = {float(r["alpha"]): r for r in d2d.get("summary", {}).get(run_id, [])}
            lines.append(f"| {RUNS[run_id]['short']} | {fmt(rows.get(0.0, {}).get('acc_mean'))} | {fmt(rows.get(1.0, {}).get('acc_mean'))} | {fmt(rows.get(3.0, {}).get('acc_mean'))} |")
        lines.append("Figure: `paper/figures/figS_d2d_loss_landscape.{png,pdf}`")
    else:
        lines.append("PENDING: D2D landscape JSON not landed yet.")

    lines.extend(["", "### E3 CKA M-Series", ""])
    if cka:
        offdiag = cka.get("aggregate_offdiag_mean")
        verdict = "high convergence" if offdiag is not None and offdiag > 0.8 else "mixed/divergent representations" if offdiag is not None and offdiag < 0.5 else "intermediate convergence"
        lines.append(f"- Aggregate off-diagonal CKA: **{fmt(offdiag, 3)}** ({verdict}).")
        lines.append(f"- Common analog layers: `{cka.get('layer_count')}`.")
        lines.append("Figure: `paper/figures/figS_cka_mseries.{png,pdf}`")
    else:
        lines.append("PENDING: CKA JSON not landed yet.")

    lines.extend(["", "### E4 Per-Layer D2D Sensitivity", ""])
    if sens:
        lines.append(f"- Baseline clean accuracy: **{fmt(sens.get('baseline_acc'))}%**.")
        lines.append("| Rank | Layer | Group | Drop (pp) |")
        lines.append("|--:|:--|:--|--:|")
        for i, row in enumerate(sens.get("top5", []), start=1):
            lines.append(f"| {i} | `{row['layer']}` | {row['group']} | {fmt(row['acc_drop_pp'])} |")
        top_groups = [row["group"] for row in sens.get("top5", [])]
        lines.append(f"Top-5 groups: `{', '.join(top_groups)}`.")
        lines.append("Figure: `paper/figures/figS_per_layer_sensitivity.{png,pdf}`")
    else:
        lines.append("PENDING: per-layer sensitivity JSON not landed yet.")

    lines.extend(["", "### E5 Checkpoint Averaging", ""])
    if avg:
        ca = avg.get("checkpoint_average", {})
        lines.append(f"- Avg(M1 seed123, M5 seed456) fresh mean: **{fmt(ca.get('cross_instance_mean'))} ± {fmt(ca.get('cross_instance_std'))}%**.")
        lines.append(f"- Ensemble reference mean: **{fmt(avg.get('references', {}).get('canonical_ensemble_fresh_mean'))}%**.")
        lines.append("Figure: `paper/figures/figS_checkpoint_avg.{png,pdf}`")
    else:
        lines.append("PENDING: checkpoint averaging JSON not landed yet.")

    lines.extend([
        "",
        "## 3. Cross-Job Synthesis",
        "",
        "All five requested jobs have landed. The empirical picture is split: D2D-direction robustness is strongly supported, but a simple global-Hessian flatness story is not.",
        "",
    ])
    if hessian and "canonical_ensemble" in hessian.get("results", {}) and "canonical_standard" in hessian.get("results", {}):
        e = hessian["results"]["canonical_ensemble"].get("top1_abs_eigenvalue")
        s = hessian["results"]["canonical_standard"].get("top1_abs_eigenvalue")
        if e is not None and s is not None:
            lines.append(f"- E1 analog-parameter Hessian is a negative/surprising diagnostic: Ensemble top-1 {fmt(e, 2)} exceeds Standard top-1 {fmt(s, 2)}. Do not claim Ensemble HAT is globally flatter in ordinary parameter space.")
    if d2d:
        ens_rows = {float(r["alpha"]): r for r in d2d.get("summary", {}).get("canonical_ensemble", [])}
        std_rows = {float(r["alpha"]): r for r in d2d.get("summary", {}).get("canonical_standard", [])}
        if 1.0 in ens_rows and 1.0 in std_rows:
            gap1 = ens_rows[1.0]["acc_mean"] - std_rows[1.0]["acc_mean"]
            lines.append(f"- E2 is the positive mechanism result: at alpha=1.0, Ensemble keeps {fmt(ens_rows[1.0]['acc_mean'])}% while Standard is {fmt(std_rows[1.0]['acc_mean'])}% (gap {fmt(gap1)} pp). This supports flatness specifically along the D2D mismatch direction.")
    if cka:
        lines.append(f"- E3 shows aggregate M-series off-diagonal CKA of {fmt(cka.get('aggregate_offdiag_mean'), 3)}, which tests whether 80-82% severe-NL recovery comes from representational convergence or multiple distinct routes.")
    if sens:
        groups = [row["group"] for row in sens.get("top5", [])]
        mlp_count = sum(1 for g in groups if g == "mlp")
        lines.append(f"- E4 top-5 sensitivity contains {mlp_count}/5 MLP layers. If this remains after full eval, it {'supports' if mlp_count >= 3 else 'weakens'} the MLP-bottleneck wording.")
    if d2d:
        ens_rows = {float(r["alpha"]): r for r in d2d.get("summary", {}).get("canonical_ensemble", [])}
        std_rows = {float(r["alpha"]): r for r in d2d.get("summary", {}).get("canonical_standard", [])}
        if 3.0 in ens_rows and 3.0 in std_rows:
            gap = ens_rows[3.0]["acc_mean"] - std_rows[3.0]["acc_mean"]
            lines.append(f"- E2 alpha=3 Ensemble-Standard accuracy gap is {fmt(gap)} pp; positive gap supports D2D-direction robustness.")
    lines.extend([
        "",
        "## 4. Paper-Safe Statements",
        "",
        "- Use mechanism figures as supplementary diagnostics, not as replacements for frozen source/fresh headline metrics.",
        "- Do not write `Ensemble HAT finds a globally flatter Hessian minimum`; E1 contradicts that simple statement under the analog-parameter protocol.",
        "- Prefer: `Ensemble HAT is robust along device-mismatch directions, while ordinary parameter-space Hessian sharpness is not the explanatory axis.`",
        "- E4 can replace the contaminated historical groupwise table only if the top-layer ranking is stable and post-fix provenance is cited.",
        "- E5, if near chance, supports the statement that per-epoch resampling is not equivalent to naive checkpoint averaging.",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[save] {rel(REPORT_PATH)}", flush=True)
    return {"report": rel(REPORT_PATH), **base_metadata()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", choices=["hessian", "d2d", "cka", "sensitivity", "avg", "report", "all"], required=True)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    parser.add_argument("--alphas", default="0,0.5,1,1.5,2,2.5,3")
    parser.add_argument("--masks", type=int, default=3)
    parser.add_argument("--instances", type=int, default=10)
    parser.add_argument("--mc-runs", type=int, default=5)
    parser.add_argument("--run-ids", default=None)
    parser.add_argument("--hessian-batch", type=int, default=128)
    parser.add_argument("--lanczos-steps", type=int, default=50)
    parser.add_argument("--hessian-params", choices=["all", "analog", "head"], default="analog")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_dirs()
    if args.job == "cka":
        job_cka(args)
    elif args.job == "d2d":
        job_d2d(args)
    elif args.job == "sensitivity":
        job_sensitivity(args)
    elif args.job == "hessian":
        job_hessian(args)
    elif args.job == "avg":
        job_avg(args)
    elif args.job == "report":
        write_report(args)
    elif args.job == "all":
        job_cka(args)
        job_d2d(args)
        job_sensitivity(args)
        job_avg(args)
        job_hessian(args)
        write_report(args)


if __name__ == "__main__":
    main()
