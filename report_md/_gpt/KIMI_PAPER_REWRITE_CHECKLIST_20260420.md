# KIMI PAPER REWRITE CHECKLIST (K-Y22 Update)
**Status:** Pre-staged edits only. NO PROSE MODIFICATIONS to actual files until GPU loop closure.

## Deferred Edits (From Arbitration 2026-04-20)
When the loop closure trigger fires, execute the following surgical prose edits:

1. **`paper/00_abstract.md`:** 
   - *Target:* "chance level for balanced 10-class task" phrasing.
   - *Action:* Clarify the chance-level baseline context rigorously.
2. **`paper/05_results.md` (§3.4):**
   - *Target:* No-AMP verification paragraph.
   - *Action:* Strengthen the evidence showing the 10.00% collapse is not a mixed-precision artifact.
3. **`paper/05_results.md` (§4.5):**
   - *Target:* Training overhead footnote.
   - *Action:* Expand on the computational cost/overhead of the mitigations.
4. **`paper/cover_letter.md`:**
   - *Target:* Main contribution framing.
   - *Action:* Integrate the "simulation baseline + risk ranking" argument drafted in `GEMINI_COVER_LETTER_FRAMING_MEMO_20260420.md`.

*Note: Phase α/β Chinese thesis work is continuing independently in `paper/thesis_cn/`.*