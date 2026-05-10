<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# V4 Provenance Confirmation — Branch A Validity

**Date**: 2026-04-23
**Agent**: kimi-cli
**Canonical Commit**: `ab56c2d`

## Checkpoint Inspected

```
checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt
```

## Metadata Extracted

| Field | Value | Interpretation |
|:------|:------|:---------------|
| `dataset` | `cifar10` | Correct |
| `best_acc` | `91.13%` | Train best (same-instance) |
| `best_epoch` | `94` | Late convergence |
| `nl_ltp` | `1.0` | **Default = identity backward** |
| `nl_ltd` | `-1.0` | **Default = identity backward** |
| `use_second_order_ste` | `None` / not set | **Second-order NOT activated** |
| `second_order_alpha` | `None` | N/A |
| `delta_g_eff` | `None` | N/A |
| `protected_group` | `None` | Standard (non-groupwise) |

## Branch A Validity Verdict

✅ **V4 results are VALID under Branch A semantics.**

**Reasoning**:
1. `nl_ltp = 1.0` and `nl_ltd = -1.0` (default) mean the first-order STE backward scale is `(...)^(NL-1)` = `(...)^0` = **1.0** (identity).
2. The `nl` multiplier bug (`c3dbeb3`) would have multiplied this by `nl_ltp = 1.0`, yielding the same identity result. Therefore the bug was a **no-op** for V4.
3. `use_second_order_ste` is **not set / false**, so the second-order Taylor correction was **never activated** during V4 training.
4. Because the second-order term was inactive, the wrong-sign issue (positive `+0.5` vs negative `-0.5`) **cannot have affected V4**.

## Consequences

The following V4-derived results are **preserved as valid** under Branch A:

| Result | Value | Status |
|:-------|:------|:-------|
| V4 same-instance (train best) | 91.13% | ✅ Valid |
| V4 same-instance MC eval | ~91.3% | ✅ Valid |
| V4 scale-masking (V2→standard) | ~97.39% | ✅ Valid |
| V4 retention curve | 91.63% → 79% | ✅ Valid (forward-only eval) |
| V4 severe-NL inference-only | 27.72% | ✅ Valid (forward-only eval) |
| V4 fresh-instance collapse | 10.00% | ✅ Valid |

## Warning

V4 is valid **only because NL=1 makes the STE debate a no-op**.
Any experiment that activated `NL ≠ 1` or `use_second_order_ste=True` on pre-`ab56c2d` code is **invalid**.
This includes:
- K1–K4 (pre-`ab56c2d`)
- NL-HAT retraining (Task 35): 27.37%, 27.72±0.82% ❌
- Ensemble HAT 86.37% (Task 37): trained with `NL=2` active + wrong signs ❌
- MLP-linearized 32.12%, all-linear 32.60% ❌

## Action Items

- [ ] Update `CODEX` to record V4 provenance confirmation
- [ ] Cross-reference this note in any document that cites V4 as valid
- [ ] Use this metadata format as the template for verifying future checkpoints
