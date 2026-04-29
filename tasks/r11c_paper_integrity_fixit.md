# Task: R11C Paper Integrity Fix-It (11 issues, bundled)

**task_id:** r11c_paper_integrity_fixit
**priority:** HIGH (submission-blocking presentation polish)
**target output:** `outputs/r11c_paper_integrity_fixit.md`

---

## Background

Claude self-audit (`report_md/_gpt/CLAUDE_PROJECT_SELF_AUDIT_20260426.md`) flagged 11 outstanding paper integrity + structure issues. All preserve numerical claims; this is presentation polish, not new science. Most are surgical edits.

V6 PHANTOM (C1) is **already fixed** by Claude in `paper/latex_gpt/supplementary.tex` L132 (95.82±0.12 → 82.58 single-seed, real value from `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json`). Pipeline should verify this stayed fixed and grep for stragglers.

---

## Goal

Close all 11 issues in one bundled pass, with `latexmk -pdf main.tex` returning RC 0 zero undefined refs. Word count post-fix must satisfy main body ≤ 5,700.

---

## Issue list (full spec)

### CRITICAL (data integrity)

**C1 — V6 PHANTOM** (DONE, verify only)
- Verify `paper/latex_gpt/supplementary.tex` L132 reads `82.58 (single-seed)`, not `95.82 ± 0.12`
- Grep `95.82` across `paper/latex_gpt/` — must return zero hits

**C2.1 — broken supp note ref**
- File: `paper/latex_gpt/sections/05_results.tex:41`
- Reads: `Supplementary Note S-Verification` (does not resolve)
- Fix: change to `Supplementary Information S1` (matching the FP32-no-AMP confirmation actually in `supplementary.tex` §S1)

**C2.2 — missing supp figure ref**
- File: `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex:33`
- Reads: `Supplementary Fig.~S-Resampling-Cadence` (does not exist)
- Fix: REMOVE the reference (preserve theoretical argument; figure is out of R11C scope)

**C2.3 — cross-doc table ref**
- File: `paper/latex_gpt/sections/05_results.tex:101`
- Reads: `tab:r10d-nl-interpolation` (lives in `supplementary.tex:724`; resolves to `??` because main.tex doesn't `\input{supplementary.tex}`)
- Fix: REPLACE with prose: "Detailed NL-interpolation results are provided in the Supplementary Information"

**C3 — C2C noise mis-classified as per-instance**
- File: `paper/latex_gpt/sections/02_related_work.tex:7`
- Wrong: lists C2C noise alongside D2D mismatch as "fixed per hardware instance"
- Right: C2C is per-forward-pass; only D2D is per-instance
- Fix: replace that sentence with:
  > "Hardware-induced perturbations decompose into device-to-device (D2D) mismatch—spatially structured and fixed for a given fabricated instance—and cycle-to-cycle (C2C) noise—stochastic per-read with zero mean."

**C4 — V7 contradiction**
- File 1: `paper/latex_gpt/sections/03_methodology.tex:50` — "V7 evaluates retention drift"
- File 2: `paper/latex_gpt/sections/04_experimental_setup.tex:24` — "V7 & Legacy retention-aware model, excluded from canonical claims"
- Fix in 03_methodology.tex:50: rewrite to refer to V8 (the corrected retention-aware follow-up in current §5.3) and note V7 is legacy

**C5 — Introduction MLP-path overclaim**
- File: `paper/latex_gpt/sections/01_introduction.tex:9`
- Wrong: "localization of NL=2.0 surrogate failure primarily to the MLP path"
- Reason invalid: `supplementary.tex:719` shows under revised gradient-scaling recipe, fresh-instance transfer recovers regardless of which path is protected
- Fix: rewrite to:
  > "and by characterizing the post-hoc behavior of severe nonlinear write under a revised gradient-scaling recipe, recovering deployment accuracy to the ~80-82% band."

### HIGH (structure)

**H1 — appendix relocation**
- Action: `paper/latex_gpt/sections/08_appendix.tex` (~1,200 words) → move into `paper/latex_gpt/supplementary.tex` as new section §S-Appendix
- Update `main.tex` to remove `\include{08_appendix}` (or `\input{sections/08_appendix}`)
- Update any cross-refs in main to point to the new supp section
- Target: main body shrinks from ~16 pages to ~8-10

**H2 — figure renumbering** (coordinate with R11B-1 inventory)
- Read `report_md/_gpt/GEMINI_R11B_FIGURE_INVENTORY_20260426.md` for renumbering plan
- Apply main → contiguous Fig 1, 2, 3, ...
- Apply supp → Fig S1, S2, ...
- Update all `\ref{fig:...}` in `paper/latex_gpt/sections/*.tex` and `paper/latex_gpt/supplementary.tex`
- Verify `fig11_energy_breakdown.pdf` either has a `\ref` or moves to `paper/latex_gpt/figures/deprecated/`

**H3 — duplicate labels (6)**
- Labels: `tab:v4-three-seed-summary`, `tab:provenance`, `tab:sensitivity`, `tab:retention-comparison`, `supp:theory-ensemble-hat`, `eq:weight-perturbation`
- Fix: rename the supplementary copy with a `supp-` prefix (e.g., `tab:supp-v4-three-seed-summary`); update all `\ref` accordingly

**H4 — orphan files (4)**
- `08_appendix.tex` — handled by H1
- `S_energy_provenance.tex` (Round-10 R10H output, never `\input`'d) — add `\input{supplementary/S_energy_provenance}` at the appropriate location in `supplementary.tex`
- `S_opect_distribution.tex` (Round-10 R10C output, never `\input`'d) — same fix
- `S_theory_ensemble_hat_clean.tex` — appears to be duplicate of `S_theory_ensemble_hat.tex`. Diff them; remove the unused one

**H5 — `\branchatag` review-mode macro**
- File: `paper/latex_gpt/main.tex:25`
- Fix: remove or comment out the `\branchatag` macro/command (review artifact)

**H6 — conclusion gap incomplete**
- File: `paper/latex_gpt/sections/07_conclusion.tex:7`
- Current: "5pp gap to NL=1.0"
- Missing: 15pp gap to digital baseline (mentioned in abstract + results)
- Fix: extend sentence to:
  > "leaving a residual ~5 pp gap to the canonical NL=1.0 baseline and ~15 pp gap to the digital reference, primarily due to the joint effect of nonlinear write dynamics and fresh-instance transfer."

---

## Decision rule (reviewer/critic phase)

**Approve** if:
- All 11 issues addressed (or H2 explicitly deferred with note if Gemini inventory not yet landed)
- `latexmk -pdf paper/latex_gpt/main.tex` returns RC 0 with **zero** undefined refs
- `latexmk -pdf paper/latex_gpt/supplementary_main.tex` returns RC 0
- Main body word count ≤ 5,700
- No numerical changes (V6 PHANTOM was a fabrication, not a claim)
- No new content beyond the surgical edits specified above

**Reject** if:
- Any undefined ref remains
- Word count exceeds 5,700
- A fix introduces unnecessary content additions
- Banned wording appears: "post-fix", "deployment-fidelity", "bug-retrospective" (without their hook qualifiers)
- Zone discipline (3A / 3B / 3C) is broken in any edit

---

## Files the pipeline should read

- `report_md/_gpt/CLAUDE_PROJECT_SELF_AUDIT_20260426.md` — original full issue list
- `report_md/_gpt/DISPATCH_KIMI_R11C_PAPER_FIXIT_20260426.md` — issue spec source
- `report_md/_gpt/GEMINI_R11B_FIGURE_INVENTORY_20260426.md` — H2 renumbering plan
- `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json` — V6 real-number provenance for C1 verification
- All files listed in §Issue list above

---

## Files the pipeline will edit

| File | Issues |
|:--|:--|
| `paper/latex_gpt/main.tex` | H1 (remove `\include{08_appendix}`), H5 |
| `paper/latex_gpt/sections/01_introduction.tex` | C5 |
| `paper/latex_gpt/sections/02_related_work.tex` | C3 |
| `paper/latex_gpt/sections/03_methodology.tex` | C4 |
| `paper/latex_gpt/sections/04_experimental_setup.tex` | C4 |
| `paper/latex_gpt/sections/05_results.tex` | C2.1, C2.3 |
| `paper/latex_gpt/sections/07_conclusion.tex` | H6 |
| `paper/latex_gpt/sections/08_appendix.tex` | H1 (DELETE / MOVE) |
| `paper/latex_gpt/supplementary.tex` | H1 (absorb 08_appendix), H3, H4, plus per-section H2 ref updates |
| `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` | C2.2 |
| `paper/latex_gpt/supplementary/S_theory_ensemble_hat_clean.tex` | H4 (DELETE if duplicate) |
| All `*.tex` with `\ref{fig:...}` | H2 (per Gemini inventory) |

---

## Constraints

- **No content additions** beyond the surgical edits specified
- **No numerical changes**
- **Zone discipline preserved** (3A / 3B / 3C unchanged)
- **No bug-retrospective phrasing** (use neutral protocol language)
- **Word count post-fix:** main body ≤ 5,700
- **Compile gate:** `latexmk` RC 0 with zero undefined refs is hard-required

---

## Specific output expected

In `outputs/r11c_paper_integrity_fixit.md`:

1. **Per-issue change log** — for each of the 11 issues: status (DONE / DEFERRED / N/A) + diff snippet + 1-line rationale
2. **Word count summary** — main body before / after, supplementary before / after
3. **Compile verification** — `latexmk` exit codes for `main.tex` and `supplementary_main.tex`, plus undefined-ref count
4. **Grep results** — `95.82` hits across `paper/latex_gpt/` (must be zero post-fix)
5. **Diff summary** showing every file touched

---

## Done definition

- All 11 issues either closed or explicitly deferred with reason
- `latexmk -pdf main.tex` RC 0, zero undefined refs
- `latexmk -pdf supplementary_main.tex` RC 0
- Main body ≤ 5,700 words
- All cross-refs resolve
- Final per-issue change log reads cleanly to a senior reviewer
