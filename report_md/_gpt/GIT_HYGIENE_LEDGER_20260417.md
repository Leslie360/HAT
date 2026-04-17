# GIT HYGIENE LEDGER — 2026-04-17

Audit basis: `git status --porcelain=v1 -z` in `/home/qiaosir/projects/compute_vit` after Dispatch #9 TX-32 file moves.

Counts:
- `TRACK`: 204
- `IGNORE`: 91
- `ARCHIVE`: 93
- `TOTAL`: 388

## TRACK (204)

| Path | Git Status | Reason | Suggested action |
|:--|:--:|:--|:--|
| `.gitignore` | `??` | live root documentation or repo policy file | keep as versioned project metadata and include in the next intentional commit |
| `AGENT_SYNC/` | `??` | deprecated but still script-referenced coordination artifact | keep versioned until the caller is removed |
| `EXPERIMENT_PROTOCOL.md` | `??` | live root documentation or repo policy file | keep as versioned project metadata and include in the next intentional commit |
| `LICENSE` | `??` | live root documentation or repo policy file | keep as versioned project metadata and include in the next intentional commit |
| `MASTER_PLAN.md` | ` M` | live root documentation or repo policy file | keep as versioned project metadata and include in the next intentional commit |
| `README.md` | `??` | live root documentation or repo policy file | keep as versioned project metadata and include in the next intentional commit |
| `RELEASE_CHECKLIST.md` | `??` | live root documentation or repo policy file | keep as versioned project metadata and include in the next intentional commit |
| `ablation_ensemble_hat_vs_iid.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `analog_layers.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `device_profile_utils.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `docs/` | `??` | stable repository documentation | track under git rather than leaving docs/ untracked |
| `download_imagenet_val.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `eval_imagenet_analog.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `eval_measured_profile.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `eval_resnet18_checkpoints.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `experiment_nonideality_sweep.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `generate_final_report.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `inference_analysis_utils.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `paper/08_appendix.md` | ` M` | paper-side live source or script | keep versioned with the manuscript pipeline |
| `paper/FIGURE_PLAN.md` | ` M` | paper-side live source or script | keep versioned with the manuscript pipeline |
| `paper/generate_schematic_figures_gpt.py` | `??` | paper-side live source or script | keep versioned with the manuscript pipeline |
| `paper/latex_gpt/CITATION_BACKLOG_gpt.md` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/CITATION_MAP_gpt.md` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/README_gpt.md` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/SUBMISSION_PACKET_gpt.md` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/cover_letter.tex` | `??` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/figures/fig1_system_architecture.pdf` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/fig2_weight_mapping.pdf` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/figA.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/figB.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/figC.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/figD.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/figS1_asymmetry_concept.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/figS2_nonideality.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/figures/graphical_abstract.png` | `??` | non-derivable canonical art asset consumed by the LaTeX paper | track the final asset; do not rely on regeneration |
| `paper/latex_gpt/main.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/refs_gpt.bib` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/00_abstract.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/01_introduction.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/02_related_work.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/03_methodology.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/04_experimental_setup.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/05_results.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/06_discussion.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/07_conclusion.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/sections/08_appendix.tex` | ` M` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/supplementary.tex` | `??` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/latex_gpt/supplementary_main.tex` | `??` | canonical manuscript source or build instructions | keep versioned; stage with the paper revision set |
| `paper/plot_paper_figures.py` | ` M` | paper-side live source or script | keep versioned with the manuscript pipeline |
| `prepare_imagenet_val.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `probe_resnet_ckpts.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `proxy_sensitivity_sweep_gpt.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `report_md/_gpt/CLAUDE_DISPATCH5_CLOSEOUT_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CLAUDE_REVIEW_PACKET_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CLAUDE_TASK_gpt.md` | ` M` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260415_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260416_final_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260416_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260416_tex_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260417_fix_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260417_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260417_index_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_DISPATCH_20260417_tidy_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_PATH_GUIDE_20260416_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CODEX_TASK_COMPLETION_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CONTOUR_AUDIT_20260416_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CORRECTION_BROADCAST_20260415_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CROSSSIM_CLEAN_BASELINE_AUDIT_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/CROSSSIM_PHASE_SUMMARY_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/DOCTOR_MEASURED_PROFILE_AUDIT_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/DOCTOR_MEASURED_PROFILE_VALIDATION_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/ENSEMBLE_HAT_LITERATURE_SURVEY_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/EXTERNAL_REVIEW_FOLLOWUP_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/FIGURE_PROVENANCE_MANIFEST_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/FINAL_ALIGNMENT_CHECKLIST_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GEMINI_DISPATCH_20260414_PHASE2_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GEMINI_DISPATCH_20260416_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GEMINI_PROJECT_TRUTH_PACK_20260413_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GEMINI_REASSIGNMENT_20260415_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GM_FIX_1_LANDED_MODIFICATIONS.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GM_X47_NEW_EXPERIMENT_PROPOSALS.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GROUP_MEETING_PPT_PROMPT_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/GROUP_MEETING_PPT_PROMPT_20260417_v2.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/HIGH_VALUE_REMAINING_ACTIONS_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/KIMI_DISPATCH_20260414_PHASE2_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/KIMI_HANDOFF_TO_CLAUDE_20260414.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/LATEX_MAIN_FIGURE_REVIEW_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/LATEX_SUPPLEMENTARY_FIGURE_REVIEW_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/MAIN_SUPP_FIGURE_AUDIT_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/MASTER_DISPATCH_20260415_PHASE3_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/NC_REVIEWER_FEEDBACK_ANALYSIS_20260414.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/NL_SWEEP_LEGACY_AUDIT_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/NUMERIC_CONSISTENCY_AUDIT_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/PROJECT_MASTER_SUMMARY_FOR_AGENTS_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/RESNET18_CX3_REPORT.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/RESNET18_DIAGNOSIS_FINAL.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/RESNET18_FIX_PLAN_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/RESNET_DEBUG_FINDINGS_20260414.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/REVIEWER_ARCHIVE_MANIFEST_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/STATISTICAL_VALIDATION_SUMMARY.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/STRATEGY_RESET_20260412_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/SUBMISSION_BUNDLE_CHECKLIST_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/SUBMISSION_PREFLIGHT_20260416.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/TIDY_MANIFEST_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/TX14_TABLE2_EVIDENCE_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/adc_layerwise_nonideality_full_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/adc_layerwise_nonideality_pilot_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/adc_layerwise_nonideality_smoke_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/adc_nonideality_final.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/attention_maps_gpt.md` | ` M` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/convnext_adc_sweep_results.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/crosssim_clean_baseline.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/crosssim_comparison_results.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/crosssim_convnext_results.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/crosssim_low_noise.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/crosssim_resnet_results.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/crosssim_standard_noise.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/csv_gpt/tinyvit_results_gpt.csv` | ` M` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/doctor_measured_profile_eval.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/doctor_measured_profile_eval_standard_hat.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/doctor_temp_norm_profile_eval.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/doctor_temp_programming_profile_eval.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/doctor_temp_uniform_profile_eval.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/energy_sensitivity_analysis.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/ensemble_frequency_ablation.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/ensemble_hat_ablation_FIXED.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/ensemble_hat_data_reconciliation.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/ensemble_literature_profile_eval.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/error_analysis_results.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/framework_comparison.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/ir_drop_sensitivity_final.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/iso_accuracy_contour_data.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/iso_accuracy_contour_data.pre_codex_20260416_005459.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/iso_accuracy_contour_errors.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/json/` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/json_gpt/attention_maps_gpt.json` | ` M` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/layer_wise_nl_sensitivity_corrected.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/nl_gradient_distortion_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/nl_gradient_distortion_pilot_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/reviewer_response/` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/sobol_sensitivity.json` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/tidy_records_20260417.tsv` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/_gpt/v4_nl_interp15_results_gpt.md` | `??` | current coordination / audit / response artifact still on the active NC submission path | keep versioned; review content, then stage with the corresponding manuscript changes |
| `report_md/images/Differential Pair Asymmetry Concept (Fig S1).png` | `??` | live repository content | keep under version control |
| `report_md/images/Ensemble Hardware-Aware Training Concept (Fig S3).png` | `??` | live repository content | keep under version control |
| `report_md/images/Graphical Abstract  TOC Image.png` | `??` | live repository content | keep under version control |
| `report_md/images/Hybrid AnalogDigital Architecture (Fig 1 Enhancement).png` | `??` | live repository content | keep under version control |
| `report_md/images/Physical Non-Idealities in Memory Arrays (Fig S2).png` | `??` | live repository content | keep under version control |
| `report_md/json/resnet18_cifar10_adc_sweep.json` | `??` | live repository content | keep under version control |
| `report_md/参考文献2.md` | `??` | live repository content | keep under version control |
| `report_md/审稿人意见-4.10.md` | `??` | live repository content | keep under version control |
| `report_md/审稿人意见from_model.md` | `??` | live repository content | keep under version control |
| `report_md/审稿意见0412.md` | `??` | live repository content | keep under version control |
| `report_md/审稿意见model_0411.md` | `??` | live repository content | keep under version control |
| `run_adc_cliff_analysis.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_adc_layerwise_nonideality_gpt.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_adc_nonideality_v2.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_cifar100_fast.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_combined_nonideality.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_contour_sweep.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_convnext_adc_sweep.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_comparison_v2.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_convnext.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_final.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_quicktest.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_resnet.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_style_comparison.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_crosssim_tinyvit.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_energy_sensitivity.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_ensemble_frequency_ablation.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_ensemble_hat_ablation_FIXED.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_ensemble_hat_fixed.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_error_analysis.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_flowers102_training.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_framework_comparison.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_ir_drop_sensitivity_v3.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_layer_wise_nl_sensitivity.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_nl_gradient_distortion_gpt.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_nl_layer_sensitivity.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_nl_layer_sensitivity_fixed.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_pure_digital_adc_sweep.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_resnet18_adc_sweep.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_retention_sensitivity.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_sobol_analysis.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_spatial_ablation.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_statistical_validation.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_svhn_training.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `run_visualization_suite.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `scripts/` | `??` | live repository content | keep under version control |
| `test_additional_datasets.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `test_analog_layers.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `test_checkpoint_behavior.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `test_device_profile_utils_gpt.py` | `??` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `test_run_device_comparison.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `train_convnext.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `train_resnet18.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `train_tinyvit.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `train_tinyvit_ensemble.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |
| `visualize_attention.py` | ` M` | live code / experiment entry point / test | keep versioned and stage only when its corresponding result or bugfix is ready |

## IGNORE (91)

| Path | Git Status | Reason | Suggested action |
|:--|:--:|:--|:--|
| `.vscode/` | `??` | editor-local settings | append to .gitignore rather than track workspace-local IDE files |
| `auto_fitted_profile.json` | `??` | generated local profile fit output | ignore as machine-generated scratch JSON |
| `data/test_32x32.mat` | `??` | raw external dataset / measured data payload | leave outside git history; document provenance separately if needed |
| `data/train_32x32.mat` | `??` | raw external dataset / measured data payload | leave outside git history; document provenance separately if needed |
| `logs/_gpt/tinyvit_hybrid_dryrun_gpt.log` | ` M` | runtime log output | ignore as generated stdout/stderr artifact |
| `logs/_gpt/visualize_attention_gpt.log` | ` M` | runtime log output | ignore as generated stdout/stderr artifact |
| `outputs/` | `??` | submission/reviewer bundle output regenerated from tracked sources | ignore bundle artifacts instead of tracking archives/tarballs |
| `paper/__pycache__/plot_paper_figures.cpython-311.pyc` | ` D` | Python bytecode cache | ignore cache directories |
| `paper/__pycache__/plot_paper_figures.cpython-313.pyc` | ` D` | Python bytecode cache | ignore cache directories |
| `paper/figures/fig10_zero_shot_transferability.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig10_zero_shot_transferability.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig11_energy_breakdown.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig11_energy_breakdown.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig3_snr_curves.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig3_snr_curves.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig4_accuracy_comparison.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig4_accuracy_comparison.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig5_hat_recovery.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig5_hat_recovery.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig6_physical_compensation.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig6_physical_compensation.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig7_retention_curve.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig7_retention_curve.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig8_pareto_energy_accuracy.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig8_pareto_energy_accuracy.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig9_noise_sensitivity.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig9_noise_sensitivity.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/figA.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/figB.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/figC.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/figD.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/figS3_ensemble_hat.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/figS3_ensemble_hat.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_attention_differences.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_attention_differences.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_attention_maps.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_attention_maps.png` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_contour_map.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_contour_map.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_fresh_instance_ablation.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_fresh_instance_ablation.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_nl_gradient_distortion.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_nl_gradient_distortion.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_nl_gradient_distortion_pilot.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_proxy_sensitivity_map.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_proxy_sensitivity_map.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_sobol_sensitivity.pdf` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/figures/fig_sobol_sensitivity.png` | `??` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `paper/latex_gpt/figures/fig10_zero_shot_transferability.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig10_zero_shot_transferability.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig11_energy_breakdown.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig11_energy_breakdown.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig3_snr_curves.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig3_snr_curves.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig4_accuracy_comparison.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig4_accuracy_comparison.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig5_hat_recovery.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig5_hat_recovery.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig6_physical_compensation.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig6_physical_compensation.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig7_retention_curve.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig7_retention_curve.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig8_pareto_energy_accuracy.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig8_pareto_energy_accuracy.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig9_noise_sensitivity.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig9_noise_sensitivity.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/figS3_ensemble_hat.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/figS3_ensemble_hat.png` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_attention_differences.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_attention_differences.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_attention_maps.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_attention_maps.png` | ` M` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_contour_map.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_contour_map.png` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_fresh_instance_ablation.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_fresh_instance_ablation.png` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_nl_gradient_distortion.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_nl_gradient_distortion.png` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_proxy_sensitivity_map.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_proxy_sensitivity_map.png` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_sobol_sensitivity.pdf` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/figures/fig_sobol_sensitivity.png` | `??` | plot-generated figure export duplicated from reproducible scripts | ignore the generated export or regenerate on demand |
| `paper/latex_gpt/main.pdf` | ` M` | derived figure/PDF build artifact | ignore regenerated build outputs |
| `report_md/41467_2025_66891_MOESM1_ESM.pdf` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `report_md/How to submit _ Nature Communications.pdf` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `report_md/Organic_Optoelectronic_Task_Simulation.pdf` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `report_md/Organic_Optoelectronic_Task_Simulation_(2).pptx` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `report_md/WQY-基于缺陷工程的易失性和非易失性 用于高效分类的光储备池计算-第8稿.docx` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `report_md/d5mh00948k.pdf` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `report_md/记忆类型可调的光电突触和存储器用于储备池计算-第8稿(1).pptx` | `??` | external reference / presentation asset, not source-of-truth code or manuscript text | ignore or keep outside git unless explicitly curating a docs bundle |
| `数据_博士/` | `??` | raw external dataset / measured data payload | leave outside git history; document provenance separately if needed |

## ARCHIVE (93)

| Path | Git Status | Reason | Suggested action |
|:--|:--:|:--|:--|
| `_archive/paper-drafts/BANANA_JOURNAL_SCHEMATIC_PROMPTS_20260408_gpt.md` | `??` | already retired under _archive/ | keep archived and stage as archival move only if Claude wants that history recorded |
| `_archive/paper-drafts/NANOBANANA_SCHEMATIC_PROMPTS_gpt.md` | `??` | already retired under _archive/ | keep archived and stage as archival move only if Claude wants that history recorded |
| `_archive/paper-drafts/PERPLEXITY_TARGETED_CITATION_PROMPTS_gpt.md` | `??` | already retired under _archive/ | keep archived and stage as archival move only if Claude wants that history recorded |
| `logs/model_profiling_20260403_092017.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/physical_noise_pipeline_20260403_093730.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/physical_noise_pipeline_20260403_093857.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/plot_resnet18_20260403_201558.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/run_a23_20260403_203036.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/test_analog_layers_20260403_092209.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/test_analog_layers_20260403_093327.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/test_analog_layers_20260403_093553.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/test_analog_layers_20260403_095221.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/train_convnext_full_20260403_202645.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `logs/train_resnet18_full_20260403_095144.log` | ` D` | historical log already retired from the live logs tree | treat as archival move, not as an active deletion |
| `paper/01_introduction.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/02_related_work.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/03_methodology.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/04_experimental_setup.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/05_results.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/06_discussion.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/07_conclusion.md` | ` M` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `paper/latex_gpt/figures/fig1_enhanced.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig1_system_architecture_banana.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig1_system_architecture_banana_clean.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig1_system_architecture_banana_crop.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig1_system_architecture_banana_final.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig2_weight_mapping_banana.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig2_weight_mapping_banana_clean.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig2_weight_mapping_banana_clean2.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig2_weight_mapping_banana_crop.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig2_weight_mapping_banana_final.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig_bottleneck_hierarchy_banana.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/latex_gpt/figures/fig_bridge_materials_to_system_banana.png` | `??` | intermediate figure-art variant (_banana/_clean/_crop/enhanced) | archive under a figure-drafts subtree; keep only the canonical final asset live |
| `paper/仿真.tex` | ` D` | draft-superseded paper note or prompt file | move to _archive/paper-drafts once live callers are gone; do not keep editing it as if live |
| `patch_fig11.py` | ` D` | one-shot root helper superseded by archived/scripted workflows | move/keep under _archive/scripts-oneshot rather than at repo root |
| `port_05.py` | ` D` | one-shot root helper superseded by archived/scripted workflows | move/keep under _archive/scripts-oneshot rather than at repo root |
| `report_md/_gpt/CLAUDE_REPLAY_POINTERS_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/EXTERNAL_REVIEW_DETAILED_BROADCAST_20260408_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/GEMINI_HANDOFF_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/GEMINI_TAKEOVER_BRIEF_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/Gemini_REPLY_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/LLM_CHANGELOG_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/LLM_HANDOFF_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/RUNTIME_MANIFEST_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/_codex_verify_v4_retention_probe_cuda_20260407.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/_probe_convnext_cifar100_c1_resume.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/_tmp_retention_probe_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/c4_nl_moderate_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/c4_proportional_hat_train_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/codex_a3_plan_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_c1_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_c9_retention_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_cifar100_c134_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_experiment_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_flowers102_c134_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_full_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/convnext_resume_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/device_comparison_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/layer_sensitivity_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/literature_fake_profile_workflow_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/literature_profile_zhang2025_provenance_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/measured_device_data_bridge_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/noise_sweep_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_cifar100_v134_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_flowers102_v134_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_noise_diagnostic_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_retention_diagnostic_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_v1_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_v2v7_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_v4_retention_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/tinyvit_v7_retention_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v2_under_noise_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_ensemble_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_nl2_hat_eval_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_nl2_hat_train_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_nl_moderate_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_nl_severe_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_proportional_hat_eval_proportional_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_proportional_hat_eval_uniform_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_proportional_hat_train_results_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `report_md/_gpt/v4_proportional_noise_report_gpt.md` | ` D` | historical coordination note already retired from the live _gpt layer | treat as archival move to _archive/coordination |
| `run_exp_b.sh` | `??` | one-shot shell queue/launcher outside the stable scripts tree | archive under _archive/scripts-oneshot or scripts/archive_* |
| `run_hardening_experiments.sh` | `??` | one-shot shell queue/launcher outside the stable scripts tree | archive under _archive/scripts-oneshot or scripts/archive_* |
| `run_imagenet_eval.sh` | `??` | one-shot shell queue/launcher outside the stable scripts tree | archive under _archive/scripts-oneshot or scripts/archive_* |
| `run_nl_landscape_scan.sh` | `??` | one-shot shell queue/launcher outside the stable scripts tree | archive under _archive/scripts-oneshot or scripts/archive_* |
| `run_resnet18_cifar100.sh` | `??` | one-shot shell queue/launcher outside the stable scripts tree | archive under _archive/scripts-oneshot or scripts/archive_* |
| `run_task24_tinyvit_nl15_interp_gpt.sh` | `??` | one-shot shell queue/launcher outside the stable scripts tree | archive under _archive/scripts-oneshot or scripts/archive_* |
| `sync_zh.py` | ` D` | one-shot root helper superseded by archived/scripted workflows | move/keep under _archive/scripts-oneshot rather than at repo root |
| `upgrade_plots.py` | ` D` | one-shot root helper superseded by archived/scripted workflows | move/keep under _archive/scripts-oneshot rather than at repo root |

