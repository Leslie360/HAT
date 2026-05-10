# Kimi Task: 6-bit PCM Drift Closure Report

**Date:** 2026-05-09
**Task Owner:** kimi (per codex revised dispatch 2026-05-09T12:15+08:00)
**Scope:** Run missing new-protocol 6-bit drift evals for seeds 456/457/789

---

## Status: ✅ COMPLETE

All three missing drift evals have been run and JSON outputs are written.

---

## Raw Results

### Seed 456
- **Checkpoint:** `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/best.pt`
- **t=0s:** 62.41%
- **t=3600s:** 62.57%
- **t=86400s:** 62.12%
- **24h drift:** -0.29 pp
- **JSON:** `checkpoints/r11d_6bit_pcm_seed456/drift_eval.json`

### Seed 457
- **Checkpoint:** `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/best.pt`
- **t=0s:** 76.63%
- **t=3600s:** 76.66%
- **t=86400s:** 76.68%
- **24h drift:** +0.05 pp
- **JSON:** `checkpoints/r11d_6bit_pcm_seed457/drift_eval.json`

### Seed 789
- **Checkpoint:** `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/best.pt`
- **t=0s:** 66.14%
- **t=3600s:** 66.09%
- **t=86400s:** 66.07%
- **24h drift:** -0.07 pp
- **JSON:** `checkpoints/r11d_6bit_pcm_seed789/drift_eval.json`

### Seed 123 (pre-existing)
- **t=0s:** 68.93%
- **t=3600s:** 68.97%
- **t=86400s:** 68.98%
- **24h drift:** +0.05 pp

---

## Aggregate Drift Summary

| Seed | Fresh (t=0) | 1h Drift | 1d Drift | Net 24h |
|------|-------------|----------|----------|---------|
| 123 | 68.93% | 68.97% | 68.98% | **+0.05 pp** |
| 456 | 62.41% | 62.57% | 62.12% | **-0.29 pp** |
| 457 | 76.63% | 76.66% | 76.68% | **+0.05 pp** |
| 789 | 66.14% | 66.09% | 66.07% | **-0.07 pp** |

**4-seed mean drift:** -0.07 pp
**4-seed std:** 0.14 pp

---

## Key Finding

**6-bit PCM under the new protocol (`enable_during_test=True`) is drift-flat.**

All four seeds show 24h drift within ±0.3 pp. This confirms DS's physical prediction: at the 6-bit resolution, PCM retention decay is negligible for the CIFAR-10 deployment window.

The trade-off is **not** "accuracy vs retention" (as the old narrative framed it). The real trade-off is:

- **4-bit:** high fresh accuracy (76.68%) but poor retention (-4.0 pp)
- **6-bit:** low fresh accuracy (68.55%) with high cross-seed variance (±6 pp) but excellent retention (~0 pp)
- **8-bit:** high fresh accuracy (77.60%) with low variance and excellent retention (~0 pp)

In other words, **6-bit does not dominate on either axis.** 8-bit is strictly better on fresh accuracy and comparable on retention. The only reason to consider 6-bit is if chip area / energy constraints make 8-bit infeasible — a system-level claim that requires circuit-level evidence not present in this paper.

---

## Provenance

- **Training script:** `paper2_aihwkit_baseline/r11d4_train_pcm_extended.py`
- **Training protocol:** `enable_during_test=True` (line 146 patched)
- **Drift eval script:** `paper2_aihwkit_baseline/eval_aihwkit_drift.py`
- **Python env:** `/home/qiaosir/miniconda3/envs/aihwkit/bin/python`
- **GPU:** Single CUDA device (no multi-GPU)
- **Run date:** 2026-05-09 ~01:20–01:40 CST

---

## Recommendation for Paper-1

1. **Replace all 6-bit claims** referencing 77.86% with 68.55 ± 6.03%.
2. **Drop "Pareto midpoint"** framing entirely. 8-bit dominates 6-bit on accuracy with equal retention.
3. **If 6-bit is retained in the narrative**, frame it as: "a seed-sensitive transition regime where quantization-D2D interaction suppresses fresh accuracy but preserves long-term retention."
4. **Add a cautionary note** about cross-seed variance (std ~6 pp) — this is larger than the 4-bit/8-bit drift penalties and is a real deployment risk.

---

*Report by kimi. Data sourced from local checkpoint filesystem as of 2026-05-09.*
