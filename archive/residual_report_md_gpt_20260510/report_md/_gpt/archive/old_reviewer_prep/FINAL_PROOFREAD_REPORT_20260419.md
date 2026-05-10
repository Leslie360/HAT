# Final Proofread Report — 2026-04-19

**Scope:** Main manuscript (15 pp), supplementary (21 pp), cover letter (2 pp), response draft, key coordination files.
**Status:** All issues identified and patched. Three PDFs recompile cleanly.

---

## Issues found and patched

### 1. Abstract — OPECT precision missing error bars
- **Before:** "reaches 88.53\% zero-shot transfer accuracy"
- **After:** "reaches 88.53$\\pm$0.08\% zero-shot transfer accuracy ($n=10$ fresh-instance evaluations)"
- **File:** `00_abstract.tex`
- **Severity:** HIGH (manuscript claims ±0.08% everywhere else)

### 2. Conclusion — OPECT precision missing error bars
- **Before:** "zero-shot deployment reaches 88.53\%"
- **After:** "zero-shot deployment reaches 88.53$\\pm$0.08\% ($n=10$ fresh-instance evaluations)"
- **File:** `07_conclusion.tex`
- **Severity:** HIGH

### 3. Cover letter — stale page count
- **Before:** "14 pages of main text"
- **After:** "15 pages of main text"
- **File:** `cover_letter.tex`
- **Severity:** MEDIUM

### 4. Cover letter — contribution count mismatch
- **Before:** 6 items (splitting manuscript's 4th contribution into 3 items + adding hybrid deployment as separate)
- **After:** 4 items aligned with §1 introduction
- **File:** `cover_letter.tex`
- **Severity:** HIGH (reviewer-scope consistency)

### 5. Response draft — gradient-diagnostic vs. training-reality gap
- **Before:** "`Attention Proj` remain at `1.00`, indicating negligible distortion"
- **After:** Added caveat that frozen-checkpoint diagnostic cosine does not predict training-dynamics collapse; attn_proj-only independently collapses at ~11%.
- **File:** `REVIEWER_RESPONSE_DRAFT_gpt.md`
- **Severity:** HIGH (reviewer-honesty)

### 6. §6 Discussion — dual-attention-collapse tightening
- **Before:** "The $NL=2.0$ limit reflects the present gradient-scaling surrogate, not a materials bound."
- **After:** "... Group-wise ablation confirms that the bottleneck is concentrated in the MLP analog path, while both attention-side linearizations (QKV and projection) collapse structurally."
- **File:** `06_discussion.tex`
- **Severity:** MEDIUM

### 7. Table SX.N — row (e) filled
- **Before:** "\textit{pending} / \textit{pending} / \textit{pending}"
- **After:** "$18.86$ / $\\sim$10.25 (stopped @ ep 54) / $-9.14$"
- **File:** `supplementary.tex`
- **Severity:** HIGH (blocking table completion)

### 8. NL_LANE_RESULTS — attn_proj-only row appended
- **File:** `NL_LANE_RESULTS_20260418.md`
- **Status:** Updated with epoch 54 snapshot data.

---

## Consistency checks passed

| Check | Result |
|:---|:---|
| Key numbers across abstract→results→discussion→conclusion | ✅ All found |
| Figure/table labels vs. refs | ✅ No dangling refs |
| Cover letter vs. manuscript contributions | ✅ Now aligned (4 each) |
| OPECT precision (88.53±0.08%) | ✅ All three locations consistent |
| Page counts | ✅ Main 15, Supp 21, Cover 2 |

---

## Style notes (no action needed)

- "Supplementary Fig.~" is acceptable NC style for supplementary figure references.
- "97.39±0.00%" is technically correct for 10 identical deterministic evaluations; kept as-is.
- Equation environment double-spaces are LaTeX-normal and compile correctly.

---

## Compile verification

| File | Pages | Size | Status |
|:---|:---:|:---:|:---:|
| `main.pdf` | 15 | 245.18 KiB | ✅ clean |
| `supplementary_main.pdf` | 21 | 9.60 MiB | ✅ clean |
| `cover_letter.pdf` | 2 | 27.08 KiB | ✅ clean |

---

## Residual exposure (post-proofread)

| Issue | Mitigation | Likelihood |
|:---|:---|:---:|
| Reviewer pushes on 88.53±0.08% in abstract vs. 88.53% in appendix sensitivity table | Appendix table is mean of 10 MC runs at nominal C2C=2%; abstract uses same data with SD disclosed | LOW |
| "~10.25" in Table SX.N is approximate because training stopped at ep 54 | Footnote in table explains stopped @ ep 54; pattern already clear | LOW |

---

**Proofreader:** Claude
**Date:** 2026-04-19
**Recommendation:** Manuscript is submission-ready pending formal sign-off on the above patches.
