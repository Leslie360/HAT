#!/usr/bin/env python3
"""Long-running GPU binding test to verify nvidia-smi visibility."""
import time
import torch
import torch.nn as nn
from aihwkit.nn import AnalogLinear
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierType
from aihwkit.simulator.presets import PCMPresetUnitCell

cfg = InferenceRPUConfig()
cfg.forward.inp_res = 1.0 / 256.0
cfg.forward.out_res = 1.0 / 256.0
cfg.device = PCMPresetUnitCell()
cfg.modifier.type = WeightModifierType.ADD_NORMAL
cfg.modifier.std_dev = 0.10
cfg.modifier.enable_during_test = False

device = torch.device("cuda")
model = nn.Sequential(
    nn.Flatten(),
    AnalogLinear(3*32*32, 128, rpu_config=cfg),
    nn.ReLU(),
    AnalogLinear(128, 10, rpu_config=cfg),
).to(device)

x = torch.randn(64, 3, 32, 32, device=device)

print(f"PID: {__import__('os').getpid()}")
print("Running 1000 forward passes...")
for i in range(1000):
    y = model(x)
    if device.type == "cuda":
        torch.cuda.synchronize()
    if (i+1) % 100 == 0:
        print(f"  Pass {i+1}/1000")

print("Done. Keeping alive for 30s for nvidia-smi check...")
for i in range(30):
    time.sleep(1)
    print(f"  {i+1}s/30s")
