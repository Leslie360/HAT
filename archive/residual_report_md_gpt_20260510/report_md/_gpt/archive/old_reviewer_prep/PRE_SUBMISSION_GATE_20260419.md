# Pre-Submission Quality Gate Report

**Date:** 2026-04-18
**Bundle:** `outputs/submission_bundle_20260419/`
**Target Journal:** Nature Communications
**Verdict:** **CONDITIONAL** (one blocker fixed during gate; two minor reference gaps remain)

---

## 1. File Completeness

**Status: PASS**

All required files are present in the submission bundle:

| Path | Status |
|------|--------|
| `manuscript/main.tex` | ✅ Present |
| `manuscript/main.pdf` | ✅ Present |
| `manuscript/refs_gpt.bib` | ✅ Present |
| `manuscript/sections/00_abstract.tex` | ✅ Present |
| `manuscript/sections/01_introduction.tex` | ✅ Present |
| `manuscript/sections/02_related_work.tex` | ✅ Present |
| `manuscript/sections/03_methodology.tex` | ✅ Present |
| `manuscript/sections/04_experimental_setup.tex` | ✅ Present |
| `manuscript/sections/05_results.tex` | ✅ Present |
| `manuscript/sections/06_discussion.tex` | ✅ Present |
| `manuscript/sections/07_conclusion.tex` | ✅ Present |
| `manuscript/sections/08_appendix.tex` | ✅ Present |
| `manuscript/figures/` (5 figure pairs: pdf+png) | ✅ Present |
| `supplementary/supplementary_main.tex` | ✅ Present |
| `supplementary/supplementary_main.pdf` | ✅ Present |
| `supplementary/supplementary.tex` | ✅ Present |
| `supplementary/refs_gpt.bib` | ✅ Present |
| `supplementary/figures/` (17 figure pairs/files) | ✅ Present |
| `cover_letter/cover_letter.pdf` | ✅ Present |
| `source_data/source_data_v1.zip` | ✅ Present (symlink to `release_artifacts/`) |
| `README_SUBMISSION.txt` | ✅ Present |

**Note:** `README_SUBMISSION.txt` contains placeholders (`[YOUR NAME]`, `[YOUR EMAIL]`, `[YOUR INSTITUTION]`) on lines 7–9. These are expected in a template but must be filled before archival upload.

**Note:** `source_data_v1.zip` is a symlink. The README correctly advises using `tar -ch` to dereference symlinks when creating the final archive.

---

## 2. LaTeX Build Health

**Status: PASS** (after in-gate fix)

| Document | Compilation | Errors | Broken `??` refs |
|----------|-------------|--------|------------------|
| `main.tex` | ✅ Clean (pdfLaTeX → BibTeX → 2× pdfLaTeX) | None | 0 |
| `supplementary_main.tex` | ✅ Clean (same cycle) | None | 0 |
| `cover_letter.pdf` | ✅ Recompiled and copied to bundle | None | 0 (was 1) |

**Issue found & fixed:** The cover letter PDF contained a broken reference:

> "both attention-side linearizations collapse structurally (supplementary Table ??)"

**Root cause:** `cover_letter.tex` used `\ref{tab:supp-nl-ablation}` but is a standalone document that does not include the supplementary source.
**Fix applied:** Replaced the `\ref` with the resolved literal "Supplementary Table S16" in the source (`paper/latex_gpt/cover_letter.tex`, line 40), recompiled with pdfLaTeX, and copied the updated PDF into the bundle.
**Verification:** `pdftotext` no longer reports `??` in any of the three PDFs.

Tectonic shows a benign "internal consistency problem when checking if .bbl changed" warning during rerun detection; this is a Tectonic-specific heuristic quirk and does not affect output correctness.

---

## 3. Cross-Reference Integrity

**Status: PASS** (main + supplementary documents)

### 3.1 Undefined references
- **None** after full compilation cycle in either document.

### 3.2 Duplicate labels
Five labels are duplicated across `manuscript/sections/08_appendix.tex` and `supplementary/supplementary.tex`:

| Label | Appendix line | Supplementary line |
|-------|--------------|--------------------|
| `tab:v4-three-seed-summary` | 15 | 201 |
| `tab:provenance` | 34 | 220 |
| `tab:sensitivity` | 76 | 267 |
| `tab:sensitivity-ci` | 93 | 284 |
| `tab:retention-comparison` | 119 | 336 |

**Impact:** None at compile time because the appendix and supplementary are separate root documents. However, if the two documents are ever merged, these will produce "multiply-defined label" warnings. Recommended action: append a suffix (e.g., `-app`, `-supp`) to disambiguate if a unified build is ever attempted.

### 3.3 Unreferenced labels in main manuscript
The following main-text figures/tables have `\label{}` but are never called with `\ref{}` anywhere in the main document:

| Label | File | Line | Severity |
|-------|------|------|----------|
| `fig:ensemble-hat-concept` | `05_results.tex` | 69 | **Should fix** |
| `tab:exp-notation` | `04_experimental_setup.tex` | 12 | **Should fix** |

**`fig:ensemble-hat-concept`:** This figure appears in the Results section but is never referenced in the narrative. It should receive a `Figure~\ref{fig:ensemble-hat-concept}` call-out when Ensemble HAT is first introduced (e.g., near the discussion of Eq.~\ref{eq:hat-ensemble} or in Section~\ref{subsec:nl-hat-stress}).

**`tab:exp-notation`:** The V1–V8 notation table is never referenced. Because these IDs are used extensively in Results (e.g., "V2 retains 97.39%", "V4 collapses"), the table should be explicitly introduced with `Table~\ref{tab:exp-notation}` on first use.

*Appendix-only labels (e.g., `tab:v4-three-seed-summary`, `tab:provenance`) are intentionally presented as self-contained data tables and are acceptable without inline references.*

---

## 4. Table Completeness

**Status: PASS**

- **22 tables** total: 6 in main manuscript (including appendix) + 16 in supplementary.
- **Every `table` environment contains a `\caption`.**
- **No empty or placeholder cells** were found in data rows. Dashes (`-`, `--`) are used legitimately for "not applicable" or "same value repeated" entries.

**Minor note:** `supplementary/supplementary.tex:184` contains a single dash `-` in the CIFAR-100 column for the V6 row, indicating that the CIFAR-100 V6 experiment was not run. This is an acceptable convention, but a brief footnote or explicit "n/a" would be slightly clearer.

---

## 5. Figure Completeness

**Status: PASS**

- **19 figures** total: 5 in main manuscript + 14 in supplementary.
- **Every `figure` environment contains a `\caption`.**
- **Every `\includegraphics` resolves to an existing file** (PDF or PNG) in the expected `figures/` directory.

The manuscript `\graphicspath` is set to `{./figures/}` in both root files, which is correct.

**Note:** Some supplementary figures (e.g., `fig:supp-pareto`, `fig:supp-noise-sensitivity`, `fig:supp-zero-shot-transfer`, `fig:supp-asymmetry-concept`, `fig:supp-nonideality`) do not carry an explicit `\ref` call-out in the supplementary text. They are acceptable as standalone supporting panels, but adding a brief narrative pointer would improve readability.

---

## 6. Manuscript Metadata

**Status: PASS**

| Field | Status | Detail |
|-------|--------|--------|
| **Title** | ✅ Present | "Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision" |
| **Authors** | ✅ Present | Songqiao Li (complete for single-author submission) |
| **Abstract** | ✅ Within limits | **155 words** (Nature Communications target: 150–250 words) |
| **Keywords** | ⚠️ Not in `.tex` | Typically entered via submission portal; not a blocker |
| **Competing Interests** | ✅ Present | Declared in `07_conclusion.tex` |
| **Data Availability** | ✅ Present | Declared in `07_conclusion.tex` |
| **Code Availability** | ✅ Present | URL and reviewer-access archive noted |

---

## 7. Submission Checklist

| Metric | Count | Notes |
|--------|-------|-------|
| **Main text word count** (excluding refs, captions, appendix) | **~3,705 words** | Well within typical Nature Communications limits (~5,000 words for Articles) |
| **Main text figures** | **5** | fig4, fig5, fig_contour_map, figS3_ensemble_hat, fig10 |
| **Main text tables** | **1** | `tab:exp-notation` (plus 5 appendix tables) |
| **Appendix tables** | **5** | v4-three-seed, provenance, sensitivity, sensitivity-ci, retention-comparison |
| **Supplementary figures** | **14** | Includes architecture diagrams, Sobol maps, retention curves, attention maps, etc. |
| **Supplementary tables** | **16** | Operator mapping, baselines, result summary, sensitivity sweeps, ablations, risk matrix |
| **References** | **48** | In `refs_gpt.bib` |
| **Supplementary sections** | **1 section + 12 subsections + 16 subsubsections** | ~21 pages PDF |

---

## Blockers & Recommended Actions

### Blockers (must fix before submission)
1. ~~**Cover letter broken reference**~~ — **FIXED during this gate.** The `??` has been replaced with the resolved table number and the PDF updated.

### Strongly recommended fixes (5-minute edits)
2. **Add a `\ref` call-out for `fig:ensemble-hat-concept`** in `05_results.tex` near the first discussion of Ensemble HAT (e.g., around line 41 or 63).
3. **Add a `\ref` call-out for `tab:exp-notation`** in `05_results.tex` when V1–V8 notation is first used (e.g., line 13 where "V2" is first mentioned), or add a forward reference in `04_experimental_setup.tex` itself.

### Nice-to-have improvements
4. **Disambiguate duplicate labels** across `08_appendix.tex` and `supplementary.tex` by adding a suffix (`-app` / `-supp`) if there is any chance the files will be merged into a single build.
5. **Fill in README placeholders** (`[YOUR NAME]`, `[YOUR EMAIL]`, `[YOUR INSTITUTION]`) before final archival upload.
6. **Add explicit narrative pointers** for a few standalone supplementary figures/tables that currently lack `\ref` mentions (e.g., `fig:supp-pareto`, `fig:supp-noise-sensitivity`).

---

## Overall Verdict: CONDITIONAL

The submission package is **scientifically complete, compiles cleanly, and contains no broken PDF references** after the in-gate cover-letter fix. The two unreferenced main-text elements (`fig:ensemble-hat-concept` and `tab:exp-notation`) are the only remaining items that could generate editorial queries or reviewer confusion. They are trivial to fix (add two `\ref` call-outs). Once those are addressed, the package is **READY** for submission.
