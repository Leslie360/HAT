# HAT Analog KV — Deliverable

## Structure

```
deliverable/
├── sync_results.sh        # Run after pipeline finishes: copies new JSONs
├── README.md              # this file
│
├── code/                  # Core reproduction code
│   ├── p3_hat_train.py    # HAT training (STE, retention, D2D/C2C)
│   ├── p3_hat_eval.py     # Evaluate checkpoint under noise
│   ├── analog_layers.py   # Analog linear layer definitions
│   └── analog_kv_cache.py # AnalogKVCacheConfig
│
├── pipeline/              # Auto-dispatch pipeline (40 tasks, 8 GPUs)
│   ├── pipeline_runner.py
│   └── pipeline_health.sh
│
├── results_v2/            # v2 corrected results (current)
│   ├── baseline_digital_seed42.json       # PPL 15.68
│   ├── eval_hat_*_v2_*.json               # 20 generalization eval runs
│   └── hat_*_v2_seed*.json                # ~20 training results
│
└── p0_p3_archive/         # Pre-v2 results (ctx512 bug, P0-P3 sweep)
    ├── baseline_digital.json
    ├── hat_*.json                          # v1 training results
    ├── p0_*.json / p1_*.json / p2_*.json / p3_*.json
```

## How to update

```bash
# After pipeline completes Phase 3:
bash deliverable/sync_results.sh
git add deliverable/
git commit -m "update results"
git push
```

## Key findings (v2)

| Metric | v1 (bug) | v2 (corrected) |
|--------|----------|----------------|
| D2D=0.02 noise | 22.29 PPL | 25.49 PPL |
| D2D=0.04 noise | 31.85 PPL | 35.93 PPL |
| C2C=0.01 noise | 19.97 PPL | 21.21 PPL |
| Baseline digital | 15.68 PPL | 15.68 PPL |
| Best selective (last1) | — | 18.14 PPL |

See `RESULTS_v2.md` for full tables.
