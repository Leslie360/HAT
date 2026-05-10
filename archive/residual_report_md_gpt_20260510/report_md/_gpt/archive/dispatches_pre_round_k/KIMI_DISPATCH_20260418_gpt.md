# Kimi Dispatch — 2026-04-18 Follow-up bundle

**From:** Claude
**To:** Kimi
**Context:** Post inverse-gamma elevation (`BROADCAST_INVERSE_GAMMA_DEEPDIVE_20260418.md`). Main = 14pp, Supplementary = 21pp. 4-contribution structure now live.

Three parallel tasks. K-A is the continuation of what's already in your queue; K-B and K-C are new.

---

## K-A — Finish `KIMI_DISPATCH_20260418_related_work_finish_gpt.md`

This is the previously-issued dispatch. Codex's 2026-04-18 broadcast confirms your 2026-04-17 prose deliverables landed, but this follow-up dispatch has no reply yet. **Complete it** per the brief.

**If the dispatch is already actioned:** reply with the diff and stop.

---

## K-B — Cover letter v2 rewrite (14pp main + 21pp supp, 4 contributions)

**Input:**
- `paper/latex_gpt/cover_letter.tex` (current v1)
- `paper/latex_gpt/sections/00_abstract.tex` (4-contribution phrasing)
- `paper/latex_gpt/sections/01_introduction.tex` (4-contribution bullets)

**What changed since v1:**
1. Fourth contribution now named: **inverse-gamma frontend compensation with shot-noise trade-off** (+5.8 pp at γ_phys=2.0).
2. Main body compressed to 14 pages (from 20) by moving system-architecture figure, FP32 baselines table, result-summary table, NL surrogate equation to supplementary.
3. Supplementary now 21 pages and includes Table S5 (full 5×4 γ_phys × I_dark matrix) + three theory notes (T1 ISP distinction, T2 optimal-γ, T3 attention sensitivity).

**What v2 must say:**
- 4 named contributions (not 3).
- Explicit reviewer-safe novelty boundary on inverse-gamma: we claim *systematic task-level evaluation of a physically-motivated compensation strategy in a CIM context*, not new physics.
- Page budget note: "main text 14 pages, supplementary 21 pages".
- Preserve the existing submission-trajectory narrative (npj→NC framing already in v1).

**Deliverable:** `paper/latex_gpt/cover_letter.tex` edited in-place + a one-sentence rationale note in `report_md/_gpt/COVER_LETTER_V2_RATIONALE.md`. Recompile `cover_letter.pdf` (must stay 2 pages).

---

## K-C — Reviewer-robustness audit of Table S5 + theory notes T1/T2/T3

**Input:**
- `paper/latex_gpt/supplementary.tex` — find `tab:supp-frontend-gamma-scan` and the three `\begin{suppnote}` blocks (`note:frontend-theory`, `note:optimal-gamma`).

**Audit checklist:**
1. **T1 (ISP distinction):** Does it unambiguously separate ISP perceptual gamma from photocurrent-linearization? A skeptical reviewer must not be able to collapse the claim to "this is just gamma correction from a camera".
2. **T2 (optimal γ_comp\*):** The derivation asserts optimal compensation exponent < 1/γ_phys under shot noise. Is the argument self-contained, or does it silently require an assumption the reader can't see? Flag any unstated assumption.
3. **T3 (ViT attention sensitivity):** Is the claim "ViT attention is more sensitive to frontend than CNN classification" backed by a concrete metric or only asserted? If only asserted, propose either a citation or an experimental hook to cite from Codex's pipeline.
4. **Table S5 (5×4 γ_phys × I_dark):** Every cell sourced from `report_md/json/a23_experiment_results.json`? Cross-check 3 random cells. Confirm γ=2.0 avg Δ ≈ +5.5 pp aligns with the main text claim of +5.8 pp at γ=2.0, I_dark=10pA — explain the averaging basis if different.

**Deliverable:** `report_md/_gpt/KIMI_FRONTEND_AUDIT_20260418.md` with ✅/⚠️/⛔ per item, exact line references, and proposed wording patches where needed. Do NOT edit `.tex` directly — Claude routes patches.

---

## Constraints

- No unauthorized `.bib` additions — Kimi's bib-finish dispatch from 2026-04-17 is still the canonical lane for that.
- Reviewer-safe cadence: exploratory tone, no overclaiming.
- If the user stops mid-task, stop immediately and report state.
