#!/usr/bin/env python3
"""Minimal GPU binding test for AnalogLinear + PCMPresetUnitCell."""
import sys
import time
import torch
import torch.nn as nn
from aihwkit.nn import AnalogLinear
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierType

try:
    from aihwkit.simulator.presets import PCMPresetUnitCell
    pcm_device = PCMPresetUnitCell()
    preset_name = "PCMPresetUnitCell"
except Exception as e:
    print(f"[ERROR] Cannot load PCM preset: {e}")
    sys.exit(1)

cfg = InferenceRPUConfig()
cfg.forward.inp_res = 1.0 / 256.0
cfg.forward.out_res = 1.0 / 256.0
cfg.device = pcm_device
cfg.modifier.type = WeightModifierType.ADD_NORMAL
cfg.modifier.std_dev = 0.10
cfg.modifier.enable_during_test = False

print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device: {torch.cuda.get_device_name(0)}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Build a small model with AnalogLinear
model = nn.Sequential(
    nn.Flatten(),
    AnalogLinear(3*32*32, 128, rpu_config=cfg),
    nn.ReLU(),
    AnalogLinear(128, 10, rpu_config=cfg),
)
model = model.to(device)

# Check parameter device
for name, p in model.named_parameters():
    print(f"  {name}: device={p.device}")

# Run forward pass with timing
x = torch.randn(64, 3, 32, 32, device=device)

# Warm-up
try:
    _ = model(x)
    if device.type == "cuda":
        torch.cuda.synchronize()
except Exception as e:
    print(f"[ERROR] Forward pass failed: {e}")
    sys.exit(1)

# Timed run
t0 = time.time()
for _ in range(10):
    y = model(x)
    if device.type == "cuda":
        torch.cuda.synchronize()
t1 = time.time()

print(f"\n10 forward passes: {(t1-t0)*1000:.1f} ms total, {(t1-t0)/10*1000:.1f} ms avg")
print(f"Output shape: {y.shape}, device: {y.device}")

# GPU memory check
if device.type == "cuda":
    mem_alloc = torch.cuda.memory_allocated() / 1024**2
    mem_res = torch.cuda.memory_reserved() / 1024**2
    print(f"GPU memory allocated: {mem_alloc:.1f} MiB")
    print(f"GPU memory reserved:  {mem_res:.1f} MiB")

print("\n[INFO] Now check nvidia-smi in another terminal.")
print("If python process does NOT appear in nvidia-smi Processes,")
print("AIHWKit is likely running simulation on CPU despite PyTorch tensor on GPU.")

# Keep process alive briefly so user can check nvidia-smi
print("\nSleeping 10s for nvidia-smi check...")
time.sleep(10)
print("Test complete.")
