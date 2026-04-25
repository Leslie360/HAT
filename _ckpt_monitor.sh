#!/bin/bash
while true; do
    clear
    echo "=== $(date '+%H:%M:%S') GPU+CKPT MONITOR ==="
    nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader 2>/dev/null
    echo ""
    
    /home/qiaosir/miniconda3/envs/LLM/bin/python << 'PYEOF'
import torch, glob, os
from datetime import datetime

dirs = [
    ("Standard HAT (V3)", "checkpoints/_gpt/postfix_standard_hat"),
    ("Proportional HAT (V4)", "checkpoints/_gpt/postfix_proportional"),
    ("V1 Baseline", "checkpoints/_gpt/postfix_v1_baseline"),
]

for name, d in dirs:
    last = os.path.join(d, "*_last.pt")
    best = os.path.join(d, "*_best.pt")
    last_files = glob.glob(last)
    best_files = glob.glob(best)
    if last_files:
        ckpt = torch.load(last_files[0], map_location='cpu')
        epoch = ckpt.get('epoch', '?')
        history = ckpt.get('history', {})
        if isinstance(history, dict):
            test_acc = history.get('test_acc', [])
            train_acc = history.get('train_acc', [])
            if test_acc:
                print(f"{name}: epoch={epoch}, test={test_acc[-1]:.2f}%, train={train_acc[-1]:.2f}%, max_test={max(test_acc):.2f}%")
            else:
                print(f"{name}: epoch={epoch}, no history")
        else:
            print(f"{name}: epoch={epoch}")
        mtime = os.path.getmtime(last_files[0])
        print(f"  last saved: {datetime.fromtimestamp(mtime).strftime('%H:%M:%S')}")
    else:
        print(f"{name}: no checkpoint yet")
    print("")
PYEOF
    sleep 30
done
