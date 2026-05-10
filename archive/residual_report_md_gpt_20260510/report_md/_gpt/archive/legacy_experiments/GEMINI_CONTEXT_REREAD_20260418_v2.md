# Gemini Context Re-read v2 — 2026-04-18

**Reread of canonical state:**
I have re-read `CLAUDE_A_DECISION_FINAL_20260418.md`, `PRE_SUBMISSION_CHECKLIST.md`, `R1_R4_LANDING_AUDIT_20260418.md`, and `NL_LANE_RESULTS_20260418.md`.

**(a) What Option B means for §6 and §7:**
Option B locks the NL mitigation story as a supplementary ablation (Table SX.N) rather than promoting it to a 5th main-paper contribution. The narrative maintains the 4 original contributions. Severe NL=2.0 is framed as a baseline-recipe bottleneck, and the text in the main paper simply points to the supplement to note that the MLP channel-mixing path is the dominant recoverable failure site.

**(b) What's still pending:**
- **B1**: `attn_proj-only` NL mitigation is still running (started ~17:00).
- **B2**: Integration of the `attn_proj-only` result into Table SX.N row (e) once B1 finishes.
- **D13**: The decision on how to handle Figure 4's mixed error bars (split panel vs. caption disclosure vs. computing MC for bare cells) remains deferred to post-attn_proj.

**(c) Open question for Claude:**
*Given that the MLP-only rescue is largely a source-domain recovery and does not inherit the Ensemble-HAT fresh-instance transferability (fresh-instance mean is only 32.12±7.72%), should the thesis chapter still pursue MLP-only linearization as the ultimate architectural solution, or should it shift focus toward developing robust training recipes for the highly sensitive QKV path?*