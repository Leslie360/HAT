<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Thesis v0 Lock Checklist

**Document:** `compute_vit/paper/thesis/main.tex` + 8 chapter files + `acknowledgements.tex`
**Generated:** 2026-04-21
**Checker:** Kimi Code CLI subagent (Task K-X16)
**Page count (single-pass pdflatex):** 118 pages

---

## 1. All 8 chapters compile clean ✅/❌
**Status: ❌ FAIL**

A single-pass `pdflatex` produces a 118-page PDF, but with unresolved bibliography and forward-references:
- `LaTeX Warning: There were undefined references.`
- `Package natbib Warning: There were undefined citations.`
- `No file main.bbl.` — BibTeX has not been run.
- Multiple `Reference '...' undefined` warnings at the end of the document (pages 112–115) because only one LaTeX pass was executed and `.aux` files were not fully settled.

**What needs to change:**
- Run `bibtex main` (or `biber main`) to resolve citations and generate `main.bbl`.
- Run `pdflatex` **twice more** after BibTeX to resolve forward references and the table-of-contents page numbers.

---

## 2. Table of contents generated ✅/❌
**Status: ✅ PASS**

`\tableofcontents` is present in `main.tex` (line 88). The PDF contains a populated TOC after compilation.

---

## 3. All figures visible in PDF ✅/❌
**Status: ✅ PASS**

All 8 unique figure paths referenced via `\includegraphics` resolve to existing files in `../latex_gpt/figures/`:
- `figS3_ensemble_hat` ✅
- `fig1_system_architecture` ✅
- `fig2_weight_mapping` ✅
- `fig6_physical_compensation` ✅
- `fig7_retention_curve` ✅
- `fig_nl_gradient_distortion` ✅
- `fig_fresh_instance_ablation` ✅
- `figS_corr_d2d` ✅

No missing figure errors were emitted during compilation.

---

## 4. All locked numbers exact ✅/❌
**Status: ❌ FAIL — canonical Ensemble HAT fresh-instance number is inconsistent**

The "paper-locked" canonical Ensemble HAT fresh-instance accuracy is reported as **two different values** across the thesis:

| Value | Location |
|-------|----------|
| `86.37 ± 1.54 %` | Ch 1 (l. 17), Ch 3 text (ll. 43, 112, 225), Ch 4 caption (l. 51) & summary (l. 279), Ch 5 text (ll. 29, 66, 73, 201, 250, 258, 309, 359, 380, 386, 408), Ch 6 intro (l. 24) & text (l. 61), Ch 7 (ll. 11, 61, 144, 193, 272, 336), Ch 8 (ll. 37, 179, 233, 241) |
| `86.33 ± 1.61 %` | **Ch 4 table** (l. 142), **Ch 5 table** (ll. 130–141), **Ch 6 table** (l. 73) & summary (l. 400), **Ch 8** (ll. 53, 118) |

**What needs to change:**
- Pick the definitive locked value and harmonize every occurrence.
  **File:** `chapter_4_failure_modes.tex` **line 142** — change `86.33` → `86.37` and `1.61` → `1.54`.
  **File:** `chapter_5_mitigation.tex` **line 141** — change `86.33` → `86.37` and `1.61` → `1.54`.
  **File:** `chapter_6_physical_realism.tex` **line 73** — change `86.33` → `86.37` and `1.61` → `1.54`.
  **File:** `chapter_6_physical_realism.tex` **line 400** — change `86.33` → `86.37` and `1.61` → `1.54`.
  **File:** `chapter_8_outlook.tex` **lines 53 & 118** — change `86.33` → `86.37` and `1.61` → `1.54`.

*(Note: The `1.61` pp spread of canonical Ensemble HAT is also incorrectly cited in Ch 4 l. 150 and Ch 5 l. 128 as the "tight spread"; it should read `1.54` pp to match the canonical value.)*

---

## 5. Bibliography resolves (no ??) ✅/❌
**Status: ❌ FAIL**

`main.bbl` is missing. `natbib` emitted:

```
No file main.bbl.
Package natbib Warning: There were undefined citations.
```

**What needs to change:**
- Execute `bibtex main` (or equivalent) in `paper/thesis/` to process `../latex_gpt/refs_gpt.bib`, then re-run `pdflatex` twice.

---

## 6. Negative-result framing consistent ✅/❌
**Status: ✅ PASS**

The thesis maintains a uniform and rigorous voice around negative results:
- Ch 4 (Failure Mode Atlas) frames each breakdown as "trigger → signature → mitigation → open question."
- Ch 5 (Mitigation Case Studies) explicitly labels the CX-J1 joint-training result as a "definitive negative result" and the ~30 % ceiling as a "structural barrier, not an optimization gap."
- Ch 6 (Physical-Realism Extensions) tiers contributions as "core / extended / future" so that unexecuted experiments are not misrepresented as completed.
- Ch 7 (Deployment Envelope) marks extrapolated cells in decision tables with "(extrap.)" or "(interpol.)" flags.

---

## 7. Chapter boundaries have connective tissue ✅/❌
**Status: ✅ PASS (with one caveat)**

Every chapter includes explicit forward/backward pointers:
- Ch 1 → Ch 2 (framework), Ch 5 (falsification), Ch 7 (correlated D2D).
- Ch 2 → Ch 1 (instance overfitting), Ch 3 (severe-NL boundary).
- Ch 3 → Ch 1 (instance overfitting), Ch 4 (failure modes), Ch 5 (mitigations), Ch 6 (physical realism).
- Ch 4 → Ch 5 (mitigations), Ch 6 (physical realism), Ch 7 (deployment).
- Ch 5 → Ch 4 (atlas), Ch 6 (physical realism).
- Ch 6 → Ch 4 (atlas), Ch 7 (deployment).
- Ch 7 → Ch 4 (atlas), Ch 8 (outlook).
- Ch 8 → all preceding chapters in the concluding narrative.

**Caveat:** Ch 1, §3 and §4 are still skeleton bullet lists (see Item 10), so the connective tissue in those subsections is missing.

---

## 8. Acknowledgements present ✅/❌
**Status: ❌ FAIL**

`acknowledgements.tex` exists and contains Dedication, Acknowledgements, and Declaration chapters, but **it is never included** in `main.tex`.

**What needs to change:**
- **File:** `main.tex` **line 89** — insert `\include{acknowledgements}` immediately before `\include{chapter_1_hat_instance_overfitting}` (or after the Abstract).

---

## 9. Abstract ≤300 words ✅/❌
**Status: ❌ FAIL**

The abstract is a placeholder:

```tex
\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
[Abstract text goes here.]
```

**File:** `main.tex` **lines 83–85**
**What needs to change:** Replace `[Abstract text goes here.]` with a substantive abstract of ≤300 words summarizing the three core contributions (profile-driven framework, hardware-instance overfitting discovery, and deployment envelope).

---

## 10. No TODO/FIXME/placeholder in prose ✅/❌
**Status: ❌ FAIL — multiple placeholders and skeleton sections remain**

### Placeholder strings in `main.tex`
- **Line 53:** `\title{\textbf{[THESIS TITLE]}}`
- **Line 54:** `\author{[Author Name]}`
- **Line 55:** `\date{[Date]}`
- **Line 66:** `{\Huge\bfseries [THESIS TITLE]\par}`
- **Line 70:** `{\LARGE [Author Name]\par}`
- **Line 72–75:** `[Degree]`, `[Department]`, `[University]`
- **Line 77:** `{\Large [Date]\par}`
- **Line 85:** `[Abstract text goes here.]`

### Placeholder strings in `acknowledgements.tex`
- **Line 27:** `[Advisor Name]` (×2), `[Committee Member 1]`, `[Committee Member 2]`, `[Committee Member 3]`
- **Line 29:** `[Collaborator Name]` (×3)
- **Line 31:** `[Institution]`
- **Line 33:** `[Funding Agency 1]`, `[Grant Number]` (×2), `[Funding Agency 2]`, `[Fellowship Name]`
- **Line 43:** `[Thesis Title]`, `[Advisor Name]`, `[Institution Name]`
- **Lines 47–49:** `[Author Name]`, `[City, Country]`, `[Month Year]`

### Skeleton sections (bullet lists instead of prose)
- **File:** `chapter_1_hat_instance_overfitting.tex`
  - **Lines 33–37:** `\section{Mechanism of hardware-instance overfitting}` is an `itemize` with three bullet directives (`Explain...`, `Connect...`, `Use manuscript...`).
  - **Lines 40–44:** `\section{Ensemble HAT as a distributional training objective}` is an `itemize` with three bullet directives (`Reuse...`, `Introduce...`, `Point forward...`).
  - **Lines 50–54:** `\section{Implications for the rest of the thesis}` is an `itemize` with three bullet directives (`Set up...`, `Set up...`, `Motivate...`).

**What needs to change:**
- Replace all bracketed placeholders with real metadata.
- Expand Ch 1 §3, §4, and the last `itemize` into full prose paragraphs.

---

## 11. Page count reasonable (target: 100–150) ✅/❌
**Status: ✅ PASS**

Single-pass compilation yields **118 pages** (PDF size 840 958 bytes). With BibTeX resolved, acknowledgements included, and abstract expanded, the final count is expected to remain comfortably inside the 100–150 page envelope.

---

## 12. Advisor-ready formatting ✅/❌
**Status: ❌ FAIL**

While the LaTeX class (`report`, 12 pt, 1.25 in margins) and macro packages are appropriate, the document is **not advisor-ready** because of the blocking issues catalogued above:
1. Unresolved bibliography and undefined citations.
2. Missing abstract (placeholder only).
3. Missing acknowledgements inclusion.
4. Skeleton bullet sections in Chapter 1.
5. Personal/procedural placeholders (`[Author Name]`, `[Advisor Name]`, `[Degree]`, etc.) throughout title page and acknowledgements.
6. Internal number inconsistency (86.37 vs 86.33) that undermines the "locked numbers" claim.

**What needs to change:** Resolve Items 1, 4, 5, 8, 9, and 10 above, then run the full `latex → bibtex → latex → latex` cycle before submission.

---

## Final Verdict

> **Thesis v0 NOT READY — see items above.**

**Blocking checklist items:** 1, 4, 5, 8, 9, 10, 12
**Clean items:** 2, 3, 6, 7, 11

**Recommended priority order for remediation:**
1. Harmonize the canonical Ensemble HAT number (Item 4).
2. Replace all placeholders with real metadata (Item 10).
3. Write the abstract (Item 9).
4. Include `acknowledgements.tex` in `main.tex` (Item 8).
5. Expand Ch 1 skeleton bullets into prose (Item 10).
6. Run `bibtex` + two additional `pdflatex` passes (Items 1 & 5).
7. Re-run this checklist to confirm "Thesis v0 LOCKED."
