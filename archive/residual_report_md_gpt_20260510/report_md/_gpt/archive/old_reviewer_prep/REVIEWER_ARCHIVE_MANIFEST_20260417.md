# Reviewer Archive Manifest — 2026-04-17

## Purpose

This manifest defines what should be included in the reviewer-accessible archive promised in the current `Data Availability` and `Code Availability` statements.

It is intentionally practical:

- `ready now` means the file already exists and can be packaged immediately
- `needs assembly` means the source files exist but have not yet been collated into a clean reviewer archive

## Recommended Archive Layout

```text
reviewer_archive/
  manuscript/
  response/
  source_data/
  code_snapshot/
  audit/
```

## 1. Manuscript

### Ready now

- [main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf)
- [supplementary_main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf)
- [cover_letter.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.pdf)

## 2. Response

### Ready now

- [REVIEWER_RESPONSE_DRAFT_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md)
- [TX14_TABLE2_RESPONSE_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md)

### Optional supporting response-analysis files

- [POINT_BY_POINT_RESPONSE.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/reviewer_response/POINT_BY_POINT_RESPONSE.md)
- [MINOR_REVISION_RESPONSE.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/reviewer_response/MINOR_REVISION_RESPONSE.md)

## 3. Source Data

### A. Locked manuscript-facing reference files

#### Ready now

- [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md)
- [FIGURE_CAPTION_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/FIGURE_CAPTION_LOCK_gpt.md)
- [SUBMISSION_PACKET_gpt.md](/home/qiaosir/projects/compute_vit/paper/latex_gpt/SUBMISSION_PACKET_gpt.md)

### B. Core machine-readable result artifacts supporting main claims

#### Ready now

- [tinyvit_v1_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json)
- [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json)
- [v2_under_noise_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/v2_under_noise_results_gpt.json)
- [\_codex\_verify\_v4\_canonical\_eval\_cuda\_20260407.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.json)
- [convnext_results.json](/home/qiaosir/projects/compute_vit/report_md/json/convnext_results.json)
- [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json)

### C. Figure-supporting source artifacts

#### Ready now

- [iso_accuracy_contour_data.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/iso_accuracy_contour_data.json)
- [sobol_sensitivity.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/sobol_sensitivity.json)
- [adc_layerwise_nonideality_full_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/adc_layerwise_nonideality_full_gpt.json)
- [adc_layerwise_nonideality_full_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/adc_layerwise_nonideality_full_gpt.md)
- [nl_gradient_distortion_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/nl_gradient_distortion_gpt.json)
- [nl_gradient_distortion_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/nl_gradient_distortion_gpt.md)
- [fig_nl_gradient_distortion.png](/home/qiaosir/projects/compute_vit/paper/figures/fig_nl_gradient_distortion.png)
- [fig_nl_gradient_distortion.pdf](/home/qiaosir/projects/compute_vit/paper/figures/fig_nl_gradient_distortion.pdf)
- [v4_nl_interp15_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/v4_nl_interp15_results_gpt.json)
- [v4_nl_interp15_results_gpt.csv](/home/qiaosir/projects/compute_vit/report_md/_gpt/csv_gpt/v4_nl_interp15_results_gpt.csv)
- [v4_nl_interp15_results_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/v4_nl_interp15_results_gpt.md)
- [convnext_adc_sweep_results.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/convnext_adc_sweep_results.json)
- [crosssim_clean_baseline.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_clean_baseline.json)
- [crosssim_low_noise.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_low_noise.json)
- [crosssim_standard_noise.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_standard_noise.json)
- [ensemble_literature_profile_eval.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/ensemble_literature_profile_eval.json)

### D. Profile-substitution / measured-profile artifacts

#### Ready now

- [doctor_measured_profile_eval.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/doctor_measured_profile_eval.json)
- [doctor_measured_profile_eval_standard_hat.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/doctor_measured_profile_eval_standard_hat.json)
- [doctor_measured_profile_summary.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/doctor_measured_profile_summary.json)
- [doctor_measured_profiles.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/doctor_measured_profiles.json)

## 4. Code Snapshot

### Recommended snapshot root

- `/home/qiaosir/projects/compute_vit/`

### Recommended include set

#### Core training / evaluation

- [train_tinyvit.py](/home/qiaosir/projects/compute_vit/train_tinyvit.py)
- [train_tinyvit_ensemble.py](/home/qiaosir/projects/compute_vit/train_tinyvit_ensemble.py)
- [train_convnext.py](/home/qiaosir/projects/compute_vit/train_convnext.py)
- [train_resnet18.py](/home/qiaosir/projects/compute_vit/train_resnet18.py)
- [eval_measured_profile.py](/home/qiaosir/projects/compute_vit/eval_measured_profile.py)
- [eval_imagenet_analog.py](/home/qiaosir/projects/compute_vit/eval_imagenet_analog.py)

#### Core simulation utilities

- [analog_layers.py](/home/qiaosir/projects/compute_vit/analog_layers.py)
- [device_profile_utils.py](/home/qiaosir/projects/compute_vit/device_profile_utils.py)
- [inference_analysis_utils.py](/home/qiaosir/projects/compute_vit/inference_analysis_utils.py)
- [run_nl_gradient_distortion_gpt.py](/home/qiaosir/projects/compute_vit/run_nl_gradient_distortion_gpt.py)

#### Figure generation / analysis

- [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py)
- [visualize_attention.py](/home/qiaosir/projects/compute_vit/visualize_attention.py)

### Exclude from clean reviewer-code zip unless explicitly needed

- `__pycache__/`
- local logs unrelated to the submission package
- large checkpoints if the portal size budget is small

## 5. Audit / Consistency Memos

### Ready now

- [FINAL_ALIGNMENT_CHECKLIST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/FINAL_ALIGNMENT_CHECKLIST_20260417.md)
- [EXTERNAL_REVIEW_SYNTHESIS_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_20260417.md)

## Assembly Status

### Ready now

- manuscript PDFs
- cover letter PDF
- response draft
- main machine-readable result JSONs
- core audit memos
- canonical lightweight bundle directory:
  - [outputs/submission_bundle_20260417](/home/qiaosir/projects/compute_vit/outputs/submission_bundle_20260417)
- frozen copy-based reviewer archive:
  - [outputs/reviewer_archive_20260417](/home/qiaosir/projects/compute_vit/outputs/reviewer_archive_20260417)

### Needs assembly

1. An optional zip/tar export of `outputs/reviewer_archive_20260417/` if the submission portal does not accept directory uploads
2. Optional checkpoint subset if reviewers are expected to rerun selected evaluations locally

## Bottom Line

The evidence files now exist in both manifest form and as a frozen reviewer-accessible archive. The remaining work is limited to optional packaging format conversion (for example, zip/tar) and any later checkpoint subset the portal may require.
