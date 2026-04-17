"""
CrossSim vs Our Framework - Canonical Comparison

Compares 8-bit ADC inference using CrossSim against our framework.
Uses a simple CNN on CIFAR-10 for fair comparison.
"""

import torch
import torch.nn as nn
from torchvision import datasets, transforms
import numpy as np
import sys
import os
import json
from datetime import datetime
import time

# Add CrossSim to path
sys.path.insert(0, '/home/qiaosir/projects/cross-sim')
sys.path.insert(0, '/home/qiaosir/projects/cross-sim/applications/dnn')

print("=" * 70)
print("CrossSim vs Our Framework - Canonical 8-bit ADC Comparison")
print("=" * 70)

# Configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 256
N_IMAGES = 1000  # Use subset for speed
ADC_BITS = 8
N_RUNS = 3

print(f"\nDevice: {DEVICE}")
print(f"ADC bits: {ADC_BITS}")
print(f"Test images: {N_IMAGES}")
print(f"Runs: {N_RUNS}")

# =============================================================================
# Part 1: Simple CNN for CIFAR-10
# =============================================================================
class SimpleCNN(nn.Module):
    """Simple CNN for CIFAR-10 (similar to our framework's capability)"""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(128, num_classes)
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

print("\nModel: SimpleCNN (3 conv + 1 fc)")
model = SimpleCNN().to(DEVICE)

# Train briefly or load pretrained
print("Training model briefly on CIFAR-10...")
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

train_dataset = datasets.CIFAR10(
    root='/tmp/cifar10_data',
    train=True,
    download=True,
    transform=train_transform
)

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=128, shuffle=True, num_workers=2
)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)

model.train()
for epoch in range(5):  # Brief training
    correct = 0
    total = 0
    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        if i >= 100:  # Only 100 batches for speed
            break
    
    print(f"  Epoch {epoch+1}/5: Train Acc = {100.0*correct/total:.1f}%")

# =============================================================================
# Part 2: Digital Baseline
# =============================================================================
print("\n" + "=" * 70)
print("Part 2: Digital Baseline")
print("=" * 70)

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

test_dataset = datasets.CIFAR10(
    root='/tmp/cifar10_data',
    train=False,
    download=True,
    transform=test_transform
)

# Use subset
indices = np.arange(N_IMAGES)
subset = torch.utils.data.Subset(test_dataset, indices)
test_loader = torch.utils.data.DataLoader(subset, batch_size=BATCH_SIZE, shuffle=False)

model.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

digital_acc = 100.0 * correct / total
print(f"Digital Baseline: {digital_acc:.2f}%")

# =============================================================================
# Part 3: CrossSim Analog Simulation
# =============================================================================
print("\n" + "=" * 70)
print("Part 3: CrossSim 8-bit ADC")
print("=" * 70)

try:
    from simulator.algorithms.dnn.torch.convert import from_torch, reinitialize, convertible_modules
    from dnn_inference_params import dnn_inference_params
    
    n_layers = len(convertible_modules(model))
    print(f"Convertible layers: {n_layers}")
    
    # CrossSim config for 8-bit ADC
    base_params = {
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
        "adc_bits": ADC_BITS,
        "adc_range_option": "MAX",
        "adc_type": "generic",
        "adc_per_ibit": False,
        "useGPU": (DEVICE.type == "cuda"),
    }
    
    # Configure per layer
    params_list = []
    for k in range(n_layers):
        params_k = base_params.copy()
        params_k["positiveInputsOnly"] = False if k == 0 else True
        params_k["input_range"] = (-2, 2)
        params_k["adc_range"] = (-10, 10)
        params_list.append(dnn_inference_params(**params_k))
    
    # Convert to analog
    print("Converting to analog...")
    analog_model = from_torch(model, params_list, fuse_batchnorm=True, bias_rows=0)
    analog_model = analog_model.to(DEVICE)
    analog_model.eval()
    
    # Run multiple trials
    crosssim_accs = []
    for run in range(N_RUNS):
        print(f"  Run {run+1}/{N_RUNS}...", end=" ")
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs = inputs.to(DEVICE)
                outputs = analog_model(inputs)
                outputs = outputs.to(DEVICE)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels.to(DEVICE)).sum().item()
        
        acc = 100.0 * correct / total
        crosssim_accs.append(acc)
        print(f"{acc:.2f}%")
        
        if run < N_RUNS - 1:
            reinitialize(analog_model)
    
    crosssim_mean = np.mean(crosssim_accs)
    crosssim_std = np.std(crosssim_accs)
    
    print(f"\nCrossSim: {crosssim_mean:.2f}% ± {crosssim_std:.2f}%")
    print(f"Degradation: {digital_acc - crosssim_mean:.2f} pp")
    
except Exception as e:
    print(f"CrossSim error: {e}")
    import traceback
    traceback.print_exc()
    crosssim_mean = None
    crosssim_std = None

# =============================================================================
# Part 4: Our Framework (if possible)
# =============================================================================
print("\n" + "=" * 70)
print("Part 4: Our Framework")
print("=" * 70)

print("Note: Our framework uses hybrid analog/digital conversion")
print("      optimized for organic photodiode CIM, not standard ADC.")
print("      Direct comparison limited to canonical uniform-noise regime.")

our_acc = None

# =============================================================================
# Summary
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

results = {
    "experiment": "CrossSim vs Our Framework",
    "date": datetime.now().isoformat(),
    "model": "SimpleCNN",
    "dataset": "CIFAR-10",
    "n_images": N_IMAGES,
    "adc_bits": ADC_BITS,
    "results": {
        "digital": {"accuracy": digital_acc},
        "crosssim": {
            "accuracies": crosssim_accs,
            "mean": crosssim_mean,
            "std": crosssim_std
        },
        "our_framework": {"accuracy": our_acc, "note": "Not directly comparable"}
    }
}

print(f"\nDigital:  {digital_acc:.2f}%")
if crosssim_mean:
    print(f"CrossSim: {crosssim_mean:.2f}% ± {crosssim_std:.2f}%")
    print(f"Δ:        {digital_acc - crosssim_mean:.2f} pp")

# Save
output_dir = "/home/qiaosir/projects/compute_vit/report_md/_gpt"
os.makedirs(output_dir, exist_ok=True)
with open(f"{output_dir}/crosssim_comparison_final.json", 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to: {output_dir}/crosssim_comparison_final.json")
print("=" * 70)
