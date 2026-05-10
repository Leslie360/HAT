# Source Data v1 — Nature Communications Submission

**Paper:** "Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision"

---

## Contents

| File | Description | Figure/Table reference |
|:---|:---|:---|
| `fig4_source_data.csv` | Cross-dataset accuracy under canonical deployment | Main Fig. 4 |
| `nl_ablation_lanes.csv` | Group-wise NL=2.0 mitigation ablation summary | Supp Table SX.N |
| `*.json` (73 files) | Raw experiment JSONs for all locked numbers and robustness sweeps | All figures and tables |

---

## JSON file index (key files)

| JSON file | Content | Manuscript reference |
|:---|:---|:---|
| `a23_experiment_results.json` | Inverse-gamma frontend sweep (γ_phys × I_dark) | Fig. 6, Table S5 |
| `adc_layerwise_nonideality_full_gpt.json` | ADC offset/gain/INL full-test sweep | Table S3 |
| `doctor_measured_profiles.json` | Fitted OPECT device profile | Fig. 7, Table S2 |
| `fresh_instance_cadence_control.json` | Cadence scan (fixed/epoch/batch) | Fig. S4 |
| `fresh_instance_eval.json` | Fresh-instance robustness (10 arrays) | Fig. 5, Fig. S6 |
| `fresh_instance_eval_v4_ensemble_correlated_d2d.json` | Correlated-D2D fresh-instance stress test | Supp. Note SX.Z / Fig. S\_corr\_d2d |
| `learnable_gamma_*.json` | Learnable γ_comp experiment | Supp §E3 |
| `literature_profile_eval.json` | OPECT zero-shot transfer | Fig. 7 |
| `tinyvit_v1_results_gpt.json` | FP32 baseline (single seed) | Table 1 |
| `tinyvit_v2v7_results_gpt.json` | V2–V7 canonical regime results | Table 2 |
| `tinyvit_v4_ensemble_results_gpt.json` | Ensemble HAT 10-seed eval | Fig. 5, §5.6 |
| `tinyvit_v4_nl2_hat_eval_results_gpt.json` | NL=2.0 severe nonlinearity eval | Table 2, §5.7 |
| `tinyvit_v4_retention_results_gpt.json` | Retention decay time series | Fig. 2, Table S4 |
| `v4_ensemble_results_gpt.json` | Ensemble HAT canonical eval | §5.6 |
| `v4_nl2_mlp_linear_comp_train_results_gpt.json` | MLP-only NL mitigation | Table SX.N row (c) |
| `v4_nl2_qkv_linear_comp_train_results_gpt.json` | QKV-only NL mitigation | Table SX.N row (d) |
| `v4_nl2_all_linear_comp_train_results_gpt.json` | All-linear NL mitigation | Table SX.N row (f) |

---

## Notes

- All accuracy values are percentages.
- Error bars denote ±1 standard deviation where Monte Carlo statistics are available.
- "n/a" indicates deterministic baselines or single-run point estimates.
- The `nl_ablation_lanes.csv` row (e) reflects the training trajectory at epoch 54 (shell timeout); the collapse pattern is already fully established.
- The correlated-D2D sweep uses the same `10 fresh instances × 5 MC evaluations` protocol as the canonical fresh-instance Ensemble HAT result; only the D2D sampling law changes.

---

*Generated: 2026-04-19*
