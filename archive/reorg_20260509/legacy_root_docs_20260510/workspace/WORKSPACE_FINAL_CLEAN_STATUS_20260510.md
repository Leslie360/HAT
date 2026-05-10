# compute_vit Final Clean Status

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit`

## Final organization

- Manuscripts: `manuscripts/`
- Paper-1 active LaTeX: `manuscripts/paper1/src/`
- Paper-1 compatibility path: `paper/latex_gpt -> ../manuscripts/paper1/src`
- Thesis compatibility path: `thesis/latex_gpt -> ../manuscripts/paper1/src`
- Paper-2 snippets: `manuscripts/paper2/snippets/`
- Active coordination: `coordination/active/`
- Current report index: `report_md/_gpt/INDEX_CURRENT_20260509.md`
- Validation/plotting tools: `tools/validation/`, `tools/plotting/`
- Root Markdown after final root-doc pass: `README.md`, `PROJECT_INDEX.md`, `WORKSPACE_LAYOUT.md`
- Detailed project/reproducibility/workspace docs: `docs/project/`, `docs/reproducibility/`, `docs/workspace/`

## Verification

| Check | Result |
|---|---|
| Active broken symlinks | `0` |
| Final Paper-1 bundle SHA | `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4` |
| Paper-1 build | PASS from canonical and compatibility paths |
| Broadcast divergence | fixed; compute_vit broadcast paths point to root `BROADCAST.md` |
| Deletion/commit/push | none by Claude |
| Root files after root-doc pass | `31` regular files; only `3` root Markdown files |

## Active file distribution excluding `.git`, `archive`, `data`, `checkpoints`

```text
  344 manuscripts/paper1
  135 paper1/release
  120 paper2/results
   74 paper1/provenance
   73 thesis/xjtu_template
   71 paper/figures
   49 paper1/reports
   20 report_md/_gpt
   15 thesis/cn
   14 thesis/en
   11 report_md/images
    6 paper2/src
    5 logs/learnable_gamma_gpt
    5 report_md/json
    3 report_md/csv
    3 coordination/active
    3 coordination/audits
    3 coordination/dispatches
    3 manuscripts/thesis
    3 scripts/_gpt
    2 coordination/remote_tasks
    2 tools/plotting
    1 analog_layers_ensemble.py
    1 requirements.txt
    1 train_tinyvit.py
    1 hybrid_calibration.py
    1 train_resnet18.py
    1 physical_noise_pipeline.py
    1 train_tinyvit_ensemble.py
    1 PROJECT_INDEX.md
    1 eval_literature_profile.py
    1 report_asset_paths.py
    1 model_profiling.py
    1 WORKSPACE_LAYOUT_V2_20260509.md
    1 eval_imagenet_analog.py
    1 train_convnext.py
    1 eval_fresh_instances_postfix.py
    1 tinyvit_hybrid_utils.py
    1 requirements-optional.txt
    1 REPRODUCIBILITY.md
    1 environment.yml
    1 ROOT_REORG_PLAN_20260509.md
    1 auto_fitted_profile.json
    1 RELEASE_CHECKLIST.md
    1 eval_fresh_instances.py
    1 README.md
    1 inference_analysis_utils.py
    1 download_data.sh
    1 WORKSPACE_LAYOUT.md
    1 device_profile_utils.py
    1 README_REPRODUCIBILITY_PAPER1.md
    1 analog_layers.py
    1 .gitignore
    1 eval_measured_profile.py
    1 EXPERIMENT_PROTOCOL.md
    1 amp_utils.py
    1 hybrid_runtime_compiler.py
    1 eval_resnet18_checkpoints.py
    1 LICENSE
    1 MASTER_PLAN.md
    1 broadcast.md
    1 logs/archive_stale_markdown_wave2_20260510_001330.log
    1 logs/file_organization_report_scratch_mv_20260509_225434.log
    1 logs/file_organization_legacy_logs_mv_20260509_225735.log
    1 logs/file_organization_mv_only_20260509_224800.log
    1 logs/final_cleanup_broadcast_20260510_002830.log
    1 logs/claude_takeover_structured_reorg_broadcast_20260510_000557.log
    1 logs/p8_cleanup_20260509_221101.log
    1 logs/latex_unused_figures_move_retry_20260510_004600.log
    1 logs/file_organization_build_outputs_mv_20260509_224849.log
    1 logs/latex_build_manuscripts_paper1_20260510_004625.log
    1 logs/file_organization_legacy_coordination_mv_20260509_230209.log
    1 logs/latex_unused_figures_move_20260510_004537.log
    1 logs/file_organization_old_reports_mv_20260509_224916.log
    1 logs/p8_trackE_final_bundle_refresh_20260509_223000.log
    1 logs/file_organization_final_strays_mv_20260509_225702.log
    1 logs/file_organization_paper2_scripts_mv_20260509_225018.log
    1 logs/p8_trackE_bundle_refresh_20260509_222149.log
    1 logs/p8_pcm_guard_20260509_223000.log
    1 logs/file_organization_paper2_aux_mv_20260509_225548.log
```

## Latest residual cleanup archives

- `archive/residual_report_md_gpt_20260510/`
- `archive/residual_scripts_20260510/`
- `archive/residual_logs_gpt_20260510/`
- `archive/final_tiny_residuals_20260510/`

## Restore scripts

- `archive/reorg_20260509/restore/ROOT_DOCS_CLEANUP_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/RESIDUAL_REPORT_MD_GPT_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/RESIDUAL_SCRIPTS_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/RESIDUAL_LOGS_GPT_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/FINAL_TINY_RESIDUALS_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/LATEX_MANUSCRIPT_REORG_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/LATEX_UNUSED_FIGURES_20260510_RESTORE.sh`
