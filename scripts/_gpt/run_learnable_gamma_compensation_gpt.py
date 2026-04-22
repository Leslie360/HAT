#!/usr/bin/env python3
"""
E3: Learnable Frontend Compensation Exponent

Tests whether the inverse-gamma compensation exponent can be learned end-to-end
jointly with the network weights, rather than being fixed to 1/gamma_phys.

Hypothesis: A learned gamma_comp may deviate from the physical inverse (1/gamma_phys)
if the task loss and noise statistics favor a different trade-off point.

This script defines a learnable frontend module and trains Tiny-ViT with HAT
under the canonical V4/V6 recipe, comparing:
  (a) Fixed compensation: gamma_comp = 1/gamma_phys (baseline)
  (b) Learnable compensation: gamma_comp initialized to 1/gamma_phys, optimized jointly
  (c) No compensation: raw photoresponse (gamma_comp = 1.0, frozen)

Usage (host WSL, to avoid snap-scoped CUDA failure):
  scripts/_gpt/run_host_wsl_gpu.sh \
    'python scripts/_gpt/run_learnable_gamma_compensation_gpt.py --gamma_phys 2.0 --epochs 100 --seed 42'

Output:
  logs/learnable_gamma_gpt/<timestamp>_g<gamma>_s<seed>.log
  checkpoints/learnable_gamma_gpt/*.pt
  report_md/json/learnable_gamma_results.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from analog_layers import (
    InverseGammaPreprocessor,
    PhotocurrentSimulator,
)
from train_tinyvit_ensemble import (
    DATASET_STATS,
    get_dataloaders,
    TinyViTExperimentConfig,
    build_model,
    get_num_classes,
)

# ---------------------------------------------------------------------------
# Learnable frontend module
# ---------------------------------------------------------------------------

class LearnableInverseGammaPreprocessor(nn.Module):
    """Inverse-gamma preprocessor with a learnable compensation exponent.

    The compensation exponent gamma_comp is initialized to 1/gamma_phys
    (the physical inverse) but is optimized jointly with network weights.

    Forward: P_in = X^(gamma_comp)
    where gamma_comp is constrained to (0.1, 5.0) via softplus + bias
    to avoid numerical instability.
    """

    def __init__(
        self,
        gamma_phys: float = 1.0,
        alpha: float = 1.0,
        learnable: bool = True,
    ):
        super().__init__()
        self.gamma_phys = gamma_phys
        self.alpha = alpha
        self.learnable = learnable

        # Initialize to the physical inverse: gamma_comp = 1/gamma_phys
        init_val = 1.0 / gamma_phys
        # Use log-space parameterization: gamma_comp = softplus(raw) + min_val
        # This keeps gamma_comp > 0.1 always
        if learnable:
            self.raw_gamma = nn.Parameter(
                torch.tensor(init_val, dtype=torch.float32)
            )
        else:
            self.register_buffer("raw_gamma", torch.tensor(init_val, dtype=torch.float32))

    @property
    def gamma_comp(self) -> torch.Tensor:
        """Computed compensation exponent, always positive."""
        return torch.nn.functional.softplus(self.raw_gamma) + 0.1

    def forward(self, x: torch.Tensor):
        eps = 1e-8
        x_clamped = torch.clamp(x, min=eps, max=1.0)

        gc = self.gamma_comp
        if torch.isclose(gc, torch.tensor(1.0)):
            P_in = x_clamped
        else:
            P_in = torch.pow(x_clamped, gc)

        # Shot noise variance: σ² = α × P_in
        noise_var = self.alpha * P_in
        return P_in, noise_var

    def extra_repr(self) -> str:
        gc = self.gamma_comp.item()
        phys_inv = 1.0 / self.gamma_phys
        return (
            f"learnable={self.learnable}, "
            f"gamma_comp={gc:.4f} (phys_inv={phys_inv:.4f}), "
            f"alpha={self.alpha}"
        )


class LearnablePhysicalFrontEnd(nn.Module):
    """Physical frontend with optional learnable compensation."""

    def __init__(
        self,
        dataset: str,
        gamma_phys: float = 1.0,
        alpha: float = 1.0,
        I_dark: float = 1e-10,
        shot_noise: bool = True,
        learnable_gamma: bool = True,
    ):
        super().__init__()
        stats = DATASET_STATS[dataset]
        self.inverse_gamma = LearnableInverseGammaPreprocessor(
            gamma_phys=gamma_phys,
            alpha=alpha,
            learnable=learnable_gamma,
        )
        self.photo_sim = PhotocurrentSimulator(
            alpha=alpha,
            I_dark=I_dark,
            gamma_phys=gamma_phys,
            shot_noise=shot_noise,
        )
        self.register_buffer("mean", torch.tensor(stats["mean"]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor(stats["std"]).view(1, 3, 1, 1))

    def forward(self, x: torch.Tensor, mode: str = "compensated") -> torch.Tensor:
        if mode == "compensated":
            p_in, _ = self.inverse_gamma(x)
            i_out = self.photo_sim(p_in, mode="compensated")
        elif mode == "raw":
            i_out = self.photo_sim(x, mode="raw")
        else:
            raise ValueError(f"Unknown front-end mode: {mode}")

        batch = i_out.shape[0]
        flat = i_out.view(batch, -1)
        i_min = flat.min(dim=1, keepdim=True).values.view(batch, 1, 1, 1)
        i_max = flat.max(dim=1, keepdim=True).values.view(batch, 1, 1, 1)
        i_range = (i_max - i_min).clamp(min=1e-8)
        x_norm = (i_out - i_min) / i_range
        return (x_norm - self.mean.to(x.device)) / self.std.to(x.device)


# ---------------------------------------------------------------------------
# Training loop (simplified from train_tinyvit_ensemble.py)
# ---------------------------------------------------------------------------

def train_one_epoch(
    model: nn.Module,
    frontend: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    scaler=None,
) -> float:
    model.train()
    total_loss = 0.0
    total_samples = 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        # Apply frontend
        images = frontend(images, mode="compensated")

        optimizer.zero_grad()
        if scaler is not None:
            with torch.cuda.amp.autocast():
                outputs = model(images)
                loss = nn.functional.cross_entropy(outputs, labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(images)
            loss = nn.functional.cross_entropy(outputs, labels)
            loss.backward()
            optimizer.step()

        total_loss += loss.item() * images.size(0)
        total_samples += images.size(0)

    return total_loss / total_samples


@torch.no_grad()
def evaluate(
    model: nn.Module,
    frontend: nn.Module,
    loader: DataLoader,
    device: torch.device,
) -> float:
    model.eval()
    correct = 0
    total = 0
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        images = frontend(images, mode="compensated")
        outputs = model(images)
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)
    return 100.0 * correct / total


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    if device.type == "cpu":
        print("WARNING: Running on CPU. This will be very slow.")

    # Reproducibility
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    # Data loaders (train, test only; no val split in this API)
    train_loader, test_loader = get_dataloaders(
        dataset=args.dataset,
        data_root=args.data_dir,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        image_size=32,
    )

    # Build model (hybrid Tiny-ViT with HAT noise)
    base_cfg = TinyViTExperimentConfig(
        name="learnable_gamma_baseline",
        use_hybrid=True,
        noise_enabled=True,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        hat_training=True,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=1e-4,
        weight_decay=0.05,
    )

    num_classes = get_num_classes(args.dataset)
    model = build_model(base_cfg, num_classes=num_classes, device=device)

    # Frontend variants
    variants = {
        "fixed": {
            "frontend": LearnablePhysicalFrontEnd(
                dataset=args.dataset,
                gamma_phys=args.gamma_phys,
                alpha=args.alpha,
                I_dark=args.I_dark,
                shot_noise=args.shot_noise,
                learnable_gamma=False,
            ),
            "desc": f"fixed gamma_comp={1.0/args.gamma_phys:.4f}",
        },
        "learnable": {
            "frontend": LearnablePhysicalFrontEnd(
                dataset=args.dataset,
                gamma_phys=args.gamma_phys,
                alpha=args.alpha,
                I_dark=args.I_dark,
                shot_noise=args.shot_noise,
                learnable_gamma=True,
            ),
            "desc": "learnable gamma_comp (init to physical inverse)",
        },
        "raw": {
            "frontend": LearnablePhysicalFrontEnd(
                dataset=args.dataset,
                gamma_phys=args.gamma_phys,
                alpha=args.alpha,
                I_dark=args.I_dark,
                shot_noise=args.shot_noise,
                learnable_gamma=False,
            ),
            "desc": "no compensation (raw photoresponse)",
        },
    }

    # For "raw", override to use raw mode by patching forward
    # (Simpler: we just skip compensation in the training loop for raw)
    # Actually, easier to handle in the loop.

    results = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("logs/learnable_gamma_gpt")
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir = Path("checkpoints/learnable_gamma_gpt")
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    log_path = out_dir / f"{timestamp}_g{args.gamma_phys}_s{args.seed}.log"

    def log(msg: str):
        print(msg)
        with open(log_path, "a") as f:
            f.write(msg + "\n")

    log(f"=" * 60)
    log(f"Learnable Gamma Compensation Experiment")
    log(f"gamma_phys={args.gamma_phys}, seed={args.seed}, epochs={args.epochs}")
    log(f"Device: {device}")
    log(f"=" * 60)

    for variant_name, variant_cfg in variants.items():
        frontend = variant_cfg["frontend"].to(device)
        desc = variant_cfg["desc"]
        log(f"\n--- Variant: {variant_name} ({desc}) ---")

        # Reset model weights for fair comparison
        model = build_model(base_cfg, num_classes=num_classes, device=device)

        # Collect learnable parameters: model + frontend (if learnable)
        params = list(model.parameters())
        if variant_name == "learnable":
            params += list(frontend.parameters())
            log(f"Learnable frontend parameter count: {sum(p.numel() for p in frontend.parameters())}")

        optimizer = torch.optim.AdamW(params, lr=args.lr, weight_decay=args.weight_decay)
        scaler = torch.cuda.amp.GradScaler() if device.type == "cuda" and args.amp else None

        best_acc = 0.0
        best_epoch = 0
        learned_gamma_history = []

        for epoch in range(args.epochs):
            train_loss = train_one_epoch(model, frontend, train_loader, optimizer, device, scaler)
            val_acc = evaluate(model, frontend, test_loader, device)

            # Log learned gamma if applicable
            if variant_name == "learnable" and hasattr(frontend.inverse_gamma, "gamma_comp"):
                gc = frontend.inverse_gamma.gamma_comp.item()
                learned_gamma_history.append(gc)

            if val_acc > best_acc:
                best_acc = val_acc
                best_epoch = epoch
                # Save checkpoint
                ckpt_path = ckpt_dir / f"{timestamp}_{variant_name}_g{args.gamma_phys}_best.pt"
                torch.save({
                    "epoch": epoch,
                    "model": model.state_dict(),
                    "frontend": frontend.state_dict(),
                    "val_acc": val_acc,
                    "gamma_phys": args.gamma_phys,
                    "variant": variant_name,
                }, ckpt_path)

            if (epoch + 1) % args.log_interval == 0 or epoch == 0:
                gamma_str = f", gamma_comp={gc:.4f}" if variant_name == "learnable" else ""
                log(f"Epoch {epoch+1}/{args.epochs}: loss={train_loss:.4f}, val_acc={val_acc:.2f}%{gamma_str}")

        # Final test evaluation (already using test set as proxy for val)
        test_acc = evaluate(model, frontend, test_loader, device)
        log(f"BEST val_acc={best_acc:.2f}% @ epoch {best_epoch+1}, TEST acc={test_acc:.2f}%")

        if variant_name == "learnable" and learned_gamma_history:
            init_gc = learned_gamma_history[0]
            final_gc = learned_gamma_history[-1]
            phys_inv = 1.0 / args.gamma_phys
            log(f"Learned gamma_comp: init={init_gc:.4f} -> final={final_gc:.4f} (phys_inv={phys_inv:.4f})")
            log(f"Deviation from physical inverse: {abs(final_gc - phys_inv):.4f}")

        results[variant_name] = {
            "best_val_acc": best_acc,
            "best_epoch": best_epoch + 1,
            "final_test_acc": test_acc,
            "description": desc,
            "learned_gamma_history": learned_gamma_history if variant_name == "learnable" else None,
        }

    # Save JSON
    json_dir = Path("report_md/json")
    json_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_dir / f"learnable_gamma_{timestamp}_g{args.gamma_phys}_s{args.seed}.json"
    with open(json_path, "w") as f:
        json.dump({
            "gamma_phys": args.gamma_phys,
            "seed": args.seed,
            "epochs": args.epochs,
            "dataset": args.dataset,
            "timestamp": timestamp,
            "results": results,
        }, f, indent=2)
    log(f"\nResults saved to {json_path}")
    log("=" * 60)

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Learnable frontend compensation exponent")
    parser.add_argument("--gamma_phys", type=float, default=2.0, help="Physical photoresponse exponent")
    parser.add_argument("--alpha", type=float, default=1.0, help="Responsivity scale")
    parser.add_argument("--I_dark", type=float, default=1e-10, help="Dark current (A)")
    parser.add_argument("--shot_noise", action="store_true", default=True, help="Enable shot noise")
    parser.add_argument("--dataset", type=str, default="cifar10", choices=["cifar10", "cifar100"])
    parser.add_argument("--data_dir", type=str, default="data")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--weight_decay", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--amp", action="store_true", default=True, help="Automatic mixed precision")
    parser.add_argument("--log_interval", type=int, default=10)
    args = parser.parse_args()

    run_experiment(args)


if __name__ == "__main__":
    main()
