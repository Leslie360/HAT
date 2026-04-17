# Cleanup Candidates (Conservative)

This file lists what can be removed from the repository **without harming**:

- reproducibility of the paper-level results
- future open-source release of the simulator/code
- preservation of the reference materials / source-paper PDFs / report assets

Status: **no files have been deleted yet**. This is a review checklist only.

## Ground rules

The following are treated as **must-keep** for now:

- canonical code paths:
  - `analog_layers.py`
  - `analog_layers_ensemble.py`
  - `device_profile_utils.py`
  - `train_tinyvit.py`
  - `train_tinyvit_ensemble.py`
  - `train_convnext.py`
  - `train_resnet18.py`
  - `run_device_comparison.py`
  - `run_noise_sweep.py`
- tests and utilities that still exercise core code paths
- `device_profiles/`
- `data/`
- canonical top-level checkpoints under `checkpoints/*.pt`
- final English paper source under `paper/latex_gpt/`
- final paper PDFs currently under review:
  - `paper/latex_gpt/main.pdf`
  - `paper/latex_gpt/supplementary_main.pdf`
  - `paper/latex_gpt/cover_letter.pdf`
- reference materials / source-paper PDFs:
  - `report_md/s41467-025-66891-6.pdf`
  - `report_md/41467_2025_66891_MOESM1_ESM.pdf`
  - `report_md/How to submit _ Nature Communications.pdf`
- Chinese draft / parallel manuscript materials:
  - `paper_zh/`

## A. Safe To Delete Now

These are the lowest-risk items. Deleting them does **not** remove canonical code, canonical paper source, or source-paper references.

### A1. Python cache and pure build byproducts

- `__pycache__/`
- `paper/latex_gpt/*.aux`
- `paper/latex_gpt/*.bbl`
- `paper/latex_gpt/*.blg`
- `paper/latex_gpt/*.fdb_latexmk`
- `paper/latex_gpt/*.fls`
- `paper/latex_gpt/*.log`
- `paper/latex_gpt/*.out`

Why safe:

- all of these are generated artifacts
- LaTeX can regenerate them at any time
- Python will regenerate cache files automatically

Approximate reclaim:

- `paper/latex_gpt` build byproducts: about `328K`
- `__pycache__/`: about `120K`

### A2. Clearly obsolete smoke / suspect / badscale checkpoints

- `checkpoints/_gpt/_codex_smoke_V1_s42/`
- `checkpoints/_gpt/_codex_smoke_V1_s42_amp4_fg/`
- `checkpoints/_gpt/_codex_smoke_V1_s42_nw0/`
- `checkpoints/_gpt/_codex_smoke_V1_s42_amp4_tty/`
- `checkpoints/_gpt/_codex_smoke_C1_s42/`
- `checkpoints/_ensemble_smoke/`
- `checkpoints/_gpt_badscale/`
- `checkpoints/_gpt_v3_suspect/`

Why safe:

- these are explicitly smoke, suspect, or known-bad branches
- they are not canonical checkpoints for the paper
- keeping them does not help open-source users reproduce the final claims

Approximate reclaim:

- about `1.2G`

### A3. Unused figure drafts / Banana variants not referenced by LaTeX

- `paper/latex_gpt/figures/figA.png`
- `paper/latex_gpt/figures/figB.png`
- `paper/latex_gpt/figures/figC.png`
- `paper/latex_gpt/figures/figD.png`
- `paper/latex_gpt/figures/fig1_enhanced.png`
- `paper/latex_gpt/figures/fig1_system_architecture_banana.png`
- `paper/latex_gpt/figures/fig1_system_architecture_banana_clean.png`
- `paper/latex_gpt/figures/fig1_system_architecture_banana_crop.png`
- `paper/latex_gpt/figures/fig1_system_architecture_banana_final.png`
- `paper/latex_gpt/figures/fig2_weight_mapping_banana.png`
- `paper/latex_gpt/figures/fig2_weight_mapping_banana_clean.png`
- `paper/latex_gpt/figures/fig2_weight_mapping_banana_clean2.png`
- `paper/latex_gpt/figures/fig2_weight_mapping_banana_crop.png`
- `paper/latex_gpt/figures/fig2_weight_mapping_banana_final.png`
- `paper/latex_gpt/figures/fig_bottleneck_hierarchy_banana.png`
- `paper/latex_gpt/figures/fig_bridge_materials_to_system_banana.png`

Why safe:

- current LaTeX source does not reference these filenames
- they are draft image iterations rather than active figure assets
- final paper uses `fig1_system_architecture.pdf`, `fig2_weight_mapping.pdf`, `figS1_asymmetry_concept.png`, `figS2_nonideality.png`, `figS3_ensemble_hat.png`, etc.

Approximate reclaim:

- about `76M`

### A4. Empty / trivial one-off logs

- `logs/train_convnext_full_20260403_202645.log` (currently zero bytes)

Why safe:

- no informational content

## B. Archive First, Then Delete Locally

These are good cleanup targets, but I recommend making a single tarball or external archive first.

### B1. Internal collaboration / coordination history

- `report_md/_gpt/`
- top-level coordination leftovers:
  - `EXPERIMENT_DESIGN_PRELIM_gpt.md`
  - `KIMI_ROUND2_REPORT.md`
  - `internal/DATA_REQUIREMENTS_FULL_v1.md`
- paper-planning helpers:
  - `paper/BANANA_JOURNAL_SCHEMATIC_PROMPTS_20260408_gpt.md`
  - `paper/CANONICAL_RESULT_LOCK_gpt.md`
  - `paper/FIG1_FIG2_BRIEF_gpt.md`
  - `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
  - `paper/FIGURE_CAPTION_LOCK_gpt.md`
  - `paper/NANOBANANA_SCHEMATIC_PROMPTS_gpt.md`
  - `paper/PAPER_OUTLINE.md`
  - `paper/PERPLEXITY_TARGETED_CITATION_PROMPTS_gpt.md`
- LaTeX-side writing aids:
  - `paper/latex_gpt/CITATION_BACKLOG_gpt.md`
  - `paper/latex_gpt/CITATION_MAP_gpt.md`
  - `paper/latex_gpt/CLOSEOUT_CHECKLIST_gpt.md`
  - `paper/latex_gpt/README_gpt.md`
  - `paper/latex_gpt/SUBMISSION_PACKET_gpt.md`
  - `paper/latex_gpt/TEMPLATE_MIGRATION_GUIDE_gpt.md`

Why archive-first:

- they are not needed for scientific reproducibility
- they are not part of the release-facing simulator
- but they do preserve process history, reviewer handling, and editorial trace

Approximate reclaim:

- around `5.0M` for the most obvious coordination bundle above

### B2. One-off orchestration scripts and watchers

Top-level helpers that are only for internal experiment choreography:

- `append_batch3.py`
- `append_kimi_km14.py`
- `append_kimi_km14_part2.py`
- `append_kimi_km14_v2.py`
- `append_kimi_part2.py`
- `append_sync.py`
- `append_sync_batch4.py`
- `append_sync_final.py`
- `append_sync_k5.py`
- `append_sync_kimi.py`
- `run_task16c_gpt.sh`
- `run_task21_convnext_flowers102_gpt.sh`
- `run_task21_convnext_multidataset_gpt.sh`
- `run_task23_convnext_c4_nl_moderate_gpt.sh`
- `run_task23_task24_after_task21_gpt.sh`
- `run_task23_tinyvit_nl_suite_gpt.sh`
- `run_task24_v4_proportional_eval_gpt.sh`
- `run_task34_task35_task36_chain_gpt.sh`
- `run_task34_v4_proportional_hat_gpt.sh`
- `run_task35_v4_nl2_hat_gpt.sh`
- `run_task36_c4_proportional_hat_gpt.sh`
- `run_post_v4_suite_gpt.sh`
- `watch_convnext_task21_stage1_completion_gpt.py`
- `watch_convnext_task21_stage2_completion_gpt.py`
- `watch_convnext_task21_stage2_then_launch_task23_task24_gpt.py`
- `watch_noise_sweep_completion_gpt.py`

And the `_gpt` queue/watcher layer:

- `scripts/_gpt/run_*queue*.sh`
- `scripts/_gpt/watch_*.sh`
- `scripts/_gpt/check_p13_status_gpt.sh`

Why archive-first:

- they encode historical execution choreography
- they are useful for audit trail
- but they are not part of a clean open-source core API
- core reproducibility should be driven by the canonical training/eval scripts, not by old task wrappers

### B3. Internal logs

- `logs/_gpt/`
- old root logs under `logs/` except any file you personally still use as evidence

Why archive-first:

- useful as audit evidence
- not needed in the final public codebase
- not needed to reproduce the paper if final metrics are already locked in paper + canonical reports

Approximate reclaim:

- `logs/_gpt/`: about `1.3M`

### B4. Heavy rerun / ablation checkpoint branches

These are the biggest optional archive targets if you want to slim the repo without losing canonical top-level checkpoints:

- `checkpoints/_gpt/multi_seed/` (`5.2G`)
- `checkpoints/_gpt/multi_seed_fix/` (`2.5G`)
- `checkpoints/_gpt/multi_seed_fix256/` (`2.5G`)
- `checkpoints/_gpt/multi_seed_v3/` (`2.5G`)
- `checkpoints/_gpt/task23/` (`730M`)
- `checkpoints/_gpt/task34_v4_proportional_hat/` (`153M`)
- `checkpoints/_gpt/task35_v4_nl2_hat/` (`153M`)
- `checkpoints/_gpt/task36_c4_proportional_hat/` (`424M`)
- `checkpoints/_gpt/flowers102_ablation/` (`154M`)

Why archive-first:

- they are valuable for internal audit and exact rerun provenance
- but they are not the minimal artifact set required for code release
- if you keep canonical top-level checkpoints and the final manuscript tables, these can be moved to cold storage

Recommended rule:

- keep the canonical top-level checkpoints in `checkpoints/*.pt`
- archive these rerun trees outside the repo before local deletion

### B5. Redundant manuscript mirrors

- `paper/01_introduction.md`
- `paper/02_related_work.md`
- `paper/03_methodology.md`
- `paper/04_experimental_setup.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/07_conclusion.md`
- `paper/08_appendix.md`

Why archive-first:

- the canonical paper source is now LaTeX
- these Markdown mirrors are convenient, but not required for reproduction or release
- if you want a lean repo, they are removable after archival

## C. Keep

I do **not** recommend deleting these right now.

### C1. Core scientific and release assets

- `data/`
- `device_profiles/`
- `docs/`
- top-level canonical code and tests
- top-level canonical checkpoints in `checkpoints/*.pt`
- `checkpoints/_ensemble/`

### C2. Final paper package

- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/supplementary_main.tex`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/refs_gpt.bib`
- `paper/latex_gpt/sections/*`
- `paper/latex_gpt/main.pdf`
- `paper/latex_gpt/supplementary_main.pdf`
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/cover_letter.pdf`

### C3. Active figure assets still referenced by LaTeX

Keep all currently referenced final figures, including:

- `paper/latex_gpt/figures/fig1_system_architecture.pdf`
- `paper/latex_gpt/figures/fig2_weight_mapping.pdf`
- `paper/latex_gpt/figures/fig3_snr_curves.pdf`
- `paper/latex_gpt/figures/fig4_accuracy_comparison.pdf`
- `paper/latex_gpt/figures/fig5_hat_recovery.pdf`
- `paper/latex_gpt/figures/fig6_physical_compensation.pdf`
- `paper/latex_gpt/figures/fig7_retention_curve.pdf`
- `paper/latex_gpt/figures/fig8_pareto_energy_accuracy.pdf`
- `paper/latex_gpt/figures/fig9_noise_sensitivity.pdf`
- `paper/latex_gpt/figures/fig10_zero_shot_transferability.pdf`
- `paper/latex_gpt/figures/fig11_energy_breakdown.pdf`
- `paper/latex_gpt/figures/fig_attention_maps.pdf`
- `paper/latex_gpt/figures/figS1_asymmetry_concept.png`
- `paper/latex_gpt/figures/figS2_nonideality.png`
- `paper/latex_gpt/figures/figS3_ensemble_hat.png`

### C4. Reference-paper and submission-guideline materials

- `report_md/s41467-025-66891-6.pdf`
- `report_md/41467_2025_66891_MOESM1_ESM.pdf`
- `report_md/How to submit _ Nature Communications.pdf`
- `report_md/json/`
- `report_md/csv/`
- `report_md/images/`

Reason:

- these still serve as evidence packs / source-data seeds / reference material
- they are small compared with checkpoints

## Recommended deletion order

If you want a safe, low-drama cleanup sequence:

1. Delete `__pycache__/` and LaTeX build byproducts
2. Delete clearly obsolete smoke / suspect checkpoints
3. Delete unused Banana figure drafts
4. Archive `report_md/_gpt/`, `logs/_gpt/`, orchestration scripts, then delete local copies
5. Only then consider archiving large rerun checkpoint trees under `checkpoints/_gpt/`

## Quick estimate

Very conservative immediate reclaim:

- smoke/suspect checkpoints: `~1.2G`
- unused Banana / draft figures: `~76M`
- LaTeX build byproducts + cache: `~0.4M`

Total immediate low-risk reclaim:

- roughly `~1.3G`

If you also archive-and-delete the internal coordination bundle:

- add `~5M`

If you later archive-and-delete heavy rerun checkpoint trees:

- add `10G+`

## Suggested next step

If you want, I can do the next step in two safer phases:

1. generate a **shell-safe deletion script** for only section A
2. generate an **archive script** for section B so nothing important is lost
