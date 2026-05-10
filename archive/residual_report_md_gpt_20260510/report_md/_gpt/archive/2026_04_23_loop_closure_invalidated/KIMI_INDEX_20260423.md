<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Report Archive Index — Round Q Day 2 (2026-04-23)

## Branch A Canonicalization

| File | Status | Description |
|:-----|:-------|:------------|
| `KIMI_BRANCH_A_CONTAMINATION_SCRUB_20260422.md` | ✅ Complete | Initial contamination audit and scrub plan |
| `KIMI_PAPER_CONSISTENCY_AUDIT_20260423.md` | ✅ Complete | Systematic audit of 5 paper/thesis files |
| `KIMI_V4_PROVENANCE_CONFIRMED_20260423.md` | ✅ Complete | V4 checkpoint metadata + validity verdict |

## Code & Experiments

| File | Status | Description |
|:-----|:-------|:------------|
| `launch_cx_k4r_fresh_eval.sh` | ✅ Ready | Auto-trigger fresh eval on K4R completion |
| `analyze_k4r_fresh_eval.py` | ✅ Ready | Post-eval analysis + markdown report generator |
| `KIMI_K4R_RESULT_TEMPLATE_20260423.md` | ✅ Ready | Fill-in template for K4R interpretation |
| `KIMI_K4R_LIVE_PROGRESS.md` | 🔄 Updating | Real-time training progress (auto-updated) |
| `KIMI_EXPERIMENT_QUEUE_POST_K4R_20260423.md` | ✅ Ready | P0–P3 experiment queue with decision gates |

## Defense & Communication

| File | Status | Description |
|:-----|:-------|:------------|
| `KIMI_DEFENSE_SLIDES_OUTLINE_20260423.md` | ✅ Complete | 12-slide outline (10 core + 2 appendix) |
| `KIMI_DEFENSE_SLIDES_CONTENT_20260423.md` | ✅ Complete | Full slide content (~3,900 words) |
| `KIMI_DEFENSE_BEAMER_20260423.tex` | ✅ Complete | LaTeX Beamer source (compiles to PDF) |
| `KIMI_DEFENSE_QA_PREP_20260422.md` | ✅ Updated | QA prep with [INVALID] tags |
| `KIMI_BLOG_DRAFT_20260423.md` | ✅ Complete | Public blog draft (~1,420 words) |
| `KIMI_PUBLIC_FAQ_20260423.md` | ✅ Complete | 20 Q&A public FAQ (~1,550 words) |

## Codex & Broadcast

| File | Status | Description |
|:-----|:-------|:------------|
| `KIMI_CODEX_BROADCAST_20260423.md` | ✅ Complete | Archival summary of Day 2 work |
| `BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md` | ✅ Complete | Broadcast announcing scrub completion |

## Active Monitors

| Process | PID | Purpose |
|:--------|:----|:--------|
| K4R auto-eval monitor | 362673 | Triggers eval when K4R finishes |
| K4R live progress tracker | 426843 | Updates progress markdown every 5 min |

## Paper/Thesis Scrub Status

| File | INVALID | PENDING | VALID |
|:-----|:--------|:--------|:------|
| `paper/latex_gpt/sections/05_results.tex` | 1 | 2 | 1 |
| `paper/latex_gpt/sections/06_discussion.tex` | 1 | 0 | 0 |
| `paper/latex_gpt/sections/08_appendix.tex` | 1 (table) | 0 | 0 |
| `paper/thesis/chapter_1_hat_instance_overfitting.tex` | 10 | 1 | 1 |

## Next Milestone

**K4R Epoch 100 completion** → Auto-eval (10×5) → Analysis → P1 decision

ETA: ~40–50 min from now.
