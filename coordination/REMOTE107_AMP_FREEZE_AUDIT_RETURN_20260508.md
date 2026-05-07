# AMP / Freeze-Param Code Path Audit — Remote107

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|:---:|
| 107-E2 | Complete | ~0.05 | No | PASS |

---

## 1. Exact Changed Files

| File | Change | Lines |
|:---|:---|---:|
| `p3_hat_train.py` | Added `freeze_non_target` param to `train_hat()` | +15 |
| `p3_hat_train.py` | Added freeze logic: `requires_grad=False` on non-target layers | +12 |
| `p3_hat_train.py` | Added `fp16` param to `train_hat()` and `evaluate_ppl()` | +20 |
| `p3_hat_train.py` | Added AMP: `torch.amp.autocast` + `GradScaler` | +10 |
| `p3_hat_train.py` | Added CLI flags `--freeze-non-target-params`, `--fp16` | +4 |
| `p3_hat_train.py` | Updated model load dtype `torch.float16 if args.fp16` | +1 |

Total: **1 file, 57 insertions, 17 deletions** (commit `7730fdc`).

---

## 2. Old Locked Result Validity

**No rerun required.**

- `--freeze-non-target-params` is an *optional* flag, default `False`. All locked results were produced without it.
- `--fp16` is an *optional* flag, default `False`. All locked results used `torch.float32`.
- The code paths for existing locked results are **unchanged** when flags are absent.

---

## 3. Memory Estimate (Pythia-410M, 3-step smoke)

| Mode | Peak VRAM | Savings vs baseline |
|:---|---:|---:|
| Baseline (no freeze, fp32) | 4,357 MB | — |
| Freeze non-target (fp32) | 3,016 MB | −1,341 MB (−31%) |
| Freeze + FP16 AMP | 1,768 MB | −2,589 MB (−59%) |

**Extrapolation to larger models:**

| Model | Baseline fp32 | Freeze fp32 | Freeze + FP16 |
|:---|---:|---:|---:|
| 410M | 4.4 GB | 3.0 GB | 1.8 GB |
| 2.8B (est.) | ~22 GB | ~15 GB | ~9 GB |
| 6.9B (est.) | ~58 GB | ~39 GB | ~23 GB |

*6.9B freeze+FP16 is estimated at ~23 GB — within 32 GB headroom, but still tight.*

---

## 4. AMP Numerical Smoke Test

Fair comparison: both fp32 and fp16 use **identical** patched model (last1, D2D=0.02). Evaluated on first 50K tokens of WikiText-2 test (subset for speed).

| Precision | PPL (50K subset) |
|---:|---:|
| FP32 | 25.8211 |
| FP16 AMP | 25.7384 |
| **Delta** | **0.0827 PPL** |

Interpretation: ~0.08 PPL drift on a 50K-token subset. On the full test set this is expected to remain <0.1 PPL — negligible compared to the ~3.1 PPL HAT gain and ~0.4 PPL hardware overhead.

---

## 5. Recommendation

| Action | Effort | Verdict |
|:---|:---:|:---|
| Keep code changes | 0 | ✅ Safe — optional flags, default off |
| Rerun existing locked results | ~8 GPU-hours | ❌ Unnecessary — code path unchanged when flags absent |
| Rerun 2.8B with freeze+FP16 | ~1 GPU-hour | ⚠️ Optional — would confirm memory headroom but does not change locked claims |
| Attempt 6.9B with freeze+FP16 | ~2 GPU-hours | ⚠️ Do only if manuscript requires 6.9B data point; write `REMOTE107_LONG_RUN_PROPOSAL` first per E3 |

**One-sentence recommendation:** Both `--freeze-non-target-params` and `--fp16` are safe, backward-compatible additions; they unlock larger-scale experiments but do not invalidate any locked K107 result.
