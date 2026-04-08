# Closeout Checklist (GPT)

This is the final English-side closeout checklist for the current submission package.

It is intentionally short and only tracks the tasks that still matter after data lock.

## Scope Boundary

- Codex owns:
  - `paper/*.md`
  - `paper/latex_gpt/*`
  - `paper/FIGURE_PLAN.md`
  - figure scripts / figure consistency
- Gemini owns:
  - `paper_zh/*`

## Must Finish Before Template Submission

- [ ] Lock the last unresolved bibliography decisions
  - choose the exact `Fault-Aware Training Survey` reference or keep the prose generic
  - finalize the venue-specific bibliographic form for `MemTorch`
- [ ] Final figure-caption consistency pass
  - Fig.4 cross-dataset accuracy
  - Fig.5 degradation / recovery deltas
  - Fig.7 corrected V4 retention (`~79% plateau`)
  - Fig.10 zero-shot transferability wording
- [ ] Keep `paper/FIGURE_CAPTION_LOCK_gpt.md` aligned with the final figure set
- [ ] Port `paper/FIGURE_CAPTION_DRAFTS_gpt.md` into the final venue template
- [ ] Keep `paper/CANONICAL_RESULT_LOCK_gpt.md` aligned with the final tables and captions
- [ ] Keep `paper/latex_gpt/SUBMISSION_PACKET_gpt.md` aligned with the final template payload
- [ ] Draw manual `Fig.1` and `Fig.2`
  - use `paper/FIG1_FIG2_BRIEF_gpt.md`
- [ ] Port the synchronized `latex_gpt` scaffold into the venue template
  - use `paper/latex_gpt/TEMPLATE_MIGRATION_GUIDE_gpt.md`
- [ ] Final claim-strength pass after template migration

## Explicitly Not Required for This Submission Pass

- [ ] ImageNet eval-only
- [ ] V8 / corrected retention-aware retraining
- [ ] multi-seed reruns
- [ ] state-dependent retention drift model
- [ ] conductance INL lookup tables
- [ ] raw measurement -> fitted profile auto-conversion

These remain revision-stage or future-work items unless project priorities change.

## Alignment Notes for Gemini

- Keep `Flowers-102` framed as a **low-data boundary** for HAT, not a generic method failure.
- Keep `Task 34` framed as **distribution-matched recovery**, not universal robustness.
- Keep `Task 35` framed as a **major remaining failure mode**.
- Keep `Task 36` framed as **architecture-gap evidence**, not proof that CNNs are universally robust.
- Keep the manuscript-wide downgrade:
  - `first-order behavioral simulation framework`
