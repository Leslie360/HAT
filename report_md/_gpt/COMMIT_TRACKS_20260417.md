# COMMIT TRACKS — 2026-04-17

Purpose: exact split of the current worktree into two intentional commits:

1. `cleanup-only`
2. `paper/core`

No path below should require interpretation at staging time.

## Recommended Order

1. `cleanup-only`
2. `paper/core`

Reason: the cleanup commit removes archive/noise churn first, so the paper-facing diff becomes smaller and easier to review.

---

## Commit 1 — `cleanup-only`

### Include

Stage exactly these paths:

```bash
git add \
  .gitignore \
  PROJECT_INDEX.md \
  report_md/_gpt/PROJECT_INDEX_AUDIT_20260417.md \
  report_md/_gpt/GIT_HYGIENE_LEDGER_20260417.md \
  report_md/_gpt/READY_TO_STAGE_SHORTLIST_20260417.md \
  report_md/_gpt/COMMIT_TRACKS_20260417.md \
  report_md/_gpt/AGENT_SYNC_gpt.md \
  report_md/_gpt/CLAUDE_TASK_gpt.md \
  _archive/figure-drafts \
  _archive/paper-drafts/BANANA_JOURNAL_SCHEMATIC_PROMPTS_20260408_gpt.md \
  _archive/paper-drafts/NANOBANANA_SCHEMATIC_PROMPTS_gpt.md \
  _archive/paper-drafts/PERPLEXITY_TARGETED_CITATION_PROMPTS_gpt.md \
  _archive/scripts-oneshot/run_exp_b.sh \
  _archive/scripts-oneshot/run_hardening_experiments.sh \
  _archive/scripts-oneshot/run_imagenet_eval.sh \
  _archive/scripts-oneshot/run_nl_landscape_scan.sh \
  _archive/scripts-oneshot/run_post_v4_suite_gpt.sh \
  _archive/scripts-oneshot/run_resnet18_cifar100.sh \
  _archive/scripts-oneshot/run_task16c_gpt.sh \
  _archive/scripts-oneshot/run_task21_convnext_flowers102_gpt.sh \
  _archive/scripts-oneshot/run_task21_convnext_multidataset_gpt.sh \
  _archive/scripts-oneshot/run_task23_convnext_c4_nl_moderate_gpt.sh \
  _archive/scripts-oneshot/run_task23_task24_after_task21_gpt.sh \
  _archive/scripts-oneshot/run_task23_tinyvit_nl_suite_gpt.sh \
  _archive/scripts-oneshot/run_task24_tinyvit_nl15_interp_gpt.sh \
  _archive/scripts-oneshot/run_task24_v4_proportional_eval_gpt.sh \
  _archive/scripts-oneshot/run_task34_task35_task36_chain_gpt.sh \
  _archive/scripts-oneshot/run_task34_v4_proportional_hat_gpt.sh \
  _archive/scripts-oneshot/run_task35_v4_nl2_hat_gpt.sh \
  _archive/scripts-oneshot/run_task36_c4_proportional_hat_gpt.sh
```

Stage the cleanup deletions together with:

```bash
git add -u \
  patch_fig11.py \
  port_05.py \
  sync_zh.py \
  upgrade_plots.py \
  run_post_v4_suite_gpt.sh \
  run_task16c_gpt.sh \
  run_task21_convnext_flowers102_gpt.sh \
  run_task21_convnext_multidataset_gpt.sh \
  run_task23_convnext_c4_nl_moderate_gpt.sh \
  run_task23_task24_after_task21_gpt.sh \
  run_task23_tinyvit_nl_suite_gpt.sh \
  run_task24_v4_proportional_eval_gpt.sh \
  run_task34_task35_task36_chain_gpt.sh \
  run_task34_v4_proportional_hat_gpt.sh \
  run_task35_v4_nl2_hat_gpt.sh \
  run_task36_c4_proportional_hat_gpt.sh \
  paper/仿真.tex \
  logs/model_profiling_20260403_092017.log \
  logs/physical_noise_pipeline_20260403_093730.log \
  logs/physical_noise_pipeline_20260403_093857.log \
  logs/plot_resnet18_20260403_201558.log \
  logs/run_a23_20260403_203036.log \
  logs/test_analog_layers_20260403_092209.log \
  logs/test_analog_layers_20260403_093327.log \
  logs/test_analog_layers_20260403_093553.log \
  logs/test_analog_layers_20260403_095221.log \
  logs/train_convnext_full_20260403_202645.log \
  logs/train_resnet18_full_20260403_095144.log \
  report_md/_gpt/CLAUDE_REPLAY_POINTERS_gpt.md \
  report_md/_gpt/EXTERNAL_REVIEW_DETAILED_BROADCAST_20260408_gpt.md \
  report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_gpt.md \
  report_md/_gpt/GEMINI_HANDOFF_gpt.md \
  report_md/_gpt/GEMINI_TAKEOVER_BRIEF_gpt.md \
  report_md/_gpt/Gemini_REPLY_gpt.md \
  report_md/_gpt/LLM_CHANGELOG_gpt.md \
  report_md/_gpt/LLM_HANDOFF_gpt.md \
  report_md/_gpt/RUNTIME_MANIFEST_gpt.md \
  report_md/_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.md \
  report_md/_gpt/_codex_verify_v4_retention_probe_cuda_20260407.md \
  report_md/_gpt/_probe_convnext_cifar100_c1_resume.md \
  report_md/_gpt/_tmp_retention_probe_gpt.md \
  report_md/_gpt/c4_nl_moderate_results_gpt.md \
  report_md/_gpt/c4_proportional_hat_train_results_gpt.md \
  report_md/_gpt/codex_a3_plan_gpt.md \
  report_md/_gpt/convnext_c1_report_gpt.md \
  report_md/_gpt/convnext_c9_retention_report_gpt.md \
  report_md/_gpt/convnext_cifar100_c134_results_gpt.md \
  report_md/_gpt/convnext_experiment_report_gpt.md \
  report_md/_gpt/convnext_flowers102_c134_results_gpt.md \
  report_md/_gpt/convnext_full_report_gpt.md \
  report_md/_gpt/convnext_resume_report_gpt.md \
  report_md/_gpt/device_comparison_report_gpt.md \
  report_md/_gpt/layer_sensitivity_report_gpt.md \
  report_md/_gpt/literature_fake_profile_workflow_gpt.md \
  report_md/_gpt/literature_profile_zhang2025_provenance_gpt.md \
  report_md/_gpt/measured_device_data_bridge_gpt.md \
  report_md/_gpt/noise_sweep_report_gpt.md \
  report_md/_gpt/tinyvit_cifar100_v134_results_gpt.md \
  report_md/_gpt/tinyvit_flowers102_v134_results_gpt.md \
  report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md \
  report_md/_gpt/tinyvit_noise_diagnostic_gpt.md \
  report_md/_gpt/tinyvit_results_gpt.md \
  report_md/_gpt/tinyvit_retention_diagnostic_gpt.md \
  report_md/_gpt/tinyvit_v1_results_gpt.md \
  report_md/_gpt/tinyvit_v2v7_results_gpt.md \
  report_md/_gpt/tinyvit_v4_retention_report_gpt.md \
  report_md/_gpt/tinyvit_v7_retention_report_gpt.md \
  report_md/_gpt/v2_under_noise_report_gpt.md \
  report_md/_gpt/v4_ensemble_report_gpt.md \
  report_md/_gpt/v4_nl2_hat_eval_results_gpt.md \
  report_md/_gpt/v4_nl2_hat_train_results_gpt.md \
  report_md/_gpt/v4_nl_moderate_results_gpt.md \
  report_md/_gpt/v4_nl_severe_results_gpt.md \
  report_md/_gpt/v4_proportional_hat_eval_proportional_results_gpt.md \
  report_md/_gpt/v4_proportional_hat_eval_uniform_results_gpt.md \
  report_md/_gpt/v4_proportional_hat_train_results_gpt.md \
  report_md/_gpt/v4_proportional_noise_report_gpt.md
```

### Exclude

Do **not** stage any of the following in `cleanup-only`:

- any `paper/latex_gpt/*.tex`, `paper/latex_gpt/*.bib`, or `paper/latex_gpt/*.md`
- any active runtime/training/test `.py`
- `paper/08_appendix.md`
- `paper/FIGURE_PLAN.md`
- generated `paper/figures/*.png|*.pdf`
- generated `paper/latex_gpt/figures/fig3+` result exports
- `paper/latex_gpt/main.pdf`
- any `report_md/_gpt` file that is submission/content evidence rather than cleanup bookkeeping

### Suggested commit message

```bash
git commit -m "repo: archive one-shot artifacts and refresh project index"
```

---

## Commit 2 — `paper/core`

### Include

Stage exact manuscript source files:

```bash
git add \
  paper/08_appendix.md \
  paper/FIGURE_PLAN.md \
  paper/plot_paper_figures.py \
  paper/generate_schematic_figures_gpt.py \
  paper/latex_gpt/main.tex \
  paper/latex_gpt/cover_letter.tex \
  paper/latex_gpt/supplementary.tex \
  paper/latex_gpt/supplementary_main.tex \
  paper/latex_gpt/refs_gpt.bib \
  paper/latex_gpt/README_gpt.md \
  paper/latex_gpt/CITATION_MAP_gpt.md \
  paper/latex_gpt/CITATION_BACKLOG_gpt.md \
  paper/latex_gpt/SUBMISSION_PACKET_gpt.md \
  paper/latex_gpt/sections/00_abstract.tex \
  paper/latex_gpt/sections/01_introduction.tex \
  paper/latex_gpt/sections/02_related_work.tex \
  paper/latex_gpt/sections/03_methodology.tex \
  paper/latex_gpt/sections/04_experimental_setup.tex \
  paper/latex_gpt/sections/05_results.tex \
  paper/latex_gpt/sections/06_discussion.tex \
  paper/latex_gpt/sections/07_conclusion.tex \
  paper/latex_gpt/sections/08_appendix.tex
```

Stage exact active code and tests:

```bash
git add \
  analog_layers.py \
  device_profile_utils.py \
  eval_imagenet_analog.py \
  eval_measured_profile.py \
  eval_resnet18_checkpoints.py \
  inference_analysis_utils.py \
  train_convnext.py \
  train_resnet18.py \
  train_tinyvit.py \
  train_tinyvit_ensemble.py \
  visualize_attention.py \
  test_analog_layers.py \
  test_run_device_comparison.py \
  ablation_ensemble_hat_vs_iid.py \
  experiment_nonideality_sweep.py \
  generate_final_report.py \
  download_imagenet_val.py \
  prepare_imagenet_val.py \
  probe_resnet_ckpts.py \
  proxy_sensitivity_sweep_gpt.py
```

Stage exact curated static assets:

```bash
git add \
  paper/latex_gpt/figures/fig1_system_architecture.pdf \
  paper/latex_gpt/figures/fig2_weight_mapping.pdf \
  paper/latex_gpt/figures/figA.png \
  paper/latex_gpt/figures/figB.png \
  paper/latex_gpt/figures/figC.png \
  paper/latex_gpt/figures/figD.png \
  paper/latex_gpt/figures/figS1_asymmetry_concept.png \
  paper/latex_gpt/figures/figS2_nonideality.png \
  paper/latex_gpt/figures/graphical_abstract.png
```

Stage exact submission/review packet docs that are current and paper-facing:

```bash
git add \
  report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md \
  report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md \
  report_md/_gpt/REVIEWER_ARCHIVE_MANIFEST_20260417.md \
  report_md/_gpt/FIGURE_PROVENANCE_MANIFEST_20260417.md \
  report_md/_gpt/FINAL_ALIGNMENT_CHECKLIST_20260417.md \
  report_md/_gpt/EXTERNAL_REVIEW_FOLLOWUP_20260417.md \
  report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_20260417.md \
  report_md/_gpt/SUBMISSION_BUNDLE_CHECKLIST_20260417.md \
  report_md/_gpt/SUBMISSION_PREFLIGHT_20260416.md \
  report_md/_gpt/CLAUDE_REVIEW_PACKET_20260417.md
```

### Exclude

Do **not** stage any of the following in `paper/core`:

- `_archive/**`
- `.gitignore`
- cleanup bookkeeping docs:
  - `report_md/_gpt/PROJECT_INDEX_AUDIT_20260417.md`
  - `report_md/_gpt/GIT_HYGIENE_LEDGER_20260417.md`
  - `report_md/_gpt/READY_TO_STAGE_SHORTLIST_20260417.md`
  - `report_md/_gpt/COMMIT_TRACKS_20260417.md`
- generated figure exports:
  - `paper/figures/*.png`
  - `paper/figures/*.pdf`
  - `paper/latex_gpt/figures/fig3_snr_curves.png`
  - `paper/latex_gpt/figures/fig4_accuracy_comparison.png`
  - `paper/latex_gpt/figures/fig5_hat_recovery.png`
  - `paper/latex_gpt/figures/fig6_physical_compensation.png`
  - `paper/latex_gpt/figures/fig7_retention_curve.png`
  - `paper/latex_gpt/figures/fig8_pareto_energy_accuracy.png`
  - `paper/latex_gpt/figures/fig9_noise_sensitivity.png`
  - `paper/latex_gpt/figures/fig10_zero_shot_transferability.png`
  - `paper/latex_gpt/figures/fig11_energy_breakdown.png`
  - `paper/latex_gpt/figures/fig_attention_differences.png`
  - `paper/latex_gpt/figures/fig_attention_maps.png`
- build output PDFs:
  - `paper/latex_gpt/main.pdf`
- draft-superseded markdown still blocked by live callers:
  - `paper/01_introduction.md`
  - `paper/02_related_work.md`
  - `paper/03_methodology.md`
  - `paper/04_experimental_setup.md`
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/07_conclusion.md`
  - `paper/PAPER_OUTLINE.md`
  - `paper/FIG1_FIG2_BRIEF_gpt.md`
  - `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
  - `paper/参考文献库.md`
- root repo docs/policy not reviewed as part of the paper bundle:
  - `README.md`
  - `LICENSE`
  - `RELEASE_CHECKLIST.md`
  - `EXPERIMENT_PROTOCOL.md`
  - `MASTER_PLAN.md`
  - `docs/`
  - `AGENT_SYNC/`
- non-paper office/reference assets in `report_md/`:
  - `report_md/*.pdf`
  - `report_md/*.pptx`
  - `report_md/*.docx`

### Suggested commit message

```bash
git commit -m "paper: sync NC manuscript, active code, and canonical assets"
```

---

## Deferred / Blocked

Keep these out of both commits for now:

- blocked paper draft files with live callers:
  - `paper/01_introduction.md`
  - `paper/02_related_work.md`
  - `paper/03_methodology.md`
  - `paper/04_experimental_setup.md`
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/07_conclusion.md`
  - `paper/PAPER_OUTLINE.md`
  - `paper/FIG1_FIG2_BRIEF_gpt.md`
  - `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
  - `paper/参考文献库.md`
- root documentation/policy files not reviewed in this packaging step:
  - `README.md`
  - `LICENSE`
  - `RELEASE_CHECKLIST.md`
  - `EXPERIMENT_PROTOCOL.md`
  - `MASTER_PLAN.md`
  - `docs/`
  - `AGENT_SYNC/`
- report assets and office documents under `report_md/`
- generated CSV/JSON result artifacts under `report_md/_gpt/` unless later curated into a dedicated source-data commit

## Acceptance Check

After staging each commit candidate:

```bash
git diff --cached --name-only
```

Expected outcome:

- `cleanup-only` shows only archive/index/ignore/coordination-hygiene paths
- `paper/core` shows only manuscript source, active code, curated static assets, and current submission/review docs
