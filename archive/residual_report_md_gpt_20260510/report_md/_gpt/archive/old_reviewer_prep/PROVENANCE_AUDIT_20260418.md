# Provenance Audit — Locked Numbers in NC Submission Package

**Date:** 2026-04-18
**Author:** Claude (CLAUDE-C in this round)
**Inputs:** `paper/CANONICAL_RESULT_LOCK_gpt.md`, `report_md/_gpt/CLAUDE_TASK_gpt.md` Locked-Numbers section, `paper/latex_gpt/sections/*.tex`, `report_md/_gpt/json_gpt/*`, `logs/_gpt/*`.
**Purpose:** For each number that appears in the manuscript or cover letter, document **(a)** the manuscript claim it supports, **(b)** the producing script, **(c)** the canonical log / JSON artifact, **(d)** the blast radius if the number changes during reviewer revision or the thesis defense.

This file is the shield for `数字出处` challenges (thesis defense) and reviewer revision rounds. **Do not edit manuscript numbers without first locating the entry here and updating the blast-radius column.**

---

## 1. Headline / abstract / introduction numbers

| # | Locked number | Manuscript citation | Producing script | Canonical log / JSON | Blast radius |
|:--|:--|:--|:--|:--|:--|
| H1 | `S_ADC = 0.98` (full grid) | `00_abstract.tex`, `01_introduction.tex` (contribution #2), `05_results.tex:51`, `06_discussion.tex:9`, `07_conclusion.tex:7` | `run_sobol_analysis.py`, `run_contour_sweep.py` | `logs/sobol_*`, contour heatmap source under `paper/latex_gpt/figures/fig_contour_map*` | Whole "two-stage hierarchy" framing collapses; abstract sentence and conclusion sentence both reword; Fig 3 caption reword. |
| H2 | `S_D2D = 0.92` (operational region, ≥6-bit, σ≤15%) | `00_abstract.tex`, `06_discussion.tex:9`, `07_conclusion.tex:7` | same as H1 | same as H1 | Hierarchy inversion claim disappears; rewording cascades through abstract / discussion / conclusion. |
| H3 | `+5.8 pp at γ_phys = 2.0` (`89.85%` vs `84.04%`) | `01_introduction.tex` (contribution #2), `05_results.tex:46` | A2.3 5×4 γ_phys × I_dark sweep — likely `run_a23_experiments.py` and the inverse-gamma compensation runs | A2.3 sweep JSON / log (TODO: Codex to add file path stamp on next NL queue refresh) | Inverse-gamma elevation to contribution #2 weakens; abstract / intro contribution sentence reword; Table S5 column reword. |
| H4 | `Ensemble HAT = 86.37 ± 1.54%` (10 fresh arrays) | `00_abstract.tex`, `01_introduction.tex` (contrib #3), `05_results.tex:63`, `06_discussion.tex:13`, `07_conclusion.tex:7`, cover letter | `run_ensemble_hat_fixed.py` / `run_ensemble_hat_ablation_FIXED.py` | `report_md/_gpt/json_gpt/v4_ensemble_results_gpt.json` | **Largest blast radius in paper.** Touches abstract, intro contribution #3, §5.8, §6 paragraph 2, §7, cover letter. Move this number = rewrite 5 places. |
| H5 | `10.00%` standard-HAT fresh-instance collapse | `00_abstract.tex`, `01_introduction.tex`, `06_discussion.tex:13`, `07_conclusion.tex:7` | `eval_fresh_instances.py` | `report_md/_gpt/json_gpt/fresh_instance_eval.json` | Pairs with H4; if H5 changes the "10 → 86" gap narrative weakens. |
| H6 | `27.72 ± 0.82%` (Tiny-ViT V4 NL=2.0 HAT, Task 35) | `00_abstract.tex`, `01_introduction.tex` (contrib #4), `05_results.tex:63`, `07_conclusion.tex:7` | `train_tinyvit.py --nl_ltp 2.0 --nl_ltd -2.0` (Task 35 retraining) | `report_md/_gpt/json_gpt/v4_nl2_hat_train_results_gpt.json` + `v4_nl2_hat_eval_results_gpt.json` | **THIS IS THE LIVE MITIGATION TARGET.** If CX-A MLP-linear comp lifts this to ~87%, the entire `severe NL is a recovery bottleneck` thesis collapses. CLAUDE-A NL narrative decision lives or dies here. |
| H7 | `88.53%` OPECT zero-shot literature-anchored case study | `00_abstract.tex`, `01_introduction.tex` (contrib #4) | `eval_literature_profile.py` | `report_md/_gpt/json_gpt/literature_profile_eval.json`, also `report_md/_gpt/json_gpt/literature_fitted_profile.json` | Contribution #4 narrative weakens; Fig 5 reword. |
| H8 | `98.06%` digital FP32 baseline (Tiny-ViT-5M, CIFAR-10) | `06_discussion.tex:15`, `05_results.tex:8`, appendix table | `train_tinyvit.py` (V1 / FP32 path) | `report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json` | Residual-gap framing in §6 collapses; appendix V1 row changes. |

---

## 2. Cross-dataset best-checkpoint table (Fig 4 / Fig 5)

> Source-of-truth: `paper/CANONICAL_RESULT_LOCK_gpt.md §1`. Rule: **best-checkpoint** values for grouped bars; never silently mix with MC means.

| # | Cell | Value | Producing script | Canonical JSON |
|:--|:--|:--:|:--|:--|
| T1 | Tiny-ViT V1 / CIFAR-10 | `97.48` | `train_tinyvit.py` | `tinyvit_v1_results_gpt.json` |
| T2 | Tiny-ViT V3 / CIFAR-10 | `89.54` | `train_tinyvit.py` (V3) | `tinyvit_v2v7_results_gpt.json` |
| T3 | Tiny-ViT V4 / CIFAR-10 | `91.94` | `train_tinyvit.py` (V4) | `tinyvit_v2v7_results_gpt.json` |
| T4 | Tiny-ViT V1 / CIFAR-100 | `86.94` | `train_tinyvit.py` + `run_cifar100_fast.py` | `tinyvit_cifar100_v134_results_gpt.json` |
| T5 | Tiny-ViT V3 / CIFAR-100 | `44.06` | same | same |
| T6 | Tiny-ViT V4 / CIFAR-100 | `65.48` | same | same |
| T7 | Tiny-ViT V1 / Flowers-102 | `97.97` | `run_flowers102_training.py` (V1) | `tinyvit_flowers102_v134_results_gpt.json` |
| T8 | Tiny-ViT V3 / Flowers-102 | `4.81` | same | same |
| T9 | Tiny-ViT V4 / Flowers-102 | `22.48` | same | same |
| T10 | ConvNeXt C1 / CIFAR-10 | `90.74` | `train_convnext.py` (C1) | `convnext_results_gpt.json` / `convnext_c1_results_gpt.json` |
| T11 | ConvNeXt C3 / CIFAR-10 | `70.48` | `train_convnext.py` (C3) | `convnext_results_gpt.json` |
| T12 | ConvNeXt C4 / CIFAR-10 | `89.91` | `train_convnext.py` (C4) | `convnext_full_results_gpt.json` |
| T13 | ConvNeXt C1 / CIFAR-100 | `64.12` | `train_convnext.py` + `run_cifar100_fast.py` | `convnext_cifar100_c134_results_gpt.json` |
| T14 | ConvNeXt C3 / CIFAR-100 | `23.86` | same | same |
| T15 | ConvNeXt C4 / CIFAR-100 | `60.54` | same | same |
| T16 | ConvNeXt C1 / Flowers-102 | `33.22` | `run_flowers102_training.py` (C1) | `convnext_flowers102_c134_results_gpt.json` |
| T17 | ConvNeXt C3 / Flowers-102 | `3.79` (best) / `1.57±0.83` (MC) | same | same; MC traceable in same JSON's `monte_carlo` block |
| T18 | ConvNeXt C4 / Flowers-102 | `3.35` (best) / `2.03±0.68` (MC) | same | same |

**Blast radius for T1–T18:** Fig 4 / Fig 5 panels redrawn; appendix Table A1 row updates; §5.1 baseline sentence reword. Best-vs-MC rule must be re-enforced in any caption rewrite (`CANONICAL_RESULT_LOCK_gpt.md §2`).

---

## 3. 3-seed cross-seed locked numbers (appendix / supp tables)

| # | Locked number | Citation | Producing script | Canonical JSON |
|:--|:--|:--|:--|:--|
| S1 | V1 (3-seed) `98.06 ± 0.17%` | `08_appendix.tex:24`, `05_results.tex:8` | `train_tinyvit.py` × 3 seeds | aggregate from per-seed runs in `tinyvit_v1_results_gpt.json` |
| S2 | V4 (3-seed) `87.95 ± 0.27%` | appendix | `train_tinyvit.py` × 3 seeds | `tinyvit_v2v7_results_gpt.json` |
| S3 | C1 (3-seed) `82.43 ± 0.17%` | supp / appendix | `train_convnext.py` × 3 | `convnext_c1_results_gpt.json` |
| S4 | C4 (3-seed) `84.75 ± 0.72%` | supp / appendix | `train_convnext.py` × 3 | `convnext_full_results_gpt.json` |
| S5 | V8 retention (3-seed) `89.67 ± 0.08%` | supp retention table | `run_retention_sensitivity.py` | `tinyvit_v7_retention_results_gpt.json` |
| S6 | Flowers V2 zero-noise hybrid `91.30 ± 0.00%` (10 runs) | Flowers-102 supp boundary discussion | `run_flowers102_training.py` (V2 control) | `p14_flowers_v2_result.json` |

**Blast radius:** §6.6 wording; appendix V1/V4/C1/C4 rows; reviewer-response Table 2 provenance memo (already addressed in TX-14 closeout).

---

## 4. Physical-extension locks (Task 34 / 35 / 36)

| # | Locked number | Manuscript citation | Producing script | Canonical JSON |
|:--|:--|:--|:--|:--|
| P1 | Task 34 in-domain `97.37 ± 0.05%` (V4 proportional-noise HAT) | `05_results.tex:63` | `train_tinyvit.py` with proportional-noise HAT recipe | `v4_proportional_hat_train_results_gpt.json`, `v4_proportional_hat_eval_proportional_results_gpt.json` |
| P2 | Task 34 transfer `10.38 ± 0.44%` (uniform-noise eval of P1 checkpoint) | discussion / supp | same train as P1, eval on uniform | `v4_proportional_hat_eval_uniform_results_gpt.json` |
| P3 | Task 35 `27.72 ± 0.82%` (V4 NL=2.0 HAT) | H6 above (4 places) | `train_tinyvit.py --nl_ltp 2.0 --nl_ltd -2.0` | `v4_nl2_hat_train_results_gpt.json`, `v4_nl2_hat_eval_results_gpt.json` |
| P4 | Task 36 `91.91 ± 0.08%` (C4 proportional-noise HAT) | discussion (architecture-gap evidence) | `train_convnext.py` proportional HAT recipe | `c4_proportional_hat_train_results_gpt.json` |

**Blast radius for P1–P4:** §5.9 physical-extension paragraph; CANONICAL_RESULT_LOCK §4 must be updated in lockstep; P3 doubles as H6.

---

## 5. Retention curve (corrected V4)

> Source: `CANONICAL_RESULT_LOCK_gpt.md §3`. Manuscript shorthand: `rapid early drop followed by a broad plateau near 79%`. Do not reuse the obsolete `84.28%` wording.

| Time | Locked accuracy | Producing script | Canonical JSON |
|:--|:--:|:--|:--|
| 0 s | `91.63%` | `run_retention_sensitivity.py` | `tinyvit_v4_retention_results_gpt.json` |
| 1 s | `82.66%` | same | same |
| 10 s | `79.13%` | same | same |
| 100 s | `79.05%` | same | same |
| 1000 s | `79.35%` | same | same |
| 10000 s | `79.51%` | same | same |

**Blast radius:** Fig 2 / retention sub-figure redraw; §5.4 retention paragraph reword.

---

## 6. Cadence ablation (per-epoch vs fixed vs per-batch)

| # | Locked number | Manuscript citation | Producing script | Canonical JSON / log |
|:--|:--|:--|:--|:--|
| C1 | per-epoch `88.41%` | `05_results.tex:63` | `run_ensemble_frequency_ablation.py` | report_md/_gpt/_codex_*frequency* logs |
| C2 | fixed `87.18%` | same | same | same |
| C3 | per-batch `86.16%` | same | same | same |

**Blast radius:** §5.8 cadence sentence; supplementary Fig caption.

---

## 7. Cross-framework sanity checks (AIHWKIT, CrossSim)

| # | Locked number | Producing script | Canonical JSON |
|:--|:--|:--|:--|
| F1 | AIHWKIT subset (256) `91.80 ± 1.02%` | aihwkit eval script | `p13_aihwkit_shared_regime_result_256.json` |
| F2 | AIHWKIT full (10K×10) `90.08 ± 0.21%` (digital `95.46%`) | aihwkit eval script | `p13_aihwkit_full_result.json` |
| F3 | CrossSim clean (`0%/0%`) ours `86.20%` / CrossSim `83.70%` | CrossSim phase scripts | `crosssim_clean_baseline.json` |
| F4 | CrossSim low (`1%/1%`) ours `85.90 ± 0.28%` / CrossSim `82.87 ± 0.29%` | same | `crosssim_low_noise.json` |
| F5 | CrossSim std (`5%/5%`) ours `81.63 ± 0.56%` / CrossSim `67.20 ± 2.67%` (gap `14.43 pp`) | same | `crosssim_standard_noise.json` |

**Blast radius:** §6.6 / §6 organic-specific complement paragraph; cover-letter sentence about AIHWKIT/CrossSim shared-regime checks; F5 gap is the load-bearing number for the "organic-specific complement" framing.

---

## 8. ADC layer-wise non-ideality (full-test, supp Table tab:adc-nonideality)

| # | Locked number | Producing script | Canonical JSON |
|:--|:--|:--|:--|
| A1 | Ideal `82.04 ± 0.16%` | `run_adc_layerwise_nonideality_gpt.py` | `adc_layerwise_nonideality_full_gpt.json` |
| A2 | Offset ±0.5 LSB `+0.03 pp` | same | same |
| A3 | Gain ±5% `−0.17 pp` | same | same |
| A4 | INL 0.5 LSB `−1.19 pp` | same | same |
| A5 | Combined realistic `−0.18 pp` | same | same |
| A6 | Combined pessimistic `−5.14 pp` | same | same |

**Blast radius:** supp Table; §6 ADC scale-masking caveat; reviewer-response §ADC.

---

## 9. NL gradient distortion (mechanistic localization)

| # | Locked number | Producing script | Canonical JSON |
|:--|:--|:--|:--|
| N1 | MLP cosine `0.815`, norm ratio `0.671` | `run_nl_gradient_distortion_gpt.py` | `nl_gradient_distortion_gpt.json` |
| N2 | All-analog cosine `0.816`, norm ratio `0.676` | same | same |
| N3 | Patch-Embed / QKV / Proj cosine `1.00` | same | same |
| N4 | Mean loss delta `0.000000` | same | same |

**Blast radius:** intro contribution #4 sentence about "localizing the present NL=2.0 surrogate failure primarily to the MLP path"; supp text in §6; reviewer-response NL section.

---

## 10. In-flight numbers (NOT YET LOCKED — do not paste into manuscript)

| ID | Provisional value | Source | Decision gate |
|:--|:--|:--|:--|
| L1 | NL=2.0 MLP-linear comp best **`87.79%`** (Tiny-ViT V4, Epoch 73/100, anchor `27.72%`) | `run_tinyvit_groupwise_nl_comp.py --protected-group mlp`; `report_md/_gpt/v4_nl2_mlp_linear_comp_train_results_gpt.json`; checkpoint `checkpoints/_gpt/nl_mitigation/v4_nl2_mlp_linear_comp/V4_hybrid_standard_noise_hat_nl2_mlp_linear_comp_best.pt` | **CLAUDE-A preliminary decision: Option B (supplementary ablation).** MLP-only recovery is +60.07 pp; QKV-only fails. Does NOT unlock contribution #4 rewrite; stays supplementary. K-B cover letter v2 unblocked with "supplementary ablation" framing. |
| L2 | NL=1.5 retrain `best_acc=19.01% @ ep1`, final `9.76%` | `logs/_gpt/train_tinyvit_v4_nl_interp15_20260417_022400_gpt.log`, `v4_nl_interp15_results_gpt.json` | Already triaged: **not** a manuscript-facing anchor; only supports the wording "present gradient-scaling surrogate and training recipe". Keep as response-side evidence. |
| L3 | E3 learnable γ_comp: fixed γ=0.5 → 48.80%; learnable → **51.65%**; raw → 49.61%; learned γ_comp = **0.7398** (vs physical inverse 0.5000) | `run_learnable_gamma_compensation_gpt.py`; `report_md/_gpt/json_gpt/learnable_gamma_20260418_110011_g2.0_s42.json` | **Validates T2 theory.** Learned γ_comp (0.7398) deviates from physical inverse (0.5000) by +0.2398, confirming task-level adaptation dominates over strict physical inversion. Improvement over fixed: +2.85 pp. Candidate for supplementary theory-validation note. |

---

## 11. Numbers I could NOT immediately trace (gap list)

These need a follow-up Codex pass to add a stamped `(script, log/JSON, line/key)` reference. Until that is filled in, treat them as defensible by reasoning but not by single-line provenance citation.

| # | Number | Where it appears | Why not yet traced |
|:--|:--|:--|:--|
| G1 | A2.3 inverse-gamma `89.85% vs 84.04%` (the explicit pair behind H3 `+5.8 pp`) | `05_results.tex:46` | **RESOLVED.** Producing script: `compute_vit/scripts/_gpt/run_a23_experiments.py` (inferred from filename pattern). Canonical JSON: `compute_vit/report_md/json/a23_experiment_results.json`, key `"2.0_1e-11"` → `acc_compensated: 89.85`, `acc_raw: 84.04`, `delta: 5.81`. Also documented in `compute_vit/report_md/a23_physical_compensation_report.md`. |
| G2 | OPECT `88.53%` (H7) | abstract, intro | **RESOLVED.** Canonical JSON: `compute_vit/report_md/_gpt/json_gpt/literature_profile_eval.json`, key `"V4_Ensemble"` → `test_acc_mean: 88.53`, `eval_runs: 10`, `test_acc_std: 0.0827`. This is the Zhang2025 literature-profile zero-shot transfer (not the doctoral measured profile). |
| G3 | "p < 10⁻¹⁵" significance for Ensemble HAT vs standard HAT | `05_results.tex:63` | **RESOLVED (with caveat).** Data source: `compute_vit/report_md/_gpt/json_gpt/fresh_instance_eval.json` — `V4_Standard.instances` = [10.0]×10 (σ=0), `V4_Ensemble.instances` = [87.282, 88.612, 87.358, 84.066, 85.554, 85.182, 86.914, 87.768, 87.104, 83.81] (σ=1.535, n=10). Computed via `scipy.stats.ttest_ind` (Welch's, equal_var=False): t=149.25, p=1.38×10⁻¹⁶. **Caveat:** Standard HAT has zero variance (all 10 instances collapse to exactly 10.00%), so Welch's df formula is numerically unstable; scipy emits a precision-loss warning. For reviewer safety, recommend re-deriving with a one-sample t-test against the known chance-level μ₀=10.00%: t=149.25, df=9, p=2.22×10⁻¹⁶. Either way, p < 10⁻¹⁵ is defensible. |
| G4 | GM-E5 full-load stress test `89.61%` | CLAUDE_TASK Locked Numbers row | **RESOLVED.** Canonical JSON: `compute_vit/_archive/old-experiment-json/combined_stress_results.json`, key `"combined_stress_accuracy": 89.61`. Settings: `sigma_c2c: 0.02`, `sigma_d2d: 0.03`, `adc_bits: 6`, `ir_drop: 0.01`, `sneak: 0.01`, `inference_time: 1000.0`. Also logged in `compute_vit/logs/_gpt/combined_stress.log`. **Note:** File is in `_archive/`; for submission reproducibility, consider copying to `report_md/_gpt/json_gpt/`. |
| G5 | Energy / ToPS numbers in §6 / cover letter | discussion, cover letter | **RESOLVED.** Energy model: `compute_vit/analog_layers.py` (or `analog_layers_ensemble.py`), class `EnergyConstants` (E_analog_MAC=100 fJ, E_ADC_8bit=25 fJ, E_DAC_8bit=30 fJ, E_digital_INT8_MAC=0.4 pJ, E_digital_FP32_MAC=2.5 pJ) and class `EnergyProfiler` with method `compare_with_fp32_gpu(total_MACs)`. Baseline output: hybrid ~274 µJ, FP32 ref ~3137 µJ, raw ratio ~11.45×. The "~11×" and "~60% digital" claims in manuscript are rounded from these exacts. Manuscript rounding rationale documented in `BROADCAST_ENERGY_PRECISION_20260418.md`. |

---

## 12. Recommended hardening (after CX-A NL queue drains)

1. **Fill G1–G5 above** in a Codex pass — each gap is a `数字出处` defense liability.
2. **Tag every Locked Number in `08_appendix.tex`** with `\href{...}{[provenance]}` to the local report file (relative link OK; thesis defense reads it).
3. **Build a tiny `scripts/_gpt/check_locked_numbers.py`** that re-reads each JSON in §1–§10 above and asserts the value still matches the manuscript. Run before any pre-submission compile.
4. **Mirror this audit into Chinese** for the thesis defense binder; the auditor structure (`number → claim → script → JSON → blast`) maps cleanly.
5. **CLAUDE-A NL decision (when CX-A drains)** must update H6 + L1 in this file in the same commit as the manuscript text edit.

---

**End of audit. Updates required whenever any Locked Number row in `CANONICAL_RESULT_LOCK_gpt.md` or `CLAUDE_TASK_gpt.md §Locked Numbers` changes.**
