# 🎯 Executive Dashboard — Project Status

**Generated:** 2026-04-19
**Project:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision
**Target Journal:** *Nature Communications*
**Bundle:** `outputs/submission_bundle_20260419/`

---

## 1. 📋 Project Overview

| Field | Status |
|:---|:---|
| **Title** | Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision |
| **Target Journal** | *Nature Communications* |
| **Author** | Songqiao Li |
| **Submission Readiness** | 🟡 **CONDITIONAL PASS** (~95%) |
| **Verdict** | Content-complete; 2 minor cross-reference gaps + cleanup remaining |
| **Blockers** | 2 unreferenced main-text labels (`fig:ensemble-hat-concept`, `tab:exp-notation`) |
| **Next Milestone** | Final sign-off + upload |

---

## 2. 🔒 Core Results Lock (Trusted Data)

All numbers below are **manuscript-locked** and verified by `check_locked_numbers.py` (16/16 PASS).

| Result | Value | Provenance / Context |
|:---|:---|:---|
| **Ensemble HAT fresh-instance** | **86.37 ± 1.54%** | `fresh_instance_eval.json` (10 instances × MC) |
| **V4 canonical (best checkpoint)** | **91.94%** | Training best; CIFAR-10 standard HAT (`tinyvit_v2v7_results_gpt.json`) |
| **V4 three-seed aggregate** | **87.95 ± 0.27%** | Appendix Table S1; contour/ensemble MC context |
| **NL = 2.0 global (severe)** | **27.72 ± 0.82%** | `v4_nl2_hat_eval_results_gpt.json` |
| **MLP-only NL mitigation** | **87.79%** | `v4_nl2_mlp_linear_comp_train_results_gpt.json` @ ep73 |
| **all-linear NL mitigation** | **87.49%** | `v4_nl2_all_linear_comp_train_results_gpt.json` @ ep59 |
| **QKV-only NL mitigation** | **18.72%** | Collapse confirmed; `v4_nl2_qkv_linear_comp_train_results_gpt.json` @ ep2 |
| **attn_proj-only NL mitigation** | **18.86%** | Collapse confirmed; stopped @ ep54, best @ ep0 |
| **OPECT zero-shot transfer** | **88.53 ± 0.08%** | `n=10` fresh-instance evaluations; literature-anchored profile |
| **Inverse-gamma recovery** | **+5.8 pp** at γ_phys=2.0 | 89.85% vs 84.04%; single-seed deterministic (`a23_experiment_results.json`) |
| **ADC cliff (Sobol)** | **S_ADC = 0.98** | 63-point D2D–ADC grid; sub-6-bit collapse confirmed |
| **Standard HAT fresh collapse** | **10.00%** | Chance level on every fresh D2D instance |
| **V2 canonical (digital baseline)** | **97.39%** | Deterministic; CIFAR-10 Tiny-ViT V2 |
| **C1 ConvNeXt FP32** | **90.74%** | `convnext_c1_results_gpt.json` |
| **C4 ConvNeXt HAT** | **89.91%** | Best checkpoint; CIFAR-10 standard HAT |

---

## 3. 📄 Manuscript Status

| Document | Pages | Words / Size | Status |
|:---|:---:|:---|:---:|
| **Main text** | 15 | ~3,705 words | ✅ Compiled, clean |
| **Supplementary** | 21 | 2.5 MiB PDF | ✅ Compiled, clean |
| **Cover letter** | 2 | 92 KiB PDF | ✅ Compiled, clean |
| **Figures (main)** | 5 | — | ✅ All render |
| **Figures (supplementary)** | 14 | — | ✅ All render |
| **Tables (main)** | 1 | — | ✅ Complete |
| **Tables (appendix)** | 5 | — | ✅ Complete |
| **Tables (supplementary)** | 16 | — | ✅ Complete |
| **References** | 48 total | 37 cited / 11 orphaned | ✅ No missing citations |
| **Response letter draft** | — | Phase 3 complete | ✅ `REVIEWER_RESPONSE_DRAFT_gpt.md` |
| **Rebuttal-ready table** | — | `REBUTTAL_READY_TABLE_20260419.md` | ✅ Complete |

**LaTeX Build Health:** Both `main.tex` and `supplementary_main.tex` compile cleanly (pdfLaTeX → BibTeX → 2× pdfLaTeX) with **zero** broken `??` references.

---

## 4. 🖥️ GPU Experiments Pipeline

**Current GPU Status:** 🟢 **IDLE** — No active training jobs. All scheduled NL-mitigation ablations are complete.

| Experiment | Status | Best Result | Final Epoch | Notes |
|:---|:---|:---|:---:|:---|
| MLP-only NL mitigation | ✅ Complete | **87.79%** | 73 / 100 | Primary recovery path |
| all-linear NL mitigation | ✅ Complete | **87.49%** | 59 / 100 | Upper-bound control |
| QKV-only NL mitigation | ✅ Complete | **18.72%** | 2 / 100 | Structural collapse |
| attn_proj-only NL mitigation | ⏹️ Stopped | **18.86%** @ ep0 | 54 / 100 | Collapse confirmed; mirrors QKV pattern |
| Severe NL=2.0 baseline | ✅ Baseline | **27.72 ± 0.82%** | — | Anchor for all comparisons |
| NL=1.0 global baseline | ✅ Baseline | **91.94%** | — | Upper bound |

**Interpretation:** MLP-only and all-linear converge to ~87–88%, confirming the MLP path is the dominant recoverable bottleneck. Both attention-side linearizations (QKV and projection) collapse structurally.

---

## 5. ✅ Quality Gate Results

| Audit | Result | Detail |
|:---|:---:|:---|
| **Locked numbers** | 🟢 **16/16 PASS** | `check_locked_numbers.py` confirms all manuscript claims match source JSONs |
| **Citation integrity** | 🟢 **PASS** | 37/48 refs cited; 0 missing citations; 0 duplicate keys |
| **JSON consistency** | 🟡 **7 issues investigated** | 4 critical + 3 moderate; recommendations documented; stale files identified |
| **Proofread** | 🟢 **Complete** | 1 critical (OPECT error bars) + 5 grammar + 15+ style fixes; all PDFs recompiled |
| **Figure audit** | 🟢 **17 figures OK** | 2 optimized (oversized PNGs flagged); all captions present; all files resolve |
| **Pre-submission gate** | 🟡 **CONDITIONAL** | 1 blocker fixed in-gate (cover letter `??`); 2 missing `\ref` call-outs remain |
| **Cross-reference integrity** | 🟢 **PASS** | 0 undefined refs; 5 duplicate labels across separate documents (non-blocking) |
| **Table completeness** | 🟢 **PASS** | 22 tables, all captioned, no empty data cells |
| **Compile verification** | 🟢 **PASS** | `main.pdf` + `supplementary_main.pdf` + `cover_letter.pdf` all clean |

---

## 6. 📝 Action Items

### 🔴 Blockers (must fix before submission)
- [ ] **Add `\ref` for `fig:ensemble-hat-concept`** in `05_results.tex` near first Ensemble HAT discussion
- [ ] **Add `\ref` for `tab:exp-notation`** in `05_results.tex` or `04_experimental_setup.tex` on first V1–V8 mention
- [ ] **Final user sign-off** on locked manuscript PDFs

### 🟡 Recommended (should fix if time permits)
- [ ] **Disambiguate duplicate labels** across `08_appendix.tex` and `supplementary.tex` (append `-app` / `-supp` suffix)
- [ ] **Fill README placeholders** (`[YOUR NAME]`, `[YOUR EMAIL]`, `[YOUR INSTITUTION]`) in `README_SUBMISSION.txt`
- [ ] **Clean stale JSON files** — move `report_md/json/convnext_results.json` (47.89% stale) to `_archive/`
- [ ] **Run multi-seed evals** for NL mitigation compensation lanes to populate `mean_eval_acc` / `std_eval_acc`
- [ ] **Remove backup `.bak` files** from `paper/latex_gpt/sections/` before submission

### 🟢 Deferred (post-submission or future work)
- [ ] **Zenodo Tier-A checkpoint deposit** (~1.5 GB) — needs DOI for cover letter / methods footnote
- [ ] **Pin `requirements.txt`** to exact PyTorch/CUDA patch versions
- [ ] **GPU-deferred thesis experiments** — MLP-Linear + Ensemble HAT joint training; all-linear fresh-instance eval
- [ ] **E5 layer-wise gamma sensitivity** sweep — script prep in progress, thesis scope

---

## 7. 📦 File Inventory

### Submission Deliverables

| File | Path | Size |
|:---|:---|:---:|
| **Manuscript PDF** | `outputs/submission_bundle_20260419/manuscript/main.pdf` | 407 KiB |
| **Supplementary PDF** | `outputs/submission_bundle_20260419/supplementary/supplementary_main.pdf` | 2.5 MiB |
| **Cover Letter PDF** | `outputs/submission_bundle_20260419/cover_letter/cover_letter.pdf` | 92 KiB |
| **Source Data ZIP** | `release_artifacts/source_data_v1.zip` | 144 KiB (76 files) |
| **Reviewer Archive** | `outputs/reviewer_archive_20260419.tar.gz` | 1.3 MiB |
| **Source Data Manifest** | `release_artifacts/source_data_v1_MANIFEST.md` | — |

### Key Source Files

| File | Path | Size |
|:---|:---|:---:|
| Main LaTeX source | `paper/latex_gpt/main.tex` | — |
| Supplementary LaTeX source | `paper/latex_gpt/supplementary_main.tex` | — |
| Cover letter source | `paper/latex_gpt/cover_letter.tex` | — |
| Bibliography | `paper/latex_gpt/refs_gpt.bib` | 48 entries |
| Locked results memo | `paper/CANONICAL_RESULT_LOCK_gpt.md` | — |

### Report / Coordination Files

| File | Path | Size |
|:---|:---|:---:|
| This dashboard | `report_md/_gpt/EXECUTIVE_DASHBOARD_20260419.md` | — |
| Submission readiness checklist | `report_md/_gpt/SUBMISSION_READINESS_CHECKLIST_20260419.md` | — |
| Pre-submission gate | `report_md/_gpt/PRE_SUBMISSION_GATE_20260419.md` | — |
| Final proofread report | `report_md/_gpt/FINAL_PROOFREAD_REPORT_20260419.md` | — |
| Citation integrity | `report_md/_gpt/CITATION_INTEGRITY_20260419.md` | — |
| JSON consistency audit | `report_md/_gpt/JSON_CONSISTENCY_20260419.md` | ~20 KiB |
| Figure audit | `report_md/_gpt/FIGURE_AUDIT_20260419.md` | ~20 KiB |
| Response letter draft | `report_md/_gpt/RESPONSE_LETTER_FINAL_20260419.md` | — |
| Rebuttal-ready table | `report_md/_gpt/REBUTTAL_READY_TABLE_20260419.md` | — |
| All `_gpt` reports (180 files) | `report_md/_gpt/` | 4.6 MiB total |

---

## 8. 🏁 Bottom Line

> **The manuscript is content-complete, compiles cleanly, and all locked numbers are verified.**
>
> **Remaining work before submission:** add 2 `\ref` call-outs (~2 minutes), obtain final user sign-off, and optionally perform a quick JSON/file cleanup.
>
> **No GPU experiments are required for submission.** All NL-mitigation ablations are complete and their results are already incorporated into the supplementary table.

---

*Dashboard compiled from: `CANONICAL_RESULT_LOCK_gpt.md`, `PRE_SUBMISSION_GATE_20260419.md`, `SUBMISSION_READINESS_CHECKLIST_20260419.md`, `JSON_CONSISTENCY_20260419.md`, `CITATION_INTEGRITY_20260419.md`, `FIGURE_AUDIT_20260419.md`, `FINAL_PROOFREAD_REPORT_20260419.md`, `NL_LANE_RESULTS_20260418.md`, and live filesystem audit.*
