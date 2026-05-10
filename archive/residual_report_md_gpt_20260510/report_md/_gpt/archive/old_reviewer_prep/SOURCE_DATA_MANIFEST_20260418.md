# Source Data Manifest — 2026-04-18

**Purpose:** Map every main-text and supplementary figure/table to its underlying data file(s) for NC source-data submission.

---

## Main Text Figures

| Figure | Caption summary | Source data file(s) | Location |
|:--|:--|:--|:--|
| Fig 1 | System architecture (moved to supplementary) | N/A — schematic | `paper/latex_gpt/figures/fig1_system_architecture.*` |
| Fig 2 | Retention decay curve | `tinyvit_v4_retention_results_gpt.json` | `report_md/_gpt/json_gpt/` |
| Fig 3 | Iso-accuracy contour map | `sobol_*.json`, contour grid data | `logs/` + `report_md/_gpt/json_gpt/` |
| Fig 4 | Cross-dataset accuracy comparison | Fresh-instance eval + canonical eval JSONs | `report_md/_gpt/json_gpt/fresh_instance_eval.json`, `v4_ensemble_results_gpt.json` |
| Fig 5 | HAT recovery bar chart | Ensemble HAT + standard HAT eval results | `report_md/_gpt/json_gpt/` |
| Fig 6 | Frontend compensation γ scan | `a23_experiment_results.json` | `report_md/_gpt/json_gpt/` |
| Fig 7 | Case-study zero-shot transfer | `literature_profile_eval.json` | `report_md/_gpt/json_gpt/` |

## Main Text Tables

| Table | Caption summary | Source data file(s) | Location |
|:--|:--|:--|:--|
| Table 1 | Architecture comparison | `tinyvit_v1_results_gpt.json`, etc. | `report_md/_gpt/json_gpt/` |
| Table 2 | Accuracy matrix (V1–V8, C1–C9, R1–R6) | Multiple training result JSONs | `report_md/_gpt/json_gpt/` |

## Supplementary Figures

| Figure | Caption summary | Source data file(s) | Location |
|:--|:--|:--|:--|
| Fig S1 | System architecture detail | N/A — schematic | `paper/latex_gpt/figures/` |
| Fig S2 | Continuous noise sensitivity / ADC sweep | `adc_sweep_*.json`, `noise_sensitivity_*.json` | `report_md/_gpt/json_gpt/` |
| Fig S3 | Ensemble HAT concept diagram | N/A — schematic | `paper/latex_gpt/figures/` |
| Fig S4 | Fresh-instance robustness + cadence scan | `fresh_instance_cadence_control.json`, `fresh_instance_eval.json` | `report_md/_gpt/json_gpt/` |
| Fig S5 | Cadence scan detail | `fresh_instance_cadence_control.json` | `report_md/_gpt/json_gpt/` |
| Fig S6 | Fresh-instance robustness (p<10⁻¹⁵) | `fresh_instance_eval.json` | `report_md/_gpt/json_gpt/` |
| Fig S7 | Frontend theory curves | `a23_experiment_results.json` | `report_md/_gpt/json_gpt/` |
| Fig S8 | SNR curves | `a23_experiment_results.json` | `report_md/_gpt/json_gpt/` |
| Fig S9 | Sobol sensitivity indices | `sobol_*.json` | `logs/` |
| Fig S10 | Group-wise gradient distortion | `nl_gradient_distortion_*.json` | `report_md/_gpt/json_gpt/` |

## Supplementary Tables

| Table | Caption summary | Source data file(s) | Location |
|:--|:--|:--|:--|
| Table S1 | Parameter provenance | `PROVENANCE_AUDIT_20260418.md` | `report_md/_gpt/` |
| Table S2 | Zhang OPECT proxy parameters | `doctor_measured_profiles.json` | `report_md/_gpt/json_gpt/` |
| Table S3 | ADC non-ideality full-test | `adc_layerwise_nonideality_full_gpt.json` | `report_md/_gpt/json_gpt/` |
| Table S4 | Retention comparison (uniform vs state-dependent) | `tinyvit_v4_retention_results_gpt.json` | `report_md/_gpt/json_gpt/` |
| Table S5 | γ_phys × I_dark sweep | `a23_experiment_results.json` | `report_md/_gpt/json_gpt/` |
| Table S6 | V4 three-seed summary | `tinyvit_v2v7_results_gpt.json` | `report_md/_gpt/json_gpt/` |
| Table S7 | Retention sensitivity | `retention_sensitivity_*.json` | `report_md/_gpt/json_gpt/` |
| Table SX.N | Group-wise NL ablation | `v4_nl2_*_linear_comp_train_results_gpt.json` | `report_md/_gpt/json_gpt/` |

## Data release readiness

| Item | Status | Action |
|:--|:--|:--|
| Fig 4 source CSV | ⏳ | Codex CX-Q |
| Fig 4 source README | ⏳ | Codex CX-Q |
| All JSON snapshots | ✅ | `report_md/_gpt/json_gpt/` already organized |
| NL ablation lane CSVs | ⏳ | Export from `NL_LANE_RESULTS_20260418.md` |
| ZIP manifest | ⏳ | Codex CX-R |

---

*Last updated: 2026-04-18*
