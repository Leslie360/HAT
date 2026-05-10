# Codex Dispatch #8 — Visual Tidy-Up (coordination/paper/logs/dirs)

**Date:** 2026-04-17
**From:** Claude
**To:** Codex
**Scope:** Visual / organizational cleanup only. **No deletions, no content edits, no code changes, no commits.** Same contract as Dispatch #7 — everything reversible via `mv`.

---

## Motivation

Post-#7, disk space is fine; the user's concern is *visual management*. `compute_vit/` root still shows 19 loose `.md` files, `paper/` mixes obsolete `.md` drafts with canonical `latex_gpt/` and stray Chinese files, `logs/` carries 2026-04-03 artifacts at root, and several top-level directories (`paper_zh/`, `npj_submission_package/`, `AGENT_SYNC/`) are historical parallels to the current canonical trees. Goal: make the layout skimmable.

Nothing on the reproducibility or submission critical path may be moved.

---

## TX-24 — Archive loose coordination `.md` at `compute_vit/` root

Create `/home/qiaosir/projects/compute_vit/report_md/_gpt/archive/coordination_20260417/`.

**Move** (these are session-specific coordination / historical broadcasts; canonical live coordination already lives under `report_md/_gpt/`):
- `BROADCAST_KIMI_RECOMMENDATIONS_20260412.md`
- `BROADCAST_KIMI_TASKS_COMPLETED_20260413.md`
- `BROADCAST_NPJ_STRATEGY_20260413.md`
- `BROADCAST_REVIEWER_0412_ANALYSIS.md`
- `BROADCAST_WORKING.md`
- `CLEANUP_CANDIDATES_20260411_gpt.md`
- `DOCTOR_MESSAGE_SHORT_20260413_gpt.md`
- `EXPERIMENT_DESIGN_PRELIM_gpt.md`
- `EXPERIMENT_STATUS.md`
- `EXTERNAL_REVIEW_PROMPT.md`
- `KIMI_ROUND2_REPORT.md`
- `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md`
- `MEASURED_DATA_REQUEST_PRIORITY_TABLE.md`
- `MEASURED_DATA_REQUIREMENTS.md`
- `STATUS_REPORT_20260415.md`

**KEEP at root** (actively referenced / submission-facing):
- `README.md`
- `MASTER_PLAN.md`
- `RELEASE_CHECKLIST.md`
- `EXPERIMENT_PROTOCOL.md` — verify: if untouched since 2026-04-08 and not referenced by current `.tex`, also archive; otherwise keep.

---

## TX-25 — Archive obsolete drafts in `compute_vit/paper/`

Create `/home/qiaosir/projects/compute_vit/paper/archive_20260417/`.

**Move** (the canonical manuscript lives in `paper/latex_gpt/sections/*.tex` — these markdown drafts are superseded):
- `paper/01_introduction.md` → `paper/archive_20260417/01_introduction.md`
- `paper/02_related_work.md`
- `paper/03_methodology.md`
- `paper/04_experimental_setup.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/07_conclusion.md`
- `paper/08_appendix.md`
- `paper/PAPER_OUTLINE.md`
- `paper/仿真.tex`  (stray Chinese LaTeX scratch, not referenced by `latex_gpt/`)
- `paper/参考文献库.md`  (Chinese bibliography notes, superseded by `refs_gpt.bib`)
- `paper/BANANA_JOURNAL_SCHEMATIC_PROMPTS_20260408_gpt.md`
- `paper/NANOBANANA_SCHEMATIC_PROMPTS_gpt.md`
- `paper/PERPLEXITY_TARGETED_CITATION_PROMPTS_gpt.md`
- `paper/FIG1_FIG2_BRIEF_gpt.md`
- `paper/FIGURE_CAPTION_DRAFTS_gpt.md`

**KEEP under `paper/`:**
- `paper/CANONICAL_RESULT_LOCK_gpt.md` — actively cited by ongoing audits
- `paper/FIGURE_CAPTION_LOCK_gpt.md` — authoritative caption source
- `paper/FIGURE_PLAN.md` — still referenced by plotting scripts
- `paper/figures/`
- `paper/latex_gpt/`
- `paper/fix_plots.py`, `paper/generate_schematic_figures_gpt.py`, `paper/plot_paper_figures.py`

Before moving any `_gpt.md` you are uncertain about, `grep -rln <filename>` under `paper/latex_gpt/` and `report_md/_gpt/` to check for cross-references. If referenced, keep.

---

## TX-26 — Reorganize `compute_vit/logs/`

Create `/home/qiaosir/projects/compute_vit/logs/archive_pre_20260404/`.

**Move** (everything date-stamped before 2026-04-04 at `logs/` root, plus same-vintage unstamped runs):
- `logs/model_profiling_20260403_092017.log`
- `logs/physical_noise_pipeline_20260403_093730.log`
- `logs/physical_noise_pipeline_20260403_093857.log`
- `logs/plot_resnet18_20260403_201558.log`
- `logs/run_a23_20260403_203036.log`
- `logs/test_analog_layers_20260403_092209.log`
- `logs/test_analog_layers_20260403_093327.log`
- `logs/test_analog_layers_20260403_093553.log`
- `logs/test_analog_layers_20260403_095221.log`
- `logs/train_convnext_full_20260403_202645.log`
- `logs/train_resnet18_full_20260403_095144.log`

**Do NOT move** anything under `logs/_gpt/` (canonical organized logs) or any undated feature-name log that is less than 30 days old (`adc_cliff_analysis.log`, `adc_nonideality_*.log`, `aihwkit_benchmark.log`, `ensemble_frequency_ablation.log`, `flowers102_training.log`, `framework_comparison.log`, `ir_drop_sensitivity*.log`, `spatial_ablation.log`, `svhn_training.log`). These may still be tailed by diagnostics.

---

## TX-27 — Archive historical parallel directories

Create `/home/qiaosir/projects/compute_vit/archive/historical_20260417/`.

**Move** (these are superseded parallel trees — keep them around as a reversibility cushion):
- `compute_vit/AGENT_SYNC/` → `compute_vit/archive/historical_20260417/AGENT_SYNC/`
  - Reason: `report_md/_gpt/AGENT_SYNC_gpt.md` is the canonical live sync; the directory form is a 2026-04-15 artifact.
- `compute_vit/npj_submission_package/` → `compute_vit/archive/historical_20260417/npj_submission_package/`
  - Reason: the repositioning to Nature Communications made this package historical. Before moving, confirm the current NC submission bundle lives under `outputs/submission_bundle_20260417/` — if not, STOP and report.
- `compute_vit/paper_zh/` → `compute_vit/archive/historical_20260417/paper_zh/`
  - Reason: Chinese mirror is not on the submission path. `sync_zh.py` at `compute_vit/` root targets this dir; include `sync_zh.py` in TX-28 archival.

**Do NOT move:**
- `数据_博士/` — this is the doctor's measured-data staging and may still be referenced by `eval_measured_profile.py`. `grep -rln 数据_博士` across code to confirm, and keep in place regardless.
- `docs/`, `device_profiles/`, `scripts/`, `outputs/` (active), `internal/` (gitignored scratch).

---

## TX-28 — Version-redundant / one-shot root `.py` scripts

Create `/home/qiaosir/projects/compute_vit/scripts/archive_20260417_versions/`.

**Move** (each pair has a clearly-later canonical sibling retained):
- `run_adc_nonideality_analysis.py` → archive (kept: `run_adc_nonideality_v2.py`)
- `run_crosssim_comparison.py` → archive (kept: `run_crosssim_comparison_v2.py`)
- `run_ensemble_hat_ablation.py` → archive (kept: `run_ensemble_hat_ablation_FIXED.py` and `run_ensemble_hat_fixed.py`)
- `run_ir_drop_sensitivity.py`, `run_ir_drop_sensitivity_v2.py` → archive (kept: `run_ir_drop_sensitivity_v3.py`)
- `run_nl_layer_sensitivity.py` → archive (kept: `run_nl_layer_sensitivity_fixed.py`)
- `sync_zh.py` → archive (follows `paper_zh/` archival from TX-27)
- `patch_fig11.py` → archive (one-shot patch; figure is regenerated by `plot_paper_figures.py`)
- `port_05.py` → archive (one-shot port helper)
- `upgrade_plots.py` → archive (one-shot)
- `proxy_sensitivity_sweep_gpt.py` → **KEEP** (referenced by discussion)

Before each move, `grep -rn '<basename>' compute_vit/ --include='*.py' --include='*.sh' --include='*.md' --include='*.tex'` to confirm no active caller. If any caller exists in a non-archived file, STOP that particular move and record it in the manifest.

**Do NOT touch** `test_*.py` (actual test suite), `train_*.py`, `analog_layers*.py`, `amp_utils.py`, `device_profile_utils.py`, `eval_*.py`, `inference_analysis_utils.py`, `physical_noise_pipeline.py`, `model_profiling.py`, `generate_final_report.py`, `generate_synthetic_device_profiles_gpt.py`, `make_appendix.py`, `download_imagenet_val.py`, `prepare_imagenet_val.py`, `probe_resnet_ckpts.py`, `report_asset_paths.py`, `tinyvit_hybrid_utils.py`, `visualize_attention.py`, any `run_*.py` not on the archive list above, `ablation_*.py`, `experiment_nonideality_sweep.py`.

---

## TX-29 — Tidy manifest

Write `/home/qiaosir/projects/compute_vit/report_md/_gpt/TIDY_MANIFEST_20260417.md`.

Include per TX-24..TX-28:
1. Table: source → destination → size → reason.
2. Any item you chose NOT to move (especially TX-27 `数据_博士/` confirmation, TX-25 cross-reference checks, TX-28 caller checks).
3. `grep` outputs that justified each judgement call.
4. Final `ls` of `compute_vit/` root showing only files, and a short count summary:
   - Root `.md` count before/after
   - Root `.py` count before/after
   - `paper/` non-dir file count before/after
   - `logs/` non-dir file count before/after

Do **not** commit. User reviews, then either you or Claude commits.

---

## Hard constraints (identical to Dispatch #7)

- **No deletions.** All moves reversible via `mv`.
- **No content edits** to `.md`, `.tex`, `.py`, `.bib`, `.json`.
- **No touching** `checkpoints/`, `data/`, `paper/latex_gpt/sections/*.tex`, `paper/latex_gpt/*.pdf`, `paper/latex_gpt/*.bib`, `paper/latex_gpt/figures/`, `report_md/_gpt/*.md` except for the manifest you are writing now.
- **No `git commit`, no `git push`.**
- **When in doubt, STOP and record in the manifest.** The bias is toward over-keeping rather than over-archiving.
- If a `grep` check reveals a reference to a file you were about to move, leave it in place and note the caller in the manifest.

---

## Reporting

Update `CLAUDE_TASK_gpt.md` TX-24..TX-29 status rows to `✅` / `⛔`, and append a single block to `AGENT_SYNC_gpt.md` summarizing scope + manifest path.
