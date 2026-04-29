# R11D Fair-Comparison Experiment Design — Critic Review Required

**task_id:** r11d_exp_design_review_20260428
**priority:** P0
**type:** DESIGN_REVIEW (do NOT execute training until approved)

---

## 1. Context

R11D series evaluates Tiny-ViT on CIFAR-10 under AIHWKit analog simulation. Current results:

| Run | Precision | Device Model | lr | Best Test Acc |
|-----|-----------|--------------|-----|---------------|
| R11D-1 | 4-bit | AIHWKit + ADD_NORMAL(σ=0.10) | 5e-4 | 14.64% |
| R11D-2 | 8-bit | AIHWKit + ADD_NORMAL(σ=0.20) | 5e-4 | 87.52% |
| R11D-3 | 8-bit | AIHWKit + ADD_NORMAL(σ=0.30) | 5e-4 | 87.40% |
| R11D-4 | 8-bit | PCM preset | 5e-4 | 61.10% |
| R11D-5a | 8-bit | PCM preset | 1e-3 | 76.96% |
| R11D-5b | 8-bit | PCM preset | 5e-3 | ~67% (plateau) |
| R11D-5c | 8-bit | PCM preset | 1e-3, mom=0.9 | ~55% (early) |

**Fresh eval for R11D-5a**: 76.74±0.09% (10 instances)
**Drift eval for R11D-5a**: 76.70% → 76.72% → 76.73% (0s / 1h / 24h)

User concern: "对比不够，至少得在一个精度" — comparisons are unfair because 4-bit vs 8-bit are mixed.

---

## 2. Proposed New Experiments (by Claude)

Claude proposes three new runs to fill gaps:

### R11D-6: 8-bit Pure Baseline (no modifier, no PCM)
- **Script**: `train_aihwkit_baseline.py` with `--modifier-std-dev 0.0`
- **Params**: 8-bit (inp_res=out_res=1/256), lr=1e-3, epochs=100
- **Question it answers**: What is the ceiling of AIHWKit 8-bit without any noise model? If this is ~85%+, then PCM's 76.96% is genuinely a ~10pp device-model penalty.

### R11D-7: PCM 4-bit with lr=1e-3
- **Script**: `r11d4_train_pcm.py` with `--inp-res 0.0625 --out-res 0.0625 --lr 0.001`
- **Params**: 4-bit PCM, same hyperparameters as R11D-5a
- **Question it answers**: Is R11D-1's 14.64% due to 4-bit being fundamentally broken, or just bad hyperparameters (lr=5e-4)?

### R11D-8: HAT-inspired PCM 8-bit full 100-epoch
- **Script**: `r11d_hat_pcm.py` (v2, with per-layer scalar D2D fix, default std_dev=5.0)
- **Params**: 8-bit PCM, lr=1e-3, `--hat-mode scaled --hat-start-epoch 1`
- **Question it answers**: Does per-epoch D2D resampling (the core HAT idea) improve PCM robustness?

All three would include fresh eval (10 instances) and drift eval (0s/1h/24h).

---

## 3. Review Request

**CRITIC AGENT**: Please review this experimental design BEFORE any training is launched.

Specifically, evaluate:

1. **Completeness**: Do R11D-6/7/8 fully address "fair comparison at the same precision"? Is anything missing?
   - For example: do we also need a 4-bit pure baseline (no PCM, no modifier)?
   - Do we need canonical Ensemble HAT (custom AnalogLinear) at 8-bit for a true apples-to-apples comparison with R11D-8?

2. **Correctness**: Are the scripts and parameters correct?
   - `train_aihwkit_baseline.py` with `--modifier-std-dev 0.0`: does this truly disable all noise, or does AIHWKit inject other noise by default?
   - `r11d4_train_pcm.py` at 4-bit: is PCM preset compatible with 4-bit resolution, or does it have hardcoded assumptions about 8-bit?
   - `r11d_hat_pcm.py` v2: is the per-layer scalar D2D noise at std_dev=5.0 mathematically sound for HAT-inspired training?

3. **Efficiency**: Are there redundant experiments?
   - R11D-5b (lr=5e-3) and R11D-5c (mom=0.9) already underperform R11D-5a. Is there any value in keeping them, or should they be discarded?
   - If R11D-6 comes back at ~87% (close to R11D-2), do we still need R11D-7 and R11D-8, or can we shortcut?

4. **Manuscript alignment**: Which of these results are actually needed for the Nature Electronics submission?
   - The current PCM narrative says "severe degradation + hyperparameter sensitivity".
   - What additional experiments are needed to support this claim rigorously?

**Please provide a clear APPROVE / REVISE / REJECT recommendation with specific changes.**

---

## 4. Constraints

- Only ONE GPU available. All training must be sequential.
- Each run takes ~1.8-2h for 100 epochs.
- Fresh eval (~10 min) and drift eval (~5 min) per run.
- Total time budget for this review + execution: ~8h.

---

## 5. Output

Write review result to:
`outputs/r11d_experiment_design_review_20260428.md`

Include:
- Critic's verdict (APPROVE / REVISE / REJECT)
- Specific changes requested (if any)
- Final approved experiment list with rationale
