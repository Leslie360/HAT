# Kimi R9C Defense Paragraphs — Integration Report
**Date:** 2026-04-26
**Assignee:** Kimi
**Auditor:** Gemini (pending hostile-reviewer cross-review)

## Summary

All 5 defense paragraphs (Track C) have been inserted into the manuscript. Net word-count increase: **+323 words** (5,792 → 6,115 before final cut; actual post-R9A baseline was 4,792 → 5,115). Well within the 5,700-word ceiling.

## Defense Paragraph Placement Log

### D1 — Hardware fidelity / no silicon validation
**File:** `sections/06_discussion.tex` §6.5 Limitations  
**Placement:** New paragraph after the opening scope sentence, before D3.  
**Key claim:** Behavioral fidelity is sufficient to rank deployment risks before fabrication closes; SPICE-level phenomena deferred to follow-on work.  
**Citations used:** `rasch2021aihwkit` ✅  
**Word count:** ~65 words  
**Status:** ✅ Inserted

### D2 — Severe-NL 5pp residual gap
**File:** `sections/06_discussion.tex` §6.5 Outlook  
**Placement:** End of Outlook paragraph, after the three extensions.  
**Key claim:** The ~5pp gap reflects training-recipe constraints, not a physical floor; severe-NL is an upper-bound stress test.  
**Citations used:** `Table~\ref{tab:severe-nl-recovery}` ✅  
**Modifications from dispatch template:** Removed references to non-existent `S-CrossHost` and `figS_noise_sweep`. R10D data not yet available, so intermediate-NL claim omitted.  
**Word count:** ~55 words  
**Status:** ✅ Inserted

### D3 — Energy ε_MAC placeholder
**File:** `sections/06_discussion.tex` §6.5 Limitations  
**Placement:** New paragraph after D1, before D5.  
**Key claim:** Energy estimates are first-order analytical projections bounding risk to an order of magnitude; silicon-grade claims deliberately avoided.  
**Citations used:** `Section~\ref{subsec:sensitivity-energy}` ✅  
**Modifications from dispatch template:** Removed specific numerical claims (23.9 μJ, 11.45×, 2.86×) that do not appear in the existing manuscript per "No new numbers" constraint. Replaced with generic per-operation constants already in text.  
**Word count:** ~60 words  
**Status:** ✅ Inserted

### D4 — OPECT single-source
**File:** `sections/05_results.tex` §5.8 end  
**Placement:** Replaced the closing sentence "This literature-anchored case study illustrates..." with the full defense paragraph.  
**Key claim:** OPECT is one validation point chosen for completeness; framework is profile-agnostic by design.  
**Citations used:** `zhang2025opect` ✅, `Supplementary Note S-HW` ✅  
**Word count:** ~70 words  
**Status:** ✅ Inserted

### D5 — CIFAR/Flowers only, no ImageNet
**File:** `sections/06_discussion.tex` §6.5 Limitations  
**Placement:** New paragraph after D3, before the closing fundamental-limitation sentence.  
**Key claim:** Dataset scope trades breadth for non-ideality coverage; ImageNet extension in progress on separate infrastructure.  
**Citations used:** `Section~\ref{subsec:iso-accuracy}` ✅  
**Word count:** ~75 words  
**Status:** ✅ Inserted

## Removed / Replaced Content

| Original text | Location | Reason |
|--------------|----------|--------|
| "The energy estimates assume ideal single-shot programming... not silicon-measured values." | 06_discussion.tex §6.5 | Replaced by D3 paragraph |
| "Likewise, the framework is behavioral rather than circuit-accurate... scalar placeholders or absent." | 06_discussion.tex §6.5 | Absorbed into D1 paragraph |
| "Within these boundaries the study is best understood as a pre-fabrication risk-ranking tool." | 06_discussion.tex §6.5 | Absorbed into D1/D3 |
| "This literature-anchored case study illustrates how the framework links reported physical metrics to algorithm deployment risk." | 05_results.tex §5.8 | Replaced by D4 paragraph |

## Compilation Status

- `main.tex`: ✅ Zero errors, zero warnings
- `supplementary_main.tex`: ✅ Zero errors, zero warnings

## Word Count

| Stage | Words |
|-------|-------|
| Post-R9A baseline | 4,792 |
| Post-R10B-text | 4,792 (+0, figure only) |
| Post-R9C (5 defenses) | 5,115 (+323 net) |
| Ceiling | 5,700 ✅ |

## Open Items for Gemini Audit

1. **D2 sharpness:** Without the intermediate-NL data (R10D pending), does the D2 defense feel like hand-waving?
2. **D3 honesty:** Is "order of magnitude" too vague, or appropriately conservative?
3. **D5 forward-pointer:** Is the "in-progress cross-architecture sweep" claim defensible if no results are yet available?
4. **Tone check:** Do any defenses sound defensive rather than anticipatory?

## Constraints Verified

- [x] No new science
- [x] No new numbers (removed dispatch-template numbers not in existing text)
- [x] No defensive vague language
- [x] Zone discipline preserved
- [x] No "post-fix" / "deployment-fidelity" / "bug-immune" wording introduced
- [x] All citations exist in `refs_gpt.bib`
