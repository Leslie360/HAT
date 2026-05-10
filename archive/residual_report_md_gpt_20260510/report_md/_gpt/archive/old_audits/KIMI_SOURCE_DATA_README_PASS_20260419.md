# Source-Data README Readability Audit

**Auditor:** Kimi Code CLI
**Date:** 2026-04-19
**Scope:** `compute_vit/outputs/submission_bundle_20260419/README_SUBMISSION.txt` and the nested `source_data_v1.zip` (→ `release_artifacts/source_data_v1.zip`).
**Persona:** Downstream user attempting to reproduce **Main Fig. 4** (accuracy comparison) from the bundled source-data zip.

---

## 1. Executive Summary

| Item | Status | Severity |
|---|---|---|
| `README_SUBMISSION.txt` top-level description | ✅ Mostly accurate | — |
| `source_data_v1.zip` README (`README.md`) | ⚠️ Needs improvement | Medium |
| `fig4_source_data.csv` completeness | ❌ **Incomplete** | **High** |
| Plotting scripts present in zip | ❌ **Missing** | **High** |
| JSON→figure value mapping documented | ❌ Missing | High |
| Broken file references in zip README | ❌ Present | Medium |
| Data consistency (CSV vs JSON) | ⚠️ Mismatches | Medium |

**Bottom line:** A user can open the CSV and see *some* of the numbers, but they cannot fully reproduce Fig. 4 from the zip alone because (a) the Flowers102 panel is missing from the CSV, (b) no plotting scripts are included, and (c) the README does not explain which JSON field corresponds to the plotted accuracy/error-bar value.

---

## 2. Detailed Findings

### 2.1 `README_SUBMISSION.txt` (bundle root)

**File:** `compute_vit/outputs/submission_bundle_20260419/README_SUBMISSION.txt`

| Line / Section | Issue | Severity |
|---|---|---|
| `Corresponding Author: TBD` | Placeholder still present | Low (editorial) |
| `Contact Email: TBD` | Placeholder still present | Low (editorial) |
| `Institution: TBD` | Placeholder still present | Low (editorial) |
| Line 61: "(raw data, CSVs, and plotting scripts)" | **False claim** — zip contains 0 scripts (76 files, all `.json`, `.csv`, `.md`). | **High** |
| Line 108: "code to reproduce every figure" | Same issue — no code is shipped in `source_data_v1.zip`. | **High** |

**Verdict:** The top-level README over-promises. It should either (a) remove the claim that plotting scripts are inside the zip, or (b) actually include them.

---

### 2.2 `source_data_v1.zip` → `fig4_source_data.csv`

**File:** `fig4_source_data.csv` (inside the zip)

**What it contains (12 rows):**
- ConvNeXt-Tiny × CIFAR-10 × {FP32, Standard-noise, HAT}
- Tiny-ViT-5M × CIFAR-10 × {FP32, Standard-noise, HAT}
- ConvNeXt-Tiny × CIFAR-100 × {FP32, Standard-noise, HAT}
- Tiny-ViT-5M × CIFAR-100 × {FP32, Standard-noise, HAT}

**What is MISSING:**
- **Flowers102** data for both architectures and all three conditions.

The manuscript’s Fig. 4 clearly has **three panels**: CIFAR-10, CIFAR-100, and Flowers102 (confirmed by `plot_paper_figures.py:486`: `datasets = ["cifar10", "cifar100", "flowers102"]`). The CSV only covers two of the three.

**CSV vs JSON value mismatches:**

| Architecture | Dataset | Condition | CSV value | Likely JSON source | JSON value | Discrepancy |
|---|---|---|---|---|---|---|
| ConvNeXt-Tiny | CIFAR-10 | Standard-noise | 69.32 | `convnext_full_results_gpt.json` C3 `mc_mean_acc` | 69.58 | **−0.26 pp** |
| ConvNeXt-Tiny | CIFAR-10 | HAT | 89.18 | `convnext_full_results_gpt.json` C4 `mc_mean_acc` | 89.71 | **−0.53 pp** |
| Tiny-ViT-5M | CIFAR-10 | FP32 | 98.06 | `tinyvit_v1_results_gpt.json` `best_test_acc` | 97.48 | **+0.58 pp** |
| Tiny-ViT-5M | CIFAR-10 | Standard-noise | 89.05 | `tinyvit_v2v7_results_gpt.json` V3 `best_test_acc` | 89.54 | **−0.49 pp** |
| Tiny-ViT-5M | CIFAR-10 | HAT | 90.05 | `tinyvit_v2v7_results_gpt.json` V4 `best_test_acc` | 91.94 | **−1.89 pp** |

> **Note:** The CSV notes say "3-seed mean" for Tiny-ViT FP32, which explains why 97.48 (single-seed JSON) ≠ 98.06 (CSV). However, the CSV does not cite which file(s) or seed IDs were averaged, so a user cannot independently verify the mean.

**Verdict:** The CSV is under-documented and incomplete. It needs:
1. Flowers102 rows.
2. A `source_file` column or header comment indicating which JSON file + experiment code each row derives from.
3. For aggregated values (e.g., multi-seed means), the seed list or a pointer to the raw per-seed JSONs.

---

### 2.3 `source_data_v1.zip` → `README.md` (inside the zip)

**File:** `README.md` (inside the zip)

**Strengths:**
- Lists the two CSV files and gives a high-level description.
- Provides a JSON index with manuscript references.

**Weaknesses:**

| Issue | Detail | Severity |
|---|---|---|
| **No schema documentation** | Does not explain which JSON keys map to plotted values. For example, some JSONs use `best_test_acc` while others use `mc_mean_acc`; the README never says "plotted accuracy = `mc_mean_acc` when available, otherwise `best_test_acc`". | High |
| **No experiment-code legend** | Codes like C1/C3/C4 and V1/V3/V4 are opaque. A user cannot know that C1 = FP32, C3 = Standard-noise, C4 = HAT without reading the plotting script source code. | High |
| **Broken file references** | `a23_experiment_results.json` and `learnable_gamma_*.json` are listed in the index but **do not exist** in the zip. | Medium |
| **Mis-named file references** | README lists `tinyvit_v4_ensemble_results_gpt.json` and `tinyvit_v4_nl2_hat_eval_results_gpt.json`; actual files in the zip are `v4_ensemble_results_gpt.json` and `v4_nl2_hat_eval_results_gpt.json` (no `tinyvit_` prefix). | Medium |
| **Missing Flowers102 mention** | The README does not flag that the CSV is missing Flowers102, nor does it tell the user to look at `convnext_flowers102_c134_results_gpt.json` and `tinyvit_flowers102_v134_results_gpt.json` for the third panel. | High |
| **No reproduction workflow** | There is no step-by-step guide (e.g., "1. Load `fig4_source_data.csv`, 2. Group by `architecture` and `condition`, 3. Plot grouped bars with `error_bar` as ±1 SD"). | High |

**Verdict:** The inner README is a good start but reads like an index rather than a reproducibility guide. It needs a schema section, a code-to-condition legend, and a brief "How to reproduce Fig. 4" paragraph.

---

### 2.4 Script references

**Finding:** No Python, shell, MATLAB, or R scripts are present in `source_data_v1.zip`.

The codebase *does* contain a plotting script (`paper/plot_paper_figures.py`), but it is **not included** in the source-data archive. That script:
- Loads JSONs from hard-coded paths like `GPT_REPORT_DIR / "json_gpt" / "tinyvit_cifar100_v134_results_gpt.json`.
- Uses internal helper functions (`accuracy_value()`, `accuracy_std()`, `has_stochastic_uncertainty()`) to decide which JSON field to plot.
- Expects a full repo checkout to run.

**Verdict:** Because the plotting script is absent, a downstream user cannot simply run code to regenerate the figure. They would need to reverse-engineer the logic from the main repository.

---

## 3. Proposed Edits (do NOT modify source unless noted)

### 3.1 `README_SUBMISSION.txt` — proposed wording changes

**Line 61 (current):**
```text
  └── source_data_v1.zip    -- Source data archive for all figures and tables
                              (raw data, CSVs, and plotting scripts)
```

**Proposed:**
```text
  └── source_data_v1.zip    -- Source data archive for all figures and tables
                              (raw experiment JSONs and summary CSVs;
                               plotting scripts are in the repository
                               paper/plot_paper_figures.py)
```

**Line 107–108 (current):**
```text
2. Source data (source_data_v1.zip) contains the underlying numerical data
   and code to reproduce every figure and table in the manuscript.
```

**Proposed:**
```text
2. Source data (source_data_v1.zip) contains the underlying numerical data
   for every figure and table. Plotting code is available in the repository
   at paper/plot_paper_figures.py.
```

> **Note:** These are wording corrections, not path fixes. Per instructions, **do not modify** `README_SUBMISSION.txt` unless explicitly told to.

---

### 3.2 `source_data_v1.zip` → `README.md` — proposed content additions

Add the following sections to the inner `README.md`:

```markdown
## Reproducing Main Fig. 4 (Accuracy Comparison)

Fig. 4 shows grouped bar charts across three datasets: CIFAR-10, CIFAR-100,
and Flowers102.  Two data sources are provided:

1. **Summary CSV:** `fig4_source_data.csv`
   - Columns: `architecture`, `dataset`, `condition`, `accuracy`, `error_bar`, `notes`
   - `condition` values: `FP32`, `Standard-noise`, `HAT`
   - `accuracy` is the plotted bar height.
   - `error_bar` is ±1 standard deviation (`n/a` for deterministic baselines).
   - ⚠️ **Known limitation:** This CSV currently omits the Flowers102 panel.
     Use the JSON files below for the complete dataset.

2. **Raw JSONs (authoritative source):**
   - **CIFAR-10:**
     - ConvNeXt: `convnext_full_results_gpt.json` — experiments C1 (FP32), C3 (Standard-noise), C4 (HAT)
     - Tiny-ViT: `tinyvit_v1_results_gpt.json` (V1, FP32) and `tinyvit_v2v7_results_gpt.json` (V3, V4)
   - **CIFAR-100:**
     - ConvNeXt: `convnext_cifar100_c134_results_gpt.json`
     - Tiny-ViT: `tinyvit_cifar100_v134_results_gpt.json`
   - **Flowers102:**
     - ConvNeXt: `convnext_flowers102_c134_results_gpt.json`
     - Tiny-ViT: `tinyvit_flowers102_v134_results_gpt.json`

### JSON schema note
Accuracies are reported in percentages.  For stochastic experiments
(Standard-noise and HAT), the plotted value is `mc_mean_acc` and the error
bar is `mc_std_acc`.  For deterministic baselines (FP32), use `best_test_acc`
(or `mc_mean_acc`, which is identical).  The `mc_*` fields reflect 10-run
Monte-Carlo inference statistics where available.

### Aggregated values
- Tiny-ViT FP32 CIFAR-10 and CIFAR-100 values are 3-seed means.
  The per-seed raw data is in the repository `logs/_gpt/multi_seed/`.
```

**Also fix broken index entries:**
- Remove `a23_experiment_results.json` and `learnable_gamma_*.json` from the index (or replace with correct filenames if they exist elsewhere).
- Correct `tinyvit_v4_ensemble_results_gpt.json` → `v4_ensemble_results_gpt.json`.
- Correct `tinyvit_v4_nl2_hat_eval_results_gpt.json` → `v4_nl2_hat_eval_results_gpt.json`.

---

### 3.3 `fig4_source_data.csv` — proposed fixes

**Must-fix (data gap):**
- Append Flowers102 rows for both architectures and all three conditions.
  Values can be extracted from:
  - `convnext_flowers102_c134_results_gpt.json`
  - `tinyvit_flowers102_v134_results_gpt.json`

**Should-fix (traceability):**
- Add a comment header (e.g., `# Source: convnext_full_results_gpt.json / experiment C1`) or an extra `source_json` + `experiment_code` column so each row is traceable.

---

## 4. Correct Paths / Typos to Fix Immediately

None of the broken items above are simple typos in `README_SUBMISSION.txt` itself; they are either:
- Missing content in the zip (CSV rows, scripts), or
- Incorrect claims in `README_SUBMISSION.txt` that require editorial judgment.

Therefore, **no edits were made to `README_SUBMISSION.txt`** per the instruction to avoid modifications unless the fix is clearly a broken path or typo.

---

## 5. Checklist for Authors

- [ ] **Add Flowers102 data** to `fig4_source_data.csv` (or create a separate `fig4_flowers102_source_data.csv`).
- [ ] **Document the JSON→CSV mapping** in the zip’s `README.md` (schema + experiment-code legend).
- [ ] **Fix broken file references** in the zip’s `README.md` (`a23_*`, `learnable_gamma_*`, `tinyvit_v4_*` names).
- [ ] **Decide on plotting scripts:** either include a minimal `reproduce_fig4.py` in the zip, or update `README_SUBMISSION.txt` to stop claiming scripts are inside the zip.
- [ ] **Resolve or explain CSV/JSON mismatches** (e.g., Tiny-ViT CIFAR-10 V3: 89.05 vs 89.54) so a user knows which number is canonical.
- [ ] **Fill in TBD fields** in `README_SUBMISSION.txt` before submission.

---

*End of audit.*
