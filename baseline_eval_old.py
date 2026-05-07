"""
Old-style digital baseline eval using p3_e2e_eval parameters.
max_length=1024, stride=512, batch_size=8.
"""
import os, sys, json, time, math
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')

def evaluate_ppl_old(model, tokenizer, device, max_length=1024, stride=512, batch_size=8):
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    encodings = tokenizer("\n\n".join(dataset["text"]), return_tensors="pt")
    input_ids = encodings.input_ids.to(device)

    nlls = []
    prev_end_loc = 0
    seq_len = input_ids.size(1)

    for begin_loc in tqdm(range(0, seq_len, stride), desc="Evaluating PPL"):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc
        input_ids_chunk = input_ids[:, begin_loc:end_loc]
        target_ids = input_ids_chunk.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids_chunk, labels=target_ids)
            neg_log_likelihood = outputs.loss * trg_len

        nlls.append(neg_log_likelihood)
        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    return ppl.item()


device = "cuda:0"
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-410m-deduped", torch_dtype=torch.float32)
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-410m-deduped")
tokenizer.pad_token = tokenizer.eos_token
model = model.to(device)

start = time.time()
ppl = evaluate_ppl_old(model, tokenizer, device, max_length=1024, stride=512, batch_size=8)
elapsed = time.time() - start

result = {
    "evaluator": "old_e2e_eval (max_length=1024, stride=512)",
    "model": "EleutherAI/pythia-410m-deduped",
    "ppl": ppl,
    "max_length": 1024,
    "stride": 512,
    "batch_size": 8,
    "dataset": "wikitext-2-raw-v1 (test)",
    "wall_clock_time": elapsed,
}

out_path = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/baseline_digital_old.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"Old digital baseline PPL = {ppl:.4f}  ({elapsed:.1f}s)")
print(f"Saved: {out_path}")
