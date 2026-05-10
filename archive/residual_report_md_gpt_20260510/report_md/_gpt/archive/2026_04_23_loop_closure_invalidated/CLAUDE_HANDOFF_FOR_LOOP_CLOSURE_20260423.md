# Claude Handoff — Loop-Closure Ready

**Date:** 2026-04-23
**Status:** K-PATCH-1 + CX-FIG complete. Ready for loop-closure declaration.

---

## Read These Files (in order)

### 1. Broadcast (your own dispatch)
- `report_md/_gpt/BROADCAST_LOOP_CLOSURE_DISPATCH_20260423.md`

### 2. Kimi Deliverables (K-PATCH-1 applied)
- `report_md/_gpt/KIMI_PAPER1_REWRITE_DIFF_20260423.md` ← **4-file minimal diff + ablation coverage note**
- `report_md/_gpt/KIMI_WORK1_LOOP_CLOSURE_ANALYSIS_20260423.md` ← **evidence matrix, corrected**
- `paper/thesis_cn/chapter_5_failure_modes.tex` ← **Chinese thesis Ch.5**

### 3. Codex Deliverables (CX-FIG)
- `CODEX_CX_FIG_SUMMARY_20260423.md` ← **figure metadata + caption candidate**
- `images_gpt/fig_structural_limit_signature.png` ← **300 dpi, embed in paper**
- `images_gpt/fig_structural_limit_signature.pdf` ← **vector, for submission zip**
- `scripts/_gpt/plot_structural_limit_signature.py` ← **reproducibility script**

### 4. Cross-Review (already resolved)
- `report_md/_gpt/CODEX_RESPONSE_TO_KIMI_REVIEW_20260423.md` ← **Codex audit trail, all 11 issues fixed**

### 5. Canonical Data (locked numbers)
- `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json` (N=30)
- `report_md/_gpt/json_gpt/cx_k2_bimodality_test.json` (p=0.9796)

---

## Action Checklist for Claude

- [ ] Read BROADCAST_LOOP_CLOSURE_DISPATCH_20260423.md
- [ ] Read Kimi diff + loop-closure analysis
- [ ] Read Codex figure summary + inspect PNG
- [ ] Write `CLAUDE_LOOP_CLOSURE_DECLARATION_20260423.md`
- [ ] Apply 4-file rewrite to frozen files (`00_abstract.tex`, `05_results.tex`, `06_discussion.tex`, `cover_letter_v3.tex`)
- [ ] Embed signature figure in `05_results.tex` at appropriate slot
- [ ] Regenerate PDF
- [ ] Run `check_locked_numbers.py` if available
- [ ] Declare ready-to-submit
