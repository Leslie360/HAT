import torch
import torch.nn as nn
import sys
import os
import json
import dataclasses

sys.path.insert(0, '/home/qiaosir/projects/cross-sim')
sys.path.insert(0, '/home/qiaosir/projects/cross-sim/applications/dnn')

from simulator.algorithms.dnn.torch.convert import from_torch, convertible_modules
from dnn_inference_params import dnn_inference_params
from train_tinyvit import build_model, get_dataloaders, evaluate, TinyViTExperimentConfig

def run_crosssim_tinyvit():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load FP32 TinyViT model
    num_classes = 10
    base_cfg = TinyViTExperimentConfig(name="V1", use_hybrid=False, noise_enabled=False)
    model = build_model(base_cfg, num_classes=num_classes, device=device)

    # Use the official V1 checkpoint
    ckpt_path = "checkpoints/V1_fp32_digital_baseline_best.pt"
    if not os.path.exists(ckpt_path):
        print(f"Checkpoint not found: {ckpt_path}")
        return

    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    # The checkpoint has 'model_state_dict' but it's for Analog model if use_analog was True.
    # V1 has use_analog=False.
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()

    # Configure CrossSim properly for 4-bit weights, 5% noise
    n_layers = len(convertible_modules(model))
    print(f"Test model has {n_layers} convertible layers")

    # CrossSim parameters
    params = dnn_inference_params(
        ideal=False,
        core_style="BALANCED",
        Nslices=1,
        weight_bits=4,
        weight_percentile=100,
        digital_bias=True,
        Rmin=1e4,
        Rmax=1e5,
        infinite_on_off_ratio=False,
        error_model="generic",
        alpha_error=0.1, # D2D noise 10%
        proportional_error=False,
        noise_model="generic",
        alpha_noise=0.05, # C2C noise 5%
        proportional_noise=False,
        drift_model="none",
        t_drift=0,
        NrowsMax=512,
        NcolsMax=None,
        Rp_row=0,
        Rp_col=0,
        interleaved_posneg=False,
        subtract_current_in_xbar=True,
        current_from_input=True,
        input_bits=8,
        input_bitslicing=False,
        input_slice_size=1,
        adc_bits=8,
        adc_range_option="CALIBRATED",
        adc_type="generic",
        adc_per_ibit=False,
        useGPU=(device.type == "cuda"),
        positiveInputsOnly=False,
        input_range=(0, 1),
        adc_range=(0, 10),
    )
    params_list = [params] * n_layers

    # Convert model to CrossSim analog model
    print("Converting model to CrossSim analog model...")
    try:
        analog_model = from_torch(model, params_list, fuse_batchnorm=True, bias_rows=0)
        analog_model = analog_model.to(device)
    except Exception as e:
        print(f"Failed to convert model: {e}")
        return

    # Get dataloader
    _, test_loader = get_dataloaders("cifar10", batch_size=64, num_workers=2)
    criterion = nn.CrossEntropyLoss()

    print("Evaluating CrossSim model...")
    running_loss = 0.0
    correct = 0
    total = 0

    # Limit evaluation to 10 batches for speed, or full? Full might be slow but let's do 20 batches
    import time
    start_time = time.time()
    for i, (inputs, targets) in enumerate(test_loader):
        inputs, targets = inputs.to(device), targets.to(device)
        with torch.no_grad():
            outputs = analog_model(inputs)
            loss = criterion(outputs, targets)

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
        if i >= 19: # 20 batches * 256 = 5120 images (half of CIFAR-10 test set)
            break

    acc = 100.0 * correct / total
    print(f"CrossSim Evaluation Accuracy: {acc:.2f}% (Time: {time.time()-start_time:.1f}s)")

    results = {
        "crosssim": {
            "accuracy": acc,
            "batches_evaluated": 20,
            "weight_bits": 4,
            "c2c_noise": 0.05,
            "d2d_noise": 0.1
        }
    }
    
    with open("report_md/_gpt/crosssim_tinyvit_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_crosssim_tinyvit()
