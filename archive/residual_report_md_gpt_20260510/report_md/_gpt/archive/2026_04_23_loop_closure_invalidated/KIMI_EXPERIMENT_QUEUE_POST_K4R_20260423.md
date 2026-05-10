<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Post-K4R Experiment Queue — Branch A Canonical

**Date**: 2026-04-23
**Agent**: kimi-cli
**Canonical Commit**: `ab56c2d`

## P0: Immediate (K4R completion → ~2h)

### P0.1 Fresh-Instance Eval Analysis
- **Trigger**: Auto-launched by monitor when Epoch 100 completes
- **Runtime**: ~30–40 min (10 instances × 5 MC passes)
- **Action**: Run `scripts/_gpt/analyze_k4r_fresh_eval.py` on JSON output
- **Decision gate**: Cross-instance mean determines P1 direction

### P0.2 V4 Re-validation on Branch A Code
- **Purpose**: Confirm V4 same-instance / scale-masking results using canonical `ab56c2d`
- **Runtime**: ~10 min (eval only, no retraining)
- **Expected**: ~91.3% same-instance, ~97.4% scale-masking (V2 control)
- **Action**: Load `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` and run eval with Branch A `analog_layers.py`

---

## P1: Conditional on K4R Fresh-Instance Result

### Scenario A: K4R ≥ 85% (Parity Achieved)

| Priority | Experiment | Config | Purpose | Runtime |
|:---------|:-----------|:-------|:--------|:--------|
| P1-A1 | **K4R α-sweep** | α ∈ {0.1, 0.25, 0.5, 1.0}, `group=all` | Characterize brake-strength sensitivity | 4 × ~90 min |
| P1-A2 | **K5 `group=mlp` diagnostic** | `group=mlp`, NL=1.0/2.0, α=0.25 | Contrast uniform-NL vs mixed-NL transfer | ~90 min |
| P1-A3 | **OPECT re-eval** | Load best K4R checkpoint, eval on literature profile | Verify zero-shot transfer survives Branch A | ~5 min |
| P1-A4 | **Proportional-noise HAT re-run** | Standard HAT, proportional noise, no NL≠1 | Validate 97.37% claim under Branch A | ~90 min |

### Scenario B: 80% ≤ K4R < 85% (Near Parity)

| Priority | Experiment | Config | Purpose | Runtime |
|:---------|:-----------|:-------|:--------|:--------|
| P1-B1 | **K4R α-down sweep** | α ∈ {0.05, 0.1, 0.15, 0.25} | Find weaker brake that recovers transfer | 4 × ~90 min |
| P1-B2 | **Joint MLP-linear + Ensemble HAT** | `group=all` + MLP-linearization | Push severe-NL ceiling with combined remedy | ~120 min |
| P1-B3 | **K4R with δg_eff = 0** | Disable curvature correction literal zero | Test if second-order is the bottleneck | ~90 min |

### Scenario C: K4R < 80% (Significant Degradation)

| Priority | Experiment | Config | Purpose | Runtime |
|:---------|:-----------|:-------|:--------|:--------|
| P1-C1 | **First-order-only ablation** | `use_second_order_ste=False` | Test if second-order brake is too aggressive | ~90 min |
| P1-C2 | **Sign-reversal ablation** | Positive `+0.5` second-order (pre-Branch-A) | Confirm that negative sign is the degradation driver | ~90 min |
| P1-C3 | **Physical derivation review** | Re-examine Gemini's brake argument | Theory–experiment reconciliation | Non-GPU |

---

## P2: Medium-Term (Next 24–48h)

### P2.1 CIFAR-100 Branch A Re-run
- **Config**: Tiny-ViT + ConvNeXt, standard HAT, CIFAR-100
- **Purpose**: Verify complexity-scaling law under Branch A
- **Expected**: Tiny-ViT ~65%, ConvNeXt ~60% (if valid)
- **Runtime**: 2 × ~90 min

### P2.2 Flowers-102 Branch A Re-run
- **Config**: Tiny-ViT + ConvNeXt, standard HAT, Flowers-102
- **Purpose**: Test data-floor hypothesis under canonical code
- **Runtime**: 2 × ~90 min

### P2.3 Correlated D2D Branch A Re-run
- **Config**: Ensemble HAT, AR(1) ρ ∈ {0.3, 0.5, 0.7}
- **Purpose**: Verify spatial robustness under canonical code
- **Expected**: Graceful degradation from i.i.d. baseline
- **Runtime**: 3 × ~90 min

### P2.4 Severe-NL (Task 35) Branch A Re-run
- **Config**: NL=2.0, `group=all`, α=0.25
- **Purpose**: Test if sign-corrected second-order improves severe-NL ceiling
- **Expected**: >27.72% if brake helps; <27.72% if brake hurts
- **Runtime**: ~90 min

---

## P3: Long-Term / Thesis-Only (Next 3–5 days)

### P3.1 ImageNet Pilot
- **Config**: Tiny-ViT-5M, ImageNet-1k subset or Tiny-ImageNet
- **Purpose**: Validate complexity scaling beyond CIFAR
- **Runtime**: ~6–8h

### P3.2 ADC Layer-Wise Sweep
- **Config**: Vary ADC precision per layer (attention vs MLP)
- **Purpose**: Optimize peripheral stack precision budget
- **Runtime**: ~4h

### P3.3 State-Dependent Retention
- **Config**: Enable true state-dependent decay (high-G faster)
- **Purpose**: Move beyond uniform double-exponential model
- **Runtime**: ~3h

### P3.4 Temperature-Dependent Physics
- **Config**: Add T-dependent mobility and threshold shifts
- **Purpose**: Close realism gap for deployment envelope
- **Runtime**: Non-GPU (modeling) + ~2h (eval)

---

## Resource Budget

| Phase | GPU Hours | Human Hours | Blocking? |
|:------|:----------|:------------|:----------|
| P0 | ~1h | 0.5h | No |
| P1-A | ~7h | 1h | No (parallelizable) |
| P1-B | ~6h | 1h | No |
| P1-C | ~5h | 2h | Yes (theory review) |
| P2 | ~9h | 1h | No |
| P3 | ~20h | 4h | Partial |
| **Total** | **~48h** | **~10h** | **P1-C only** |

With 1× RTX 5070 Ti, P0+P1+P2 can complete in ~2 days if run sequentially.
P3 can overlap with paper writing.

---

## Branch A Compliance Checklist for Every New Experiment

- [ ] Code is at or after `ab56c2d`
- [ ] `analog_layers.py` has no-multiplier first-order (`(...)^(NL-1)`)
- [ ] `analog_layers.py` has negative second-order (`-0.5`)
- [ ] Eval uses same group/NL config as training
- [ ] `delta_g_eff < 0` triggers auto-fill from module noise
- [ ] Checkpoint metadata records `git_commit`, `nl_ltp`, `nl_ltd`, `use_second_order_ste`
- [ ] Fresh-instance eval uses `10 × 5` protocol
- [ ] Results tagged with `[BRANCH A]` in report title
