# JSON Data Consistency Audit Report
**Date:** 2026-04-19
**Scope:** All JSON experiment results under `compute_vit/report_md/` and related directories
**Auditor:** Automated consistency check script

---

## 1. Executive Summary

| Metric | Value |
|:--|:--|
| **Total JSON files scanned** | 104 |
| **Primary working set** | 96 in `json_gpt/` + 25 in `_gpt/` + 7 in `json/` |
| **Total size** | ~969.5 KB |
| **Date range** | 2026-04-03 to 2026-04-18 |
| **Files older than 2026-04-15** | 57 (55% of primary set) |
| **Critical inconsistencies found** | 7 |
| **Missing / empty files flagged** | 3 |
| **Bit-identical duplicates with release_artifacts** | 72 |

**Overall assessment:** The JSON data set contains several high-severity inconsistencies where the same experiment or checkpoint is reported with contradictory accuracy values across different files. Some evaluation files return chance-level accuracy (~10%) for configurations that should yield ~90%, suggesting configuration or checkpoint mismatches. A number of stale files from earlier experimental iterations remain in the working directories and risk being cited by mistake.

---

## 2. File Inventory

### 2.1 Primary Working Directories

| Directory | File Count | Total Size | Date Range |
|:--|:--|:--|:--|
| `report_md/_gpt/json_gpt/` | 96 | ~850 KB | Apr 3 – Apr 18 |
| `report_md/_gpt/` (root JSONs) | 25 | ~95 KB | Apr 15 – Apr 18 |
| `report_md/json/` | 7 | ~200 KB | Apr 3 – Apr 18 |

### 2.2 Archive / Mirror Locations (Excluded from schema checks but noted)

| Directory | File Count | Notes |
|:--|:--|:--|
| `_archive/old-experiment-json/` | 20 | Superseded experiments; should not be cited |
| `release_artifacts/source_data_v1/` | 72 | Bit-identical mirrors of `json_gpt/` files |
| `outputs/reviewer_archive_20260417/` | 25 | Snapshot from earlier review round |
| `outputs/reviewer_archive_20260419/` | 72 | Snapshot including full repo mirror |

### 2.3 Empty or Trivial Files

| File | Size | Issue |
|:--|:--|:--|
| `report_md/_gpt/iso_accuracy_contour_errors.json` | 2 bytes (`[]`) | Completely empty; supposed to log contour-generation errors |

---

## 3. Schema Analysis by Experiment Category

### 3.1 TinyViT Training Results (Canonical / Ensemble / NL)
**Representative files:** `tinyvit_v2v7_results_gpt.json`, `v4_ensemble_results_gpt.json`, `v4_nl2_hat_train_results_gpt.json`, `v4_proportional_hat_train_results_gpt.json`

**Consistent top-level schema:** `list[dict]` with these keys:
```
mode, experiment, experiment_name, dataset, num_classes, use_hybrid,
noise_enabled, sigma_c2c, sigma_d2d, hat_training, use_physical_frontend,
retention_enabled, inference_time, epochs, batch_size, lr, weight_decay,
best_test_acc, best_epoch, final_train_loss, final_train_acc,
final_test_loss, final_test_acc, checkpoint_path
```

**Status:** ✅ Consistent schema across all 15+ training result files.
**Minor issue:** Some training-result JSONs (e.g. `smoke_v4_ensemble.json`) have `epochs=1` and should not be used for locked numbers.

---

### 3.2 ConvNeXt Training Results
**Representative files:** `convnext_c1_results_gpt.json`, `convnext_full_results_gpt.json`, `convnext_resume_results_gpt.json`, `convnext_cifar100_c134_results_gpt.json`

**Consistent top-level schema:** `dict` with keys:
```
results, histories, retention, retention_metadata
```

**Status:** ✅ Consistent within the `_gpt/json_gpt/` family.
**⚠️ Exception:** `report_md/json/convnext_results.json` (older, Apr 3) uses the same schema but contains stale/wrong data (C1 baseline only 47.89% after 2 epochs).

---

### 3.3 Eval / Sweep Results (Noise, ADC, Retention)
**Representative files:** `noise_sweep_results_gpt.json`, `v2_under_noise_results_gpt.json`, `tinyvit_v4_retention_results_gpt.json`, `adc_layerwise_nonideality_full_gpt.json`

**Consistent top-level schema:** `dict` with keys:
```
results (list[dict]), metadata (dict)
```
Each result item contains:
```
model, experiment, checkpoint_path, checkpoint_epoch, checkpoint_best_acc,
sweep_type, sigma_c2c, sigma_d2d, eval_runs,
test_loss_mean, test_acc_mean, test_acc_min, test_acc_max, test_acc_std
```

**Status:** ✅ Strongly consistent. All eval files include `test_acc_std` for error bars.

---

### 3.4 CrossSim Comparison
**Files:** `crosssim_clean_baseline.json`, `crosssim_low_noise.json`, `crosssim_standard_noise.json`, `crosssim_comparison_results.json`, `crosssim_convnext_results.json`

**Consistent top-level schema:** `dict` with keys:
```
experiment, timestamp, checkpoint, dataset, adc_bits, weight_bits,
sigma_c2c, sigma_d2d, crosssim_alpha_noise, crosssim_alpha_error,
max_samples, our_framework, crosssim, notes
```

**Status:** ✅ Schema consistent.
**⚠️ Data concern:** `crosssim_comparison_results.json` reports `our_framework.mean = 54.69%` for ConvNeXt-Tiny on CIFAR-10 — far below the expected ~90% for this model. The low value may reflect a subset-evaluation artifact (`max_samples=64`) but is not clearly documented as such.

---

### 3.5 Device / Measured Profile Evaluations
**Files:** `doctor_measured_profile_eval.json`, `doctor_measured_profile_eval_standard_hat.json`, `doctor_temp_norm_profile_eval.json`, `doctor_temp_programming_profile_eval.json`, `doctor_temp_uniform_profile_eval.json`, `ensemble_literature_profile_eval.json`, `device_comparison_results_gpt.json`

**Consistent top-level schema:** `dict` with keys:
```
generated_at, device, profile_json, results (list[dict])
```
Each result item contains device parameters + `test_acc_mean`, `test_acc_std`, etc.

**Status:** ⚠️ Schema consistent, but **data values are catastrophically inconsistent** (see Section 4).

---

### 3.6 Framework Comparison
**File:** `framework_comparison.json`

**Schema:** `dict` with `timestamp`, `device`, `comparisons` (list).
**Status:** ✅ Well-structured. References `p13_aihwkit_shared_regime_result.json` as source.

---

### 3.7 Sensitivity & Contour Data
**Files:** `iso_accuracy_contour_data.json`, `sobol_sensitivity.json`, `zhang_sensitivity_sweep.json`, `ir_drop_sensitivity_final.json`, `energy_sensitivity_analysis.json`

**Status:** ✅ All contain `mean` and `std` where appropriate. `iso_accuracy_contour_data.json` has 63 entries, zero missing `std` fields.

---

## 4. Cross-File Consistency Issues

### 🔴 CRITICAL-1: ConvNeXt C1 Baseline — Two Conflicting Values

| File | C1 `best_test_acc` | Epochs | Status |
|:--|:--|:--|:--|
| `report_md/json/convnext_results.json` | **47.89%** | 2 | **Stale / aborted run** |
| `report_md/_gpt/json_gpt/convnext_c1_results_gpt.json` | **90.74%** | 200 | ✅ Corrected run |
| `report_md/_gpt/json_gpt/convnext_full_results_gpt.json` | **90.74%** | 200 | ✅ Matches above |

**Risk:** The old `convnext_results.json` (Apr 3, 200-line file in `report_md/json/`) is still present and could be cited by legacy scripts or LaTeX compilation. It was produced from an aborted 2-epoch run.

**Recommendation:** Move `report_md/json/convnext_results.json` to `_archive/` or delete it. Update any LaTeX source-data references to point to `convnext_c1_results_gpt.json` or `convnext_full_results_gpt.json`.

---

### 🔴 CRITICAL-2: V4 Canonical Accuracy — Three Slightly Different Values

The canonical V4 (standard noise + HAT, CIFAR-10) checkpoint `V4_hybrid_standard_noise_hat_best.pt` is reported with:

| File | Reported Accuracy | Context |
|:--|:--|:--|
| `_codex_verify_v4_canonical_eval_cuda_20260407.json` | `test_acc_mean = 91.69%` | Direct eval run (10 MC runs) |
| `_codex_verify_v4_canonical_eval_cuda_20260407.json` | `checkpoint_best_acc = 91.94%` | Checkpoint metadata |
| `framework_comparison.json` (ours, canonical) | `accuracy = 91.65%` | Framework comparison table |
| `noise_sweep_results_gpt.json` (native ADC) | `test_acc_mean = 91.71%` | Noise sweep baseline |
| `ir_drop_sensitivity_final.json` (0% IR drop) | `mean = 91.67%` | IR-drop sensitivity baseline |

These values differ by up to **0.29 pp** (91.65% vs 91.94%). The differences are small enough to be explained by stochastic evaluation variance, but the manuscript should **lock one canonical value** and reference it consistently.

**Recommendation:** Designate `91.69%` (mean of 10 eval runs, Apr 7) or `91.94%` (training best checkpoint) as the locked canonical number. Update `framework_comparison.json` to match.

---

### 🔴 CRITICAL-3: Two Different V4 Checkpoints Cited Interchangeably

There are **two physically different checkpoints** both named `V4_hybrid_standard_noise_hat_best.pt`:

| Checkpoint Path | `checkpoint_best_acc` | Used in |
|:--|:--|:--|
| `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | **91.94%** | Most eval files, doctor temp profiles, device comparison |
| `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | **91.13%** | Ensemble eval, literature profile eval, doctor measured profile eval |

**Consequence:** Files using the ensemble checkpoint (91.13%) report lower baseline accuracy, which propagates into downstream comparisons.

**Affected files:**
- `v4_ensemble_results_gpt.json` — `best_test_acc = 91.13%`
- `ensemble_literature_profile_eval.json` — `checkpoint_best_acc = 91.13%`
- `doctor_measured_profile_eval.json` — `checkpoint_best_acc = 91.13%`
- `ensemble_hat_ablation_FIXED.json` — references ensemble checkpoint

**Recommendation:** Clarify in the manuscript which checkpoint is the canonical one. If the ensemble checkpoint is a separate re-training, rename it (e.g., `V4_ensemble_retrain_best.pt`) to avoid confusion.

---

### 🔴 CRITICAL-4: Device Comparison & Doctor Temp Profiles — All at Chance Level (~10%)

| File | Reported Accuracy | Expected | Status |
|:--|:--|:--|:--|
| `device_comparison_results_gpt.json` (all devices) | **10.0%** | ~90% | ❌ Broken |
| `doctor_temp_norm_profile_eval.json` (all variants) | **~10.2%** | ~90% | ❌ Broken |
| `doctor_temp_programming_profile_eval.json` (all variants) | **~10.2%** | ~90% | ❌ Broken |
| `doctor_temp_uniform_profile_eval.json` (all variants) | **~10.2%** | ~90% | ❌ Broken |
| `doctor_measured_profile_eval_standard_hat.json` (RC-16) | **10.2%** | ~90% | ❌ Broken |

All of these files use `checkpoints/V4_hybrid_standard_noise_hat_best.pt` (`checkpoint_best_acc = 91.94`) but evaluation yields chance-level accuracy. This strongly suggests a **profile-to-checkpoint mismatch** or a bug in the evaluation script used for these runs (e.g., wrong `num_classes`, missing normalization, or ADC frontend not applied correctly).

**Exception:** `doctor_measured_profile_eval.json` (non-standard-hat version) uses the ensemble checkpoint and achieves **89.8%** for RC-16 — this appears to be the only correctly functioning doctor measured profile eval.

**Recommendation:** Re-run the broken evaluations. Do not include the 10.2% values in any manuscript figure or table until the root cause is fixed.

---

### 🟡 MODERATE-1: Fresh-Instance Eval — V4_Standard at 10%

`fresh_instance_eval.json` reports:
- `V4_Standard.mean = 10.0%` (chance level)
- `V4_Ensemble.mean = 86.37%` (plausible)

The standard HAT result at 10% is inconsistent with every other canonical eval (~91%). This may be a config error in the fresh-instance protocol.

**Recommendation:** Re-run or debug the fresh-instance standard-HAT evaluation. If the 10% value is correct under the fresh-instance protocol, document the protocol difference explicitly in the figure caption.

---

### 🟡 MODERATE-2: Ensemble HAT Values Diverge

| File | Standard HAT | Ensemble HAT | IID Noise | Notes |
|:--|:--|:--|:--|:--|
| `ensemble_hat_ablation_FIXED.json` | 90.77% | 86.57% | 87.39% | Uses ensemble checkpoint |
| `ensemble_frequency_ablation.json` (epoch mode) | — | 88.41% | — | Different experiment |
| `fresh_instance_eval.json` | 10.0% | 86.37% | — | Fresh-instance protocol |
| `doctor_measured_profile_eval.json` | 89.8% (RC-16) | — | — | Uses ensemble checkpoint |

The ensemble HAT value varies from **86.37%** to **88.41%** depending on the experiment. The standard HAT varies from **10.0%** to **90.77%**. This makes it impossible to state a single locked number without specifying the exact protocol.

**Recommendation:** In the manuscript, always pair the accuracy number with its protocol tag (e.g., "Ensemble HAT (per-epoch resampling): 88.41%" vs "Ensemble HAT (FIXED ablation): 86.57%").

---

### 🟡 MODERATE-3: CrossSim Comparison — Very Low ConvNeXt Accuracy

`crosssim_comparison_results.json`:
- Our framework: **54.69%**
- CrossSim: **4.69%**

Both values are far below the expected ConvNeXt-Tiny CIFAR-10 baseline (~90%). The JSON notes `max_samples=64`, suggesting this may be a tiny subset evaluation. If so, the subset size must be stated in any manuscript table; otherwise readers will assume the full test set.

**Recommendation:** Add an explicit `note` field stating whether this is subset or full-set evaluation. Re-run on the full test set if the manuscript claims full-set numbers.

---

### 🟡 MODERATE-4: NL Mitigation Summary — Missing `std` for Train Results

`nl_mitigation_summary_20260418.json`:
- Baseline eval: has `mean_eval_acc = 27.716%` and `std_eval_acc = 0.822%` ✅
- MLP compensation: has `best_test_acc = 87.79%` but `mean_eval_acc = null`, `std_eval_acc = null` ❌
- QKV compensation: has `best_test_acc = 18.72%` but `mean_eval_acc = null`, `std_eval_acc = null` ❌
- All-linear compensation: has `best_test_acc = 87.49%` but `mean_eval_acc = null`, `std_eval_acc = null` ❌

If the manuscript claims error bars for these compensation experiments, the evaluation JSONs must be run with multiple seeds/runs.

**Recommendation:** Run multi-seed evals for the compensation lanes and populate `mean_eval_acc` / `std_eval_acc`.

---

## 5. Missing Fields

| File | Expected Field | Status | Impact |
|:--|:--|:--|:--|
| `iso_accuracy_contour_errors.json` | Any content | Completely empty (`[]`) | Low — error log only |
| `layer_wise_nl_sensitivity_corrected.json` | `std` per layer | Absent | Medium — error bars claimed in figure? |
| `nl_mitigation_summary_20260418.json` (train rows) | `mean_eval_acc`, `std_eval_acc` | `null` | High — cannot report error bars |
| `convnext_results.json` | Proper C1 history | Only 2 epochs recorded | High — stale file |
| `smoke_v4_ensemble.json` | `epochs` > 1 | `epochs = 1` | Low — smoke test, should be excluded |
| `zhang_sensitivity_sweep.json` | Top-level `std` | Not present | Low — raw array data available |

---

## 6. Data Freshness

### 6.1 Files from Current Round (Apr 15–18, 2026) — Likely Valid

| File | Date | Notes |
|:--|:--|:--|
| `nl_mitigation_summary_20260418.json` | Apr 18 | Current NL mitigation summary |
| `fresh_instance_cadence_control.json` | Apr 18 | Fresh-instance cadence scan |
| `v4_nl2_*_linear_comp_train_results_gpt.json` | Apr 18 | NL compensation training runs |
| `learnable_gamma_20260418_110011_g2.0_s42.json` | Apr 18 | γ scan |
| `convnext_adc_sweep_results.json` | Apr 15 | ADC sweep |
| `ensemble_hat_ablation_FIXED.json` | Apr 15 | Ensemble ablation (locked) |
| `framework_comparison.json` | Apr 15 | Framework comparison |
| `iso_accuracy_contour_data.json` | Apr 16 | Contour data |
| `doctor_measured_profile_eval*.json` | Apr 16 | Doctor measured profiles |
| `ensemble_literature_profile_eval.json` | Apr 16 | Literature profile eval |
| `nl_sweep_consolidated_20260417.json` | Apr 17 | NL sweep consolidation |
| `adc_layerwise_nonideality_*_gpt.json` | Apr 17 | ADC nonideality tests |
| `nl_gradient_distortion_gpt.json` | Apr 17 | Gradient distortion |

### 6.2 Stale Files from Earlier Iterations — Review for Deletion

| File | Date | Issue |
|:--|:--|:--|
| `convnext_results.json` (`report_md/json/`) | Apr 3 | Stale C1 baseline (47.89%) |
| `resnet18_results.json` (`report_md/json/`) | Apr 3 | Very old; may be superseded |
| `physical_noise_sweep.json` | Apr 3 | Unclear if still referenced |
| `a23_experiment_results.json` | Apr 3 | γ scan; check if replaced by newer file |
| `smoke_v4_ensemble.json` | Apr 7 | 1-epoch smoke test |
| `_tmp_retention_probe_gpt.json` | Apr 6 | Temporary probe file |
| `_probe_convnext_cifar100_c1_resume.json` | Apr 5 | Probe / resume artifact |
| `iso_accuracy_contour_data.pre_codex_20260416_005459.json` | Apr 16 | Pre-Codex backup; superseded by final version |
| `_codex_auto_fitter_demo_20260408.json` | Apr 8 | Demo file; likely not for manuscript |
| `_codex_auto_fitter_demo_fixed_20260408.json` | Apr 8 | Demo file; likely not for manuscript |
| `convnext_results_gpt.json` | Apr 4 | Only contains C2/C3; superseded by `convnext_full_results_gpt.json` |

---

## 7. Recommendations for Data Cleanup

### Immediate Actions (Before Submission)

1. **Remove or archive stale files**
   - Move `report_md/json/convnext_results.json` to `_archive/` — it contains the wrong C1 baseline.
   - Delete `iso_accuracy_contour_errors.json` or populate it with actual error data.
   - Delete `smoke_v4_ensemble.json`, `_tmp_retention_probe_gpt.json`, and `_probe_convnext_cifar100_c1_resume.json` from the working set.
   - Delete `iso_accuracy_contour_data.pre_codex_20260416_005459.json` (backup no longer needed).

2. **Lock the V4 canonical number**
   - Choose one value: either `91.69%` (eval mean) or `91.94%` (training best).
   - Update `framework_comparison.json` to match the locked value.
   - Add a `canonical_note` field to the source JSON explaining which number is the locked one and why.

3. **Clarify the two checkpoints**
   - Rename `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` to something distinct (e.g., `V4_ensemble_retrain_best.pt`) to prevent accidental interchange.
   - Audit all JSONs referencing `checkpoint_best_acc` and tag which checkpoint they actually used.

4. **Fix or exclude broken doctor profile evals**
   - All doctor temp profile evals returning ~10.2% need to be re-run or excluded from figures.
   - `device_comparison_results_gpt.json` (all 10.0%) must be re-run or removed.

5. **Fix fresh_instance_eval.json standard HAT**
   - Debug why V4_Standard = 10.0%. If it cannot be fixed, exclude it from Fig 4 / S4.

6. **Add missing error-bar data**
   - Run multi-seed evals for NL mitigation compensation lanes and update `nl_mitigation_summary_20260418.json`.
   - If `layer_wise_nl_sensitivity_corrected.json` is used for a figure with error bars, add `std` per layer.

7. **Deduplicate release artifacts**
   - 72 files in `release_artifacts/source_data_v1/` are bit-identical to `json_gpt/`. Verify that the release artifact directory is generated by a copy script rather than maintained manually, to avoid drift.

### Medium-Priority

8. **Document subset evaluations**
   - `crosssim_comparison_results.json` and any other file using `max_samples` or subset evaluation should have an explicit `subset_size` or `note` field.

9. **Standardize file naming**
   - Some files use `_gpt` suffix, others don't. Consider renaming all primary result files to a consistent convention (e.g., `YYYY-MM-DD_experiment_tag.json`).

10. **Add `best_epoch` to all training summaries**
    - Some training JSONs (e.g., `c4_nl_moderate_results_gpt.json`) include `best_epoch` inside the `results` list; others store it only in `histories`. Standardize.

---

## 8. Locked-Number Cross-Reference (Quick Lookup)

| Claimed Number | Source File(s) | Consistency |
|:--|:--|:--|
| V2 canonical = 97.38–97.39% | `tinyvit_v2v7_results_gpt.json`, `v2_under_noise_results_gpt.json` | ✅ Consistent |
| V4 canonical = 91.65–91.94% | `framework_comparison.json`, `_codex_verify_v4_canonical_eval_cuda_20260407.json`, `noise_sweep_results_gpt.json` | ⚠️ 0.29 pp spread |
| V4 ensemble = 91.13% | `v4_ensemble_results_gpt.json` | ✅ Internally consistent |
| Ensemble HAT = 86.37–88.41% | `ensemble_hat_ablation_FIXED.json`, `ensemble_frequency_ablation.json`, `fresh_instance_eval.json` | ⚠️ Protocol-dependent |
| Standard HAT (measured) = 89.8% | `doctor_measured_profile_eval.json` | ✅ Single source |
| Standard HAT (measured, standard checkpoint) = 10.2% | `doctor_measured_profile_eval_standard_hat.json` | ❌ Broken — do not use |
| C1 FP32 = 90.74% | `convnext_c1_results_gpt.json`, `convnext_full_results_gpt.json` | ✅ Consistent |
| C1 FP32 = 47.89% | `report_md/json/convnext_results.json` | ❌ Stale — do not use |
| R1 FP32 = 95.46% | `resnet18_results.json` | ✅ Single source |
| IR drop 0% = 91.67% | `ir_drop_sensitivity_final.json` | ✅ Consistent with V4 canonical |
| Error analysis overall = 87.45% | `error_analysis_results.json` | ✅ Single source |
| Literature profile eval = 89.7% | `ensemble_literature_profile_eval.json` | ✅ Single source |

---

*Report generated by automated JSON consistency audit.*
