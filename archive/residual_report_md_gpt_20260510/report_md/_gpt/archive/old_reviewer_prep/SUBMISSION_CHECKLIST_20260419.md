# Nature Communications Submission Checklist

**Manuscript:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision
**Date:** 2026-04-18
**Target Journal:** Nature Communications
**Bundle Path:** `compute_vit/outputs/submission_bundle_20260419/`

---

## 1. Manuscript Requirements

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1.1 | **Title** (≤150 characters recommended) | ✅ Present and correct | 70 characters. Concise, informative, no abbreviations. |
| 1.2 | **Abstract** (~150 words for NC) | ⚠️ Present but needs attention | 155 words. Slightly exceeds the ~150-word target for Nature Communications Articles. **Action:** Trim 5–10 words (e.g., compress parentheticals or remove "that are not directly captured by inorganic-memory simulators"). |
| 1.3 | **Main text length** (NC typical ~3,000–5,000 words) | ✅ Present and correct | 3,516 words (excluding abstract, appendix, references, captions). Well within typical limits. |
| 1.4 | **Keywords** (5–8) | ❌ Missing | No keyword block in the `.tex` source. **Action:** Add a `\paragraph{Keywords:}` line after the abstract with 5–8 terms (e.g., organic optoelectronics, compute-in-memory, vision transformer, hardware-aware training, edge inference, device simulation, analog computing). Note: NC also accepts keywords via the submission portal; confirm entry there if not added to the manuscript. |
| 1.5 | **Author list with affiliations and ORCIDs** | ⚠️ Present but needs attention | Only "Songqiao Li" is listed with no affiliation, address, or ORCID. **Action:** Add full institutional affiliation (department, university, city, country) and ORCID iD. NC strongly encourages ORCIDs for all authors and requires one for the corresponding author. |
| 1.6 | **Corresponding author marked** | ❌ Missing | No asterisk (`*`) or email is attached to the author name. **Action:** Add `\thanks{Corresponding author. Email: ...}` or equivalent, and mark with `*` in the author list. |
| 1.7 | **Competing interests statement** | ✅ Present and correct | Declared in `07_conclusion.tex`: "The authors declare no competing interests." |
| 1.8 | **Data availability statement** | ✅ Present and correct | Declared in `07_conclusion.tex`. Specifies public datasets (CIFAR-10/100, Flowers-102) and reviewer-accessible repository plan. |
| 1.9 | **Code availability statement** | ✅ Present and correct | Declared in `07_conclusion.tex`. Provides GitHub URL (`https://github.com/OrgOptEdge/compute_vit`) and notes reviewer-accessible archive at submission. |
| 1.10 | **Acknowledgements** | ❌ Missing | No acknowledgements section found. **Action:** Add `\section*{Acknowledgements}` before References if funding sources, discussions, or institutional support should be recognized; otherwise explicitly mark as "Not applicable" if truly none. |
| 1.11 | **Author contributions** | ✅ Present and correct | Declared in `07_conclusion.tex`: "S.L. conceived the framework, implemented the simulator, conducted all experiments, and wrote the manuscript." |

---

## 2. Figures and Tables

| # | Item | Status | Notes |
|---|------|--------|-------|
| 2.1 | **All figures numbered consecutively** | ✅ Present and correct | 5 main-text figures (LaTeX auto-numbers Fig. 1–5). 14 supplementary figures numbered S1–S14 via `\renewcommand{\thefigure}{S\arabic{figure}}`. |
| 2.2 | **All tables numbered consecutively** | ✅ Present and correct | 1 main-text table (`tab:exp-notation`) + 5 appendix tables. 16 supplementary tables numbered S1–S16 via `\renewcommand{\thetable}{S\arabic{table}}`. |
| 2.3 | **Figure captions are standalone** | ✅ Present and correct | All captions describe the panel content without requiring the main text (e.g., "Cross-dataset accuracy under canonical deployment...", "Iso-accuracy contour map..."). |
| 2.4 | **All figures referenced in text** | ⚠️ Present but needs attention | `fig:ensemble-hat-concept` (Results, line 69) has a `\label{}` but is **never called with `\ref{}`** in the main narrative. `tab:exp-notation` is also unreferenced. **Action:** Add `Figure~\ref{fig:ensemble-hat-concept}` near the first discussion of Ensemble HAT (e.g., around Eq. 2 or Section 5.5). Add `Table~\ref{tab:exp-notation}` when V1–V8 notation is first used (e.g., in Section 5.1 or 4). |
| 2.5 | **Minimum resolution: 300 DPI for raster, vector preferred** | ✅ Present and correct | All figures are provided as vector PDFs (primary) plus PNG fallbacks. No scanned images. |
| 2.6 | **Color figures: check accessibility for colorblind readers** | ⚠️ Present but needs attention | No explicit colorblind-safe palette verification found. Contour maps, accuracy bars, and Pareto plots rely on color differentiation. **Action:** Run figures through a CVD simulator (e.g., Color Oracle, Coblis) to confirm distinguishability for deuteranopia/protanopia. Consider adding hatching, markers, or line styles in addition to color for critical data series. |
| 2.7 | **Display item count** (NC Article limit: ≤10 figures + tables combined) | ⚠️ Present but needs attention | Main text contains 5 figures + 1 table = 6 display items. The appendix (compiled into main PDF) adds 5 more tables, bringing the manuscript total to **11 display items** if appendix tables count toward the limit. **Action:** Verify NC policy on whether appendix tables count; if they do, consider moving 1–2 appendix tables entirely into the Supplementary Information to stay within the 10-item guideline. |

---

## 3. References

| # | Item | Status | Notes |
|---|------|--------|-------|
| 3.1 | **All references cited in text appear in bibliography** | ✅ Present and correct | All 48 `\citep`/ `\cite` calls resolve to entries in `refs_gpt.bib`. No compilation warnings for missing citations. |
| 3.2 | **All DOIs present where available** | ✅ Present and correct | All 48 bibliography entries contain a `doi` field. Verified programmatically. |
| 3.3 | **Consistent formatting** (Nature numbered style) | ⚠️ Present but needs attention | Current style is `unsrtnat` (numbered, sorted by appearance). Nature Communications uses a specific Nature numbered reference format (e.g., `sn-nature.bst`). **Action:** For initial submission this is acceptable, but if a revision is requested, switch to the Springer Nature LaTeX template (`sn-jnl` class with `nature` option and `sn-nature.bst`) to match production requirements exactly. |
| 3.4 | **No personal communications without permission** | ✅ Present and correct | No "personal communication" or "unpublished" citations found in the text or bibliography. |
| 3.5 | **Reference count** (NC Article guideline: ~60) | ✅ Present and correct | 48 references. Within the typical ~60-reference cap for NC Articles. |

---

## 4. Supplementary Information

| # | Item | Status | Notes |
|---|------|--------|-------|
| 4.1 | **Supplementary figures numbered S1, S2, etc.** | ✅ Present and correct | 14 supplementary figures numbered S1–S14. Renumbering command is active. |
| 4.2 | **Supplementary tables numbered ST1, ST2, etc.** | ⚠️ Present but needs attention | Tables are numbered S1–S16 (same prefix as figures). NC convention is "Supplementary Table 1" (or ST1 if abbreviated). **Action:** The current rendering is acceptable for initial submission, but verify whether NC production requires a distinct prefix. The `\renewcommand{\thetable}{S\arabic{table}}` produces "Table S1", which is standard. |
| 4.3 | **Source data provided for all main figures** | ✅ Present and correct | `source_data/source_data_v1.zip` exists and contains underlying numerical data and plotting scripts for all figures and tables. README confirms contents. |
| 4.4 | **Additional methods in supplementary** | ✅ Present and correct | Extended Methods section present (operator mapping, weight-to-conductance pipeline, system architecture, frontend theory, energy model, Sobol methodology). |
| 4.5 | **Supplementary Information PDF size** | ⚠️ Present but needs attention | `supplementary_main.pdf` is **2.5 MB** (under 10 MB), but contains many high-resolution raster plots. **Action:** If the portal imposes a lower per-file limit, compress images or submit as separate files. |
| 4.6 | **Duplicate labels across main appendix and supplementary** | ⚠️ Present but needs attention | 5 table labels are duplicated (`tab:v4-three-seed-summary`, `tab:provenance`, `tab:sensitivity`, `tab:sensitivity-ci`, `tab:retention-comparison`) across `08_appendix.tex` and `supplementary.tex`. **Action:** Disambiguate with suffixes (e.g., `-app` and `-supp`) in case the documents are ever merged. Currently benign because they compile as separate root documents. |

---

## 5. Editorial Requirements

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5.1 | **Cover letter explains significance and audience** | ✅ Present and correct | Cover letter (`cover_letter.pdf`) contains a 150-word editorial summary, a "Why Nature Communications?" paragraph, key contributions, and transparency disclosures. Explains cross-disciplinary significance (materials + ML systems + emerging computing). |
| 5.2 | **Suggested reviewers (3–5) with emails** | ❌ Missing | Cover letter states: "Suggested and excluded reviewers will be provided through the submission system." No separate reviewer list file exists in the bundle. **Action:** Prepare a list of 3–5 suggested reviewers with names, emails, affiliations, and 1–2 sentences on why each is qualified. Upload via the submission portal or attach as a separate file. |
| 5.3 | **Opposed reviewers declared if any** | N/A | No opposed reviewers are declared. If none exist, no action needed beyond confirming this in the submission system declarations. |
| 5.4 | **Previous submissions disclosed** | ✅ Present and correct | Cover letter explicitly states: "None; this work is submitted exclusively to Nature Communications." and "Prior Publication: None." |
| 5.5 | **Related manuscripts disclosed** | ✅ Present and correct | Cover letter notes no overlapping manuscripts under consideration elsewhere. |
| 5.6 | **Preprint policy compliance** | ✅ Present and correct | Cover letter states: "Preprint: None; this work is submitted exclusively to Nature Communications." |
| 5.7 | **Reporting Summary** | ❌ Missing | Nature Communications requires a completed **Nature Portfolio Reporting Summary** for all primary research submissions. **Action:** Download the Reporting Summary form from the NC author guidelines, complete it (covering statistical methods, data exclusions, replication details), and upload with the submission. |

---

## 6. Technical

| # | Item | Status | Notes |
|---|------|--------|-------|
| 6.1 | **All LaTeX compiles without errors** | ✅ Present and correct | Both `main.tex` and `supplementary_main.tex` compile cleanly via pdfLaTeX → BibTeX → 2× pdfLaTeX. No undefined citations or environments. |
| 6.2 | **No broken cross-references** | ✅ Present and correct | Verified: zero `??` placeholders in `main.pdf`, `supplementary_main.pdf`, and `cover_letter.pdf`. (A broken `??` in the cover letter was fixed during the 2026-04-18 pre-submission gate.) |
| 6.3 | **PDFs are text-searchable** (not scanned images) | ✅ Present and correct | All PDFs are generated directly from LaTeX source. Text extraction (`pdftotext`) confirms selectable text throughout. |
| 6.4 | **File sizes reasonable** (<10 MB per PDF recommended) | ✅ Present and correct | `main.pdf`: ~415 KB. `cover_letter.pdf`: ~94 KB. `supplementary_main.pdf`: ~2.5 MB. All well under 10 MB. |
| 6.5 | **No proprietary fonts or non-standard packages** | ✅ Present and correct | Uses standard CTAN packages (`geometry`, `graphicx`, `booktabs`, `amsmath`, `natbib`, `hyperref`, etc.). No custom `.sty` or `.cls` files required. |
| 6.6 | **README / instructions for editorial production** | ✅ Present and correct | `README_SUBMISSION.txt` documents file structure, compilation instructions, and figure formats. **Action:** Fill in remaining placeholders (`TBD` for Corresponding Author, Contact Email, Institution on lines 7–9). |

---

## Summary of Actions Required Before Submission

### 🔴 Must Fix (Blockers)
| Priority | Item | Effort |
|----------|------|--------|
| 1 | Add **affiliation, ORCID, and corresponding-author email** to the title page | 5 min |
| 2 | Add **Keywords** (5–8 terms) to the manuscript | 5 min |
| 3 | Complete and upload the **Nature Portfolio Reporting Summary** | 15–30 min |
| 4 | Add **Acknowledgements** section (or explicitly state "None") | 5 min |
| 5 | Prepare **suggested reviewer list** (3–5 names + emails) | 15 min |

### 🟡 Strongly Recommended (5–15 min fixes)
| Priority | Item | Effort |
|----------|------|--------|
| 6 | Add `\ref` call-outs for `fig:ensemble-hat-concept` and `tab:exp-notation` | 5 min |
| 7 | Trim abstract from **155 to ~150 words** | 10 min |
| 8 | Verify **colorblind accessibility** for main figures (contour map, accuracy bars) | 15 min |
| 9 | Disambiguate **duplicate labels** across appendix and supplementary | 10 min |
| 10 | Confirm **display item count** policy (11 items including appendix tables) | 5 min |

### 🟢 Nice to Have
| Priority | Item | Effort |
|----------|------|--------|
| 11 | Fill in `README_SUBMISSION.txt` placeholders | 2 min |
| 12 | Add narrative pointers for standalone supplementary figures | 10 min |
| 13 | Switch to `sn-jnl` / `sn-nature.bst` for production-ready formatting (revision stage) | 30 min |

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Corresponding Author | | | |
| Co-author(s) | | | |

---

*Checklist generated based on Nature Communications author guidelines (verified against live guidelines as of 2026-04-18) and inspection of the submission bundle at `compute_vit/outputs/submission_bundle_20260419/`.*
