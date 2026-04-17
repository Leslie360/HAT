import torch
import torch.nn as nn
import sys
import os
import json
import time

sys.path.insert(0, '/home/qiaosir/projects/cross-sim')
sys.path.insert(0, '/home/qiaosir/projects/cross-sim/applications/dnn')

from simulator.algorithms.dnn.torch.convert import from_torch, convertible_modules
from dnn_inference_params import dnn_inference_params
from train_resnet18 import build_model, get_dataloaders, evaluate, ExperimentConfig

def run_crosssim_resnet():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load FP32 ResNet-18 model
    num_classes = 10
    # Use 'name' as positional arg
    exp_cfg = ExperimentConfig(name="R1_alignment", use_analog=False)
    model = build_model(exp_cfg, num_classes=num_classes, device=device)

    # Use the official R1 checkpoint
    ckpt_path = "checkpoints/R1_FP32_baseline_best.pt"
    if not os.path.exists(ckpt_path):
        print(f"Checkpoint not found: {ckpt_path}")
        return

    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()

    # Configure CrossSim properly for 4-bit weights, 5% C2C, 10% D2D
    n_layers = len(convertible_modules(model))
    print(f"Test model has {n_layers} convertible layers")

    # CrossSim parameters (Canonical Alignment)
    params = dnn_inference_params(
        ideal=False,
        core_style="BALANCED",
        Nslices=1,
        weight_bits=4,
        weight_percentile=100,
        digital_bias=True,
        error_model="generic",
        alpha_error=0.1, # D2D noise 10%
        proportional_error=False,
        noise_model="generic",
        alpha_noise=0.05, # C2C noise 5%
        proportional_noise=False,
        drift_model="IdealDevice", # Use a valid name
        t_drift=0,
        adc_bits=8,
        adc_range_option="CALIBRATED",
        useGPU=(device.type == "cuda"),
        input_range=(0, 1),
        adc_range=(0, 10),
    )
    params_list = [params] * n_layers

    # Convert model to CrossSim
    print("Converting model to CrossSim analog model...")
    analog_model = from_torch(model, params_list, fuse_batchnorm=True)
    analog_model = analog_model.to(device)

    # Get dataloader
    _, test_loader = get_dataloaders("cifar10", batch_size=1, num_workers=1)
    criterion = nn.CrossEntropyLoss()

    print("Evaluating CrossSim ResNet-18 (Batch Size 1)...")
    correct = 0
    total = 0
    start_time = time.time()
    
    # Evaluate 50 images for numerical sanity check
    for i, (inputs, targets) in enumerate(test_loader):
        inputs, targets = inputs.to(device), targets.to(device)
        with torch.no_grad():
            outputs = analog_model(inputs)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
        if i >= 49: break 

    acc = 100.0 * correct / total
    print(f"CrossSim ResNet-18 Accuracy: {acc:.2f}% (Time: {time.time()-start_time:.1f}s)")

    results = {
        "model": "resnet18",
        "dataset": "cifar10",
        "crosssim": {
            "accuracy": acc,
            "weight_bits": 4,
            "c2c_noise": 0.05,
            "d2d_noise": 0.1
        }
    }
    
    with open("report_md/_gpt/crosssim_resnet_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_crosssim_resnet()
