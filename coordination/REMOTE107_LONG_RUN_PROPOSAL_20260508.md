# Remote107 Long-Run Proposal — Pythia-6.9B Selective Terminal-Layer Analog KV

| Task | Proposed GPU-hours | Expected VRAM | Claim it changes |
|---|---:|---:|:---|
| 107-P3-6P9B-VALIDATION | ~2 GPU-hours | ~23 GB (fp16+freeze) | Extends monotonic scale trend 410M→1B→2.8B→6.9B |

---

## 1. Motivation

Locked results show a monotonic scale trend:

| Model | D2D=0.02 PPL |
|:---|---:|
| Pythia-410M | 19.48 |
| Pythia-1B | 14.60 |
| Pythia-2.8B | 13.33 |
| **Pythia-6.9B** | **?** |

If 6.9B continues the trend (expected ~12.5–12.8 PPL), it strengthens the manuscript claim that **analog KV cache viability improves with model scale**. Without 6.9B, the trend stops at 2.8B and leaves a gap.

---

## 2. Memory Plan

| Component | FP32 | FP16+freeze |
|:---|---:|---:|
| Model weights | ~27.6 GB | ~13.8 GB |
| Gradients | ~27.6 GB | ~0.1 GB (only last1 attention) |
| Activations (bs=1, seq=512) | ~2–4 GB | ~2–4 GB |
| Optimizer state (AdamW, selective) | ~0.4 GB | ~0.4 GB |
| **Total estimated** | **~58 GB** | **~17–19 GB** |

Headroom on 32GB GPU: ~13–15 GB. Safe even with CUDA fragmentation.

Code flags required:
```bash
--analog_layers 31 \
--fp16 \
--freeze-non-target-params
```

---

## 3. Exact Command

### Phase A — Dry-run eval smoke (no training)

```bash
CUDA_VISIBLE_DEVICES=0 \
/home/lisq753/miniconda3/envs/LLM/bin/python p3_hat_eval.py \
  --checkpoint_dir "EleutherAI/pythia-6.9b-deduped" \
  --n_states 256 \
  --sigma_d2d 0.02 \
  --sigma_c2c 0.0 \
  --max_length 512 \
  --output_dir /tmp/p6p9b_smoke
```

*If this OOMs, abort immediately.*

### Phase B — 20-step HAT smoke (not full 100-step)

```bash
CUDA_VISIBLE_DEVICES=0 \
/home/lisq753/miniconda3/envs/LLM/bin/python p3_hat_train.py \
  --name p6p9b_last1_d2d002 \
  --model_name "EleutherAI/pythia-6.9b-deduped" \
  --n_states 256 \
  --sigma_c2c 0.01 \
  --sigma_d2d 0.02 \
  --max_steps 20 \
  --analog_layers 31 \
  --fp16 \
  --freeze-non-target-params \
  --output_dir /home/lisq753/projects/HAT_kv107/paper2/results/remote107
```

### Phase C — Full 100-step train + eval (only if Phase B succeeds)

Same as Phase B but `--max_steps 100`, plus 3-seed eval at D2D=0.02 and 0.05.

---

## 4. Stop Criteria

| Condition | Action |
|:---|:---|
| Phase A OOM | Kill — fp16+freeze insufficient |
| Phase B OOM at step < 5 | Kill — need DeepSpeed or multi-GPU |
| Phase B loss diverges (nan/inf) | Kill — fp16 numerically unstable at 6.9B |
| Phase B PPL after 20 steps > 50 | Kill — model incompatible with analog KV |
| Wall time > 2 hours for 20 steps | Kill — impractical for full run |

---

## 5. What Claim Changes

| Scenario | Claim |
|:---|:---|
| Phase C completes, D2D=0.02 PPL < 13.0 | **Strong**: monotonic trend holds to 6.9B |
| Phase C completes, D2D=0.02 PPL 13.0–13.5 | **Moderate**: 6.9B viable but gains plateau |
| Phase C completes, PPL > 15.0 | **Weak**: scale advantage saturates or reverses |
| Any phase killed | **No claim change** — manuscript stays at 2.8B |

---

## 6. Risk Mitigation

- **Download risk:** 6.9B weights (~14GB) may take 10–30 min to download. Run Phase A in background while doing other work.
- **GPU lock:** Use only 1 GPU (CUDA_VISIBLE_DEVICES=0). Remaining 7 GPUs stay available for other tasks.
- **Disk risk:** Checkpoint ~14GB. Ensure `HAT_kv107` mount has >50GB free.

---

## 7. One-Sentence Summary

Pythia-6.9B last1 analog KV is analytically feasible on 32GB GPUs with fp16+freeze; a 20-step smoke test costs ~1 GPU-hour and either extends the scale trend to 6.9B or cleanly bounds it — low risk, high information value.
