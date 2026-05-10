<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# CODEX_BROADCAST — K4R Completion & Fresh-Instance Result

**Classification**: [RATING TO FILL]
**Provenance**: kimi-cli
**Canonical Commit**: `ab56c2d`

## Experiment Completed

- **Experiment**: K4R (α=0.25, `group=all` uniform-NL + SO2)
- **Train best**: [FILL]% (epoch [FILL])
- **Fresh-instance mean**: [FILL]% ± [FILL]%
- **Runtime**: [FILL]
- **JSON**: `report_md/_gpt/json_gpt/cx_k4r_fresh_eval.json`

## Result Classification

| Cross-instance mean | Classification | P1 Path |
|:--------------------|:---------------|:--------|
| ≥ 85% | ✅ PARITY ACHIEVED | P1-A: α-sweep, K5 diagnostic, OPECT re-eval |
| 80–85% | ⚠️ NEAR PARITY | P1-B: α-down sweep, joint MLP-linear + Ensemble HAT |
| < 80% | ❌ DEGRADATION | P1-C: First-order-only ablation, theory review |

## Branch A Compliance

- [ ] Produced on `ab56c2d` or later
- [ ] First-order: no `nl` multiplier
- [ ] Second-order: negative sign (`-0.5`)
- [ ] Eval uses same `group=all` uniform-NL as training
- [ ] δg_eff auto-computed from module noise

## Comparison with Pre-Branch-A Baseline

| Metric | Pre-Branch-A `[INVALID]` | K4R (Branch A) |
|:-------|:-------------------------|:---------------|
| Fresh-instance mean | 86.37% [INVALID] | [FILL]% |
| Fresh-instance std | 1.54% [INVALID] | [FILL]% |

## Immediate Next Actions

1. [FILL based on scenario]
2. Archive result in `KIMI_K4R_FRESH_EVAL_REPORT.md`
3. Update experiment queue status
4. Notify all agents (Codex, Gemini) of canonical re-anchor

## Agent Tasking

- **Codex**: GPU scheduling for P1 experiments
- **Kimi**: Paper/thesis text update with canonical number
- **Gemini**: Theory reconciliation if result < 85%
