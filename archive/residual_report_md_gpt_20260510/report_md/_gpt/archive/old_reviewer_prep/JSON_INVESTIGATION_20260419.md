# JSON Data Investigation Report
**Date:** 2026-04-19
**Scope:** Critical inconsistencies flagged in `JSON_CONSISTENCY_20260419.md`
**Investigator:** Automated deep-dive

---

## Executive Summary

| Issue | Severity | Verdict |
|:--|:--|:--|
| V4 canonical accuracy spread | Low | **Not a real inconsistency** — explained by eval stochasticity |
| Ensemble HAT divergence | Medium | **Protocol-dependent, not contradictory** — 86.37% is the locked eval number |
| Device comparison / doctor temp profiles ~10% | Critical | **Broken / stale** — discard all 10% values |
| CrossSim ConvNeXt 54.69% | Medium | **Subset artifact** — discard; use 81.63% (1000-sample) or re-run on full set |

---

## 1. V4 Canonical Accuracy Spread (91.65%–91.94%)

### 1.1 Files and Values Found

| File | Field | Value | Context |
|:--|:--|:--|:--|
| `_codex_verify_v4_canonical_eval_cuda_20260407.json` | `test_acc_mean` | **91.69%** | 10 MC eval runs, direct canonical verification |
| `_codex_verify_v4_canonical_eval_cuda_20260407.json` | `checkpoint_best_acc` | **91.94%** | Checkpoint metadata (training best, epoch 99) |
| `framework_comparison.json` | `accuracy` | **91.65%** | Single-run framework comparison (ours vs aihwkit) |
| `noise_sweep_results_gpt.json` | `test_acc_mean` | **91.707%** | Noise-sweep baseline (σ_c2c=0.05, σ_d2d=0.10, native ADC) |
| `ir_drop_sensitivity_final.json` | `mean` | **91.67%** | 0% IR-drop baseline (3 seeds: 91.65, 91.80, 91.56) |
| `tinyvit_v4_retention_results_gpt.json` | `test_acc_mean` | **91.627%** | Retention t=0 baseline (10 MC runs) |

### 1.2 Root Cause Analysis

The spread of **0.29 pp** (91.65%–91.94%) is **entirely explained by different statistical estimators and random seeds**:

- **91.94%** is the *training best* (single deterministic value from the best epoch). It is NOT an eval mean.
- **91.69%** is the *mean of 10 independent MC eval runs* on the canonical checkpoint (`_codex_verify_v4_canonical_eval_cuda_20260407.json`). The std is 0.233%, so the 95% CI is roughly 91.69% ± 0.46%.
- **91.707%** is another 10-run mean from the noise-sweep script (`noise_sweep_results_gpt.json`, σ_c2c=0.05, σ_d2d=0.10). The std is 0.187%.
- **91.67%** is the mean across 3 seeds (42, 123, 456) for IR-drop 0% (`ir_drop_sensitivity_final.json`).
- **91.65%** in `framework_comparison.json` is a single-run value, likely within the natural eval variance.

All eval means cluster tightly around **91.68% ± 0.05%** when normalized to the same estimator (mean of multiple runs). The outlier is 91.94%, which is a different statistic (training best).

### 1.3 Recommendation

**Lock `91.69%` as the canonical V4 eval mean** (source: `_codex_verify_v4_canonical_eval_cuda_20260407.json`, 10 runs, std=0.233%).

- Update `framework_comparison.json` to report `91.69%` instead of `91.65%`.
- If the manuscript needs a single "best" number, use `91.94%` (training best) and label it explicitly as "training best checkpoint accuracy".
- Do **not** mix training-best and eval-mean numbers in the same table without explicit labels.

---

## 2. Ensemble HAT Divergence (86.37%–88.41%)

### 2.1 Files and Values Found

| File | Value | Protocol | Checkpoint | Notes |
|:--|:--|:--|:--|:--|
| `ensemble_hat_ablation_FIXED.json` | **86.567%** (std=1.658) | FIXED ablation, 10 MC runs | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | Locked ablation study |
| `fresh_instance_eval.json` | **86.365%** (std=1.535) | Fresh-instance protocol, 10 instances × 5 MC runs each | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | Cross-instance variability |
| `ensemble_frequency_ablation.json` | **88.41%** | Per-epoch resampling, 50-epoch training from scratch | *New model trained with freq_mode=epoch* | **Different experiment entirely** |

### 2.2 Root Cause Analysis

The **86.37%** and **86.57%** values are consistent: both evaluate the **same ensemble checkpoint** under protocols that resample D2D per epoch or per instance. The small difference (~0.20 pp) is within the expected stochastic variance (std ~1.5–1.7%).

The **88.41%** value is **not an evaluation of the ensemble checkpoint**. It comes from `run_ensemble_frequency_ablation.py`, which **trains a brand-new model from scratch** for 50 epochs with `freq_mode=epoch` (per-epoch D2D resampling). This is a training ablation, not an inference evaluation. The model architecture and training budget (50 epochs vs 100 epochs for the canonical checkpoint) are different. Therefore, 88.41% is **not comparable** to the 86.37% ensemble HAT eval number.

### 2.3 Recommendation

**Lock `86.37 ± 1.54%` as the Ensemble HAT number** for the ensemble checkpoint.

- Source: `fresh_instance_eval.json` (10 fresh instances, cross-instance mean=86.365%, std=1.535%).
- Alternative source: `ensemble_hat_ablation_FIXED.json` (mean=86.567%, std=1.658%).
- **Discard 88.41%** from any claim about the ensemble checkpoint's inference accuracy. If it is cited, it must be explicitly labeled as "separate 50-epoch training ablation".
- In manuscript tables, always pair the accuracy with its protocol tag:
  - "Ensemble HAT (fresh-instance eval): 86.37 ± 1.54%"
  - "Ensemble HAT (FIXED ablation): 86.57 ± 1.66%"

---

## 3. Device Comparison & Doctor Temp Profiles at ~10%

### 3.1 Files and Values Found

| File | Reported Accuracy | Checkpoint | Device | Status |
|:--|:--|:--|:--|:--|
| `device_comparison_results_gpt.json` (all tinyvit rows) | **10.0%** | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | cuda | ❌ Broken |
| `doctor_temp_norm_profile_eval.json` | **10.2%** | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | cuda | ❌ Broken |
| `doctor_temp_programming_profile_eval.json` | **10.2%** | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | cuda | ❌ Broken |
| `doctor_temp_uniform_profile_eval.json` | **10.2%** | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | cuda | ❌ Broken |
| `doctor_measured_profile_eval_standard_hat.json` | **10.2%** | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | cuda | ❌ Broken |
| `doctor_measured_profile_eval.json` | **89.8%** | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | cuda | ✅ Works |
| Bundle runs (CPU, measured profile) | **93.75%** | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | cpu | ✅ Works |

### 3.2 Root Cause Analysis

**The 10% values are catastrophically wrong and must not be used.**

Key evidence:
1. **Even the "Ideal" profile** in `device_comparison_results_gpt.json` returns 10.0%. The Ideal profile has σ_c2c=0, σ_d2d=0, n_states=256 — it should perform within a few pp of the digital baseline (~91.94%). Chance-level accuracy with zero noise is impossible under correct operation.
2. **The ensemble checkpoint works** on CUDA with the same doctor profiles (89.8%). This rules out a universal CUDA bug in the evaluation script.
3. **CPU bundle runs work** for the ensemble checkpoint (93.75%). This rules out a fundamental profile-to-checkpoint incompatibility.
4. **The standard checkpoint works fine** on CUDA when evaluated *without* profile changes (`noise_sweep_results_gpt.json` gives ~91.7%). This means the checkpoint itself is valid.

**The failure mode is specific to: standard checkpoint + profile application + CUDA.**

Several hypotheses for the root cause (not fully isolated):
- **Profile-state restoration bug:** `snapshot_analog_state` / `restore_analog_state` does not capture the `d2d_noise` buffer. If a profile with `σ_d2d=0` is applied first, `d2d_noise` is zeroed. Subsequent evaluations may retain zero D2D even when the config says otherwise, but `set_noise_for_eval` resets σ_d2d to 0.10 without resampling. However, this alone cannot explain 10.0% on the very first profile evaluation.
- **CUDA dtype / AMP interaction:** The broken files all ran with `amp_enabled=true` on CUDA. The CPU bundle runs (which work) ran without AMP. There may be a float16 overflow or NaN propagation when analog layers with extreme G_min/G_max ratios (e.g., doctor temp programming profile: G_min=4.07e-09, G_max=8.42e-08) are evaluated under AMP.
- **Checkpoint / config mismatch:** The standard checkpoint was saved with `AnalogLinearConfig` defaults and `restore_weight_scale=True`. If `apply_device_profile` changes `G_min`/`G_max` to values orders of magnitude smaller (e.g., 1e-9 vs 1.0), the conductance-to-weight math may produce NaN or Inf under CUDA float16, causing uniform outputs.

**Most likely root cause:** An AMP + extreme G_range interaction. The doctor temp profiles have G_min/G_max in the 1e-9 to 1e-7 range (programming/uniform variants). Under AMP autocast to float16, operations at this scale can underflow or lose precision, corrupting the model output. The ensemble checkpoint may be less sensitive because its weights were trained with more D2D variability, masking the numerical issue slightly (89.8% instead of 10%).

### 3.3 Recommendation

1. **Discard ALL ~10% values** from manuscript claims immediately:
   - `device_comparison_results_gpt.json` (tinyvit rows)
   - `doctor_temp_norm_profile_eval.json`
   - `doctor_temp_programming_profile_eval.json`
   - `doctor_temp_uniform_profile_eval.json`
   - `doctor_measured_profile_eval_standard_hat.json`

2. **Do not re-run these evaluations with AMP enabled.** Re-run on CUDA with `--no-amp` or on CPU.

3. **If doctor profile numbers are needed for the manuscript:**
   - Use the CPU bundle runs (93.75% for measured profile on ensemble checkpoint) as a provisional upper bound.
   - Re-run `eval_measured_profile.py` and `run_device_comparison.py` on the **standard checkpoint** with `--no-amp` to get valid numbers.
   - Verify that the "Ideal" profile returns >90% before trusting any other profile result.

4. **Actionable code fix:** Add an AMP guard or force `amp_enabled=False` in `eval_measured_profile.py` and `run_device_comparison.py` when analog layers are involved, until the float16 interaction is fully understood.

---

## 4. CrossSim ConvNeXt 54.69%

### 4.1 Files and Values Found

| File | `max_samples` | Our Framework | CrossSim | Notes |
|:--|:--|:--|:--|:--|
| `crosssim_comparison_results.json` | **64** | **54.69%** | 4.69% | Tiny subset; NOT full test set |
| `crosssim_convnext_results.json` | **1000** | **81.63%** (std=0.56) | 67.2% (std=2.67) | Larger subset; still not full |

### 4.2 Root Cause Analysis

The 54.69% value is explicitly tagged with `max_samples: 64` in the JSON. CIFAR-10 has 10,000 test images. Evaluating on 64 samples (~0.6% of the test set) produces a noisy, non-representative accuracy. Both frameworks (ours and CrossSim) perform poorly on this tiny subset because 64 samples is insufficient to estimate model accuracy reliably.

The later file (`crosssim_convnext_results.json`) uses `max_samples: 1000` and yields 81.63% for our framework and 67.2% for CrossSim. This is more reasonable but still a subset.

The JSON does not state the subset size in any human-readable `note` field — it only appears in the machine-readable `max_samples` key. The audit correctly flagged this as undocumented.

### 4.3 Recommendation

1. **Do NOT cite 54.69% or 4.69% in any manuscript table or figure.** These are subset artifacts.
2. **Do NOT cite 81.63% as a full-set number.** It is a 1000-sample subset (10% of CIFAR-10 test).
3. **Re-run `run_crosssim_convnext.py` with `--max-samples 0`** (or omit the flag) to evaluate on the full 10,000-image test set. Update `crosssim_comparison_results.json` with the full-set results.
4. **Add an explicit `note` field** to the JSON payload documenting the subset size whenever `max_samples > 0`:
   ```json
   "notes": {
     "subset_evaluation": "max_samples=1000 out of 10000 total test images"
   }
   ```

---

## 5. File Archive / Update Recommendations

| File | Action | Reason |
|:--|:--|:--|
| `report_md/_gpt/json_gpt/fresh_instance_eval.json` | **Keep** | V4_Ensemble=86.37% is a locked number; V4_Standard=10.0% is broken and should be ignored or replaced after re-run |
| `report_md/_gpt/ensemble_hat_ablation_FIXED.json` | **Keep** | Locked ablation data; 86.57% confirms fresh-instance number |
| `report_md/_gpt/ensemble_frequency_ablation.json` | **Keep but label** | 88.41% is a training ablation, not an eval of the ensemble checkpoint |
| `report_md/_gpt/json_gpt/device_comparison_results_gpt.json` | **Archive / delete tinyvit rows** | All tinyvit rows are 10.0% (broken). ConvNeXt rows (71.6%–84.1%) may be valid but should be re-verified |
| `report_md/_gpt/doctor_temp_norm_profile_eval.json` | **Archive / delete** | 10.2% is broken |
| `report_md/_gpt/doctor_temp_programming_profile_eval.json` | **Archive / delete** | 10.2% is broken |
| `report_md/_gpt/doctor_temp_uniform_profile_eval.json` | **Archive / delete** | 10.2% is broken |
| `report_md/_gpt/doctor_measured_profile_eval_standard_hat.json` | **Archive / delete** | 10.2% is broken |
| `report_md/_gpt/doctor_measured_profile_eval.json` | **Keep provisional** | 89.8% on ensemble checkpoint is plausible, but re-run on full set without AMP for confirmation |
| `report_md/_gpt/crosssim_comparison_results.json` | **Archive / delete** | 54.69% on 64-sample subset is not manuscript-worthy |
| `report_md/_gpt/crosssim_convnext_results.json` | **Keep provisional** | 81.63% on 1000-sample subset is better but still not full-set |
| `report_md/_gpt/framework_comparison.json` | **Update** | Change canonical accuracy from 91.65% to 91.69% |

---

*Report generated by targeted JSON investigation.*
