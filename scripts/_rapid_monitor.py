#!/usr/bin/env python3
"""Rapid monitor: checks all three experiments every 15 seconds."""
import sys, time, os
sys.path.insert(0, ".")
import torch

def check():
    now = time.strftime("%H:%M:%S")
    print(f"\n=== {now} ===")
    
    # 1. Ensemble HAT (stopped, show fresh eval result)
    json_path = "report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json"
    if os.path.exists(json_path):
        import json
        with open(json_path) as f:
            d = json.load(f)
        print(f"Ensemble HAT FRESH: mean={d['cross_instance_mean']:.2f}%, std={d['cross_instance_std']:.2f}%")
    
    # 2. Standard HAT
    p1 = "checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_last.pt"
    if os.path.exists(p1):
        c = torch.load(p1, map_location='cpu', weights_only=False)
        h = c.get('history', {})
        print(f"Standard HAT: epoch={c.get('epoch')}, best={c.get('best_acc')}%, last_test={h.get('test_acc',[-1])[-1] if h.get('test_acc') else 'N/A'}%")
    
    # 3. Proportional HAT
    p2 = "checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_last.pt"
    if os.path.exists(p2):
        c = torch.load(p2, map_location='cpu', weights_only=False)
        h = c.get('history', {})
        print(f"Proportional HAT: epoch={c.get('epoch')}, best={c.get('best_acc')}%, last_test={h.get('test_acc',[-1])[-1] if h.get('test_acc') else 'N/A'}%")
    
    # 4. GPU
    import subprocess
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,temperature.gpu", "--format=csv,noheader"], text=True)
        print(f"GPU: {out.strip()}")
    except:
        pass

if __name__ == "__main__":
    while True:
        check()
        time.sleep(15)
