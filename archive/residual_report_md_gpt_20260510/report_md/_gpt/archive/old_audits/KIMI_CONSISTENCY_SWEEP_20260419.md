# K-O4: Consistency Sweep Across Manuscript Files

**Date:** 2026-04-19
**Scope:** All `.tex` files in `sections/`, `cover_letter.tex`, and first 200 lines of `supplementary.tex`

---

## Check 1: Contribution-count lock (4 contributions)

**Query:** `five contributions`, `5 contributions`, `6 contributions`

**Result:** PASS
No stray references to 5 or 6 contributions found in any active file. The cover letter lists exactly 4 numbered contributions, and `01_introduction.tex` (line 17) states "this study makes four concrete contributions."

---

## Check 2: MLP-only phrasing overstatement

**Query:** Patterns such as `only MLP recovers`, `only the MLP`, `MLP-only`, `MLP path is the dominant`

**Result:** PASS
All MLP-related phrasing in active files is properly scoped:
- `cover_letter.tex:40` — "the MLP path is the **dominant recoverable** failure site; both attention-side linearizations collapse structurally" (accurate; does not claim exclusive recovery).
- `06_discussion.tex:43` — "the bottleneck is concentrated in the MLP analog path, while both attention-side linearizations (QKV and projection) collapse structurally."
- `supplementary.tex:747,760` — Correctly localizes the NL=2.0 training surrogate to the MLP path without implying it is the only relevant factor for fresh-instance transfer.

No instance of "only MLP recovers" or equivalent overstatement was found.

---

## Check 3: QKV claims missing matching `attn_proj` after dual-attention-collapse patch

**Result:** FAIL

| File | Line | Finding | Suggested Fix |
|------|------|---------|---------------|
| `supplementary.tex` | 785 | Stale interpretation text: "The attention projection path (row~e) is **pending completion**." Row~(e) in Table~`tab:supp-nl-ablation` is **already populated** (`18.86` / `~10.25`). Additionally, the sentence "because the **QKV-only failure** limits the generality of any single-path mitigation claim" understates the dual collapse: row~(d) QKV-only *and* row~(e) attn_proj-only both collapse structurally. | Update line 785 to: "Both attention-side linearizations (QKV and projection) collapse structurally, limiting the generality of any single-path mitigation claim." |

**Supporting evidence:**
- Table `tab:supp-nl-ablation` (`supplementary.tex:772-782`):
  - Row (d) QKV only: `18.72` / `10.15`
  - Row (e) Attn proj only: `18.86` / `~10.25 (stopped @ ep 54)`
- The text at `06_discussion.tex:43` correctly states "both attention-side linearizations (QKV and projection) collapse structurally," confirming the dual-collapse patch is in place elsewhere. The supplementary interpretation text was not updated to match.

---

## Check 4: Stale numbers not in the 16-locked list

**Query:** Conductance-state / quantization values outside the canonical 16-state (4-bit) lock

**Result:** PASS (active manuscript)

Active files correctly maintain the 16-state lock for the canonical and stress-test regimes:
- `08_appendix.tex:43` — "Effective States ($n_{states}$) & 16 (4-bit) & **34** & 16 (4-bit)"
- `supplementary.tex:229` — Same as above

The **34** value appears exclusively in the Zhang 2025 OPECT case-study column, which is intentional and literature-anchored (noted as anchored to Fig.3h & Supp.Fig.8 of \cite{zhang2026opect}). No stale or inconsistent state counts were found in active `.tex` files.

**Caution:** Backup files `sections/00_abstract.tex.bak_20260418` and `sections/05_results.tex.bak_20260418` contain the pre-revision "88.53%" (without `±0.08%`) and old phrasing; they are not compiled by `main.tex` but should be removed before submission to avoid accidental inclusion.

---

## Check 5: `88.53` must always appear with `±0.08%` in Abstract, Results, Discussion, Conclusion

**Result:** PASS

| Section | File | Line | Status |
|---------|------|------|--------|
| Abstract | `00_abstract.tex` | 5 | `88.53$\pm$0.08\%` ✓ |
| Results | `05_results.tex` | 77 | `88.53$\pm$0.08\%` ✓ |
| Discussion | `06_discussion.tex` | — | `88.53` does not appear (no issue) ✓ |
| Conclusion | `07_conclusion.tex` | 9 | `88.53$\pm$0.08\%` ✓ |

All occurrences of `88.53` in the four specified sections carry the required `±0.08%` error bar and `$n=10$ fresh-instance evaluations` qualifier where contextually appropriate.

---

## Additional Finding: Stale Placeholder Reference

| File | Line | Finding | Suggested Fix |
|------|------|---------|---------------|
| `cover_letter.tex` | 40 | Stale placeholder reference: `(supplementary Table~SX.N)` | Replace with the actual supplementary table reference, e.g. `(Supplementary Table~\ref{tab:supp-nl-ablation})`, or remove the parenthetical if the cover letter cannot resolve LaTeX labels from the supplementary document. |

---

## Summary

| Check | Status | Notes |
|-------|--------|-------|
| 1. Contribution-count lock | **PASS** | Exactly 4 contributions everywhere |
| 2. MLP-only overstatement | **PASS** | All MLP phrasing properly scoped |
| 3. QKV / `attn_proj` consistency | **FAIL** | `supplementary.tex:785` has stale "pending completion" text and understates dual collapse |
| 4. Stale numbers (16-locked) | **PASS** | 34 is OPECT-only and intentional |
| 5. `88.53 ±0.08%` lock | **PASS** | All four target sections compliant |

**Action items:**
1. Fix `supplementary.tex` line 785 to reflect completed `attn_proj` row and dual-collapse interpretation.
2. Fix or remove `cover_letter.tex` line 40 placeholder `SX.N`.
3. Optionally delete `.bak_20260418` backup files in `sections/` to prevent accidental inclusion.
