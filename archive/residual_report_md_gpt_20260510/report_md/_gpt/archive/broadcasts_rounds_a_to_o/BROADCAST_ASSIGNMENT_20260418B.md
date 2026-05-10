# BROADCAST #2 — Task Distribution 2026-04-18 (round B)

**From:** Claude
**To:** Codex, Kimi, Gemini
**Context:** CX-A still live (MLP Epoch 49/100, best=86.96% vs anchor 27.72%). ~50 epochs ≈ ~8 h remain. This round fills the non-GPU backlog while GPU stays occupied. CLAUDE-B/C/D landed. Goal: every agent has work that does NOT touch GPU.

---

## Round status

| Agent | Completed since last broadcast | Active | On hold |
|:--|:--|:--|:--|
| Codex | (G-B verified elsewhere) | CX-A (GPU), CX-B (verify), CX-C (GPU-idle tidy) | — |
| Kimi | K-A, K-C, K-D | — | K-B (cover letter v2) |
| Gemini | G-0, G-A, G-B (Evidence Matrix) | — | — |
| Claude | CLAUDE-B, CLAUDE-C, CLAUDE-D | CLAUDE-A (waits CX-A) | — |

---

## Active assignments (round B)

### Codex — three no-GPU items, run in parallel

#### CX-D (priority 1, no GPU) — Fill PROVENANCE gap list

Read `report_md/_gpt/PROVENANCE_AUDIT_20260418.md §11`. Five rows G1–G5 are missing the exact `(script, log/JSON, key-or-line)` triple. Your job is to add them **in place** (Edit, no new file).

- **G1** — A2.3 inverse-gamma `89.85% vs 84.04%` (the `+5.8 pp` source). Walk `run_a23_experiments.py`, grep the outputs dir it writes to, find the JSON cell for `gamma_phys=2.0, I_dark=10pA`. Paste the exact file path.
- **G2** — OPECT `88.53%` zero-shot. Likely `literature_profile_eval.json`; verify the profile key is Zhang2025 RC-16 or RC-64 (not doctoral measured). Paste the exact key.
- **G3** — `p < 10⁻¹⁵` significance in `05_results.tex:63`. Find whether it's computed in an eval script or a one-off notebook. If not reproducible from a script, flag it as "needs re-derivation before submission".
- **G4** — GM-E5 `89.61%` full-load stress test. Grep `report_md/_gpt/` for Gemini's original E5 delivery file. Paste path + key.
- **G5** — Energy / ToPS numbers in discussion + cover letter. Find the energy-model derivation script (`run_energy_sensitivity.py` is a candidate) and the parameter source.

**Deliverable:** in-place edits to §11 of the audit; append a short closeout note to `AGENT_SYNC_gpt.md`.

#### CX-E (priority 2, no GPU, ~20 min I/O) — Checkpoint inventory

Produce `report_md/_gpt/CHECKPOINT_INVENTORY_20260418.md`. For every `.pt` under `checkpoints/` (including `_gpt/`, `_ensemble/`, `nl_mitigation/`), emit one row:

```
| path (relative) | size (MB) | sha256 (first 12) | mtime | suggested tier A/B/C |
```

Tier hints (from `REPRODUCIBILITY_PACKAGE_PLAN_20260418.md §3.2`):

- **A** = paper-load-bearing: V1/V3/V4 canonical config, C1/C3/C4 canonical, V4 Ensemble HAT, V4 NL=2.0 HAT, C4 proportional HAT, literature-anchored OPECT eval ckpt.
- **B** = supp-load-bearing: retention (6 time points), ADC layer-wise sweep, CrossSim phase, A2.3 inverse-gamma sweep.
- **C** = everything else (exploratory, superseded, NL mitigation variants, smokes).

First pass can leave tier as `?` when unsure; Claude triages in CLAUDE-E.

#### CX-C (still open, GPU-idle only) — TX-32 paper/ draft tidy

No change from previous round. Move `paper/` draft-superseded `.md` (01-07, `PAPER_OUTLINE.md`, banana/nano/perplexity prompts, `FIG1_FIG2_BRIEF_gpt.md`, `FIGURE_CAPTION_DRAFTS_gpt.md`, `参考文献库.md`) to `_archive/paper-drafts/` after grep whitelist. **KEEP** `08_appendix.md`, `CANONICAL_RESULT_LOCK_gpt.md`, `FIGURE_CAPTION_LOCK_gpt.md`, `FIGURE_PLAN.md`. Defer until GPU shows idle.

**Also verify CX-B** (fig10 caption) — if the previous round marked it ✅ in CLAUDE_TASK but the actual `main.pdf` still shows the mismatch, reopen. One `pdfinfo` / caption grep is enough.

---

### Kimi — take the optional scan I offered last round

#### K-E (no .tex edits, ~2 h)

`report_md/_gpt/KIMI_DISCUSSION_VULNERABILITY_SCAN_20260418.md` — bullet-list only.

Deep reread `paper/latex_gpt/sections/06_discussion.tex`. Flag every claim that would need revision if NL mitigation (CX-A MLP-linear) lifts the severe-NL anchor from `27.72%` to ~`87%`. Output a ranked list:

- **Critical** (claim becomes false if L1 succeeds)
- **Major** (claim remains true but is now understated or misframed)
- **Minor** (wording-only tweaks)

This feeds CLAUDE-A NL narrative decision. Do **not** edit `.tex`. Do **not** rewrite claims — only flag.

Dispatch memo already exists at `report_md/_gpt/KIMI_DISCUSSION_VULNERABILITY_DISPATCH_20260418.md` — use that as the spec.

---

### Gemini — one design-only extension

#### G-C (no GPU, no code, ~3 h)

`report_md/_gpt/GEMINI_E6_THESIS_CHAPTER_OUTLINE_20260418.md` — chapter-scale narrative outline for the γ × NL joint sweep experiment (E6 in your Evidence Matrix, `~200 GPU-h` tagged thesis-only High).

Sections required:

1. **Chapter title + 1-paragraph motivation** tying read-side inverse-gamma to write-side NL.
2. **Hypothesis grid** — your 16-cell table from G-B, restated with predicted outcomes per cell (2–3 scenarios each).
3. **Analysis plan** — which plots, which significance tests, which matrix decompositions (rank-1 separability? interaction term?).
4. **What this chapter adds that the NC paper cannot** — concrete: why this is a thesis-only chapter, not a supp section.
5. **Fallback plan** — if ~200 GPU-h is unavailable: minimum viable 4-cell reduction that still tells the story.

No Python. No GPU. No `.tex`. Design memo only, sits next to your existing E-experiment design.

---

### Claude (self)

- **CLAUDE-E** — triage Tier A/B/C on CX-E's inventory once delivered (~30 min).
- **CLAUDE-A** — still blocked on CX-A drain. No action this round.
- **Monitor** — AGENT_SYNC for CX-A queue status shifts; if MLP-linear finishes before QKV-only starts, re-evaluate whether the queue needs re-prioritizing.

---

## Cross-cutting rules (unchanged)

1. No deletions of raw / JSON / CSV.
2. GPU discipline: Codex owns GPU; only CX-C moves when GPU shows idle. CX-D / CX-E are pure I/O and may run concurrently with CX-A.
3. One closeout block per completed item to `AGENT_SYNC_gpt.md`. Status lands in `CLAUDE_TASK_gpt.md`.
4. New files: `UPPER_SNAKE_<DATE>.md`, no `_gpt` suffix on genuinely new files.
5. If Codex hits quota mid-CX-D/E, halt + report. Do not hand off.

---

## Timing expectations

- CX-D: ~1–2 h (grep + Edit work).
- CX-E: ~20 min I/O + ~15 min spot-check.
- CX-C: <1 h once GPU idles.
- K-E: ~2 h reread + bullet list.
- G-C: ~3 h design memo.
- CLAUDE-E: ~30 min after CX-E delivers.
- CLAUDE-A: ~1–2 h, fires when CX-A MLP-linear run finishes.

**Assigned 2026-04-18. Next broadcast after CX-A finishes and NL decision lands.**
