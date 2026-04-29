#!/usr/bin/env python3
"""
R11D-HAT-inspired PCM: Per-Epoch Noise Resampling + PCM device model.

Hybrid approach:
- Uses aihwkit AnalogLinear + PCMPresetUnitCell + AnalogSGD (real PCM physics)
- Adds per-epoch D2D mismatch resampling on tile weights (HAT-inspired)
- Disables per-batch ADD_NORMAL noise; D2D is injected once per epoch and fixed

This is an *approximate* HAT implementation because aihwkit tiles do not expose
a clean "ideal weight" vs "D2D offset" separation.  We maintain a running
estimate by subtracting the previous epoch's noise before adding new noise.
"""

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from aihwkit.nn import AnalogLinear
from aihwkit.optim import AnalogSGD
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierParameter, WeightModifierType

sys.stdout.reconfigure(line_buffering=True)

DATASET_STATS = {
    "cifar10": {
        "num_classes": 10,
        "mean": (0.4914, 0.4822, 0.4465),
        "std": (0.2023, 0.1994, 0.2010),
        "dataset_cls": torchvision.datasets.CIFAR10,
    },
}

PCM_PRESET_REGISTRY = [
    ("aihwkit.simulator.presets", "PCMPresetUnitCell"),
    ("aihwkit.simulator.presets", "PCMPresetDevice"),
    ("aihwkit.simulator.presets.devices", "PCMPresetDevice"),
]


def _resolve_pcm_preset():
    """Try PCM presets in order. Returns (device_instance, name_string) or raises."""
    last_err = None
    for module_path, class_name in PCM_PRESET_REGISTRY:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            instance = cls()
            print(f"[PCM] Resolved preset: {module_path}.{class_name}")
            return instance, class_name
        except (ImportError, AttributeError, Exception) as e:
            last_err = e
            print(f"[PCM] {module_path}.{class_name} failed: {e}")
    raise ImportError(
        f"No usable PCM device preset found. Tried: "
        f"{[f'{m}.{c}' for m, c in PCM_PRESET_REGISTRY]}. "
        f"Last error: {last_err}"
    )


def get_dataloaders(dataset_name="cifar10", batch_size=64, num_workers=2, pin=False):
    stats = DATASET_STATS[dataset_name]
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])
    train_ds = stats["dataset_cls"](root="./data", train=True, download=True, transform=transform_train)
    test_ds = stats["dataset_cls"](root="./data", train=False, download=True, transform=transform_test)
    train_loader = torch.utils.data.DataLoader(
        train_ds, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=pin
    )
    test_loader = torch.utils.data.DataLoader(
        test_ds, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=pin
    )
    return train_loader, test_loader, stats["num_classes"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True,
        ).strip()
    except Exception:
        return "unknown"


def make_rpu_config(inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10,
                    disable_modifier=False):
    pcm_device, pcm_name = _resolve_pcm_preset()
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = inp_res
    cfg.forward.out_res = out_res
    cfg.device = pcm_device
    if disable_modifier:
        cfg.modifier.type = WeightModifierType.NONE
        cfg.modifier.std_dev = 0.0
        cfg.modifier.enable_during_test = False
    else:
        cfg.modifier.type = WeightModifierType.ADD_NORMAL
        cfg.modifier.std_dev = modifier_std_dev
        cfg.modifier.enable_during_test = False
    return cfg, pcm_name


def replace_linear_with_analog(module, rpu_config, parent_name=""):
    for name, child in list(module.named_children()):
        full_name = f"{parent_name}.{name}" if parent_name else name
        if isinstance(child, nn.Linear):
            analog_layer = AnalogLinear(
                in_features=child.in_features,
                out_features=child.out_features,
                bias=child.bias is not None,
                rpu_config=rpu_config,
            )
            with torch.no_grad():
                analog_layer.set_weights(child.weight, child.bias)
            setattr(module, name, analog_layer)
        else:
            replace_linear_with_analog(child, rpu_config, full_name)


def build_model(num_classes=10, inp_res=1.0 / 256.0, out_res=1.0 / 256.0,
                modifier_std_dev=0.10, disable_modifier=False,
                rpu_config=None, pcm_name=None):
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    if rpu_config is None:
        rpu_config, pcm_name = make_rpu_config(
            inp_res=inp_res,
            out_res=out_res,
            modifier_std_dev=modifier_std_dev,
            disable_modifier=disable_modifier,
        )
    replace_linear_with_analog(model, rpu_config)
    return model, rpu_config, pcm_name


def init_hat_noise_buffers(model, std_dev):
    """
    Initialize HAT noise tracking for all AnalogLinear layers.
    Returns a dict mapping layer name -> {'old_noise': Tensor}.
    old_noise starts as zeros so the first epoch treats current weights as reference.
    """
    buffers = {}
    for name, module in model.named_modules():
        if isinstance(module, AnalogLinear):
            w, _ = module.get_weights()
            buffers[name] = {
                "old_noise": torch.zeros_like(w),
                "std_dev": std_dev,
            }
    return buffers


def resample_all_d2d_noise(model, noise_buffers, mode="scaled"):
    """
    Per-epoch D2D mismatch resampling for aihwkit AnalogLinear layers.

    Args:
        mode: "scaled" (default) or "additive".
            - "scaled":  estimate ideal weight, then add noise scaled by weight magnitude.
              noise = randn * std_dev * w.abs().mean().  This approximates
              sigma_d2d * G_range in the original HAT code.
            - "additive": directly add noise to current weights without restoring ideal.
              Simpler but noise accumulates across epochs.
    """
    model.eval()
    count = 0
    for name, module in model.named_modules():
        if not isinstance(module, AnalogLinear):
            continue
        buf = noise_buffers.get(name)
        if buf is None:
            continue

        w, b = module.get_weights()
        old_noise = buf["old_noise"]
        std_dev = buf["std_dev"]

        if mode == "scaled":
            # Estimate ideal weight by subtracting last epoch's noise
            w_ideal = w - old_noise
            # Scale noise by mean absolute weight (approximates G_range scaling)
            scale = w_ideal.abs().mean().item()
            if scale < 1e-8:
                scale = 1e-8
            d2d_offset = torch.randn(1, device=w_ideal.device) * std_dev * scale
            noise_new = d2d_offset.expand_as(w_ideal)
            w_new = w_ideal + noise_new
        elif mode == "additive":
            scale = w.abs().mean().item()
            if scale < 1e-8:
                scale = 1e-8
            d2d_offset = torch.randn(1, device=w.device) * std_dev * scale
            noise_new = d2d_offset.expand_as(w)
            w_new = w + noise_new
        else:
            raise ValueError(f"Unknown hat_mode: {mode}")

        module.set_weights(w_new, b)
        buf["old_noise"] = noise_new
        count += 1

    return count


def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
    return total_loss / total, 100.0 * correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        total_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
    return total_loss / total, 100.0 * correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--wd", type=float, default=0.05)
    parser.add_argument("--momentum", type=float, default=0.0)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--save-dir", default="paper2_aihwkit_baseline/checkpoints/r11d_hat_inspired_pcm")
    parser.add_argument("--log-interval", type=int, default=10)
    parser.add_argument("--inp-res", type=float, default=1.0 / 256.0)
    parser.add_argument("--out-res", type=float, default=1.0 / 256.0)
    parser.add_argument("--modifier-std-dev", type=float, default=0.10)
    parser.add_argument("--early-stop-patience", type=int, default=0)
    parser.add_argument("--early-stop-min-delta", type=float, default=0.0)
    parser.add_argument("--run-id", default="r11d_hat_inspired_pcm")
    parser.add_argument("--hat-std-dev", type=float, default=5.0,
                        help="Std dev of per-epoch D2D noise, scaled by mean|weight|.")
    parser.add_argument("--hat-mode", type=str, default="scaled", choices=["scaled", "additive"],
                        help="scaled: restore ideal weight then add scaled noise. additive: add noise to current weights.")
    parser.add_argument("--hat-start-epoch", type=int, default=1,
                        help="First epoch to apply HAT resampling (1-based).")
    parser.add_argument("--resume", type=str, default=None,
                        help="Path to checkpoint to resume from.")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    os.makedirs(args.save_dir, exist_ok=True)
    device = torch.device(args.device)

    print(f"=== R11D-HAT-inspired PCM: Per-Epoch Noise Resampling + PCM Device Model ===")
    print(f"Device: {device}")
    print(f"PyTorch: {torch.__version__}")
    print(
        "Config: "
        f"run_id={args.run_id}, epochs={args.epochs}, bs={args.batch_size}, lr={args.lr}, "
        f"inp_res={args.inp_res}, out_res={args.out_res}, hat_std_dev={args.hat_std_dev}"
    )

    # --- Resolve PCM preset early so we fail fast ---
    print("[PCM] Resolving device preset...")
    try:
        _rpu_config, pcm_name = make_rpu_config(
            inp_res=args.inp_res,
            out_res=args.out_res,
            modifier_std_dev=args.modifier_std_dev,
            disable_modifier=True,  # HAT manages D2D noise manually
        )
    except ImportError as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(2)

    train_loader, test_loader, num_classes = get_dataloaders(
        batch_size=args.batch_size, num_workers=args.workers,
        pin=device.type == "cuda"
    )

    # --- OOM wrapper ---
    batch_size_tried = args.batch_size
    try:
        model, rpu_config, pcm_name = build_model(
            num_classes=num_classes,
            inp_res=args.inp_res,
            out_res=args.out_res,
            modifier_std_dev=args.modifier_std_dev,
            disable_modifier=True,
            rpu_config=_rpu_config,
            pcm_name=pcm_name,
        )
        model = model.to(device)
    except RuntimeError as e:
        if "out of memory" in str(e).lower() and args.batch_size > 32:
            print(f"[OOM] batch_size={args.batch_size} OOM. Retrying with batch_size=32")
            torch.cuda.empty_cache()
            args.batch_size = 32
            batch_size_tried = 32
            train_loader, test_loader, num_classes = get_dataloaders(
                batch_size=args.batch_size, num_workers=args.workers,
                pin=device.type == "cuda"
            )
            model, rpu_config, pcm_name = build_model(
                num_classes=num_classes,
                inp_res=args.inp_res,
                out_res=args.out_res,
                modifier_std_dev=args.modifier_std_dev,
                disable_modifier=True,
                rpu_config=_rpu_config,
                pcm_name=pcm_name,
            )
            model = model.to(device)
        else:
            raise

    n_analog = sum(1 for _ in model.modules() if isinstance(_, AnalogLinear))
    print(f"AnalogLinear layers: {n_analog}")
    print(f"PCM preset: {pcm_name}")
    print(f"Dataset: CIFAR-10, {len(train_loader.dataset)} train, {len(test_loader.dataset)} test")

    # --- Resume from checkpoint ---
    if args.resume:
        print(f"[Resume] Loading checkpoint from {args.resume}")
        ckpt = torch.load(args.resume, map_location=device, weights_only=False)
        model.load_state_dict(ckpt["model_state_dict"])
        print(f"[Resume] Loaded checkpoint (best_acc was {ckpt.get('best_acc', 'N/A')})")

    # --- HAT noise buffers ---
    noise_buffers = init_hat_noise_buffers(model, std_dev=args.hat_std_dev)
    print(f"HAT-inspired: Initialized D2D noise buffers for {len(noise_buffers)} analog layers, "
          f"std_dev={args.hat_std_dev}, mode={args.hat_mode}, start_epoch={args.hat_start_epoch}")

    criterion = nn.CrossEntropyLoss()
    optimizer = AnalogSGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.wd)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)

    best_acc = 0.0
    best_epoch = -1
    history = []
    start_time = time.time()
    rpu_config_spec = {
        "forward_inp_res": args.inp_res,
        "forward_out_res": args.out_res,
        "modifier_type": "NONE",
        "modifier_std_dev": 0.0,
        "modifier_enable_during_test": False,
        "pcm_preset": pcm_name,
        "hat_std_dev": args.hat_std_dev,
        "hat_mode": args.hat_mode,
        "hat_start_epoch": args.hat_start_epoch,
    }
    provenance = {
        "run_id": args.run_id,
        "commit_hash": git_commit_hash(),
        "code_sha256": sha256_file(__file__),
        "cuda_device_name": torch.cuda.get_device_name(device) if device.type == "cuda" else "cpu",
        "pytorch_version": torch.__version__,
        "exp_cfg": vars(args),
        "rpu_config_spec": rpu_config_spec,
        "pcm_preset_used": pcm_name,
        "optimizer": "AnalogSGD",
        "method": "HAT-inspired per-epoch noise resampling",
        "method_note": (
            "Per-epoch D2D noise resampling on tile weights + AnalogSGD PCM pulse-update. "
            "Modifier disabled; D2D injected manually at epoch boundary. "
            "Ideal-weight estimate is approximate because PCM pulse-update is non-linear "
            "and aihwkit does not expose programmed_weight vs noise_offset separation."
        ),
    }

    for epoch in range(args.epochs):
        t0 = time.time()

        # --- HAT: resample D2D noise before training this epoch ---
        if epoch + 1 >= args.hat_start_epoch:
            n_resampled = resample_all_d2d_noise(model, noise_buffers, mode=args.hat_mode)
            if n_resampled > 0 and (epoch == 0 or (epoch + 1) % args.log_interval == 0):
                print(f"  [HAT-inspired] Resampled D2D noise for {n_resampled} analog layers")

        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
        test_loss, test_acc = evaluate(model, test_loader, criterion, device)
        scheduler.step()
        epoch_time = time.time() - t0

        # --- Divergence detection ---
        if torch.isnan(torch.tensor(train_loss)) or torch.isnan(torch.tensor(test_loss)):
            if epoch < 5:
                diag = {
                    "epoch": epoch + 1,
                    "train_loss": float(train_loss),
                    "test_loss": float(test_loss),
                    "train_acc": float(train_acc),
                    "test_acc": float(test_acc),
                    "grad_norms": [],
                }
                for p in model.parameters():
                    if p.grad is not None:
                        diag["grad_norms"].append(p.grad.norm().item())
                diag_path = os.path.join(args.save_dir, "divergence_diagnostics.json")
                with open(diag_path, "w") as f:
                    json.dump(diag, f, indent=2)
                print(f"[DIVERGENCE] NaN at epoch {epoch+1}. Diagnostics: {diag_path}")
                sys.exit(3)
            else:
                print(f"[WARN] NaN at epoch {epoch+1} (>5), continuing...")

        history.append({
            "epoch": epoch + 1,
            "train_loss": round(train_loss, 4),
            "train_acc": round(train_acc, 4),
            "test_loss": round(test_loss, 4),
            "test_acc": round(test_acc, 4),
            "lr": round(optimizer.param_groups[0]["lr"], 6),
            "epoch_time_sec": round(epoch_time, 1),
            "hat_resampled": epoch + 1 >= args.hat_start_epoch,
        })

        if test_acc > best_acc + args.early_stop_min_delta:
            best_acc = test_acc
            best_epoch = epoch
            ckpt = os.path.join(args.save_dir, "best.pt")
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "test_acc": test_acc,
                "args": vars(args),
                "rpu_config_spec": rpu_config_spec,
                "provenance": provenance,
            }, ckpt)

        if (epoch + 1) % args.log_interval == 0 or epoch == 0 or epoch == args.epochs - 1:
            elapsed = time.time() - start_time
            eta = elapsed / (epoch + 1) * (args.epochs - epoch - 1) if epoch > 0 else 0
            print(f"Epoch {epoch+1:3d}/{args.epochs} | Train {train_acc:.2f}% | Test {test_acc:.2f}% | Best {best_acc:.2f}% | {epoch_time:.1f}s/epoch | ETA {eta/3600:.1f}h")

        if args.early_stop_patience > 0 and best_epoch >= 0:
            epochs_without_improvement = epoch - best_epoch
            if epochs_without_improvement >= args.early_stop_patience:
                print(f"Early stop at epoch {epoch+1}: no improvement for {args.early_stop_patience} epochs.")
                break

    total_elapsed = time.time() - start_time
    print(f"\n=== Complete ===")
    print(f"Best test accuracy: {best_acc:.2f}%")
    print(f"Total time: {total_elapsed/3600:.2f}h")
    print(f"Finish: {datetime.now().isoformat()}")

    last_ckpt = os.path.join(args.save_dir, "last.pt")
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "test_acc": test_acc,
        "args": vars(args),
        "rpu_config_spec": rpu_config_spec,
        "provenance": provenance,
    }, last_ckpt)

    hist_path = os.path.join(args.save_dir, "training_history.json")
    oom_info = {"oom_retry_batch_size": batch_size_tried} if batch_size_tried != args.batch_size else {}
    with open(hist_path, "w") as f:
        json.dump({
            "best_acc": best_acc,
            "total_seconds": total_elapsed,
            "history": history,
            "args": vars(args),
            "aihwkit_version": "1.1.0",
            "rpu_config": str(rpu_config),
            "rpu_config_spec": rpu_config_spec,
            "provenance": provenance,
            **oom_info,
            "device": str(device),
            "finish_time": datetime.now().isoformat(),
        }, f, indent=2)
    print(f"Saved: {hist_path}")


if __name__ == "__main__":
    main()
