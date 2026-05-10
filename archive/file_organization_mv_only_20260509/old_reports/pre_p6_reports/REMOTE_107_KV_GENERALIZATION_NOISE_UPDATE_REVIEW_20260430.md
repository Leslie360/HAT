# Remote 107 KV-HAT Generalization Noise Update Review

**Date:** 2026-04-30 15:35 CST
**Reviewer:** Codex
**Source:** User-relayed Remote 107 HAT generalization report.
**Status:** PROVISIONAL / TREND-ONLY because Remote 107 found a noise-algorithm bug and is rerunning. Current tables are preserved for route analysis, not locked numeric claims.

## 0. Executive Judgment

This update answers the right question:

> Did HAT memorize one noise pattern, or did it learn a robust analog-KV representation?

Provisional answer: **HAT appears to learn genuine noise robustness**, especially when trained at higher D2D noise and when evaluated under C2C or mixed noise. The trend is strong enough to continue the route, but all exact PPL values must be rerun after the reported noise-algorithm bug fix.

Current action:

- Preserve this as a trend record.
- Do not lock any numeric PPL from this batch.
- Require a corrected rerun with an explicit mathematical/code packet so local agents can reproduce and audit the implementation.

## 1. Experiment Design Preserved

| Test type | Training config | Eval noise configs | Purpose |
|---|---|---|---|
| D2D generalization | D2D=0.02, 500-step | D2D={0.00,0.01,0.02,0.03,0.04,0.05} | same-noise-family generalization |
| D2D generalization | D2D=0.04, 500-step | D2D={0.00,0.01,0.02,0.03,0.04,0.05} | high-noise training generalization |
| C2C generalization | C2C=0.01, 500-step | C2C={0.00,0.005,0.01,0.015,0.02} | C2C generalization |
| Cross-type | D2D=0.02+C2C=0.01 | mixed D2D/C2C eval | cross-noise-family robustness |

## 2. Provisional Results Preserved

### 2.1 D2D generalization, trained D2D=0.02, ctx=512, 500-step

| Eval D2D | PPL | vs train-noise PPL | Trend read |
|---:|---:|---:|---|
| 0.00 | 19.83 | 0.89x | good |
| 0.01 | 21.54 | 0.97x | good |
| 0.02 | 22.29 | 1.00x | train point |
| 0.03 | 43.63 | 1.96x | weak out-of-range |
| 0.04 | 81.43 | 3.65x | poor |
| 0.05 | 402.65 | 18.06x | collapse |

### 2.2 D2D generalization, trained D2D=0.04, ctx=512, 500-step

| Eval D2D | PPL | vs train-noise PPL | Trend read |
|---:|---:|---:|---|
| 0.00 | 21.00 | 0.66x | good |
| 0.01 | 21.86 | 0.69x | good |
| 0.02 | 25.40 | 0.80x | good |
| 0.03 | 31.79 | 1.00x | train-near |
| 0.04 | 31.85 | 1.00x | train point |
| 0.05 | 64.37 | 2.02x | degraded but far better than D2D=0.02 model |

### 2.3 C2C generalization, trained C2C=0.01, ctx=512, 500-step

| Eval C2C | PPL | vs train-noise PPL | Trend read |
|---:|---:|---:|---|
| 0.000 | 18.80 | 0.94x | good |
| 0.005 | 19.05 | 0.95x | good |
| 0.010 | 19.97 | 1.00x | train point |
| 0.015 | 21.84 | 1.09x | good |
| 0.020 | 25.37 | 1.27x | acceptable |

### 2.4 Cross-type generalization, trained D2D=0.02 + C2C=0.01, ctx=512, 500-step

| Eval D2D | Eval C2C | PPL | vs train-noise PPL | Trend read |
|---:|---:|---:|---:|---|
| 0.00 | 0.00 | 19.48 | 0.82x | good |
| 0.04 | 0.00 | 54.12 | 2.28x | degraded but non-catastrophic |
| 0.00 | 0.02 | 24.14 | 1.02x | good |

## 3. Provisional Analysis

1. **High-D2D training broadens robustness.** D2D=0.04-trained checkpoint is much more robust at eval D2D 0.03-0.05 than the D2D=0.02-trained checkpoint.
2. **C2C generalization is naturally stronger.** This is plausible because C2C is resampled per forward/read, making memorization of one C2C pattern unlikely.
3. **Mixed noise training looks promising.** D2D+C2C checkpoint retains good behavior under no-noise and pure C2C eval, and degrades more gracefully under higher D2D.
4. **Training noise strength is a route-level hyperparameter.** Low-noise HAT optimizes near its training point; high-noise HAT improves out-of-distribution noise tolerance at some low-noise cost.

These are trend statements only until rerun after the noise bug fix.

## 4. User-Reported Bug Caveat

User reports Remote 107 found a bug in the noise algorithm. It does not appear to invalidate the qualitative trend, but it shifts the tests numerically. Therefore:

- All current PPL numbers are **not canonical**.
- The route decision remains: continue HAT generalization and selective/all-layer comparison.
- Corrected rerun must include before/after comparison and the mathematical implementation packet.

## 5. Remote 107 Claims To Re-Validate After Fix

Rerun must answer:

1. Does high-D2D training still dominate low-D2D training under eval D2D 0.03-0.05?
2. Does C2C generalization remain smooth through C2C=0.02?
3. Does mixed D2D+C2C training remain robust under pure C2C and no-noise eval?
4. Does selective-layer HAT still outperform all-layer HAT in PPL and compute?
5. Do seed repeats remain CV < 1% after the corrected noise algorithm?
6. Are all reported PPL values evaluated on held-out WikiText-2 test, not on HAT training/calibration text?

## 6. Reported Completed Work Preserved

Remote 107 reported completion counts:

| Stage | Count | Status |
|---|---:|---|
| HAT training | 21 | complete |
| generalization noise tests | 18 | complete |
| seed repeats | 8 | complete |
| selective layer HAT | 8 | complete |
| total | 55 | complete |

Codex note: because of the noise-algorithm bug, this completed matrix is now a pre-fix exploratory matrix. The corrected rerun should not necessarily repeat all 55 cells immediately. Prioritize the diagnostic subset in Section 8.

## 7. DeepSeek Code Fixes Reported

| Bug | File | Fix |
|---|---|---|
| AMP scaler misuse | `train_tinyvit.py:333` | `if scaler:` -> `if scaler is not None and scaler.is_enabled():` |
| warm-start silent fallback | `train_tinyvit_ensemble.py:554` | missing path now raises `FileNotFoundError` |
| checkpoint path not validated | `train_tinyvit_ensemble.py:798` | added `os.path.exists()` check |

Codex note: these are outside the KV-cache core but valuable. They should be ported to local only after exact patch/diff is returned and reviewed.

## 8. Corrected Rerun Priority

Run a minimal corrected matrix first:

| Priority | Config | Why |
|---|---|---|
| P0 | Baseline clean, patched clean, all-layer 8-bit zero-noise | confirms evaluator and patch parity |
| P0 | D2D train 0.02 -> eval 0.00/0.02/0.04/0.05 | verifies low-noise generalization curve |
| P0 | D2D train 0.04 -> eval 0.00/0.02/0.04/0.05 | verifies high-noise generalization advantage |
| P0 | C2C train 0.01 -> eval 0.00/0.01/0.02 | verifies C2C smoothness |
| P0 | Combined train D2D=0.02+C2C=0.01 -> eval clean / D2D=0.04 / C2C=0.02 | verifies mixed-noise route |
| P1 | selective last1/last2/last4 HAT for best corrected noise | verifies deployment route |
| P1 | seed123/456 repeat for 2 strongest corrected configs | verifies stability |

Do not rerun all 55 cells until this corrected P0 subset confirms the trend.

## 9. Reply To Remote 107

```text
107 update received. Treat the current matrix as trend-only because of the discovered noise-algorithm bug. The trends are still valuable: high-D2D training seems to improve out-of-distribution D2D robustness, C2C generalizes smoothly, and mixed D2D+C2C training is promising.

For the rerun, do not immediately repeat all 55 cells. First run a corrected P0 subset:
1. clean baseline / patched clean / all-layer 8-bit zero-noise parity,
2. D2D train 0.02 eval 0/0.02/0.04/0.05,
3. D2D train 0.04 eval 0/0.02/0.04/0.05,
4. C2C train 0.01 eval 0/0.01/0.02,
5. combined train D2D=0.02+C2C=0.01 eval clean/D2D=0.04/C2C=0.02.

Also return the core math/code packet: exact conductance mapping, quantization formula, D2D shape and sampling cadence, C2C shape and sampling cadence, retention equation, dequantization, layer mask semantics, random seed policy, and the exact functions/files implementing each. Include unit-test evidence for zero-noise parity, D2D persistence, C2C per-forward resampling, retention monotonicity, and selective-layer count.
```
