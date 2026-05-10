<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Branch A Quick Reference Card

**Ratified**: 2026-04-22
**Canonical Commit**: `ab56c2d`

## STE Semantics (Canonical)

| Order | Formula | Sign | Rationale |
|:------|:--------|:-----|:----------|
| First-order | `torch.pow(ratio, NL-1.0)` | N/A | Intentional design: position-dependent update difficulty proxy |
| Second-order | `-0.5 * NL * (NL-1) * torch.pow(..., NL-2) * delta_g` | **Negative** | Brake: penalizes narrow ravines in conductance space (Gemini physical derivation) |

**Key rule**: No `NL` multiplier on first-order. `c3dbeb3` (multiplier commit) was **reverted**.

## Mainline vs Diagnostic

| Route | Config | Status |
|:------|:-------|:-------|
| **Mainline** | `group=all` uniform-NL + domain randomization | ✅ Canonical |
| Diagnostic | `group=mlp` mixed-NL | 🔬 Exploratory only |

## Validity Map

| Result | Value | Status | Reason |
|:-------|:------|:-------|:-------|
| V4 same-instance | ~91.3% | ✅ Valid | NL=1 default → STE identity; no second-order activated |
| V4 scale-masking | ~97.4% | ✅ Valid | Same as above |
| V4 retention | 91.6% → 79% | ✅ Valid | Forward-only eval |
| V4 severe-NL (inf-only) | 27.72% | ✅ Valid | Forward-only eval |
| K4R (pending) | TBD | 🔄 Running | First canonical `group=all` + SO2 experiment |
| Ensemble HAT | 86.37±1.54% | ❌ INVALID | Pre-`ab56c2d`, wrong second-order signs, NL=2 active |
| NL-HAT retraining | 27.37%, 27.72±0.82% | ❌ INVALID | Pre-`ab56c2d`, wrong signs |
| MLP-linearized | 32.12% | ❌ INVALID | Pre-`ab56c2d` |
| All-linear | 32.60±9.18% | ❌ INVALID | Pre-`ab56c2d` |
| OPECT transfer | 88.53% | ⏳ PENDING | Pre-`ab56c2d`; needs re-eval on Branch A checkpoint |
| Proportional-noise HAT | 97.37±0.05% | ⏳ PENDING VERIFICATION | Checkpoint provenance unclear |

## Experiment Naming Convention

| Prefix | Meaning |
|:-------|:--------|
| `V` | Tiny-ViT-5M |
| `C` | ConvNeXt-Tiny |
| `R` | ResNet-18 |
| `J` | Joint (MLP-linear + standard) |
| `K` | Groupwise NL comparison (K1–K5) |

## Critical Thresholds

| Metric | Threshold | Implication |
|:-------|:----------|:------------|
| K4R fresh-instance mean | ≥ 85% | Sign-corrected brake is benign/helpful → P1-A |
| K4R fresh-instance mean | 80–85% | Brake is conservative → P1-B |
| K4R fresh-instance mean | < 80% | Brake is too aggressive → P1-C |

## Files to Never Edit (Rule B)

- `paper/00_abstract.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- Cover letters
- `KIMI_REBUTTAL_MASTER_20260420.md`
- `paper/thesis/chapter_5_*.tex` files

## One-Liner Summaries

- **Branch A ratification**: Paper Equation S2 (`(...)^(NL-1)`) is canonical by design, not a bug.
- **No-multiplier first-order**: The `nl` multiplier was a misinterpretation of the behavioral proxy.
- **Negative second-order**: The brake sign is negative because curvature correction should oppose steep gradients, not amplify them.
- **V4 survival**: V4 is valid only because NL=1 makes the entire STE debate a no-op.
- **K4R primacy**: K4R is the first experiment that tests the canonical semantics under non-trivial NL conditions.
