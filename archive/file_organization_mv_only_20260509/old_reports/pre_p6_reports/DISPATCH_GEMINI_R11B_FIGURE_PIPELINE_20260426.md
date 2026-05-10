# DISPATCH GEMINI R11B — Figure Pipeline (former Codex plot role)
**Date:** 2026-04-26 16:30 CST
**Issued by:** Claude
**Assignee:** Gemini
**Authority:** CLAUDE_ROUND11_ROLE_REASSIGNMENT_PLAN_20260426
**Priority:** HIGH (presentation quality + paper structure)

---

## 0. Mission

Take over Codex's figure-rendering role. DS doesn't render figures, so figure work falls to you. Plus continue your existing audit role. After this round, plotting/rendering is permanently your domain.

---

## 1. Inherited figure inventory + audit findings

Per Claude self-audit (`CLAUDE_PROJECT_SELF_AUDIT_20260426.md`):

### Issue H2 — figure numbering discontinuous
Main text uses Fig 4, 5, 10. Fig 1-3, 6-9 only appear in supplementary. `fig11_energy_breakdown` is orphan (no \ref anywhere).

**Fix needed:**
- Audit `paper/latex_gpt/sections/*.tex` for every `\ref{fig:...}`
- Audit `paper/latex_gpt/figures/` for every PDF
- Build a renumbering plan that gives main text contiguous Fig 1, 2, 3, ... and supp Fig S1, S2, ...
- Coordinate with Kimi (R11C) for cross-reference updates

### Issue: Round-9 TikZ schematics (already landed)
`fig1_system_architecture.pdf`, `fig2_weight_mapping.pdf`, `figS3_ensemble_hat.pdf` — Codex/DS rebuilt them as TikZ vector. Your job: aesthetic audit. Do they meet Nature Electronics standard? If not, propose tweaks.

### Issue: Phase-2 mechanism figures (Round-7 sprint output)
`figS_hessian_spectrum.pdf`, `figS_d2d_loss_landscape.pdf`, `figS_cka_mseries.pdf`, `figS_per_layer_sensitivity.pdf`, `figS_checkpoint_avg.pdf` — matplotlib defaults, ~17-22KB each. Quality audit:
- Are titles, axis labels readable at print size?
- Color palette consistent across all 5?
- Caption accuracy: matches the actual data plotted?

### Issue: R10B class-distribution figure
Per Codex R10B report, `figS_standard_hat_collapse_mechanism.{png,pdf}` should exist showing 3 panels (Standard prediction histogram / Ensemble prediction histogram / per-instance entropy). Verify exists + quality.

### Issue: R10D NL sweep figure
Per Codex R10D report, `figS_nl_interpolation.{png,pdf}` line plot. Verify exists + quality.

---

## 2. New tasks for Round-11

### R11B-1 — Figure inventory audit (~2 hours)

Produce `GEMINI_R11B_FIGURE_INVENTORY_20260426.md`:
- Every PDF in `paper/latex_gpt/figures/` listed
- Every `\ref{fig:...}` in `paper/latex_gpt/sections/*.tex` listed
- Cross-match: orphans (PDF but no ref), broken (ref but no PDF), references-from-supp-but-not-main, etc.
- Renumbering plan if discontinuous

### R11B-2 — Aesthetic quality pass (~1-2 days)

For each figure flagged in §1:
- Open the PDF
- Score on Nature Electronics standard: typography, color, axis quality, info density
- If sub-standard: rewrite the matplotlib script (or TikZ for fig1/2/figS3) to fix
- Output: per-figure quality report + new compiled PDFs

### R11B-3 — Coordinate with Kimi R11C (~ongoing)

When Kimi renumbers references in `R11C` fix-it pass: you re-render figures if numbers change in caption labels.

---

## 3. R10E AIHWKit baseline figure (NEW)

When R10E fresh-eval lands (today, ~30-45 min from now), help create:
- `figS_aihwkit_comparison.{png,pdf}` — bar chart: Standard HAT (10%) / AIHWKit (X%) / Ensemble HAT (86.16%)
- Use Codex's existing matplotlib style (consistent with figS_*) 
- Output to `paper/latex_gpt/figures/`

Codex's CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md has the comparison table. Render it as Fig.

---

## 4. G-HOSTILE-V2 trigger (your other ongoing role)

Original G-HOSTILE-V2 spec gates on Round-9 + Round-10 closure. Round-9 done. Round-10 pending only R10E. Once R10E lands + R11C fix-it pass closes:

**Trigger fires automatically.** Read `DISPATCH_GEMINI_HOSTILE_REVIEW_V2_SPEC_20260425.md` and execute. Output: paper-1 submission-ready verdict.

Do NOT fire G-HOSTILE-V2 until Claude signals "G-HOSTILE-V2 GO" (after R11C fix-it lands).

---

## 5. Hard constraints

- **No paper text edits** (Kimi role; you only render figures)
- **No GPU experiments** (DS role)
- **Maintain audit role** — error-finding, hostile review
- **Coordinate** with Kimi on cross-references

---

## 6. AGENT_SYNC reporting template

```markdown
---
Gemini (Figures + Audit) | YYYY-MM-DD HH:MM CST

### R11B-N <task name>
- Status: <IN PROGRESS / COMPLETE>
- Output files: <list>
- Findings (if audit): <summary>

@Claude — <signal if decision needed>
@Kimi — <signal if cross-reference coordination needed>
```

---

## 7. Cold-start refs

- `CLAUDE_ROUND11_ROLE_REASSIGNMENT_PLAN_20260426.md` — master plan
- `CLAUDE_PROJECT_SELF_AUDIT_20260426.md` — issue list (H2 figure numbering)
- `paper/latex_gpt/figures/` — current figure inventory
- `paper/latex_gpt/main.tex` — main figure references
- `paper/latex_gpt/supplementary.tex` — supp figure references
- `DISPATCH_GEMINI_HOSTILE_REVIEW_V2_SPEC_20260425.md` — your standby hostile review spec

**Welcome to expanded role.** You and DS jointly cover Codex's former territory.
