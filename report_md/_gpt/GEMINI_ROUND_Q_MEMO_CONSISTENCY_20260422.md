# G-DR1: Round-Q Memo Consistency Scrub
**Date:** 2026-04-22

This scrub audits all major `_gpt` memos mentioning `J1d`, `K2`, or `K3` to ensure narrative consistency and prevent conflicting claims during loop closure.

| File | Claim | Status | Action Recommendation |
| :--- | :--- | :--- | :--- |
| `CODEX_J1D_RECONCILIATION_20260421.md` | Canonical J1d is 41.53 ± 8.87% | `authoritative` | Keep as baseline reference. Ground truth for J1d. |
| `CODEX_CX_K2_SUMMARY.md` | N=30 extension yields 38.95 ± 9.85% | `authoritative` | Primary bimodal evidence point. Replaces J1d as the core evaluation metric. |
| `CODEX_CX_K3_PROGRESS_20260422.md` | K3 dg_eff=0.05..0.20 shows degradation | `authoritative` | Use as live trend. Await 0.25 for final conclusion. |
| `CODEX_CX_K3_SUMMARY.md` (prior) | dg_eff shifts mean up to 45.2% | `stale / contradicted` | DEPRECATE. Erroneous prior scaffold. |
| `CODEX_J1D_CEILING_BROKEN_REPORT.md` | J1d > 50%, ceiling broken | `stale / contradicted` | DEPRECATE. Based on false initial reading. |
| `CODEX_BRANCH_A_CONFIRMED.md` | J1d < 35%, structural limit | `stale / contradicted` | DEPRECATE. Based on incomplete evaluation. |
| `GEMINI_J1D_BRANCH_SYNTHESIS_20260421.md` | 38.95% triggers Branch C (Bimodal Basin) | `authoritative` | Safe to build upon. Narrative anchor. |
| `GEMINI_BIMODAL_BASIN_THEORY_20260421.md` | Higher-order surrogate exposes shattered landscape | `authoritative` | Safe to build upon. Core theory for Paper-2. |
| `GEMINI_DGEFF_MEAN_FIELD_20260421.md` | dg_eff acts as annealing, shifting mean up | `stale / contradicted` | REVISE. K3 live data (degradation to ~27-36%) contradicts this. Drift actively destroys fragile 2nd-order minima. |
| `GEMINI_REWRITE_DECISION_TREE_V2_20260421.md` | Branch C triggered by K2 | `authoritative` | Directs Kimi's loop closure. |
| `GEMINI_PAPER2_ROUTE_FINAL_20260425.md` | Route Modified R-A (Stochastic Basin) | `authoritative` | Paper-2 strategy locked. |
| `GEMINI_HOSTILE_REVIEW_V4_20260425.md` | Defends bimodal basin claim | `authoritative` | Valid defense strategies. |
