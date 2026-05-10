# Kimi Live .tex Audit — Contaminated Content in Frozen Files
**Date:** 2026-04-24
**Auditor:** Kimi
**Scope:** All `paper/latex_gpt/*.tex` and `paper/latex_gpt/sections/*.tex` (excluding `.kimi_draft_v2` files)

## ⚠️ Executive Summary

**5 live `.tex` files contain bug-contaminated content** that was not previously flagged. The contamination is more widespread than the §5.x Results section alone. Per broadcast §7.1, these files are frozen until CLAUDE-FC; Kimi cannot edit them. This audit report serves as a **pre-integration diff list** for Claude.

| File | Lines | Severity | Contaminated Content |
|:-----|:-----:|:--------:|:---------------------|
| `01_introduction.tex` | 15 | 🔴 High | 27.72±0.82% cited as severe-NL limit |
| `05_results.tex` | 63, 74, 76 | 🔴 Critical | 27.72%, 30.53%, "~30% barrier persists", "structural ceiling" |
| `06_discussion.tex` | 43 | 🟡 Low | "attention-side linearizations collapse structurally" (pre-fix conclusion) |
| `07_conclusion.tex` | 7 | 🔴 High | 27.72±0.82% cited as severe-NL limit |
| `cover_letter_v3.tex` | 31 | 🔴 High | "30% structural ceiling" headline claim |
| `supplementary.tex` | 783, 792 | 🟡 Moderate | 27.72%, 32.12%, 32.60% in ablation table (K-DRAFT-5 already audited) |

---

## Detailed Findings

### 🔴 01_introduction.tex (Line 15)

**Contaminated text:**
```latex
Fourth, severe nonlinear write ($NL=2.0$) remains difficult to recover under
the present gradient-scaling approximation, limiting accuracy to 27.72$\pm$0.82\%.
```

**Issue:** The Introduction presents 27.72% as a current finding, not a retracted pre-fix result. Readers will form their first impression from this sentence. The bug-fix narrative is entirely absent from the Introduction.

**Action at CLAUDE-FC:** Replace with post-fix framing: "Post-fix hardware-aware training recovers [CX-M1 pending]% under NL=2.0, falsifying the previously reported ~30% ceiling."

---

### 🔴 05_results.tex (Lines 63, 74, 76)

**Contaminated text (line 63):**
```latex
...the baseline severe-nonlinearity configuration ($NL=2.0$) recovers only
27.72$\pm$0.82\% under the present gradient-scaling recipe.
```

**Contaminated text (line 74):**
```latex
To test whether the ceiling is structural, we trained a joint MLP-linear +
Ensemble HAT model under $NL=2.0$... fresh-instance evaluation across 10 arrays
yields only \textbf{30.53$\pm$7.07\%}. This falsifies the hypothesis that coupling
severe-NL compensation with distributional resampling breaks the severe-NL ceiling;
the $\sim$30\% barrier persists.
```

**Contaminated text (line 76):**
```latex
The convergence of three independent mitigations (MLP-only, all-linear, joint)
on the same $\sim$30\% fresh-instance ceiling under $NL=2.0$ suggests that severe
write nonlinearity introduces a generalization barrier in the attention pathway
that training-recipe modifications cannot overcome within the first-order surrogate
regime.
```

**Issue:** This is the core contaminated narrative — "structural ceiling", "~30% barrier persists", "generalization barrier". All three sentences are based on pre-fix bug-contaminated data. K-DRAFT-1 already provides a replacement subsection; Claude should replace lines 61–76 with the K-DRAFT-1 content.

---

### 🟡 06_discussion.tex (Line 43)

**Contaminated text:**
```latex
Group-wise ablation confirms that the bottleneck is concentrated in the MLP
analog path, while both attention-side linearizations (QKV and projection)
collapse structurally.
```

**Issue:** This conclusion derives from the group-wise ablation table (`tab:supp-nl-ablation`) which uses a pre-fix 27.72% baseline. The qualitative conclusion (MLP bottleneck > attention bottleneck) may still hold post-fix, but "collapse structurally" echoes the deprecated structural-limit narrative.

**Action at CLAUDE-FC:** Weaken to: "Group-wise ablation suggests the MLP path dominates recovery, though attention-side paths also degrade under NL=2.0."

---

### 🔴 07_conclusion.tex (Line 7)

**Contaminated text:**
```latex
By contrast, the baseline severe write nonlinearity setting remains difficult
to recover under the present gradient-scaling approximation (27.72$\pm$0.82\%),
and determining whether physical organic devices enter this regime will require
direct nonlinear-write measurements.
```

**Issue:** The Conclusion closes with a contaminated number. The framing "remains difficult to recover" is false post-fix — recovery to ~82% is achievable.

**Action at CLAUDE-FC:** Replace with post-fix framing and residual gap narrative.

---

### 🔴 cover_letter_v3.tex (Line 31)

**Contaminated text:**
```latex
\item We falsify three severe-nonlinearity mitigation strategies, establishing
an approximately 30\% structural ceiling that defines the boundary of first-order ehavioral simulation.
```

**Issue:** This is a cover-letter headline claim. It must be replaced with the K-DRAFT-2 v4 content before submission.

**Action at CLAUDE-FC:** Use `cover_letter_v4.tex.kimi_draft_v2` as replacement.

---

## Cross-Reference: Kimi Drafts Ready for Integration

| Contaminated File | Replacement Draft | Status |
|:------------------|:------------------|:-------|
| `05_results.tex` | `05_results.tex.kimi_draft_v2` (K-DRAFT-1) | ✅ Ready |
| `cover_letter_v3.tex` | `cover_letter_v4.tex.kimi_draft_v2` (K-DRAFT-2) | ✅ Ready |
| `00_abstract.tex` | `00_abstract.tex.kimi_draft_v2` (K-DRAFT-3) | ✅ Ready |
| `06_discussion.tex` | `06_discussion.tex.kimi_draft_v2` (K-DRAFT-4) | ✅ Ready |
| `supplementary.tex` | `K_DRAFT_5_SUPPLEMENTARY_AUDIT_20260424.md` | ✅ Audit complete |
| `paper/thesis_cn/chapter_5_failure_modes.tex` | `chapter_5_failure_modes.tex.kimi_draft_v2` (K-DRAFT-6) | ✅ Ready |

**Missing replacements:**
- `01_introduction.tex` — Kimi has not drafted a replacement. The contamination is one sentence (line 15). Claude can fix inline at integration.
- `07_conclusion.tex` — Kimi has not drafted a replacement. The contamination is one sentence (line 7). Claude can fix inline at integration.

---

## Clean Files (No Contamination Found)

| File | Verified Clean |
|:-----|:-------------|
| `02_methodology.tex` | ✅ No severe-NL numbers; methodology description only |
| `03_experimental_setup.tex` | ✅ Setup parameters, no results |
| `04_baseline_results.tex` | ✅ Canonical NL=1.0 results only (bug-immune) |
| `paper/thesis_cn/chapter_*.tex` (other than Ch.5) | ✅ Not audited in scope |

---

## Method

1. Grep all live `.tex` files for known contaminated numbers: 27.72, 30.53, 38.95, 41.53, 90.88, Hartigan, bimodal, structural ceiling, structural limit.
2. Contextual read (±5 lines) of each hit.
3. Judge whether the usage is descriptive (e.g., "structural difference between CNN and ViT" = clean) or evidential (e.g., "structural ceiling at 30%" = contaminated).
4. Cross-check against bug-immunity scope (§1 of broadcast).

---

## Conclusion

The contamination is **localized but high-impact**: it appears in the Introduction, Results, Conclusion, and Cover Letter — precisely the sections a reader skims first. All contaminated content traces back to the same pre-fix severe-NL experiments (CX-J1/1b/1c/1d, CX-K1–K5).

**Kimi's drafts (K-DRAFT-1 through K-DRAFT-6) are ready to replace the contaminated sections.** Two one-sentence fixes remain for the Introduction and Conclusion; these are simple enough for Claude to handle inline at CLAUDE-FC without a separate draft.
