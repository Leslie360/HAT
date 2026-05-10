# Gemini Project Truth Pack (2026-04-13)

> **Purpose:** Gemini has experienced memory loss / stale-context drift in prior rounds.
> **Rule:** Treat this file as the shortest reliable re-entry map for the current project state.
> **Priority:** Read this before relying on old handoffs, old README notes, or historical task narratives.

---

## 1. Current Strategic Truth

The project is **not** in a single-track "rush NC now" mode anymore.

Current strategy:
- **multi-venue**
- **optional high-ROI experiments allowed**
- **measured data is welcome but not a submission prerequisite**
- **Codex is the only source-of-truth gatekeeper**
- **Kimi and Gemini provide planning / audit / draft support**

Do **not** assume:
- `NC` is the only target
- submission is urgent
- no further supplementary experiments are allowed
- measured-device data must arrive before the paper is viable

Canonical strategy documents:
- `MASTER_PLAN.md`
- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/STRATEGY_RESET_20260412_gpt.md`

---

## 2. What the Paper Is

The paper is currently positioned as a:

> **simulation-first, first-order behavioral methodology paper**

It is **not** claiming:
- fabricated-array validation
- tape-out-grade physical closure
- exact chip prediction

It **is** claiming:
- a reusable organic-specific hardware-simulation workflow
- deployment-risk ranking under explicit behavioral assumptions
- structured findings such as:
  - `6-bit ADC cliff`
  - `fresh-instance collapse`
  - `Ensemble HAT recovery`
  - regime-scoped `C2C scale masking`

---

## 3. Current Title and Main PDFs

### Locked working title

`Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision`

### Current compiled files

- `paper/latex_gpt/main.pdf`
- `paper/latex_gpt/supplementary_main.pdf`
- `paper/latex_gpt/cover_letter.pdf`

Current known status:
- `main.pdf`: 16 pages
- `supplementary_main.pdf`: 13 pages
- `cover_letter.pdf`: 2 pages

Use the PDFs only after checking they match current source and compile state.

---

## 4. Real Source of Truth for the Manuscript

For the **paper text**, trust this order:

1. `paper/latex_gpt/main.tex`
2. `paper/latex_gpt/sections/*.tex`
3. `paper/latex_gpt/supplementary.tex`
4. `paper/latex_gpt/cover_letter.tex`

For **project status / decisions**, trust this order:

1. `MASTER_PLAN.md`
2. `report_md/_gpt/CLAUDE_TASK_gpt.md`
3. `report_md/_gpt/AGENT_SYNC_gpt.md` (latest Codex blocks only)
4. `report_md/_gpt/FINAL_SUBMISSION_READINESS_gpt.md`

For **measured-data coordination**, trust:

- `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md`
- `MEASURED_DATA_REQUEST_PRIORITY_TABLE.md`

Do **not** treat old handoff notes as truth unless Codex re-verifies them.

---

## 5. Files That Are Helpful but Can Be Stale

These may still contain useful context, but are **not** truth boards:

- `report_md/_gpt/CODEX_HANDOFF_20260411_gpt.md`
- `report_md/_gpt/GEMINI_HANDOFF_gpt.md`
- older `KIMI_*REPORT*.md`
- older `NEW_REVIEW_*` summaries
- archival `_gpt` analysis memos not referenced by latest Codex sync

If any of these conflict with current source / current PDFs / latest Codex sync, **they lose**.

---

## 6. Locked / Important Numbers

Use these unless Codex explicitly reopens them:

- `Ensemble HAT fresh-instance`: `86.37 ± 1.54%`
- `Zhang 2025 OPECT bridge`: `88.53%`
- `AIHWKIT full benchmark`: `90.08 ± 0.21%`
- `Digital reference for same benchmark`: `95.46%`
- `C4 three-seed`: `84.75 ± 0.72%`
- `V8 retention-aware`: `89.67 ± 0.08%`
- `NL=2.0`: `27.72 ± 0.82%`

If you see a conflicting number in an old memo, assume the memo is stale.

---

## 7. Ensemble HAT Checkpoint Reality

Do **not** claim the Ensemble HAT checkpoint is missing without a provenance audit.

Candidate ensemble checkpoints exist at:
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_last.pt`

Other similarly named checkpoints also exist elsewhere, but these two are the most obvious candidates.

Important rule:
- a failed fresh-instance evaluation does **not** prove the true checkpoint is absent
- it may indicate:
  - wrong eval script
  - wrong mask-resampling protocol
  - stale assumption about how the result was produced
  - confusion between standard-HAT and ensemble-HAT provenance

So treat the issue as:

> **checkpoint provenance / evaluation-protocol audit**

not:

> **missing checkpoint proved**

---

## 8. What Gemini Should Optimize For Now

Gemini is most useful when doing:
- source-grounded wording audits
- experiment prioritization memos
- venue-specific reframing
- measured-data integration planning
- supplementary insertion maps
- provenance audits

Gemini is **less useful** when:
- declaring submission destination as fixed
- declaring experiments mandatory without strategy alignment
- claiming missing files without path-level proof
- treating old handoff summaries as current truth

---

## 9. Current Open Direction

The likely near-term path is:

1. keep the paper submission-ready
2. keep venue choice open
3. optionally run only high-ROI supplementary experiments
4. parallelize measured-data collection from in-group device papers / PhD raw tables
5. use real measured data later as a strengthening upgrade, not as a condition for basic paper validity

---

## 10. If You Need to Re-enter the Project Fast

Read only these 8 files first:

1. `MASTER_PLAN.md`
2. `report_md/_gpt/CLAUDE_TASK_gpt.md`
3. `report_md/_gpt/AGENT_SYNC_gpt.md` (latest Codex block only)
4. `paper/latex_gpt/main.tex`
5. `paper/latex_gpt/sections/05_results.tex`
6. `paper/latex_gpt/sections/06_discussion.tex`
7. `paper/latex_gpt/supplementary.tex`
8. `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md`

If that set conflicts with your memory, trust the files, not the memory.
