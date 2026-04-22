#!/usr/bin/env python3
"""Qualitative attention-map visualization for Tiny-ViT checkpoints."""

from __future__ import annotations

import argparse
import json
import os
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms

from report_asset_paths import asset_path
from train_tinyvit import DATASET_STATS, build_model, get_v_experiment_configs


DEFAULT_JSON_PATH = asset_path("report_md/_gpt", "json", "attention_maps_gpt.json")
DEFAULT_MD_PATH = "report_md/_gpt/attention_maps_gpt.md"
DEFAULT_FIGURE_PATH = "paper/figures/fig_attention_maps.png"
DEFAULT_DIFF_PATH = "paper/figures/fig_attention_differences.png"
DEFAULT_LOG_PATH = "logs/_gpt/visualize_attention_gpt.log"
DEFAULT_IMAGE_INDICES = [0, 23, 37]
DEFAULT_EXPERIMENT_ORDER = ["V1", "V3", "V4", "V6"]

plt.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "DejaVu Serif"],
    "font.style": "normal",
    "font.size": 8,
    "axes.titlesize": 8,
    "axes.titleweight": "semibold",
    "axes.labelsize": 8,
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "mathtext.fontset": "stix",
    "mathtext.default": "regular",
})


class RunLogger:
    """Minimal local logger to avoid coupling visualization to training internals."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        ensure_parent_dir(log_path)
        self._fh = open(log_path, "w", encoding="utf-8")

    def log(self, message: str):
        self._fh.write(f"{message}\n")
        self._fh.flush()

    def close(self):
        self._fh.close()


def ensure_parent_dir(path: Optional[str]):
    if not path:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def save_figure(fig, output_path: str, **kwargs):
    kwargs.setdefault("dpi", 300)
    fig.savefig(output_path, **kwargs)
    root, ext = os.path.splitext(output_path)
    if ext.lower() == ".png":
        fig.savefig(f"{root}.pdf", **kwargs)


def get_eval_transform():
    stats = DATASET_STATS["cifar10"]
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])


def get_display_transform():
    return transforms.Resize((224, 224))


def load_cifar10_test_dataset(data_root: str):
    return torchvision.datasets.CIFAR10(root=data_root, train=False, download=True)


def find_representative_indices(dataset, target_class_names: Sequence[str]) -> List[int]:
    class_to_index = {name: idx for idx, name in enumerate(dataset.classes)}
    targets = [class_to_index[name] for name in target_class_names if name in class_to_index]
    found: List[int] = []
    seen = set()
    for index, (_image, label) in enumerate(dataset):
        if label in targets and label not in seen:
            found.append(index)
            seen.add(label)
        if len(found) == len(targets):
            break
    return found


def resolve_visualization_indices(dataset, explicit_indices: Optional[Sequence[int]],
                                  target_class_names: Sequence[str]) -> List[int]:
    if explicit_indices:
        return [int(idx) for idx in explicit_indices]
    if DEFAULT_IMAGE_INDICES:
        return list(DEFAULT_IMAGE_INDICES)
    return find_representative_indices(dataset, target_class_names)


class AttentionCapture(AbstractContextManager):
    """Temporarily patch a Tiny-ViT attention module to capture softmax attention."""

    def __init__(self, module):
        self.module = module
        self.attn: Optional[torch.Tensor] = None
        self._original_forward = None
        self._original_fused_attn = None

    def __enter__(self):
        self._original_forward = self.module.forward
        self._original_fused_attn = self.module.fused_attn
        self.module.fused_attn = False

        def patched_forward(x):
            attn_bias = self.module.get_attention_biases(x.device)
            B, N, _ = x.shape
            x_norm = self.module.norm(x)
            qkv = self.module.qkv(x_norm)
            q, k, v = qkv.view(B, N, self.module.num_heads, -1).split(
                [self.module.key_dim, self.module.key_dim, self.module.val_dim], dim=3
            )
            q = q.permute(0, 2, 1, 3)
            k = k.permute(0, 2, 1, 3)
            v = v.permute(0, 2, 1, 3)
            q = q * self.module.scale
            attn = q @ k.transpose(-2, -1)
            attn = attn + attn_bias
            attn = attn.softmax(dim=-1)
            self.attn = attn.detach().cpu()
            out = attn @ v
            out = out.transpose(1, 2).reshape(B, N, self.module.out_dim)
            out = self.module.proj(out)
            return out

        self.module.forward = patched_forward
        return self

    def __exit__(self, exc_type, exc, tb):
        self.module.forward = self._original_forward
        self.module.fused_attn = self._original_fused_attn
        return False


def aggregate_attention_map(attn: torch.Tensor, resolution: Tuple[int, int],
                            mode: str = "mean_queries") -> np.ndarray:
    if attn.dim() != 4:
        raise ValueError(f"Expected attention tensor with shape [B,H,N,N], got {tuple(attn.shape)}")
    head_mean = attn[0].mean(dim=0)  # [N, N]
    if mode == "center_query":
        vector = head_mean[head_mean.shape[0] // 2]
    else:
        vector = head_mean.mean(dim=0)
    attn_map = vector.view(*resolution).numpy()
    attn_map = attn_map - attn_map.min()
    max_val = attn_map.max()
    if max_val > 0:
        attn_map = attn_map / max_val
    return attn_map


def resolve_checkpoint_path(exp_id: str, checkpoint_dir: str, explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    exp_cfg = get_v_experiment_configs()[exp_id]
    return os.path.join(checkpoint_dir, f"{exp_cfg.name}_best.pt")


def load_model_for_experiment(exp_id: str, checkpoint_path: str, device: str):
    configs = get_v_experiment_configs()
    exp_cfg = configs[exp_id]
    model = build_model(exp_cfg, num_classes=10, device=device, pretrained=False)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return model, ckpt


def extract_attention_map(model, target_layer: str, image_tensor: torch.Tensor,
                          aggregate_mode: str = "mean_queries"):
    modules = dict(model.named_modules())
    if target_layer not in modules:
        raise KeyError(f"Target attention layer not found: {target_layer}")
    attn_module = modules[target_layer]
    with AttentionCapture(attn_module) as capture:
        with torch.no_grad():
            logits = model(image_tensor)
    if capture.attn is None:
        raise RuntimeError(f"Failed to capture attention from layer: {target_layer}")
    
    attn_probs = capture.attn[0]
    entropy_per_query = -torch.sum(attn_probs * torch.log(attn_probs + 1e-9), dim=-1)
    mean_entropy = entropy_per_query.mean().item()
    
    attn_map = aggregate_attention_map(capture.attn, attn_module.resolution, mode=aggregate_mode)
    prediction = int(logits.argmax(dim=1).item())
    return attn_map, prediction, mean_entropy


def overlay_heatmap(ax, image_np: np.ndarray, heatmap: np.ndarray, title: str = "", row_label: Optional[str] = None):
    ax.imshow(image_np)
    ax.imshow(heatmap, cmap="magma", alpha=0.45, interpolation="bilinear")
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=9.5, pad=4)
    if row_label is not None:
        ax.set_ylabel(row_label, rotation=90, fontsize=11)


def plot_attention_grid(samples: List[dict], output_path: str):
    ensure_parent_dir(output_path)
    rows = DEFAULT_EXPERIMENT_ORDER
    # Add one extra row for input image reference
    fig, axes = plt.subplots(len(rows) + 1, len(samples), figsize=(3.9 * len(samples), 2.9 * (len(rows) + 1)))
    if len(samples) == 1:
        axes = axes.reshape(len(rows) + 1, 1)
    
    for col, sample in enumerate(samples):
        # Top row: Input reference
        ax_top = axes[0, col]
        ax_top.imshow(sample["image_np"])
        ax_top.set_title(f"Input: {sample['label_name']} (id {sample['index']})", fontsize=10)
        ax_top.set_xticks([])
        ax_top.set_yticks([])
        if col == 0:
            ax_top.set_ylabel("Original", rotation=90, fontsize=11, labelpad=10)

        for row_idx, exp_id in enumerate(rows):
            overlay_heatmap(
                axes[row_idx + 1, col],
                sample["image_np"],
                sample["maps"][exp_id],
                row_label=exp_id if col == 0 else None
            )

    # Add a global colorbar
    cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.7])
    sm = plt.cm.ScalarMappable(cmap="magma", norm=plt.Normalize(vmin=0, vmax=1))
    fig.colorbar(sm, cax=cbar_ax, label="Attention Intensity")

    fig.subplots_adjust(top=0.94, bottom=0.06, left=0.1, right=0.91, wspace=0.05, hspace=0.2)
    save_figure(fig, output_path, bbox_inches="tight")
    plt.close(fig)


def plot_difference_grid(samples: List[dict], output_path: str):
    ensure_parent_dir(output_path)
    rows = [("V3", "|V3 - V1|"), ("V4", "|V4 - V1|"), ("V6", "|V6 - V1|")]
    fig, axes = plt.subplots(len(rows), len(samples), figsize=(3.9 * len(samples), 2.9 * len(rows)))
    if len(samples) == 1:
        axes = np.array(axes).reshape(len(rows), 1)

    for col, sample in enumerate(samples):
        baseline = sample["maps"]["V1"]
        for row_idx, (exp_id, label) in enumerate(rows):
            diff = np.abs(sample["maps"][exp_id] - baseline)
            overlay_heatmap(
                axes[row_idx, col],
                sample["image_np"],
                diff,
            )

    fig.subplots_adjust(top=0.95, bottom=0.04, wspace=0.03, hspace=0.06)
    save_figure(fig, output_path, bbox_inches="tight")
    plt.close(fig)


def build_markdown(samples: List[dict], target_layer: str, figure_path: str, diff_path: str) -> str:
    lines = [
        "# Attention Visualization Results (GPT)",
        "",
        f"- Target layer: `{target_layer}`",
        f"- Main figure: `{figure_path}`",
        f"- Difference figure: `{diff_path}`",
        "",
        "| Sample idx | Label | V1 pred | V3 pred | V4 pred | V6 pred |",
        "|-----------:|:------|:--------|:--------|:--------|:--------|",
    ]
    for sample in samples:
        lines.append(
            f"| {sample['index']} | {sample['label_name']} | {sample['predictions']['V1']} | "
            f"{sample['predictions']['V3']} | {sample['predictions']['V4']} | "
            f"{sample['predictions']['V6']} |"
        )
    lines.extend([
        "",
        "## Notes",
        "",
        f"- Default paper samples use fixed CIFAR-10 indices `{DEFAULT_IMAGE_INDICES}` for reproducibility.",
        "- Heatmaps are generated from head-averaged attention after softmax.",
        "- The default aggregation averages over all query tokens to highlight globally attended spatial regions.",
        "- Difference panels use absolute deviation relative to the V1 digital baseline.",
        "",
    ])
    return "\n".join(lines) + "\n"


def export_metadata(samples: List[dict], json_path: str, md_path: str,
                    target_layer: str, figure_path: str, diff_path: str):
    ensure_parent_dir(json_path)
    ensure_parent_dir(md_path)
    payload = {
        "target_layer": target_layer,
        "samples": [
            {
                "index": sample["index"],
                "label_name": sample["label_name"],
                "predictions": sample["predictions"],
                "mean_entropy": sample.get("mean_entropy", {}),
            }
            for sample in samples
        ],
        "figure_path": figure_path,
        "difference_figure_path": diff_path,
    }
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(build_markdown(samples, target_layer, figure_path, diff_path))


def main():
    parser = argparse.ArgumentParser(description="Visualize Tiny-ViT attention maps for V1/V3/V4/V6 checkpoints.")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--v1-checkpoint", type=str, default=None)
    parser.add_argument("--v3-checkpoint", type=str, default=None)
    parser.add_argument("--v4-checkpoint", type=str, default=None)
    parser.add_argument("--v6-checkpoint", type=str, default=None)
    parser.add_argument("--target-layer", type=str, default="stages.3.blocks.0.attn")
    parser.add_argument("--aggregate-mode", choices=["mean_queries", "center_query"], default="mean_queries")
    parser.add_argument("--indices", nargs="+", type=int, default=None)
    parser.add_argument("--class-names", nargs="+", default=["bird", "cat", "ship", "truck"])
    parser.add_argument("--figure-path", type=str, default=DEFAULT_FIGURE_PATH)
    parser.add_argument("--difference-figure-path", type=str, default=DEFAULT_DIFF_PATH)
    parser.add_argument("--results-json-path", type=str, default=DEFAULT_JSON_PATH)
    parser.add_argument("--results-md-path", type=str, default=DEFAULT_MD_PATH)
    parser.add_argument("--log-path", type=str, default=DEFAULT_LOG_PATH)
    args = parser.parse_args()

    torch.manual_seed(42)
    np.random.seed(42)
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    try:
        dataset = load_cifar10_test_dataset(args.data_root)
        indices = resolve_visualization_indices(dataset, args.indices, args.class_names)
        if not indices:
            raise ValueError("No representative CIFAR-10 indices found. Pass --indices explicitly.")

        logger.log(f"Device: {device}")
        logger.log(f"Target layer: {args.target_layer}")
        logger.log(f"Selected indices: {indices}")

        eval_transform = get_eval_transform()
        display_transform = get_display_transform()

        checkpoint_paths = {
            "V1": resolve_checkpoint_path("V1", args.checkpoint_dir, args.v1_checkpoint),
            "V3": resolve_checkpoint_path("V3", args.checkpoint_dir, args.v3_checkpoint),
            "V4": resolve_checkpoint_path("V4", args.checkpoint_dir, args.v4_checkpoint),
            "V6": resolve_checkpoint_path("V6", args.checkpoint_dir, args.v6_checkpoint),
        }
        for exp_id, path in checkpoint_paths.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"Required checkpoint for {exp_id} not found: {path}")

        models = {}
        for exp_id, path in checkpoint_paths.items():
            model, ckpt = load_model_for_experiment(exp_id, path, device)
            models[exp_id] = model
            logger.log(f"{exp_id}: checkpoint={path}, epoch={ckpt.get('epoch')}, best_acc={ckpt.get('best_acc')}")

        samples = []
        for index in indices:
            image, label = dataset[index]
            image_tensor = eval_transform(image).unsqueeze(0).to(device)
            image_np = np.asarray(display_transform(image), dtype=np.float32) / 255.0
            label_name = dataset.classes[label]
            sample_record = {
                "index": index,
                "label_name": label_name,
                "image_np": image_np,
                "maps": {},
                "predictions": {},
                "mean_entropy": {},
            }
            for exp_id, model in models.items():
                attn_map, pred_idx, mean_entropy = extract_attention_map(
                    model,
                    target_layer=args.target_layer,
                    image_tensor=image_tensor,
                    aggregate_mode=args.aggregate_mode,
                )
                sample_record["maps"][exp_id] = attn_map
                sample_record["predictions"][exp_id] = dataset.classes[pred_idx]
                sample_record["mean_entropy"][exp_id] = round(float(mean_entropy), 4)
            samples.append(sample_record)

        plot_attention_grid(samples, args.figure_path)
        plot_difference_grid(samples, args.difference_figure_path)
        export_metadata(
            samples,
            json_path=args.results_json_path,
            md_path=args.results_md_path,
            target_layer=args.target_layer,
            figure_path=args.figure_path,
            diff_path=args.difference_figure_path,
        )

        logger.log(f"Figure: {args.figure_path}")
        logger.log(f"Difference figure: {args.difference_figure_path}")
        logger.log(f"JSON: {args.results_json_path}")
        logger.log(f"Markdown: {args.results_md_path}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
