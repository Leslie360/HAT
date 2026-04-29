#!/usr/bin/env python3
"""
Phase A1.1: Tiny-ViT-5M Model Profiling & Crossbar Array Mapping

Loads Tiny-ViT-5M, classifies each layer as analog (crossbar-mapped) or digital,
computes crossbar array requirements under 128×128 differential pair scheme,
and outputs summary tables for paper inclusion.

Reference: claude全栈参考手册.md §1.1, §1.2
"""

import json
import math
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import torch
import torch.nn as nn

from report_asset_paths import asset_path
from tinyvit_hybrid_utils import classify_tinyvit_layer, crossbar_array_count, is_depthwise_conv

try:
    import timm
except ImportError:
    print("ERROR: timm not installed. Run: pip install timm")
    sys.exit(1)

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
ARRAY_SIZE = 128          # 128×128 crossbar array
MODEL_NAME = "tiny_vit_5m_224"
NUM_CLASSES = 1000        # ImageNet-1k (default timm uses 21841 for 21k)


# ─────────────────────────────────────────────
# Layer info extraction
# ─────────────────────────────────────────────

@dataclass
class LayerInfo:
    name: str
    layer_type: str            # e.g. "Linear", "Conv2d", "DWConv2d"
    weight_shape: tuple        # raw weight tensor shape
    M: int                     # effective rows for crossbar mapping
    N: int                     # effective cols for crossbar mapping
    param_count: int           # total learnable params (weight + bias)
    tag: str                   # "analog" or "digital"
    # crossbar info (only for analog layers)
    n_row_tiles: int = 0
    n_col_tiles: int = 0
    arrays_single: int = 0
    arrays_diff_pair: int = 0


def extract_layer_info(name: str, module: nn.Module) -> Optional[LayerInfo]:
    """Extract profiling information from a Conv2d or Linear module."""
    if isinstance(module, nn.Linear):
        w = module.weight
        M, N = w.shape[0], w.shape[1]  # (out_features, in_features)
        param_count = w.numel() + (module.bias.numel() if module.bias is not None else 0)
        return LayerInfo(
            name=name,
            layer_type="Linear",
            weight_shape=tuple(w.shape),
            M=M, N=N,
            param_count=param_count,
            tag="",
        )
    elif isinstance(module, nn.Conv2d):
        w = module.weight
        param_count = w.numel() + (module.bias.numel() if module.bias is not None else 0)
        if is_depthwise_conv(module):
            # DWConv: (C, 1, kH, kW) — not suitable for crossbar
            C = w.shape[0]
            k = w.shape[2] * w.shape[3]
            return LayerInfo(
                name=name,
                layer_type=f"DWConv2d(g={module.groups},k={module.kernel_size})",
                weight_shape=tuple(w.shape),
                M=C, N=k,
                param_count=param_count,
                tag="",
            )
        else:
            # Standard Conv2d: (C_out, C_in, kH, kW) → unroll to M=C_out, N=C_in*kH*kW
            C_out, C_in, kH, kW = w.shape
            M = C_out
            N = C_in * kH * kW
            kernel_str = f"k={module.kernel_size},s={module.stride}"
            return LayerInfo(
                name=name,
                layer_type=f"Conv2d({kernel_str})",
                weight_shape=tuple(w.shape),
                M=M, N=N,
                param_count=param_count,
                tag="",
            )
    return None


def compute_crossbar(info: LayerInfo) -> LayerInfo:
    """Compute crossbar array requirements for an analog layer."""
    if info.tag != "analog":
        return info
    row_tiles, col_tiles, diff_arrays = crossbar_array_count(info.M, info.N, array_size=ARRAY_SIZE)
    info.n_row_tiles = row_tiles
    info.n_col_tiles = col_tiles
    info.arrays_single = row_tiles * col_tiles
    info.arrays_diff_pair = diff_arrays
    return info


# ─────────────────────────────────────────────
# Catch uncategorized parameters
# ─────────────────────────────────────────────

def find_uncategorized_params(model: nn.Module, categorized_names: set) -> List[dict]:
    """Find parameters not captured by Conv2d/Linear iteration (e.g. attention_biases)."""
    uncategorized = []
    for pname, param in model.named_parameters():
        # Check if this param belongs to any categorized module
        matched = False
        for cname in categorized_names:
            if pname.startswith(cname):
                matched = True
                break
        if not matched:
            uncategorized.append({
                "name": pname,
                "shape": tuple(param.shape),
                "numel": param.numel(),
                "tag": "digital",  # uncategorized params default to digital
            })
    return uncategorized


# ─────────────────────────────────────────────
# Output formatting
# ─────────────────────────────────────────────

def format_shape(shape: tuple) -> str:
    return "×".join(str(s) for s in shape)


def print_detailed_table(layers: List[LayerInfo], uncategorized: List[dict]):
    """Print a detailed table of all profiled layers."""
    headers = ["Layer Name", "Type", "Weight Shape", "M×N", "Params", "Tag", "Arrays(diff)"]
    rows = []
    for l in layers:
        mn_str = f"{l.M}×{l.N}" if l.M > 0 else "—"
        arr_str = str(l.arrays_diff_pair) if l.arrays_diff_pair > 0 else "—"
        rows.append([
            l.name, l.layer_type, format_shape(l.weight_shape),
            mn_str, f"{l.param_count:,}", l.tag, arr_str
        ])

    for u in uncategorized:
        rows.append([
            u["name"], "Parameter", format_shape(u["shape"]),
            "—", f"{u['numel']:,}", u["tag"], "—"
        ])

    if tabulate:
        print(tabulate(rows, headers=headers, tablefmt="pipe"))
    else:
        # Fallback: simple formatted print
        print(" | ".join(headers))
        print("-" * 120)
        for row in rows:
            print(" | ".join(str(x) for x in row))


def print_summary(layers: List[LayerInfo], uncategorized: List[dict], total_model_params: int):
    """Print summary statistics."""
    analog_params = sum(l.param_count for l in layers if l.tag == "analog")
    digital_params_layers = sum(l.param_count for l in layers if l.tag == "digital")
    digital_params_uncat = sum(u["numel"] for u in uncategorized)
    digital_params = digital_params_layers + digital_params_uncat
    categorized_total = analog_params + digital_params

    total_arrays = sum(l.arrays_diff_pair for l in layers if l.tag == "analog")
    total_devices = total_arrays * ARRAY_SIZE * ARRAY_SIZE

    analog_ratio = analog_params / categorized_total * 100 if categorized_total > 0 else 0

    print("\n" + "=" * 70)
    print("SUMMARY: Tiny-ViT-5M Crossbar Array Mapping")
    print("=" * 70)
    print(f"  Model total params (from model):   {total_model_params:>12,}")
    print(f"  Categorized params (from scan):    {categorized_total:>12,}")
    if categorized_total != total_model_params:
        print(f"  ⚠ Discrepancy:                     {total_model_params - categorized_total:>12,}")
    print(f"  ───────────────────────────────────────────")
    print(f"  Analog-mapped params:              {analog_params:>12,}  ({analog_ratio:.1f}%)")
    print(f"  Digital params:                    {digital_params:>12,}  ({100 - analog_ratio:.1f}%)")
    print(f"  ───────────────────────────────────────────")
    print(f"  Crossbar array size:               {ARRAY_SIZE}×{ARRAY_SIZE}")
    print(f"  Weight scheme:                     Differential pair (2× arrays)")
    print(f"  Total crossbar arrays (diff pair): {total_arrays:>12,}")
    print(f"  Total crossbar devices:            {total_devices:>12,}")
    print()

    return {
        "total_model_params": total_model_params,
        "analog_params": analog_params,
        "digital_params": digital_params,
        "analog_ratio_pct": round(analog_ratio, 2),
        "total_arrays_diff_pair": total_arrays,
        "total_devices": total_devices,
    }


def export_markdown_table(layers: List[LayerInfo], uncategorized: List[dict], summary: dict):
    """Generate a markdown table suitable for paper inclusion (Tab.2)."""
    lines = []
    lines.append("## Table 2: Tiny-ViT-5M Layer Mapping and Crossbar Array Requirements\n")

    # Grouped by stage
    lines.append("| Layer | Type | Dimensions (M×N) | Params | Domain | Arrays (diff pair) |")
    lines.append("|:------|:-----|:-----------------:|-------:|:------:|-------------------:|")

    # Group layers by stage prefix
    stage_groups = {}
    for l in layers:
        # Determine group
        if "patch_embed" in l.name:
            group = "Patch Embedding"
        elif l.name.startswith("stages.0"):
            group = "Stage 0 (MBConv)"
        elif "stages.1.downsample" in l.name:
            group = "Stage 1 Downsample"
        elif l.name.startswith("stages.1"):
            group = "Stage 1 (Attention)"
        elif "stages.2.downsample" in l.name:
            group = "Stage 2 Downsample"
        elif l.name.startswith("stages.2"):
            group = "Stage 2 (Attention)"
        elif "stages.3.downsample" in l.name:
            group = "Stage 3 Downsample"
        elif l.name.startswith("stages.3"):
            group = "Stage 3 (Attention)"
        elif "head" in l.name:
            group = "Classification Head"
        else:
            group = "Other"

        if group not in stage_groups:
            stage_groups[group] = []
        stage_groups[group].append(l)

    group_order = [
        "Patch Embedding",
        "Stage 0 (MBConv)",
        "Stage 1 Downsample", "Stage 1 (Attention)",
        "Stage 2 Downsample", "Stage 2 (Attention)",
        "Stage 3 Downsample", "Stage 3 (Attention)",
        "Classification Head", "Other",
    ]

    for group in group_order:
        if group not in stage_groups:
            continue
        group_layers = stage_groups[group]
        group_params = sum(l.param_count for l in group_layers)
        group_arrays = sum(l.arrays_diff_pair for l in group_layers)
        tag = group_layers[0].tag  # predominant tag

        # Collapse similar layers in same group
        # Show individual layers for clarity
        for l in group_layers:
            mn_str = f"{l.M}×{l.N}"
            arr_str = str(l.arrays_diff_pair) if l.arrays_diff_pair > 0 else "—"
            short_name = l.name
            lines.append(
                f"| {short_name} | {l.layer_type} | {mn_str} | "
                f"{l.param_count:,} | {l.tag} | {arr_str} |"
            )

        # Group subtotal
        arr_sub = str(group_arrays) if group_arrays > 0 else "—"
        lines.append(
            f"| **{group} subtotal** | | | "
            f"**{group_params:,}** | | **{arr_sub}** |"
        )

    # Uncategorized params
    if uncategorized:
        uncat_total = sum(u["numel"] for u in uncategorized)
        lines.append(f"| Other parameters (attn biases, etc.) | — | — | "
                      f"{uncat_total:,} | digital | — |")

    lines.append("")
    lines.append(f"**Total parameters:** {summary['total_model_params']:,}  ")
    lines.append(f"**Analog-mapped:** {summary['analog_params']:,} ({summary['analog_ratio_pct']:.1f}%)  ")
    lines.append(f"**Digital:** {summary['digital_params']:,} ({100 - summary['analog_ratio_pct']:.1f}%)  ")
    lines.append(f"**Total 128×128 crossbar arrays (differential pair):** {summary['total_arrays_diff_pair']}  ")
    lines.append(f"**Total devices:** {summary['total_devices']:,}  ")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print(f"Loading model: {MODEL_NAME}")
    model = timm.create_model(MODEL_NAME, pretrained=False, num_classes=NUM_CLASSES)
    model.eval()

    # Total model params
    total_model_params = sum(p.numel() for p in model.parameters())
    print(f"Total model parameters: {total_model_params:,}\n")

    # Iterate all named modules, extract info for Conv2d and Linear layers
    layers: List[LayerInfo] = []
    categorized_module_names = set()

    for name, module in model.named_modules():
        info = extract_layer_info(name, module)
        if info is None:
            continue
        info.tag = classify_tinyvit_layer(name, module)
        info = compute_crossbar(info)
        layers.append(info)
        categorized_module_names.add(name + ".")

    # Find any uncategorized parameters (attention biases, etc.)
    uncategorized = find_uncategorized_params(model, categorized_module_names)

    # Print detailed table
    print("\n── Detailed Layer Profiling ──\n")
    print_detailed_table(layers, uncategorized)

    # Print summary
    summary = print_summary(layers, uncategorized, total_model_params)

    # Export markdown for paper
    md_content = export_markdown_table(layers, uncategorized, summary)
    md_path = "report_md/array_mapping_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\nMarkdown table exported to: {md_path}")

    # Export JSON for downstream scripts
    json_data = {
        "model_name": MODEL_NAME,
        "summary": summary,
        "layers": [asdict(l) for l in layers],
        "uncategorized_params": uncategorized,
    }
    json_path = asset_path("report_md", "json", "array_mapping_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"JSON data exported to: {json_path}")


if __name__ == "__main__":
    main()
