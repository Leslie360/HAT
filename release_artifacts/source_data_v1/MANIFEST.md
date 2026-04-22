# Source Data v1 Manifest

**Date:** 2026-04-19  
**Size:** 144 KiB (compressed) / ~732 KiB (uncompressed)  
**Files:** 77 (73 JSON + 2 CSV + 1 README + 1 MANIFEST)

---

## Main-text figure source data

| Figure | File(s) | Format |
|:---|:---|:---|
| Fig 2 (retention) | `tinyvit_v4_retention_results_gpt.json` | JSON |
| Fig 3 (contour) | `noise_sweep_results_gpt.json`, `sobol_*` (in logs) | JSON |
| Fig 4 (cross-dataset) | `fig4_source_data.csv` | CSV |
| Fig 5 (HAT recovery) | `fresh_instance_eval.json`, `v4_ensemble_results_gpt.json` | JSON |
| Fig 6 (frontend γ) | `a23_experiment_results.json` | JSON |
| Fig 7 (case study) | `literature_profile_eval.json` | JSON |

## Supplementary figure/table source data

| Supp Item | File(s) | Format |
|:---|:---|:---|
| Table S3 (ADC non-ideality) | `adc_layerwise_nonideality_full_gpt.json` | JSON |
| Table S4 (retention comparison) | `tinyvit_v4_retention_results_gpt.json` | JSON |
| Table S5 (γ × I_dark) | `a23_experiment_results.json` | JSON |
| Table SX.N (NL ablation) | `nl_ablation_lanes.csv` | CSV |
| Fig S2 (noise sensitivity) | `noise_sweep_results_gpt.json` | JSON |
| Fig S4/S5 (cadence) | `fresh_instance_cadence_control.json` | JSON |
| Fig S6 (fresh-instance) | `fresh_instance_eval.json` | JSON |
| Fig S_corr_D2D / Note SX.Z | `fresh_instance_eval_v4_ensemble_correlated_d2d.json` | JSON |
| Fig S7/S8 (frontend/SNR) | `a23_experiment_results.json` | JSON |
| Fig S10 (gradient distortion) | `nl_gradient_distortion_gpt.json` | JSON |

## Complete file list

See `source_data_v1/README.md` for per-file descriptions and manuscript cross-references.

---

**Changes from v0:**
- Added `fig4_source_data.csv`
- Added `nl_ablation_lanes.csv`
- Added all NL mitigation lane JSONs
- Added `fresh_instance_eval_v4_ensemble_correlated_d2d.json`
- Pruned temporary/smoke JSONs (kept for provenance but labeled with `_` prefix)

**Next version (v2, if needed):**
- Add CrossSim comparison JSONs when available
- Add Fig 3/6/7 raw plotting arrays if reviewer requests
