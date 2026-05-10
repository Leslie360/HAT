> **⚠️ SUPERSEDED (2026-04-23):** This memo was written under the Round Q assumption that Paper-2 would be a continuation of the ViT Bimodal Basin theory (Route R-A). Claude's `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md` has since explicitly re-routed Paper-2 to **LLM KV-Cache Mapping (Direction C)**. This document is retained for archival purposes but its conclusions are officially VOID. See G-HH21 through G-HH25 for the correct Paper-2 theory.

# G-HH6: Paper-2 Locked Number Scrub
**Date:** 2026-04-21
**Scope:** Phase β

This memo specifically scrubs `paper/paper2/draft_v0/` and `paper/paper2/skeleton_v0/` for locked numbers that must be replaced before Kimi drafts `skeleton_v1/`.

## Scrub List & Replacement Wording

1. **`draft_v0/00_abstract.md`**
   - *Found:* "...results in a severe structural limit (30.53 ± 7.07%)."
   - *Action:* Replace with: "...results in stochastic basin instability with a mean recovery of `[CX-K2 mean 38.95% ± 9.85%]`."

2. **`draft_v0/SKELETON.md`**
   - *Found:* "The ~30 % fresh-instance ceiling is statistically indistinguishable across MLP-only (32.12 ± 7.72 %), all-linear (32.60 ± 9.18 %), and joint training (30.53 ± 7.07 %)..."
   - *Action:* Replace with: "Under 2nd-order STE, the fresh-instance evaluation reveals a bimodal distribution with mean `[CX-K2 mean 38.95% ± 9.85%]`, contrasting with the collapsed first-order baselines (MLP-only `32.12 ± 7.72 %`, all-linear `32.60 ± 9.18 %`)."
   - *Found:* "...while Ensemble HAT without severe NL reaches 86.37 ± 1.54 %."
   - *Action:* **SAFE**. This is the NL=1.0 positive control baseline.
   - *Found:* "10.00 ± 0.00 % (standard HAT fresh-instance collapse)"
   - *Action:* **SAFE**. This is the standard HAT baseline.
   - *Found:* "...joint training (30.53 ± 7.07 %)."
   - *Action:* Replace with `[CX-K2 mean 38.95% ± 9.85%]`.

3. **`skeleton_v0/03_methods.md`**
   - *Found:* "If $r_{Q}+r_{K}>1.8\,d_{h}$, Pillar I is falsified." (and similar $25\%$ deficit claims).
   - *Action:* **SAFE**. Theoretical criteria formulation.
   - *Found:* "The $NL=2.0$ limit reflects the present gradient-scaling surrogate..."
   - *Action:* **SAFE**. Setting parameter.

4. **`skeleton_v0/04_experiments.md`**
   - *Found:* "| E1 | CX-J1b | QKV only | $1.0$ | $2.0$ | 1st | $\sim 30\%$ | $>50\%$ |"
   - *Action:* Replace `~30%` for CX-J1b/c with `[CX-J1b/c actuals: ~26-28%]`.
   - *Found:* "| E3 | CX-J1d-2 | Attn blocks | — | $2.0$ | 2nd (attn) | $\sim 30\%$ (structural) or $>40\%$ (surrogate) | $>50\%$ |"
   - *Action:* Update table to reflect Branch C realization: `[CX-K2 bimodal 38.95%]`.

5. **`skeleton_v0/01_intro.md`**
   - *Found:* "...first-order HAT recipe that succeeds under $	ext{NL}=1.0$ collapses on fresh hardware instances."
   - *Action:* **SAFE**.

**Directive for Kimi:** When drafting `skeleton_v1/`, all references to the single `~30%` structural ceiling must be replaced with the `[CX-K2 mean 38.95% ± 9.85%]` bimodal basin narrative.
