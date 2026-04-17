import torch
import sys
sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

from train_resnet18 import (
    build_model,
    create_resnet18_cifar,
    load_experiment_config_from_checkpoint,
    set_noise_for_eval,
)
from analog_layers import AnalogLinearConfig

checkpoint_path = 'checkpoints/R4_4bit_noise_HAT_best.pt'
ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)

exp_cfg_dict = ckpt['exp_cfg']
print("Checkpoint Config:", exp_cfg_dict)
cfg = load_experiment_config_from_checkpoint(ckpt)

model = build_model(cfg, num_classes=10, device='cpu')

# Compare state dicts
model_sd = model.state_dict()
ckpt_sd = ckpt['model_state_dict']

missing_in_ckpt = set(model_sd.keys()) - set(ckpt_sd.keys())
missing_in_model = set(ckpt_sd.keys()) - set(model_sd.keys())

print("Missing in Checkpoint:", missing_in_ckpt)
print("Missing in Model:", missing_in_model)

# Let's load the state dict and see if w_abs_max is restored correctly
model.load_state_dict(ckpt_sd, strict=False)

for name, module in model.named_modules():
    if hasattr(module, 'config') and isinstance(module.config, AnalogLinearConfig):
        print(f"{name}:")
        print(f"  w_abs_max: {module.w_abs_max.item() if hasattr(module, 'w_abs_max') else 'None'}")
        if 'w_abs_max' in ckpt_sd:
            pass # wait, it's layer specific
        ckpt_key = f"{name}.w_abs_max"
        if ckpt_key in ckpt_sd:
            print(f"  ckpt_w_abs_max: {ckpt_sd[ckpt_key].item()}")
