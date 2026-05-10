# Nature Communications Submission Checklist — Article

**Manuscript source:** `/home/qiaosir/projects/compute_vit/paper/latex_gpt/`
**Check date:** 2026-04-20
**Guidelines consulted (live):**
- Nature Communications *Guide to Formatting Articles* PDF (rev. 2021-05-07) — https://www.nature.com/documents/ncomms-formatting-instructions.pdf
- Nature Communications *How to submit* page (live, extracted 2026-04-20) — https://www.nature.com/ncomms/submit/how-to-submit
- AJE Nature Communications Submission Template (Springer Nature) — https://info.authorservices.springernature.com/hubfs/AJE%20Downloadables/AJE%20Nature%20Communications%20Submission%20Template.docx
- Springer Nature editorial policies page (live, extracted 2026-04-20)

---

## 1. Article type: Article (not Review, not Brief Communication)
**Status:** ✅ PASS

**Evidence:**
`cover_letter.tex`, line 14:
```tex
\textbf{Article Type:} Article
```
The cover letter explicitly requests an **Article**. No mention of Review, Perspective, Brief Communication, or Correspondence.

---

## 2. Abstract length: typically 150 words max
**Status:** ❌ FAIL — **CRITICAL**

**Evidence:**
`sections/00_abstract.tex`, lines 3–7 (between `\begin{abstract}` and `\end{abstract}`).
**Word count (LaTeX-stripped text):** **159 words**.

**Sample quote (first sentence):**
> We present a profile-driven first-order behavioral simulation framework for organic optoelectronic compute-in-memory inference, motivated by the open question of whether multilevel conductance tuning and low static power suffice for modern vision tasks.

**Proposed patch:** Trim **≥ 9 words** from the abstract to bring it to ≤ 150.
*Suggested cuts:* condense the parenthetical list of physical effects (lines 4–5) or tighten the final summary sentence.

---

## 3. Main text word count
**Status:** ✅ PASS

**Evidence:**
Main text sections (`01_introduction` → `07_conclusion`, excluding abstract):

| Section | `detex` word count |
|---|---|
| `01_introduction.tex` | 741 |
| `02_related_work.tex` | 658 |
| `03_methodology.tex` | 975 |
| `04_experimental_setup.tex` | 289 |
| `05_results.tex` | 1,039 |
| `06_discussion.tex` | 1,201 |
| `07_conclusion.tex` | 342 |
| **Total (all main sections)** | **5,245** |
| Excluding figure captions (71 words) | 5,174 |
| Excluding Methods section (975 words) | 4,199 |

Nature Communications allows:
- **~6,000 words** for the main text *not including figure legends or Methods* (Formatting PDF, General Formatting section).
- Older brief guide says **~5,000 words** for Articles; the AJE template says **≤ 6,000 words**.

In all interpretations the manuscript is **under the limit**.

---

## 4. Figure count (main text)
**Status:** ✅ PASS

**Evidence:**
`sections/05_results.tex` contains **5** `\begin{figure}[t] … \end{figure}` environments:
- Line 15: `fig4_accuracy_comparison`
- Line 22: `fig5_hat_recovery`
- Line 53: `fig_contour_map`
- Line 65: `figS3_ensemble_hat`
- Line 79: `fig10_zero_shot_transferability`

Limit: **≤ 10 display items** (figures + tables combined). 5 figures alone is within the cap.

---

## 5. Table count (main text)
**Status:** ✅ PASS

**Evidence:**
`sections/04_experimental_setup.tex`, line 9:
```tex
\begin{table}[t]
    \centering
    \caption{Notation used for the Tiny-ViT experiment family in the main text.}
    \label{tab:exp-notation}
```

**Total main-text display items:** 5 figures + 1 table = **6** (limit = 10).

---

## 6. Reference count
**Status:** ✅ PASS

**Evidence:**
`main.bbl` contains **37** `\bibitem` entries:
```bash
$ grep -c '^\bibitem' main.bbl
37
```

Nature Communications guidelines state references should be "limited to …" (PDF truncates the number), but the older brief guide and common practice cite **~60–70** as the soft upper bound for Articles. 37 is comfortably below any cited limit.

---

## 7. Supplementary policy: allowed types, max size
**Status:** ✅ PASS

**Evidence:**
- **File:** `supplementary_main.pdf` — **2.1 MB** (single combined PDF).
- **Allowed items per PDF:** Supplementary Figures, Supplementary Tables, Supplementary Methods, Supplementary Notes, Supplementary Discussion, Supplementary References. The manuscript supplement contains all of these.
- **No disallowed items** (e.g., no Supplementary Movies / Audio / Data / Software files are referenced in the source).
- **Table size check:** All 16 supplementary tables have ≤ 13 rows (largest = 13 rows). The policy states tables **> 50 rows or > 10 columns** should be supplied as separate tabular data files; none exceed this threshold.
- **Max size:** Nature Communications does not publish a hard SI size limit in the formatting PDF; the overall submission portal accepts files up to **30 MB**. The 2.1 MB SI PDF is well within that bound.

---

## 8. Declarations required
**Status:** ✅ PASS (with one N/A)

**Evidence from `sections/07_conclusion.tex`:**

| Declaration | Present? | Location |
|---|---|---|
| **Competing Interests** | ✅ Yes | Line 17: `\section*{Competing Interests}` — "The authors declare no competing interests." |
| **Author Contributions** | ✅ Yes | Line 20: `\section*{Author Contributions}` — "S.L. conceived the framework…" |
| **Data Availability** | ✅ Yes | Line 11: `\section*{Data Availability}` — states public datasets and pending source-data deposit. |
| **Code Availability** | ✅ Yes | Line 14: `\section*{Code Availability}` — states reviewer-accessible archive and GitHub release plan. |
| **Ethics** | N/A | Computational simulation study using publicly available vision datasets (CIFAR-10/100, Flowers-102). No human or animal subjects. |

The Data Availability and Code Availability statements are in **separate sections**, as required.

---

## 9. ORCID requirement
**Status:** ❌ FAIL — **SHOULD-FIX**

**Evidence:**
`main.tex`, line 30:
```tex
\author{Songqiao Li}
```
No ORCID iD is provided for the single author, who is also the corresponding author.

**Live requirement:**
> "Corresponding authors must provide their ORCID ID before resubmitting the final version of the manuscript. Non-corresponding authors are encouraged to link their ORCID." (Nature Communications *How to submit* / Editorial policies)

**Proposed patch:** Add the ORCID to the author block (requires an ORCID package or simple text annotation), e.g.:
```tex
\usepackage{orcidlink}
\author{Songqiao Li\,\orcidlink{0000-0000-0000-0000}}
```
*(Replace with the actual ORCID.)*

---

## 10. Cover letter requirements
**Status:** ✅ PASS

**Evidence:**
`cover_letter.tex` is present and addresses all recommended elements:
- **Editorial summary** (≈150 words) stating the central finding and its significance.
- **Fit for Nature Communications** — explicitly argues cross-disciplinary scope.
- **Key Contributions** — numbered list of four main advances.
- **Transparency disclosures** — preprint status, prior publication, code/data availability, competing interests.
- **Related manuscripts** — confirms no overlap ("submitted exclusively to Nature Communications").

Cover letters are described as **optional but encouraged** by the AJE template; the manuscript provides one.

---

## 11. Suggested reviewers count (3–5)
**Status:** ❌ FAIL — **SHOULD-FIX**

**Evidence:**
- `cover_letter.tex`, line 12: `"Suggested and excluded reviewers will be provided through the submission system."`
- No file containing **actual names, institutions, and email addresses** of 3–5 suggested reviewers exists in `/home/qiaosir/projects/compute_vit/paper/latex_gpt/` or the submission packet.
- `report_md/_gpt/KIMI_REVIEWER_SUGGESTER_BRIEF_20260420.md` contains 5 *profile descriptions* (e.g., "Organic/RRAM Device Physicist") but not the required contact details.

**Proposed patch:** Create a new file (e.g., `SUGGESTED_REVIEWERS.md` or `reviewers.txt`) in the submission folder listing **3–5** reviewers with:
- Full name
- Institutional affiliation
- Institutional email address
- Brief rationale (1 sentence)

---

## 12. Formatting: line numbers, margins, fonts
**Status:** ✅ PASS / N/A

| Sub-item | Status | Evidence |
|---|---|---|
| **Margins** | ✅ PASS | `main.tex`, line 4: `\usepackage[margin=1in]{geometry}` — 1 inch on all sides. |
| **Fonts** | ✅ PASS | `main.tex` uses the default Computer Modern font (no non-standard font packages loaded). The NC LaTeX instructions explicitly state: *"All textual material should be provided as a single file in default Computer Modern fonts."* |
| **Line numbers** | N/A | **Not required** by Nature Communications for initial submission. Neither the official formatting PDF (2021) nor the live *How to submit* page mentions line numbers as a mandatory element. The manuscript does not include them, but this does not violate any stated NC rule. |

---

## Additional Structural & Formatting Observations

These items are **not part of the numbered checklist above** but were surfaced by the live NC formatting PDF and should be addressed before final submission.

### A. Extra section headings not in the NC allowed list — SHOULD-FIX
The NC formatting PDF states:
> "The text must be split into the sections given below. No other section headings are [permitted]."

Allowed sections: Title, Authors, Abstract, Introduction, Results, Discussion (optional), Methods (optional), Data Availability, Code Availability, References, Acknowledgements, Author Contributions, Competing Interests.

**Current manuscript contains disallowed top-level sections:**
- `sections/02_related_work.tex` — **"Related Work"**
- `sections/04_experimental_setup.tex` — **"Experimental Setup"**
- `sections/07_conclusion.tex` — **"Conclusion"** (in addition to the required declarations)

**Proposed patch:** Merge "Related Work" into the **Introduction**. Merge "Experimental Setup" into the **Methods** section. Absorb "Conclusion" into the **Discussion** (or rename it "Discussion" if it already serves that role).

### B. BibTeX commands in LaTeX source — SHOULD-FIX
`main.tex`, lines 38–39:
```tex
\bibliographystyle{unsrtnat}
\bibliography{refs_gpt}
```

NC LaTeX instructions state:
> "BibTeX bibliography files cannot be accepted. … If you wish to use BibTeX, please copy the reference list from the `.bbl` file, paste it into the main manuscript `.tex` file, and delete the associated `\bibliography` and `\bibliographystyle` commands."

**Proposed patch:** Inline the `main.bbl` content into `main.tex` and remove the two BibTeX commands.

### C. Figure legends embedded in text — NOTE
All 5 main-text figure legends currently sit inside their `figure` environments. The NC formatting PDF says:
> "Text for figure legends should be provided in numerical order after the references."

For **initial submission** the journal is flexible, but this will need to be reordered if a revision is invited.

---

## Summary Table

| # | Check Item | Status | Severity |
|---|---|---|---|
| 1 | Article type = Article | ✅ PASS | — |
| 2 | Abstract ≤ 150 words | ❌ FAIL | **CRITICAL** |
| 3 | Main text word count | ✅ PASS | — |
| 4 | Figure count (main) ≤ 10 | ✅ PASS | — |
| 5 | Table count (main) ≤ 10 | ✅ PASS | — |
| 6 | Reference count | ✅ PASS | — |
| 7 | Supplementary policy | ✅ PASS | — |
| 8 | Declarations (CI, AC, DA, CA, ethics) | ✅ PASS / N/A | — |
| 9 | ORCID for corresponding author | ❌ FAIL | SHOULD-FIX |
| 10 | Cover letter | ✅ PASS | — |
| 11 | Suggested reviewers (3–5) | ❌ FAIL | SHOULD-FIX |
| 12 | Margins, fonts, line numbers | ✅ PASS / N/A | — |

**Critical action required:** Trim abstract to ≤ 150 words.
**Should-fix actions:** (1) Add ORCID, (2) create a suggested-reviewers file with 3–5 names/emails, (3) merge disallowed sections (Related Work, Experimental Setup, Conclusion) into Introduction/Methods/Discussion, (4) inline BibTeX references before source submission.
