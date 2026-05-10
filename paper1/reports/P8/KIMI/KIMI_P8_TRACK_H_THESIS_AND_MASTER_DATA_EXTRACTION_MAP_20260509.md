# Kimi P8 Track H: Thesis and Master-Data Extraction Map

Date: 2026-05-09
Scope: `/home/qiaosir/projects/compute_vit`, thesis drafts, master/device-data directories, 105/107 references
Status: COMPLETE — extraction map only; no thesis rewrite

## 1. Located directories and resources

| Path | Type | Relevance |
|---|---|---|
| `thesis/en/ (compat: paper/thesis/)` | English thesis draft | HAT, PCM, deployment, failure modes |
| `thesis/cn/ (compat: paper/thesis_cn/)` | Chinese thesis draft | Chinese thesis chapters, Work-2 scope chapter |
| `thesis/en/ (compat: paper/thesis/)XJTU-thesis/` | XJTU thesis template/project | Formatting/template; not canonical data by itself |
| `数据_博士/` | Raw device/master data | EPSC / QIVD / derived profiles; important for thesis and future hardware calibration |
| `report_md/_gpt/KIMI_P3_TRACK_E_MASTER_STATUS_REPORT_20260509.md` | Master status report | Coordination/status context |
| `/home/qiaosir/projects/remote_reviews/105/` | 105 review clone | TinyImageNet cross-architecture validation data |
| `/home/qiaosir/projects/remote_reviews/107/` | 107 review clone | Work-2 analog KV-cache data |

## 2. Thesis chapter map

| File | Likely content | Status |
|---|---|---|
| `thesis/en/ (compat: paper/thesis/)chapter_1_hat_instance_overfitting.tex` | HAT instance overfitting framing | Paper-1-aligned; verify locked numbers before reuse |
| `thesis/en/ (compat: paper/thesis/)chapter_2_framework.tex` | hybrid framework / CIM stack | Paper-1-aligned |
| `thesis/en/ (compat: paper/thesis/)chapter_3_hat_taxonomy.tex` | HAT taxonomy | likely contains standard/ensemble/proportional distinctions |
| `thesis/en/ (compat: paper/thesis/)chapter_4_failure_modes.tex` | failure modes | likely maps pure quantization collapse / PCM drift |
| `thesis/en/ (compat: paper/thesis/)chapter_5_mitigation.tex` | mitigation | HAT/compensation narrative |
| `thesis/en/ (compat: paper/thesis/)chapter_6_physical_realism.tex` | physical realism | PCM/OPECT/retention/device calibration |
| `thesis/en/ (compat: paper/thesis/)chapter_7_deployment.tex` | deployment | precision-retention, energy, hardware constraints |
| `thesis/en/ (compat: paper/thesis/)chapter_8_outlook.tex` | outlook | likely Work-2 / KV-cache future direction |
| `thesis/cn/ (compat: paper/thesis_cn/)chapter_6_work2_scope.tex` | Chinese Work-2 scope | most relevant to 107 analog KV-cache |
| `thesis/cn/ (compat: paper/thesis_cn/)chapter_4_benchmarks.tex` | Chinese benchmark chapter | likely contains Paper-1/105 numerical summaries |

## 3. Data-location index

| Topic | File/path | Dataset/metric | Numbers/status | Canonical label |
|---|---|---|---|---|
| Paper-1 locked PCM ladder | `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv`; `paper/latex_gpt/source_data/canonical_json/` | CIFAR-10 accuracy/drift | 8-bit 77.60 fresh, 6-bit 68.44 fresh, 4-bit 76.68 fresh; drift drops 0.04/0.04/4.01 pp | canonical |
| Ensemble HAT 3-seed | `paper/latex_gpt/supplementary.tex` table `tab:v4-three-seed-summary` | CIFAR-10 fresh accuracy | 86.16 ± 0.19% seed-mean aggregate | canonical |
| Pure 4-bit collapse | `paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/` | CIFAR-10 fresh accuracy | 14.64% | canonical ablation |
| Ideal 8-bit baseline | `paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/` | CIFAR-10 fresh accuracy | 87.28% | canonical ablation |
| 105 TinyImageNet DeiT | `/home/qiaosir/projects/remote_reviews/105/`; P6/P7 reports | TinyImageNet fresh accuracy | proportional +1.77/+1.81 pp vs digital | supplement-candidate |
| 105 TinyImageNet ViT | same | TinyImageNet fresh accuracy | +1.27/+1.35 pp, seed456 outlier | defense-support |
| 107 KV-cache | `/home/qiaosir/projects/remote_reviews/107/`; P6/P7 reports | WikiText PPL | baseline 22.18, HAT digital 19.04, last1 19.45, last2 20.14, all-layer 37.13 | Work-2 only |
| Raw EPSC/device data | `数据_博士/*.csv`, `数据_博士/20260501/*.qivd`, `数据_博士/derived_profiles/` | EPSC/device profiles | extraction/calibration material; not Paper-1 locked values | unknown/provisional until processed |
| OPECT proxy profile | `paper/latex_gpt/supplementary/S_opect_distribution.tex` | OPECT proxy D2D/C2C | D2D 0.03, C2C 0.02; distribution shape unknown | paper-safe proxy |

## 4. Contradiction flags against Paper-1 locked values

| Potential conflict | Action |
|---|---|
| Any thesis text still saying 6-bit fresh is 68.55% or drift 0.07 pp | Must be updated before thesis reuse; Paper-1 canonical is 68.44% and 0.04 pp |
| Any thesis/master note using `86.37 ± 0.19%` as aggregate | Must be corrected; 86.37% is seed123 row, aggregate is 86.16 ± 0.19% |
| Any 107 KV-cache claim inside Paper-1 main narrative | Remove from Paper-1; allowed only as Work-2/thesis future-work content |
| Any 105 ViT proportional claim stated as definitive | Downgrade to defense/provisional because seed456 outlier remains |
| Any raw `数据_博士` EPSC number treated as canonical model accuracy | Do not do this; raw device data needs extraction/fit/provenance before claim use |

## 5. Recommended extraction order for thesis work

1. Use Paper-1 bundle/canonical JSON as the authoritative source for PCM/HAT locked values.
2. Use P6/P7 105 reports only for supplement/defense cross-architecture validation.
3. Use P6/P7 107 reports only for Work-2/Chapter outlook/KV-cache sections.
4. Treat `数据_博士/` as raw calibration material; extract through a separate data provenance notebook/report before citing values.
5. Run a thesis grep before thesis freeze: `68.55`, `0.07`, `86.37`, `last1`, `KV`, `PPL`, `TinyImageNet`.

## 6. Verdict

Track H COMPLETE. The thesis/master-data map is indexed and labels each number as canonical, supplement/defense, Work-2, or unknown/provisional.
