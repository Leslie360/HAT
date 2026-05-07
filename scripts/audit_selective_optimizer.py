"""
Audit selective optimizer: count trainable vs total params for 410M/1B/2.8B.
"""
import torch
from transformers import AutoModelForCausalLM

MODELS = [
    ("pythia-410m", "EleutherAI/pythia-410m-deduped", 23),
    ("pythia-1b", "EleutherAI/pythia-1b-deduped", 15),
    ("pythia-2.8b", "EleutherAI/pythia-2.8b-deduped", 31),
]

print("| Model | Total params | last1 attention params | Ratio |")
print("|:---|---:|---:|---:|")

for tag, name, last_layer in MODELS:
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32)
    total = sum(p.numel() for p in model.parameters())

    # Simulate selective optimizer logic from train_hat
    params_to_optimize = []
    for mod_name, module in model.named_modules():
        if 'attention' in mod_name.lower() and type(module).__name__ == 'GPTNeoXAttention':
            layer_idx = None
            for p in mod_name.split('.'):
                if p.isdigit():
                    layer_idx = int(p)
                    break
            if layer_idx is not None and layer_idx == last_layer:
                params_to_optimize.extend(list(module.parameters()))

    trainable = sum(p.numel() for p in params_to_optimize)
    ratio = trainable / total * 100
    print(f"| {tag} | {total:,} | {trainable:,} | {ratio:.2f}% |")
    del model
    torch.cuda.empty_cache()
