"""
CrossSim vs Our Framework Comparison Experiment

Compares inference accuracy using CrossSim (8-bit ADC, uniform noise)
against our organic CIM framework on CIFAR-10 with ResNet-18.
"""

import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
import numpy as np
import sys
import os
import json
from datetime import datetime

# Add CrossSim to path
sys.path.insert(0, '/home/qiaosir/projects/cross-sim')
sys.path.insert(0, '/home/qiaosir/projects/cross-sim/simulator/algorithms/dnn')

# Add our framework to path
sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

print("=" * 70)
print("CrossSim vs Our Framework - CIFAR-10 ResNet-18 Comparison")
print("=" * 70)

# Configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 128
N_IMAGES = 10000  # Full test set
ADC_BITS = 8
N_RUNS = 3  # Multiple runs for statistics

print(f"\nDevice: {DEVICE}")
print(f"ADC bits: {ADC_BITS}")
print(f"Test images: {N_IMAGES}")
print(f"Runs: {N_RUNS}")

# =============================================================================
# Part 1: Load CIFAR-10 Dataset
# =============================================================================
print("\n" + "=" * 70)
print("Loading CIFAR-10 dataset...")
print("=" * 70)

# Standard CIFAR-10 normalization
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

test_dataset = datasets.CIFAR10(
    root='/tmp/cifar10_data',
    train=False,
    download=True,
    transform=transform
)

test_loader = torch.utils.data.DataLoader(
    test_dataset, 
    batch_size=BATCH_SIZE, 
    shuffle=False,
    num_workers=2
)

# Get a subset for faster testing if needed
if N_IMAGES < len(test_dataset):
    indices = np.arange(N_IMAGES)
    subset = torch.utils.data.Subset(test_dataset, indices)
    test_loader = torch.utils.data.DataLoader(subset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Dataset loaded: {len(test_loader.dataset)} test images")

# =============================================================================
# Part 2: Load ResNet-18 Model
# =============================================================================
print("\n" + "=" * 70)
print("Loading ResNet-18 model...")
print("=" * 70)

model = models.resnet18(pretrained=True)
model = model.to(DEVICE)
model.eval()

print("ResNet-18 loaded (ImageNet pretrained)")

# =============================================================================
# Part 3: Digital Baseline (Our Framework)
# =============================================================================
print("\n" + "=" * 70)
print("Part 3: Digital Baseline Evaluation")
print("=" * 70)

def evaluate_model(model, dataloader, device):
    """Evaluate model accuracy"""
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    accuracy = 100.0 * correct / total
    return accuracy

digital_acc = evaluate_model(model, test_loader, DEVICE)
print(f"\nDigital Baseline Accuracy: {digital_acc:.2f}%")

# =============================================================================
# Part 4: CrossSim Analog Simulation
# =============================================================================
print("\n" + "=" * 70)
print("Part 4: CrossSim Analog Simulation")
print("=" * 70)

try:
    from simulator.algorithms.dnn.torch.convert import from_torch, reinitialize, convertible_modules
    from simulator.algorithms.dnn.dnn_inference_params import dnn_inference_params
    
    # Count convertible layers
    n_layers = len(convertible_modules(model))
    print(f"Number of convertible layers: {n_layers}")
    
    # Configure CrossSim parameters for 8-bit ADC with uniform noise
    base_params_args = {
        "ideal": False,
        # Mapping style
        "core_style": "BALANCED",
        "Nslices": 1,
        # Weight value representation and precision
        "weight_bits": 8,
        "weight_percentile": 100,
        "digital_bias": True,
        # Memory device (ideal for canonical comparison)
        "Rmin": 1e4,
        "Rmax": 1e6,
        "infinite_on_off_ratio": False,
        "error_model": "none",  # No programming error
        "alpha_error": 0.0,
        "proportional_error": False,
        "noise_model": "none",  # No read noise for now
        "alpha_noise": 0.0,
        "proportional_noise": False,
        "drift_model": "none",
        "t_drift": 0,
        # Array properties
        "NrowsMax": 512,  # Adjust based on model
        "NcolsMax": None,
        "Rp_row": 0,
        "Rp_col": 0,
        "interleaved_posneg": False,
        "subtract_current_in_xbar": True,
        "current_from_input": True,
        # Input quantization
        "input_bits": 8,
        "input_bitslicing": False,
        "input_slice_size": 1,
        # ADC - 8-bit as requested
        "adc_bits": ADC_BITS,
        "adc_range_option": "MAX",
        "adc_type": "generic",
        "adc_per_ibit": False,
        # Simulation parameters
        "useGPU": (DEVICE.type == "cuda"),
    }
    
    # Create parameters list for all layers
    params_list = []
    for k in range(n_layers):
        params_args_k = base_params_args.copy()
        params_args_k["positiveInputsOnly"] = False if k == 0 else True
        # Use default ranges for now (no calibration)
        params_args_k["input_range"] = (-1, 1)  # Normalized input range
        params_args_k["adc_range"] = (-5, 5)  # Estimated ADC range
        params_list.append(dnn_inference_params(**params_args_k))
    
    print(f"CrossSim parameters configured: {ADC_BITS}-bit ADC")
    
    # Convert model to analog
    print("\nConverting model to CrossSim analog layers...")
    analog_model = from_torch(model, params_list, fuse_batchnorm=True, bias_rows=0)
    analog_model = analog_model.to(DEVICE)
    analog_model.eval()
    print("Conversion complete")
    
    # Run multiple inference trials
    crosssim_accuracies = []
    
    for run in range(N_RUNS):
        print(f"\n  Run {run + 1}/{N_RUNS}...")
        
        correct = 0
        total = 0
        batch_idx = 0
        
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs = inputs.to(DEVICE)
                outputs = analog_model(inputs)
                outputs = outputs.to(DEVICE)
                
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels.to(DEVICE)).sum().item()
                
                batch_idx += 1
                if batch_idx % 10 == 0:
                    print(f"    Batch {batch_idx}/{len(test_loader)}, Acc: {100.0*correct/total:.2f}%", end="\r")
        
        accuracy = 100.0 * correct / total
        crosssim_accuracies.append(accuracy)
        print(f"\n  Run {run + 1} Accuracy: {accuracy:.2f}%")
        
        # Reinitialize for next run (resample errors)
        if run < N_RUNS - 1:
            reinitialize(analog_model)
    
    crosssim_mean = np.mean(crosssim_accuracies)
    crosssim_std = np.std(crosssim_accuracies)
    
    print(f"\n{'='*70}")
    print("CrossSim Results:")
    print(f"  Accuracies: {[f'{a:.2f}%' for a in crosssim_accuracies]}")
    print(f"  Mean: {crosssim_mean:.2f}%")
    print(f"  Std: {crosssim_std:.2f}%")
    
except Exception as e:
    print(f"\nCrossSim simulation failed: {e}")
    import traceback
    traceback.print_exc()
    crosssim_mean = None
    crosssim_std = None

# =============================================================================
# Part 5: Our Framework (8-bit ADC Simulation)
# =============================================================================
print("\n" + "=" * 70)
print("Part 5: Our Framework (8-bit ADC)")
print("=" * 70)

try:
    from models.TinyViT import tinyvit_5m
    from analog import AnalogLinear, AnalogConv2d
    from analog_utils import convert_to_hybrid, AnalogLinearConfig
    
    # Note: ResNet-18 is not directly supported in our framework
    # We'll report this limitation
    print("\nOur framework currently supports Tiny-ViT and ConvNeXt")
    print("ResNet-18 requires adapter implementation")
    print("For fair comparison, we report framework limitation")
    
    our_framework_acc = None
    
except Exception as e:
    print(f"Our framework evaluation error: {e}")
    our_framework_acc = None

# =============================================================================
# Part 6: Summary and Save Results
# =============================================================================
print("\n" + "=" * 70)
print("COMPARISON SUMMARY")
print("=" * 70)

results = {
    "experiment": "CrossSim vs Our Framework",
    "date": datetime.now().isoformat(),
    "model": "ResNet-18",
    "dataset": "CIFAR-10",
    "n_images": N_IMAGES,
    "adc_bits": ADC_BITS,
    "results": {
        "digital_baseline": {
            "accuracy": digital_acc,
            "description": "Standard PyTorch inference"
        },
        "crosssim": {
            "accuracies": crosssim_accuracies if crosssim_mean else None,
            "mean": crosssim_mean,
            "std": crosssim_std,
            "description": f"CrossSim {ADC_BITS}-bit ADC"
        },
        "our_framework": {
            "accuracy": our_framework_acc,
            "description": "Our organic CIM framework (ResNet-18 not fully supported)"
        }
    },
    "notes": [
        "CrossSim uses MAX ADC range option (no calibration)",
        "Uniform noise model (no device-specific non-idealities)",
        "Our framework comparison limited to supported architectures"
    ]
}

print(f"\nDigital Baseline:     {digital_acc:.2f}%")
if crosssim_mean:
    print(f"CrossSim ({ADC_BITS}-bit ADC):  {crosssim_mean:.2f}% ± {crosssim_std:.2f}%")
    print(f"CrossSim Degradation: {digital_acc - crosssim_mean:.2f} pp")
else:
    print("CrossSim: Failed")

# Save results
output_dir = "/home/qiaosir/projects/compute_vit/report_md/_gpt"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/crosssim_comparison_results.json"

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")
print("=" * 70)
