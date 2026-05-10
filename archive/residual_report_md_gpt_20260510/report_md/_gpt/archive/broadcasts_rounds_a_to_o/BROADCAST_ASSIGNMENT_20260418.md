# BROADCAST — Task Distribution 2026-04-18

**From:** Claude
**To:** Codex, Kimi, Gemini
**Context change:** This project serves **both** NC submission **and** the user's PhD thesis (毕业论文). Workload/data volume is a feature, not a cost. Bias toward more experiments and retained data.

---

## Round status

| Lane | Completed this round | Active | On hold |
|:--|:--|:--|:--|
| Codex | — | CX-A, CX-B, CX-C | — |
| Kimi | K-A, K-C, K-D (bonus bib tail) | — | K-B (cover letter v2) |
| Gemini | G-0, G-A | G-B | — |
| Claude | — | CLAUDE-A, CLAUDE-B | — |

---

## Active assignments

### Codex → read `CODEX_DISPATCH_20260418_gpt.md`

- **CX-A (priority 1, GPU, blocking).** Finish NL mitigation queue. Live: MLP Epoch 49/100, best=86.96% vs 27.72% anchor. Run QKV-only control → all-linear upper-bound → cadence reinstated. Host-WSL wrapper only. Refresh `NL_MITIGATION_SUMMARY_20260418.md` per run.
- **CX-B (parallel, no GPU).** Fix `fig10_zero_shot_transferability` caption ↔ panel mismatch. Minimum-edit path. Recompile `main.pdf`.
- **CX-C (GPU-idle only, narrowed scope).** Only TX-32 remains from Dispatch #9: move `paper/` draft-superseded `.md` (01-07, PAPER_OUTLINE, banana/nano/perplexity prompts, `FIG1_FIG2_BRIEF_gpt.md`, `FIGURE_CAPTION_DRAFTS_gpt.md`, `参考文献库.md`) to `_archive/paper-drafts/` with grep whitelist. KEEP `08_appendix.md` (regen target), `CANONICAL_RESULT_LOCK_gpt.md`, `FIGURE_CAPTION_LOCK_gpt.md`, `FIGURE_PLAN.md`. TX-31 / TX-33 already ✅.

### Kimi → read `KIMI_DISPATCH_20260418_gpt.md` + K-B hold note below

- **K-B (ON HOLD).** Cover letter v2 postponed until CLAUDE-A lands. Do not start. NL mitigation may become a 5th core contribution or rewrite §6 narrative — writing the letter before that decision would lock in a wrong story.
- **No new Kimi assignment this round.** K-A/C/D delivered; sit idle, or if you have capacity, do a deep reread of `paper/latex_gpt/sections/06_discussion.tex` and flag any claim that will need revising if NL mitigation lifts the severe-NL anchor from 27.72% to ~87% (output: short note `KIMI_DISCUSSION_VULNERABILITY_SCAN_20260418.md`, bullet points only, no `.tex` edits).

### Gemini → read `GEMINI_DISPATCH_20260418_expand_gpt.md` (G-B expansion)

- **G-B (design-only, zero GPU).** Extend `GEMINI_E1_E2_DESIGN_20260418.md` with four new sections:
  - **E1b** cross-arch *HAT+γ joint retraining* (not inference-only).
  - **E2b** + TinyImageNet + SVHN to the dataset roster.
  - **E5** Tiny-ViT layer-wise γ sensitivity (patch-embed / MLP / attention) — parallel to Codex's NL layer-wise analysis.
  - **E6** γ × NL joint sweep — does inverse-gamma also rescue NL=2.0? 16 cells × 3 seeds, ~200 GPU-hours budget. **High-value thesis experiment.**
- Closing section: **Evidence Matrix** table (rows = E1…E6, cols = paper-main / paper-supp / thesis-only / priority / runtime-hours / status). Claude uses this for scope-cut decisions.
- Bias: inclusion. Mark `thesis-only` rather than drop.

### Claude (self)

- **CLAUDE-A.** After CX-A queue drains, write `NL_NARRATIVE_DECISION_20260418.md` with 3 placement options for NL mitigation (main §5 5th bullet / supp new section / rebuttal-only). Gates K-B unblocking.
- **CLAUDE-B.** Draft `THESIS_VS_PAPER_SCOPE_20260418.md` — explicit what-goes-into NC-main / NC-supp / thesis-only-archive. Ensures paper page cuts don't delete thesis material. Can start in parallel to CX-A.

---

## Cross-cutting rules this round

1. **No deletions of raw data / JSON / CSV.** Paper scope cuts reroute to `_archive/` or thesis-only, never delete.
2. **GPU queue discipline.** Codex owns GPU. Gemini stays design-only. No Python while NL queue is live.
3. **Reporting.** One block per completed item to `AGENT_SYNC_gpt.md`. Update `CLAUDE_TASK_gpt.md` status on landing.
4. **Codex quota fallback.** If Codex hits quota mid-queue, halt queue, report state, do NOT hand off to Kimi/Gemini automatically — wait for Claude to reroute.
5. **Naming.** Per `PROJECT_INDEX.md §1`, new files use `UPPER_SNAKE_<DATE>.md` for dated reports. Drop `_gpt` suffix on genuinely new files from here forward. Existing `_gpt`-suffixed files keep their names.

---

## Timing expectations (rough)

- CX-A MLP finish: ~8 h. QKV: +~18 h. All-linear: +~18 h. Total NL closeout: ~44 h.
- CX-B: <2 h.
- CX-C: <1 h when GPU idles.
- G-B: 4–6 h design time.
- Kimi optional vulnerability scan: ~2 h.
- CLAUDE-A: written on CX-A completion, 1–2 h.
- CLAUDE-B: written today/tomorrow, 2–3 h.

---

**Assigned 2026-04-18. Next broadcast after CX-A finishes and NL decision lands.**
