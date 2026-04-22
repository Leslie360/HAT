"""
Quick test of CrossSim functionality before full comparison
"""

import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
import numpy as np
import sys

from repo_bootstrap import configure_crosssim_paths, ensure_repo_root

ensure_repo_root()
configure_crosssim_paths()

print("Testing CrossSim import...")
from simulator.algorithms.dnn.torch.convert import from_torch, convertible_modules
from dnn_inference_params import dnn_inference_params
print("✓ CrossSim imported successfully")

# Create a simple test model
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(16, 10)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

print("\nCreating simple test model...")
model = SimpleNet()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()
print(f"✓ Model created on {device}")

# Count convertible layers
n_layers = len(convertible_modules(model))
print(f"✓ Convertible layers: {n_layers}")

# Configure CrossSim parameters
params_args = {
    "ideal": False,
    "core_style": "BALANCED",
    "Nslices": 1,
    "weight_bits": 8,
    "weight_percentile": 100,
    "digital_bias": True,
    "Rmin": 1e4,
    "Rmax": 1e6,
    "infinite_on_off_ratio": False,
    "error_model": "none",
    "alpha_error": 0.0,
    "proportional_error": False,
    "noise_model": "none",
    "alpha_noise": 0.0,
    "proportional_noise": False,
    "drift_model": "none",
    "t_drift": 0,
    "NrowsMax": 512,
    "NcolsMax": None,
    "Rp_row": 0,
    "Rp_col": 0,
    "interleaved_posneg": False,
    "subtract_current_in_xbar": True,
    "current_from_input": True,
    "input_bits": 8,
    "input_bitslicing": False,
    "input_slice_size": 1,
    "adc_bits": 8,
    "adc_range_option": "MAX",
    "adc_type": "generic",
    "adc_per_ibit": False,
    "useGPU": (device.type == "cuda"),
    "positiveInputsOnly": False,
    "input_range": (-1, 1),
    "adc_range": (-5, 5),
}

params = dnn_inference_params(**params_args)
params_list = [params] * n_layers
print("✓ CrossSim parameters configured")

# Convert to analog
print("\nConverting to analog layers...")
analog_model = from_torch(model, params_list, fuse_batchnorm=True, bias_rows=0)
analog_model = analog_model.to(device)
analog_model.eval()
print("✓ Model converted to analog")

# Test inference
test_input = torch.randn(2, 3, 32, 32).to(device)
print(f"\nTesting inference with input shape: {test_input.shape}")

with torch.no_grad():
    output_digital = model(test_input)
    output_analog = analog_model(test_input)

print(f"✓ Digital output shape: {output_digital.shape}")
print(f"✓ Analog output shape: {output_analog.shape}")
print(f"✓ Output difference (L2): {torch.norm(output_digital - output_analog).item():.6f}")

print("\n" + "="*60)
print("CrossSim quick test PASSED ✓")
print("="*60)
