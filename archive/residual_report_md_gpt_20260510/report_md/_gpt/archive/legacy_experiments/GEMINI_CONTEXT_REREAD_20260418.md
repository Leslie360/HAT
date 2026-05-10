# Gemini Context Re-read — 2026-04-18

**Reread of canonical state:**
I have successfully synchronized with the latest project bounds and priorities by reviewing `PROJECT_INDEX.md`, `THESIS_VS_PAPER_SCOPE_20260418.md`, `CANONICAL_RESULT_LOCK_gpt.md`, and `PAPER_REVIEW_CLAUDE_20260418.md §4`.

1. **Scope Partition:** The project explicitly divides into a 14-page NC-main, a 21-page NC-supplementary, and an uncapped Thesis-Only archive. Thesis material aggressively includes all pipeline details, measured-device evaluations, and extended ablations (E1–E6).
2. **Locked Canonical Results:** Crucial figures like V4 HAT (87.95%), Ensemble HAT fresh instance (86.37%), and the CrossSim baseline comparisons are strictly frozen. No design or interpretation should conflict with these established anchors.
3. **Current GPU State & NL Mechanisms:** Codex is executing the NL=2.0 mitigation queue. QKV-only mitigation has collapsed (10.15%), while MLP-only and all-linear bounds show recovery (~87%). This indicates attention geometry is acutely vulnerable to severe write-side non-linearity.
4. **Physical Mapping Gaps (Future Work):** Per PAPER_REVIEW §4, 14 physical phenomena remain unmodeled. The most critical missing pieces for the thesis are spatial IR drop (P1), sneak-path currents (P2), and temperature coefficients (P5). These provide the foundation for upcoming thesis-chapter designs.

With these constraints affirmed, I am proceeding as a stateless agent to draft the thesis chapter outlines (G-F, G-G) and execution runbooks (G-H).