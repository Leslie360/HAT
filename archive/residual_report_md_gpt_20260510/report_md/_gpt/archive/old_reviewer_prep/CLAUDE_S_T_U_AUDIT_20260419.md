# Claude Round G — E1/E2/E3 Inline Audit Results (CLAUDE-S/T/U)

**Date:** 2026-04-19
**Status:** All three audits complete. Two issues flagged for patch, one response-draft disclosure needed.

---

## CLAUDE-S — Cover Letter Audit (E1 absorption)

### Criterion (a): NL mitigation framed as supplementary ablation
**Verdict: ✅ PASS**
- Line 41: "Approximation-scoped nonlinear-write stress test and group-wise ablation: global $NL=2.0$ collapses to 27.72$\pm$0.82\%, yet linearizing only the MLP analog layers recovers 87.79\% (supplementary Table~SX.N); the QKV path cannot be linearized without structural failure..."
- Framing is correct: supplementary table, not 5th main contribution. QKV failure is honestly disclosed.

### Criterion (b): OPECT 88.53±0.08%
**Verdict: ✅ PASS**
- Line 26: "88.53$\pm$0.08\% zero-shot transfer accuracy" — matches main text exactly.

### Criterion (c): Cross-ref to Table SX.N consistent
**Verdict: ✅ PASS**
- Line 41 cites "supplementary Table~SX.N" consistently with supp scaffold.

### Issues found

**Issue S1 — Page count stale:**
- Line 58: "The manuscript is currently 14 pages of main text..."
- **Actual:** `main.pdf` is **15 pages** (grew by 1 pp absorbing R1–R4 patches).
- **Action:** Change "14 pages" → "15 pages".

**Issue S2 — Contribution count mismatch:**
- Cover letter lists **6** contributions (lines 37–43).
- Manuscript §1 introduction states **four** concrete contributions.
- The mismatch: cover letter splits the manuscript's 4th contribution ("literature-profile substitution + severe nonlinear write") into three items (4, 5, 6), and adds "hybrid analog/digital deployment" as a separate item.
- **Risk:** Reviewer may perceive scope inflation or inconsistency.
- **Action:** Reconcile cover letter with manuscript. Recommended: keep 4 main contributions aligned with §1, and frame items 4–6 as "supporting demonstrations" or fold them into the 4th contribution.

---

## CLAUDE-T — Response Draft Audit (E2 absorption)

### Criterion (a): Table SX.N cited correctly
**Verdict: ✅ PASS**
- Response draft Major Comment 2 cites "supplementary Table SX.N" correctly.

### Criterion (b): all-linear 87.49% NOT overclaimed
**Verdict: ✅ PASS**
- Described as "Consistent with MLP-dominant recovery masking the QKV failure in the composite setting." — no overstatement.

### Criterion (c): QKV-only collapse honestly disclosed
**Verdict: ✅ PASS**
- "degrades to 18.72%, below even the unmitigated baseline. This decisive failure shows that the attention nonlinearity is structurally required."

### Issue found

**Issue T1 — Gradient diagnostic vs. training reality inconsistency:**
- Response draft states: "`Patch Embed`, `Attention QKV`, and `Attention Proj` remain at `1.00`, indicating negligible distortion under the same matched-forward diagnostic."
- **New evidence (Round G):** `attn_proj-only` is collapsing in real-time (~11% test acc, same pattern as QKV-only).
- **Implication:** The frozen-checkpoint gradient diagnostic (cosine = 1.00) is a **necessary but insufficient** condition. It measures backward-surrogate distortion on a converged model, but cannot predict training-dynamics collapse when the nonlinear write is removed from a path that is structurally required during training.
- **Action:** Add one disclosure sentence to the response draft gradient-diagnostic paragraph:
  > "We note that the gradient-diagnostic cosine of 1.00 for the attention-projection path reflects negligible backward-surrogate distortion on the frozen converged checkpoint, yet the independent training-time ablation (Table SX.N row e) shows that removing NL=2.0 from attn.proj during training still produces collapse. This indicates that the diagnostic isolates surrogate fidelity but does not capture training-dynamics dependencies."

---

## CLAUDE-U — §6 Discussion Vulnerability Scan (E3 absorption)

### Scan method
Read `06_discussion.tex` line-by-line for sentences implying MLP-exclusivity or omitting the dual-attention-collapse evidence.

### Findings

**Finding U1 — No dual-attention-collapse mention in §6:**
- The entire `06_discussion.tex` (47 lines) contains zero mention of the group-wise NL ablation results.
- This is **correct per Option B** (supp-only), but the Limitations paragraph (line 43) says: "The $NL=2.0$ limit reflects the present gradient-scaling surrogate, not a materials bound."
- **Missing:** With QKV-only (18.72%) AND attn_proj-only (~11%) both collapsed, the Limitations paragraph could be tightened to:
  > "The $NL=2.0$ limit reflects the present gradient-scaling surrogate, not a materials bound. Group-wise ablation shows that the bottleneck is concentrated in the MLP analog path, while both attention-side linearizations (QKV and projection) collapse structurally."
- **Action:** One-sentence tightening in §6.5 Limitations. Micro-patch, no structural change.

**Finding U2 — No MLP-exclusivity wording found:**
- The text does **not** claim "only MLP recovers" or "MLP-only exclusivity." The existing phrasing is appropriately cautious.
- The only place where MLP-dominance is implied is in the cover letter (Issue S2), not in §6.

**Finding U3 — Transformer sensitivity paragraph (lines 23–27) is pre-ablation:**
- "The collapse of V4 under proportional noise (10.00% accuracy)... indicates that Transformer inference depends on the precision of token projections."
- This paragraph was written before the group-wise ablation existed. It remains factually correct but does not leverage the new ablation evidence.
- **Action:** Optional — no patch needed for this revision, because the ablation is supp-only. If editor pushes, add a footnote referencing Table SX.N.

---

## Summary of required patches

| ID | File | Patch | Priority | Owner |
|:--|:--|:--|:--:|:--|
| S1 | `cover_letter.tex` | "14 pages" → "15 pages" | HIGH | Claude |
| S2 | `cover_letter.tex` | Reconcile 6 contributions with manuscript's 4 | HIGH | Claude |
| T1 | `REVIEWER_RESPONSE_DRAFT_gpt.md` | Add gradient-diagnostic vs. training-reality disclosure | MED | Claude |
| U1 | `06_discussion.tex` | One-sentence tightening in §6.5 Limitations | MED | Claude |

---

**End of audit.** All three E1/E2/E3 tasks absorbed. Four micro-patches identified, all CPU-only, no GPU needed.
