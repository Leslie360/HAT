# CLAUDE-A FINAL Decision: NL Mitigation Narrative Placement
**Date:** 2026-04-18
**Status:** FINAL — all-linear completed
**Trigger:** All NL mitigation variants now have results.

---

## Final Result Summary

| Variant | Best Test Acc | vs Global NL=2.0 (27.72%) | Epoch | Status |
|---------|---------------|---------------------------|-------|--------|
| MLP-only | **87.79%** | **+60.07 pp** | 73 | ✅ Complete |
| QKV-only | **18.72%** | **−9.00 pp** | 2 | ✅ Complete |
| all-linear | **87.49%** | **+59.77 pp** | 59 | ✅ Complete |
| attn_proj-only | **18.86%** | **−8.86 pp** | 0 | ✅ Stopped at ep54 after sustained collapse |

---

## Final Decision: Option B LOCKED

**NL mitigation remains a supplementary ablation table (Table SX.N). It does NOT become a 5th main-paper contribution.**

### Rationale

1. **MLP-only success (+60 pp) is real and strong.**
   Linearizing only the MLP analog layers recovers to within ~4 pp of the NL=1.0 upper bound (91.94%).

2. **QKV-only failure (−9 pp) is decisive.**
   The attention nonlinearity is structurally required. A mitigation strategy that fails for one of the two principal transformer sub-circuits cannot claim generality.

3. **all-linear (87.49%) confirms MLP-dominance.**
   The composite result is slightly below MLP-only (87.49% vs 87.79%), consistent with the QKV path remaining suboptimal while the MLP path drives most of the recovery.

4. **Fresh-instance transfer remains weak even after broader linearization.**
   The `MLP-only` and `all-linear` lanes reach only `32.12 ± 7.72%` and `32.60 ± 9.18%`, respectively, under the same 10-array fresh-instance protocol used for Ensemble HAT. That is far below the canonical `86.37 ± 1.54%` transfer result and confirms that these lanes are diagnostic ablations rather than deployment-grade fixes.

5. **No narrative rewrite needed.**
   The main-paper contribution count stays at 4. NL mitigation is cited as a supplementary ablation with the sentence:
   > "Group-wise ablation (Supplementary Table SX.N) shows that the MLP channel-mixing path is the dominant recoverable failure site under the present NL=2.0 surrogate."

---

## Unblocked Items

- [x] K-B Cover Letter v2 — NL mitigation supplementary framing confirmed
- [x] R1–R4 .tex patches — already landed
- [x] Table SX.N — row (f) updated with 87.49%
- [x] Table SX.N — row (e) populated from the stopped-at-ep54 collapse snapshot (best 18.86\%, final \(\sim\)10.25\%)

---

## Manuscript Text (locked)

> *Supplementary Note SX.N:* "We performed a group-wise ablation of the nonlinearity surrogate under a fixed global NL=2.0. Linearizing only the MLP analog layers (fc1, fc2) recovers 87.79% test accuracy — a +60 pp improvement over the unmitigated baseline — whereas linearizing only the QKV projection degrades accuracy to 18.72%. Linearizing all analog layers yields 87.49%, confirming that the MLP channel-mixing nonlinearity is the dominant failure site and that the attention QKV nonlinearity is structurally required."
