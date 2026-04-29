#!/usr/bin/env python3
"""
Phase A1.3: Physical Noise Injection Evaluation Pipeline

Replaces the flawed CIFAR-10-C front-end test with a physically grounded pipeline:

  Path 1 (compensated): X → InverseGamma → PhotocurrentSim(mode='compensated') → network
  Path 2 (raw):          X → PhotocurrentSim(mode='raw') → network (control group)

Sweep parameters:
  - gamma_phys: [0.5, 0.7, 1.0, 1.5, 2.0]
  - I_dark: [10 pA, 100 pA, 1 nA, 10 nA]
  - shot_noise: [on, off]

Outputs:
  - Per-configuration Top-1 accuracy on CIFAR-10 test set
  - 3D heatmap data (gamma × I_dark × accuracy) for compensated vs raw
  - CSV and JSON exports for downstream analysis

Important:
  This script is primarily an A1.3 pipeline-validation utility. If it is run with
  an untrained model, the exported markdown must be treated as a legacy validation
  artifact rather than the canonical A2.3 physical-compensation result.

Reference: claude全栈参考手册.md §4.1, §4.2; claude-report.md A1.3
"""

import argparse
import csv
import itertools
import json
import os
import time
from dataclasses import dataclass
from typing import List, Tuple

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from analog_layers import (
    InverseGammaPreprocessor,
    PhotocurrentSimulator,
)
from report_asset_paths import asset_path


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

@dataclass
class PipelineConfig:
    """Sweep configuration for physical noise injection experiments."""
    gamma_phys_values: Tuple[float, ...] = (0.5, 0.7, 1.0, 1.5, 2.0)
    I_dark_values: Tuple[float, ...] = (1e-11, 1e-10, 1e-9, 1e-8)  # 10pA to 10nA
    shot_noise_values: Tuple[bool, ...] = (True, False)
    alpha: float = 1.0           # responsivity
    batch_size: int = 128
    num_workers: int = 2
    data_root: str = "./data"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


# ─────────────────────────────────────────────
# Physical Noise Injection Wrapper
# ─────────────────────────────────────────────

class PhysicalNoiseInjector(nn.Module):
    """Wraps InverseGammaPreprocessor + PhotocurrentSimulator into a single
    differentiable transform that can be prepended to any vision model.

    Modes:
      - 'compensated': applies inverse-gamma then physical model (linearized)
      - 'raw': applies physical model directly (non-linear, control group)
      - 'clean': bypass, no physical preprocessing
    """

    def __init__(self, gamma_phys: float = 0.7, alpha: float = 1.0,
                 I_dark: float = 1e-10, shot_noise: bool = True):
        super().__init__()
        self.inverse_gamma = InverseGammaPreprocessor(gamma_phys=gamma_phys, alpha=alpha)
        self.photo_sim = PhotocurrentSimulator(
            alpha=alpha, I_dark=I_dark, gamma_phys=gamma_phys, shot_noise=shot_noise
        )
        self.gamma_phys = gamma_phys

    def forward(self, x: torch.Tensor, mode: str = 'compensated') -> torch.Tensor:
        """
        Args:
            x: Image tensor in [0, 1], shape (B, C, H, W)
            mode: 'compensated', 'raw', or 'clean'
        Returns:
            Processed image tensor, normalized back to ~[0, 1] range
        """
        if mode == 'clean':
            return x

        if mode == 'compensated':
            P_in, _ = self.inverse_gamma(x)
            I_out = self.photo_sim(P_in, mode='compensated')
        elif mode == 'raw':
            I_out = self.photo_sim(x, mode='raw')
        else:
            raise ValueError(f"Unknown mode '{mode}'")

        # Normalize output to [0, 1] range for network input
        # I_out = alpha * signal + I_dark + noise
        # We re-normalize per-sample to preserve relative structure
        B = I_out.shape[0]
        I_flat = I_out.view(B, -1)
        I_min = I_flat.min(dim=1, keepdim=True).values
        I_max = I_flat.max(dim=1, keepdim=True).values
        I_range = (I_max - I_min).clamp(min=1e-8)

        # Reshape min/max for broadcasting
        shape = [B] + [1] * (I_out.dim() - 1)
        I_min = I_min.view(shape)
        I_range = I_range.view(shape)

        return (I_out - I_min) / I_range


# ─────────────────────────────────────────────
# Evaluation
# ─────────────────────────────────────────────

@torch.no_grad()
def evaluate_accuracy(model: nn.Module, injector: PhysicalNoiseInjector,
                      dataloader, mode: str, device: str) -> float:
    """Evaluate Top-1 accuracy with physical noise injection.

    Args:
        model: Classification model
        injector: PhysicalNoiseInjector instance
        dataloader: CIFAR-10 test loader
        mode: 'compensated', 'raw', or 'clean'
        device: torch device string

    Returns:
        Top-1 accuracy (0-100)
    """
    model.eval()
    injector.eval()
    correct = 0
    total = 0

    for images, labels in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        # Apply physical noise injection
        images_processed = injector(images, mode=mode)

        outputs = model(images_processed)
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)

    return 100.0 * correct / total


def get_cifar10_loader(batch_size: int = 128, num_workers: int = 2,
                       data_root: str = "./data"):
    """Get CIFAR-10 test set loader with normalization to [0, 1]."""
    transform = transforms.Compose([
        transforms.ToTensor(),  # [0, 1] range
    ])

    testset = torchvision.datasets.CIFAR10(
        root=data_root, train=False, download=True, transform=transform
    )
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    return testloader


def get_simple_resnet(device: str = "cpu", num_classes: int = 10):
    """Get a ResNet-18 model adapted for CIFAR-10 (32×32 input).

    Uses standard torchvision ResNet-18 with modified first conv and no maxpool
    for small input sizes.
    """
    import torchvision.models as models
    model = models.resnet18(weights=None, num_classes=num_classes)
    # Adapt for CIFAR-10 (32×32): smaller first conv, no maxpool
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()
    return model.to(device)


# ─────────────────────────────────────────────
# Main sweep
# ─────────────────────────────────────────────

def run_sweep(cfg: PipelineConfig, model: nn.Module, verbose: bool = True):
    """Run the full parameter sweep.

    Args:
        cfg: PipelineConfig with sweep parameters
        model: Pre-trained classification model
        verbose: Print progress

    Returns:
        List of result dicts
    """
    device = cfg.device
    model = model.to(device)
    model.eval()

    testloader = get_cifar10_loader(cfg.batch_size, cfg.num_workers, cfg.data_root)

    results = []
    total_configs = (len(cfg.gamma_phys_values) * len(cfg.I_dark_values)
                     * len(cfg.shot_noise_values) * 2)  # ×2 for compensated + raw
    run_idx = 0

    # First: clean baseline (no physical preprocessing)
    injector_clean = PhysicalNoiseInjector(gamma_phys=1.0, shot_noise=False).to(device)
    acc_clean = evaluate_accuracy(model, injector_clean, testloader, 'clean', device)
    results.append({
        'mode': 'clean', 'gamma_phys': None, 'I_dark': None,
        'shot_noise': None, 'accuracy': acc_clean
    })
    if verbose:
        print(f"[Baseline] Clean accuracy: {acc_clean:.2f}%")

    # Sweep
    for gamma, I_dark, shot in itertools.product(
        cfg.gamma_phys_values, cfg.I_dark_values, cfg.shot_noise_values
    ):
        injector = PhysicalNoiseInjector(
            gamma_phys=gamma, alpha=cfg.alpha, I_dark=I_dark, shot_noise=shot
        ).to(device)

        for mode in ['compensated', 'raw']:
            run_idx += 1
            t0 = time.time()
            acc = evaluate_accuracy(model, injector, testloader, mode, device)
            elapsed = time.time() - t0

            result = {
                'mode': mode,
                'gamma_phys': gamma,
                'I_dark': I_dark,
                'I_dark_label': format_current(I_dark),
                'shot_noise': shot,
                'accuracy': acc,
                'elapsed_s': round(elapsed, 2),
            }
            results.append(result)

            if verbose:
                print(f"[{run_idx}/{total_configs}] γ={gamma}, I_dark={format_current(I_dark)}, "
                      f"shot={'on' if shot else 'off'}, mode={mode:12s} → "
                      f"acc={acc:.2f}%  ({elapsed:.1f}s)")

    return results


def format_current(I: float) -> str:
    """Format current value in human-readable units."""
    if I >= 1e-6:
        return f"{I*1e6:.0f}µA"
    elif I >= 1e-9:
        return f"{I*1e9:.0f}nA"
    elif I >= 1e-12:
        return f"{I*1e12:.0f}pA"
    else:
        return f"{I:.2e}A"


# ─────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────

def export_results(results: List[dict], output_dir: str = "report_md",
                   report_name: str = "physical_noise_report.md",
                   legacy_validation: bool = True,
                   model_label: str = "Untrained ResNet-18",
                   canonical_a23_report: str = "a23_physical_compensation_report.md"):
    """Export sweep results to CSV and JSON."""
    os.makedirs(output_dir, exist_ok=True)

    # CSV — collect all possible fieldnames across all result dicts
    csv_path = asset_path(output_dir, "csv", "physical_noise_sweep.csv")
    all_keys = []
    for r in results:
        for k in r.keys():
            if k not in all_keys:
                all_keys.append(k)
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    print(f"\nCSV exported to: {csv_path}")

    # JSON
    json_path = asset_path(output_dir, "json", "physical_noise_sweep.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"JSON exported to: {json_path}")

    # Markdown summary table
    md_path = os.path.join(output_dir, report_name)
    with open(md_path, 'w') as f:
        if legacy_validation:
            f.write("# Physical Noise Injection Sweep Results (Legacy A1.3 Validation)\n\n")
            f.write("> Status: legacy pipeline validation only.\n")
            f.write("> Model: ")
            f.write(f"{model_label}.\n")
            f.write("> Do not cite this file as the canonical A2.3 result.\n")
            f.write(f"> Canonical A2.3 report: `{canonical_a23_report}`.\n\n")
        else:
            f.write("# Physical Noise Injection Sweep Results\n\n")

        f.write("## Experiment Design\n\n")
        f.write("Two-path comparison:\n")
        f.write("- **Compensated**: X → InverseGamma(γ) → PhotocurrentSim → Network\n")
        f.write("- **Raw**: X → PhotocurrentSim → Network (control)\n\n")

        # Clean baseline
        clean = [r for r in results if r['mode'] == 'clean']
        if clean:
            f.write(f"**Clean baseline (no physical preprocessing):** {clean[0]['accuracy']:.2f}%\n\n")
            if legacy_validation:
                f.write("Expected behavior for this artifact: chance-level accuracy (~10%) is "
                        "normal because the model was not trained for A2.3.\n\n")

        # Delta accuracy table (compensated - raw)
        f.write("## Delta Accuracy (Compensated − Raw)\n\n")
        f.write("Positive values = compensation helps.\n\n")

        sweep_results = [r for r in results if r['mode'] != 'clean']
        # Get unique values
        gammas = sorted(set(r['gamma_phys'] for r in sweep_results))
        darks = sorted(set(r['I_dark'] for r in sweep_results))
        shots = sorted(set(r['shot_noise'] for r in sweep_results))

        for shot in shots:
            f.write(f"\n### Shot noise: {'ON' if shot else 'OFF'}\n\n")
            f.write("| γ_phys \\ I_dark |")
            for d in darks:
                f.write(f" {format_current(d)} |")
            f.write("\n|:---:|" + ":---:|" * len(darks) + "\n")

            for g in gammas:
                f.write(f"| {g} |")
                for d in darks:
                    comp = [r for r in sweep_results
                            if r['gamma_phys'] == g and r['I_dark'] == d
                            and r['shot_noise'] == shot and r['mode'] == 'compensated']
                    raw = [r for r in sweep_results
                           if r['gamma_phys'] == g and r['I_dark'] == d
                           and r['shot_noise'] == shot and r['mode'] == 'raw']
                    if comp and raw:
                        delta = comp[0]['accuracy'] - raw[0]['accuracy']
                        sign = "+" if delta >= 0 else ""
                        f.write(f" {sign}{delta:.2f}% |")
                    else:
                        f.write(" — |")
                f.write("\n")

        # Full results table
        f.write("\n## Full Results\n\n")
        f.write("| Mode | γ_phys | I_dark | Shot | Accuracy |\n")
        f.write("|:-----|:------:|:------:|:----:|:--------:|\n")
        for r in results:
            mode = r['mode']
            gamma = r.get('gamma_phys', '—') or '—'
            dark = r.get('I_dark_label', '—') or '—'
            shot = '—'
            if r.get('shot_noise') is not None:
                shot = 'on' if r['shot_noise'] else 'off'
            f.write(f"| {mode} | {gamma} | {dark} | {shot} | {r['accuracy']:.2f}% |\n")

    print(f"Markdown report exported to: {md_path}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Physical Noise Injection Pipeline (A1.3)")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--device", type=str, default=None,
                        help="Device (default: auto-detect)")
    parser.add_argument("--quick", action="store_true",
                        help="Quick mode: reduced sweep for testing")
    parser.add_argument("--output-dir", type=str, default="report_md")
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Configure sweep
    if args.quick:
        cfg = PipelineConfig(
            gamma_phys_values=(0.7, 1.0),
            I_dark_values=(1e-10, 1e-9),
            shot_noise_values=(True,),
            batch_size=args.batch_size,
            data_root=args.data_root,
            device=device,
        )
        print("Quick mode: reduced sweep (2 gamma × 2 I_dark × 1 shot × 2 modes = 8 runs)")
    else:
        cfg = PipelineConfig(
            batch_size=args.batch_size,
            data_root=args.data_root,
            device=device,
        )
        total = (len(cfg.gamma_phys_values) * len(cfg.I_dark_values)
                 * len(cfg.shot_noise_values) * 2)
        print(f"Full sweep: {total} configurations + 1 clean baseline")

    legacy_validation = True
    model_label = "Untrained ResNet-18 (A1.3 pipeline validation only)"

    # Load model (untrained ResNet-18 for now — accuracy will be random ~10%)
    # This is intentionally kept as a legacy validation path; the canonical
    # A2.3 evaluation lives in run_a23_experiments.py with the trained R4 model.
    print("\nLoading ResNet-18 (untrained, for legacy pipeline validation)...")
    model = get_simple_resnet(device=device, num_classes=10)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Run sweep
    print("\n" + "=" * 70)
    print("Starting Physical Noise Injection Sweep")
    print("=" * 70 + "\n")

    results = run_sweep(cfg, model, verbose=True)

    # Export
    print("\n" + "=" * 70)
    print("Exporting Results")
    print("=" * 70)
    export_results(
        results,
        output_dir=args.output_dir,
        legacy_validation=legacy_validation,
        model_label=model_label,
    )

    # Quick summary
    sweep_results = [r for r in results if r['mode'] != 'clean']
    comp_accs = [r['accuracy'] for r in sweep_results if r['mode'] == 'compensated']
    raw_accs = [r['accuracy'] for r in sweep_results if r['mode'] == 'raw']
    if comp_accs and raw_accs:
        print(f"\nCompensated: mean={sum(comp_accs)/len(comp_accs):.2f}%, "
              f"range=[{min(comp_accs):.2f}, {max(comp_accs):.2f}]")
        print(f"Raw:         mean={sum(raw_accs)/len(raw_accs):.2f}%, "
              f"range=[{min(raw_accs):.2f}, {max(raw_accs):.2f}]")

    print("\nDone! Legacy pipeline validation completed successfully.")
    print("Note: Accuracy is ~10% because this script uses an untrained model.")
    print("For the canonical A2.3 result, use run_a23_experiments.py / a23_physical_compensation_report.md.")


if __name__ == "__main__":
    main()
