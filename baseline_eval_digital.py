"""
Digital baseline eval using current K107 evaluator (evaluate_ppl).
"""
import os, sys, json, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from p3_hat_train import evaluate_ppl

device = "cuda:0"
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-410m-deduped", torch_dtype=torch.float32)
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-410m-deduped")
tokenizer.pad_token = tokenizer.eos_token
model = model.to(device)

start = time.time()
ppl = evaluate_ppl(model, tokenizer, device, max_length=512)
elapsed = time.time() - start

result = {
    "evaluator": "p3_hat_train.evaluate_ppl",
    "model": "EleutherAI/pythia-410m-deduped",
    "analog_patch": False,
    "ppl": ppl,
    "ctx_len": 512,
    "stride": 256,
    "batch_size": 1,
    "dataset": "wikitext-2-raw-v1 (test)",
    "wall_clock_time": elapsed,
    "gpu": torch.cuda.get_device_name(device),
}

out_path = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/baseline_digital_current.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"Digital baseline PPL = {ppl:.4f}  ({elapsed:.1f}s)")
print(f"Saved: {out_path}")
