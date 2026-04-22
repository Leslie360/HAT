# Data Integrity & Source Audit — Final Report
**Date:** 2026-04-22 22:15 CST  
**Auditor:** Kimi  
**Scope:** All Round Q experiment data (K1-K4), source code correctness, pipeline integrity

---

## Executive Summary

| Area | Status | Key Finding |
|:-----|:------:|:------------|
| Source math correctness | ⚠️ FIXED (uncommitted) | `nl` multiplier missing in backward; fixed in working tree but all K-series ran on buggy code |
| JSON data integrity | ✅ PASS | All 9 eval JSONs: mean/std calculations verified correct |
| Checkpoint provenance | ✅ PASS | All referenced checkpoints exist (76MB each) |
| Train/eval consistency | ⚠️ PARTIAL | K2 eval may have used `delta_g_eff=0.0` (literal zero) while train used auto-fill |
| K4 continuity | 🛑 BROKEN | Alpha=0.75 training stopped at epoch 2; no error logged |

---

## 1. Source Code Mathematical Correctness

### 1.1 The `nl` multiplier bug

**Location:** `analog_layers.py:237` (LTP branch) and `:243` (LTD branch)  
**Status:** FIXED in working tree, **UNCOMMITTED**

Git diff confirms both branches now have the `nl` multiplier:
```diff
-            ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)
+            ltp_scale = nl_ltp * torch.pow(ltp_ratio, nl_ltp - 1.0)
-            ltd_scale = torch.pow(ltd_ratio, nl_ltd - 1.0)
+            ltd_scale = nl_ltd * torch.pow(ltd_ratio, nl_ltd - 1.0)
```

Also fixed: `correction = alpha * torch.where(...)` now correctly scales by `second_order_alpha`.

**Impact timeline:**
- File modification time: `2026-04-22 22:03`
- K3 sweep: `2026-04-21 23:04` → `2026-04-22 10:01` (BUGGY)
- K4 alpha=0.00: `2026-04-22 10:41` → `14:07` (BUGGY)
- K4 alpha=0.25: `2026-04-22 14:10` → `17:39` (BUGGY)
- K4 alpha=0.50: `2026-04-22 ~19:00` → `21:07` (BUGGY)
- K4 alpha=0.75: `2026-04-22 21:07` → stopped epoch 2 (BUGGY)

**Conclusion:** ALL completed K-series results to date were produced with the mathematically incorrect backward.

### 1.2 Other code fixes in working tree (uncommitted)

| Fix | File | Time |
|:----|:-----|:-----|
| `nl` multiplier on both LTP/LTD scales | `analog_layers.py` | 22:03 |
| `second_order_alpha` field added to `AnalogLinearConfig` | `analog_layers.py` | 22:03 |
| `RuntimeWarning` for SO2+non-positive delta_g_eff | `analog_layers.py` | 22:03 |
| `import copy` added | `analog_layers.py` | 22:03 |
| `DEPRECATED` header | `analog_layers_ensemble.py` | ~22:00 |
| `DEPRECATED` header | `run_ensemble_hat_fixed.py` | ~22:00 |
| `%%` → `%` in help string | `train_tinyvit_ensemble.py` | ~22:00 |

---

## 2. Experiment Data Integrity

### 2.1 JSON mathematical validation

All 9 eval JSONs pass mean/std self-consistency checks:

```
cx_k3_eval_k3_dgeff_0p05.json  PASS
cx_k3_eval_k3_dgeff_0p10.json  PASS
cx_k3_eval_k3_dgeff_0p15.json  PASS
cx_k3_eval_k3_dgeff_0p20.json  PASS
cx_k3_eval_k3_dgeff_0p25.json  PASS
cx_k4_eval_k4_alpha_0p00.json  PASS
cx_k4_eval_k4_alpha_0p25.json  PASS
cx_k4_eval_k4_alpha_0p50.json  PASS
cx_k2_fresh_eval.json          PASS
```

### 2.2 Checkpoint file validation

All 9 eval JSONs reference checkpoints that exist on disk (76MB each, consistent size).

### 2.3 K2 data

- `N=30` fresh instances
- `cross_instance_mean=38.95%`, `cross_instance_std=9.85%`
- Range: `22.03% – 61.69%`
- Checkpoint: `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt` ✅ exists

### 2.4 K3 data (buggy backward)

| delta_g_eff | train best | fresh mean | fresh std |
|:------------|-----------:|-----------:|----------:|
| 0.05 | 91.52% @ 72 | 36.21% | 9.61% |
| 0.10 | 90.97% @ 92 | 30.79% | 11.59% |
| 0.15 | 91.27% @ 82 | 27.85% | 7.37% |
| 0.20 | 91.50% @ 93 | 33.25% | 10.29% |
| 0.25 | 91.24% @ 76 | 30.08% | 9.07% |

**Note:** No individual train JSONs for 0.05; data sourced from aggregate `cx_k3_dgeff_continuation.json`. Individual train JSONs exist for 0.10/0.15/0.20/0.25.

### 2.5 K4 data (buggy backward)

| alpha | train best | fresh mean | fresh std | range |
|:------|-----------:|-----------:|----------:|:------|
| 0.00 | 91.92% @ 95 | 33.28% | 9.02% | 19.5% – 52.3% |
| 0.25 | 91.32% @ 75 | **44.29%** | 13.78% | 21.7% – 63.2% |
| 0.50 | 91.72% @ 87 | 26.71% | 5.41% | 20.6% – 35.2% |
| 0.75 | 🛑 | — | — | Training stopped at epoch 2 |
| 1.00 | ⏳ | — | — | Not started |

**K4 alpha=0.75 anomaly:** Checkpoint shows `epoch=2, best_acc=83.11%`. Training log only records epoch 0. Process disappeared without error traceback. Root cause: **unknown** (possible external kill, script logic error, or silent OOM after epoch 2 checkpoint save).

---

## 3. Pipeline Integrity Issues

### 3.1 Potential train/eval mismatch for K2

`eval_joint_fresh_instance.py` was modified at `16:42` on 2026-04-22 to change `--delta-g-eff` default from `0.0` → `-1.0` (auto-fill).

K2 fresh eval ran on 2026-04-21, **before** this fix. At that time, the eval script's default was `0.0` (literal zero).

K2 training (`train_tinyvit_groupwise_nl_comp.py`) uses `--delta-g-eff -1.0` default (auto-fill).

**Result:** K2 eval may have used `delta_g_eff=0.0` while training used auto-filled `delta_g_eff=0.15`. This is a **train/eval mismatch** for the K2 canonical number.

**Impact assessment:**
- If eval used `delta_g_eff=0.0` (literal zero), the second-order correction was silently disabled during evaluation.
- This means K2's `38.95%` was measured **without** the second-order correction active.
- The training, however, **did** use the second-order correction (via auto-fill).
- This does not invalidate the result, but it means the eval was testing a **slightly different model behavior** than the training optimized for.

### 3.2 K3/K4 eval alignment

K3 and K4 evals ran on 2026-04-22, mostly **after** the `16:42` eval script fix. The eval script defaults should be aligned with training wrapper defaults (`-1.0` = auto-fill).

However, `run_cx_k4_alpha_continuation.py` **explicitly passes** `--delta-g-eff 0.15` and `--second-order-alpha <alpha>` to the eval command. This overrides any default and ensures train/eval alignment.

### 3.3 No pipeline bypass paths found

- `run_tinyvit_groupwise_nl_comp.py` correctly monkey-patches both `set_noise_for_train` and `set_noise_for_eval`.
- `eval_joint_fresh_instance.py` applies the groupwise setter before `resample_all_d2d_noise` and evaluation.
- No other eval script in `scripts/_gpt/` bypasses the groupwise setter.

---

## 4. Phantom/Stale Code

| File | Status | Risk |
|:-----|:-------|:-----|
| `analog_layers_ensemble.py` | DEPRECATED (header added) | Previously lacked SO2 support; could cause silent divergence if imported |
| `run_ensemble_hat_fixed.py` | DEPRECATED (header added) | Imports deprecated `analog_layers_ensemble` |
| `cx_k5_third_order.json` (26 bytes) | PHANTOM | Contains no real data; 3rd-order STE code does not exist |
| `cx_k3_dgeff_sweep.json` (61 bytes) | STUB | Superseded by `cx_k3_dgeff_continuation.json` (2343 bytes) |

---

## 5. Critical Decisions Required

### Decision 1: Commit the backward fix?
**YES.** The `nl` multiplier fix is mathematically correct and should be committed immediately. It is a 2-line change in `analog_layers.py`.

### Decision 2: Rerun K2 eval?
**RECOMMENDED.** K2's canonical `38.95%` may have been measured with `delta_g_eff=0.0` (no SO2 correction in eval). A rerun with the aligned eval script (`--delta-g-eff -1.0`) would give the true fresh-instance performance of the trained checkpoint.

### Decision 3: Rerun K4 on fixed backward?
**STRONGLY RECOMMENDED.** The entire K4 alpha sweep (0.00, 0.25, 0.50, plus remaining 0.75/1.00) should be rerun after the backward fix. The current 44.29% at alpha=0.25 is the best result on buggy math; the corrected landscape may shift the optimum.

### Decision 4: What about K3?
**DEFER.** K3's conclusion was negative (no delta_g_eff rescues). Even if the absolute numbers shift, the qualitative conclusion (naive curvature tuning doesn't break the ceiling) is likely robust. K3 does not need immediate rerun unless K4 on corrected math shows dramatically different behavior.

### Decision 5: K4 alpha=0.75 crash?
**INVESTIGATE.** The epoch-2 stop has no logged error. Check system logs for OOM killer or external SIGTERM. Before relaunching K4, ensure the continuation driver can survive transient failures.

---

## 6. Net Assessment

**Source code:** 1 real math bug found (missing `nl` multiplier), fixed in working tree, uncommitted. 1 asymmetric partial fix also detected and resolved. No other source-code bugs found.

**Data integrity:** All JSON math checks pass. All checkpoints exist. No phantom data beyond K5.

**Pipeline integrity:** 1 train/eval mismatch identified (K2 eval default). No bypass paths.

**Provenance:** K3/K4 results are internally consistent but produced on mathematically incorrect backward. They should be archived as "pre-fix" results and replaced after the backward fix is committed and experiments are rerun.
