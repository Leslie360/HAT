# Remote 107 KV-HAT Update Review

**Date:** 2026-04-30 15:10 CST
**Reviewer:** Codex
**Source:** User-relayed Remote 107 update.
**Scope:** Pythia analog KV-cache, SDPA patch fix, HAT training sweeps, C2C/D2D sweeps.

## 0. Executive Judgment

Remote 107 has produced a major update. The earlier all-layer analog KV-cache kill decision must be revised:

> Non-HAT all-layer analog KV remains fragile, but HAT-adapted analog KV is now a live route. The most important scientific direction is no longer simply "terminal-layer-only KV"; it is the design space of HAT adaptation, selective layer scope, noise source, and temporal retention.

However, the result is not paper-grade until three risks are closed:

1. **Data leakage / split risk:** HAT PPL sometimes improves below the reported baseline. Remote must prove that HAT training/calibration data are disjoint from final PPL evaluation data.
2. **Baseline reconciliation risk:** We now have multiple baselines: previous `15.68`, current baseline `22.18`, Base+Patch `23.86`, material sweep values starting at `107.27`. These must be mapped to exact model/evaluator/context settings.
3. **Exact command/repro risk:** Need git SHA, diff, command lines, model/tokenizer, dataset split, token counts, and HAT training/eval split for each table.

## 1. Implementation Claims Preserved

Remote 107 reports:

- Vectorized Analog KV Cache using `[B, L, H, D]` layout.
- Per-sample conductance-domain quantization.
- C2C, D2D, and retention noise implemented in physical cache path.
- Pythia-410m end-to-end PPL evaluator using sliding window, stride 512, max_length 1024, batch size 64, full WikiText-2.
- Selective layer injection via `--analog_layers 6,12,18,23`; JSON output records `analog_layers`.

Codex judgment: directionally correct; paper use requires exact code diff and tests.

## 2. Critical Bug Fix / Route Reopening

Remote reports a historical SDPA attention interface bug:

```text
patch_model_for_hat used eager matmul and caused SDPA mask mismatch.
```

After fix:

| Probe | PPL |
|---|---:|
| Baseline | 22.18 |
| Base+Patch | 23.86 |
| Quick 100-step HAT, D2D=0.02, pre | 91.46 |
| Quick 100-step HAT, D2D=0.02, post | 29.26 |

Codex judgment:

- The prior Base+Patch PPL ~644 was a bug artifact.
- All-layer HAT must be reopened as a route.
- Base+Patch parity is not perfect: 23.86 vs 22.18 is +7.6%. This may be acceptable as an implementation overhead, but it fails the earlier strict 1% parity gate. Remote should either explain this overhead or improve parity before using a 10% gate.

## 3. HAT Training Results Preserved

### 3.1 ctx=512, 500-step, 256 states, seed=42

| sigma_d2d | Pre-HAT PPL | Post-HAT PPL | Improvement |
|---:|---:|---:|---:|
| 0.000 | 23.86 | 18.28 | 0.77x |
| 0.020 | 91.46 | 22.29 | 0.24x |
| 0.025 | 140.07 | 24.77 | 0.18x |
| 0.030 | 225.14 | 27.16 | 0.12x |
| 0.035 | 376.09 | 29.47 | 0.08x |
| 0.040 | 652.37 | 31.85 | 0.05x |
| 0.045 | 1139.74 | 35.43 | 0.03x |
| 0.050 | 1988.75 | 40.18 | 0.02x |

### 3.2 C2C / combined, ctx=512, 500-step, 256 states, seed=42

| Config | Pre-HAT PPL | Post-HAT PPL |
|---|---:|---:|
| C2C=0.01 | 42.13 | 19.97 |
| D2D=0.02 + C2C=0.01 | 109.12 | 23.75 |

### 3.3 ctx=1024, 500-step, 256 states, seed=42

| Config | Pre-HAT PPL | Post-HAT PPL |
|---|---:|---:|
| D2D=0.01 | 36.30 | 17.01 |
| C2C=0.01 | 36.06 | 17.03 |

### 3.4 ctx=1024, 1000-step, 256 states, seed=42

| sigma_d2d | Pre-HAT PPL | Post-HAT PPL |
|---:|---:|---:|
| 0.025 | 113.39 | 19.00 |
| 0.030 | 177.34 | 20.44 |
| 0.040 | 461.90 | 22.60 |

### 3.5 Longer training, D2D=0.02, ctx=512, 256 states, seed=42

| Steps | Pre-HAT PPL | Post-HAT PPL |
|---:|---:|---:|
| 200 | 91.46 | 23.75 |
| 500 | 91.46 | 22.29 |
| 1000 | 91.46 | 20.82 |

### 3.6 200-step D2D sweeps

ctx=512:

| sigma_d2d | Pre-HAT PPL | Post-HAT PPL |
|---:|---:|---:|
| 0.025 | 140.07 | 29.04 |
| 0.030 | 225.14 | 33.23 |
| 0.035 | 376.09 | 38.71 |
| 0.040 | 652.37 | 42.46 |
| 0.045 | 1139.74 | 48.25 |

ctx=1024:

| sigma_d2d | Pre-HAT PPL | Post-HAT PPL |
|---:|---:|---:|
| 0.025 | 113.39 | 24.04 |
| 0.030 | 177.34 | 27.15 |
| 0.035 | 284.36 | 30.16 |
| 0.040 | 461.90 | 34.54 |
| 0.045 | 750.65 | 37.43 |

## 4. C2C / D2D Sweep Preserved

6-bit, seed=42.

### 4.1 C2C sweep, D2D=0

| sigma_c2c | PPL | Ratio |
|---:|---:|---:|
| 0.00 | 32.41 | 1.00x |
| 0.005 | 39.86 | 1.23x |
| 0.01 | 56.73 | 1.75x |
| 0.015 | 77.36 | 2.39x |
| 0.02 | 100.64 | 3.10x |
| 0.03 | 160.34 | 4.95x |
| 0.05 | 412.35 | 12.72x |

3-seed stability at sigma=0.05: seed42=412.35, seed123=413.90, seed456=412.09, CV=0.44%.

### 4.2 D2D sweep, C2C=0

| sigma_d2d | PPL | Ratio | vs C2C same sigma |
|---:|---:|---:|---:|
| 0.00 | 32.41 | 1.00x | n/a |
| 0.01 | 60.30 | 1.86x | +6.3% |
| 0.02 | 106.48 | 3.29x | +5.8% |
| 0.05 | 470.92 | 14.53x | +14.2% |
| 0.10 | 7635.49 | 235.61x | cliff |

Codex updated judgment: For sigma <= 0.05, D2D is only modestly worse than C2C, not 3-5x worse. The severe cliff appears at sigma=0.10.

## 5. Offline MSE vs E2E PPL Gap

Remote reports:

| Metric | 6-bit | 8-bit |
|---|---:|---:|
| P1 last-layer KV_rel_MSE | 0.18% | 0.01% |
| P3 E2E PPL, zero noise | 32.41 (2.07x) | 17.48 (1.11x) |

Remote hypothesis: 24-layer accumulation and softmax exponential amplification, approx `1.031^24 ~= 2.07`, pending single-layer probe.

Codex judgment: plausible and important. This should become a mechanism section only after layer-depth probe verifies the compounding model.

## 6. Code Fixes Reported By DeepSeek

| Bug | File | Fix |
|---|---|---|
| scaler misuse | `train_tinyvit.py:333` | `if scaler:` -> `if scaler is not None and scaler.is_enabled():` |
| warm_start silent fallback | `train_tinyvit_ensemble.py:554` | missing path now raises `FileNotFoundError` |
| checkpoint path not validated | `train_tinyvit_ensemble.py:798` | added `os.path.exists()` check |

Codex judgment: these are useful but need local code sync/audit before being treated as merged project fixes.

## 7. Route Decision Update

Previous stance:

- Non-HAT all-layer analog KV fails.
- Selective terminal-layer KV is safest.
- HAT all-layer open pending data.

Updated stance:

- **HAT all-layer is now a live route**, at least under the reported evaluator.
- **Selective terminal-layer remains important** because it is a lower-cost deployment design and may need fewer HAT steps.
- **Retention-driven rank inversion remains separate** until baseline/evaluator reconciliation is complete.

Do not frame 107 as a single result yet. It is now three coupled questions:

1. Can HAT rescue all-layer analog KV under clean held-out evaluation?
2. How far can selective terminal-layer analog KV go without or with HAT?
3. Does material retention invert PCM vs organic ranking under the same evaluator and scope?

## 8. Critical Questions For Remote 107

Return these before Opus/final routing:

1. **Data split:** What exact text was used for HAT training/calibration, and what exact text was used for final PPL? Confirm no WikiText-2 test leakage into HAT steps.
2. **Baseline map:** Explain all baselines: `15.68`, `22.18`, `23.86`, `32.41`, `107.27`. For each: model, context, evaluator, layer scope, bit width, quantization, noise, retention, patch state.
3. **Exact commands:** Provide one command per reported table row or a script/config manifest.
4. **Held-out validation:** For best HAT configs, re-evaluate on a held-out split not used during HAT training.
5. **No-noise parity:** Report baseline vs patched digital/no-analog-noise PPL; target should be close enough to justify gate.
6. **Seed repeats:** Repeat key HAT configs for seeds 123/456, not only noise sweeps.
7. **Selective + HAT:** Run last1/last2/last4 with HAT and compare compute/quality against all-layer HAT.
8. **Retention after HAT:** Evaluate HAT-trained cache under retention; current HAT tables focus on D2D/C2C, while the material narrative depends on retention.

## 9. Suggested Next 107 Task Order

P0:

1. Baseline/evaluator reconciliation table.
2. Data split / leakage audit.
3. Held-out re-eval for best HAT configs:
   - ctx=1024, D2D=0.01, 500-step, post=17.01
   - ctx=1024, D2D=0.04, 1000-step, post=22.60
   - ctx=512, D2D=0.02+C2C=0.01, 500-step, post=23.75
4. Selective last1/last2/last4 HAT at ctx=1024.

P1:

5. Seed repeats for 2-3 key configs.
6. Retention-time sweep after HAT.
7. Noise-source ablation under HAT.
8. Per-layer probe to test `1.031^24` compounding hypothesis.

Kill / hold:

- Do not run more 6-bit all-layer raw sweeps without HAT.
- Do not claim retention rank inversion in the same paragraph as HAT until baselines are unified.
- Do not compare `15.68` and `107.27` tables directly.

## 10. Draft Reply To Remote 107

```text
107 update received. The SDPA bug fix and HAT sweeps materially change the route: all-layer HAT is now reopened. However, before paper routing we need three clarifications.

1. Data split/leakage: for every HAT run, state exactly what text is used for HAT steps and what text is used for final PPL. Confirm final PPL is held-out from HAT training/calibration.
2. Baseline reconciliation: map 15.68 / 22.18 / 23.86 / 32.41 / 107.27 to exact model, evaluator, context length, layer scope, bit width, quant/noise/retention, and patch state.
3. Exact commands/configs: return commands or config manifest for all HAT tables.

Next experiments: held-out re-eval of best HAT configs; selective last1/last2/last4 + HAT at ctx=1024; seed repeats for 2-3 key configs; retention after HAT. Do not spend more GPU on raw all-layer 6-bit sweeps.
```
