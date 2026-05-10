<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Round Q Day 2 — Complete Manifest

**Agent**: kimi-cli
**Date**: 2026-04-23
**Canonical Commit**: `ab56c2d`

## GPU Experiments

| Experiment | Status | Key Metric | ETA |
|:-----------|:-------|:-----------|:----|
| K4R (α=0.25, `group=all` + SO2) | 🔄 Running | Train best 91.23% @ Epoch 84 | ~20 min |
| K4R fresh-instance eval (10×5) | ⏳ Queued | TBD | Auto-trigger |

## Code Changes

| File | Action | Purpose |
|:-----|:-------|:--------|
| `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py` | Modified | Branch A: auto δg_eff, SO2-off explicit reset, second_order_alpha param |
| `scripts/_gpt/eval_joint_fresh_instance.py` | Modified | Default δg_eff=-1.0 (auto) |
| `scripts/_gpt/launch_cx_k4r_fresh_eval.sh` | Modified | Added `--json-out` for K4R-specific JSON |
| `scripts/_gpt/analyze_k4r_fresh_eval.py` | **Created** | Post-eval analysis + markdown report generator |
| `scripts/_gpt/run_post_k4r_analysis.sh` | **Created** | One-click post-K4R analysis pipeline |

## Paper / Thesis

| File | Action | Tags Added |
|:-----|:-------|:-----------|
| `paper/latex_gpt/sections/05_results.tex` | Modified | 1 INVALID, 2 PENDING, 1 VALID, 1 LIKELY VALID |
| `paper/latex_gpt/sections/06_discussion.tex` | Modified | 1 INVALID |
| `paper/latex_gpt/sections/08_appendix.tex` | Modified | 1 INVALID (table-level) |
| `paper/thesis/chapter_1_hat_instance_overfitting.tex` | Modified | 10 INVALID, 1 PENDING, 1 VALID |
| `paper/latex_gpt/main.tex` | Modified | Added `\branchatag` macro |

## Defense Materials

| File | Description | Size |
|:-----|:------------|:-----|
| `KIMI_DEFENSE_SLIDES_OUTLINE_20260423.md` | 12-slide outline | ~1,200 words |
| `KIMI_DEFENSE_SLIDES_CONTENT_20260423.md` | Full content + speaker notes | ~3,900 words |
| `KIMI_DEFENSE_BEAMER_20260423.tex` | LaTeX Beamer source | Compiles to 14-page PDF |

## Public Communication

| File | Description | Size |
|:-----|:------------|:-----|
| `KIMI_BLOG_DRAFT_20260423.md` | Technical blog | ~1,420 words |
| `KIMI_PUBLIC_FAQ_20260423.md` | 20 Q&A pairs | ~1,550 words |

## Analysis & Planning

| File | Description |
|:-----|:------------|
| `KIMI_K4R_INTERIM_ANALYSIS_20260423.md` | Training curve forecast (plateau detected) |
| `KIMI_K4R_RESULT_TEMPLATE_20260423.md` | Fill-in template for 3 scenarios |
| `KIMI_K4R_RESULTS_CONDITIONAL_DRAFT_20260423.md` | LaTeX-ready paragraphs for 3 scenarios |
| `KIMI_EXPERIMENT_QUEUE_POST_K4R_20260423.md` | P0–P3 experiment queue with decision gates |
| `KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md` | Paper/thesis/defense submission checklist |

## Provenance & Verification

| File | Description |
|:-----|:------------|
| `KIMI_V4_PROVENANCE_CONFIRMED_20260423.md` | V4 checkpoint metadata → validity verdict |
| `KIMI_K4R_CONFIG_VERIFIED_20260423.md` | Training↔eval config alignment proof |

## Archival & Broadcast

| File | Description |
|:-----|:------------|
| `KIMI_CODEX_BROADCAST_20260423.md` | Day 2 archival summary |
| `KIMI_K4R_COMPLETION_BROADCAST_TEMPLATE_20260423.md` | Template for post-eval broadcast |
| `KIMI_BRANCH_A_QUICK_REFERENCE_20260423.md` | One-page reference card |
| `KIMI_INDEX_20260423.md` | Full report archive index |
| `KIMI_DAY2_MANIFEST_20260423.md` | This file |

## Monitors & Automation

| Process | PID | Purpose |
|:--------|:----|:--------|
| K4R auto-eval monitor | 362673 | Triggers eval when K4R finishes |
| K4R live progress tracker | 426843 | Updates progress markdown every 5 min |

## Total Count

- **Documents created**: 21
- **Scripts created/modified**: 5
- **LaTeX files modified**: 5
- **Pre-Branch-A tags applied**: ~25 instances across 4 files
