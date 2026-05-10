# Claude Review Packet — 2026-04-17

## Purpose

This is the minimal high-signal packet to send Claude for final paper review without flooding it with internal scratch logs.

## Send First

1. [main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf)
2. [supplementary_main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf)
3. [cover_letter.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.pdf)
4. [FINAL_ALIGNMENT_CHECKLIST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/FINAL_ALIGNMENT_CHECKLIST_20260417.md)

## Send If Claude Challenges Data Consistency

5. [TX14_TABLE2_RESPONSE_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md)
6. [NUMERIC_CONSISTENCY_AUDIT_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/NUMERIC_CONSISTENCY_AUDIT_20260417.md)
7. [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md)

## Send If Claude Challenges Reviewer Robustness / Positioning

8. [EXTERNAL_REVIEW_SYNTHESIS_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_20260417.md)
9. [REVIEWER_RESPONSE_DRAFT_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md)
10. [SUBMISSION_BUNDLE_CHECKLIST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/SUBMISSION_BUNDLE_CHECKLIST_20260417.md)

## Send If Claude Challenges Figure/Data Traceability

11. [FIGURE_PROVENANCE_MANIFEST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/FIGURE_PROVENANCE_MANIFEST_20260417.md)
12. [REVIEWER_ARCHIVE_MANIFEST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/REVIEWER_ARCHIVE_MANIFEST_20260417.md)

## Current Known Caveat To Keep Explicit

- The Tiny-ViT CIFAR-10 FP32 `98.06` vs `97.48` statistic-family mismatch remains tracked rather than silently rewritten.
- Source of record for that issue:
  - [TX14_TABLE2_RESPONSE_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md)

## Current Compile State

- `main.pdf`: current compiled manuscript artifact
- `supplementary_main.pdf`: current compiled supplementary artifact
- `cover_letter.pdf`: current compiled cover letter artifact
- Tectonic still prints repeated `.bbl changed` rerun warnings, but current logs are clean for:
  - `undefined reference`
  - `multiply defined`
  - `Overfull \hbox`
  - `Underfull \hbox`

## Optional Convenience Path

A lightweight symlinked handoff directory already exists at:

- `/home/qiaosir/projects/compute_vit/outputs/submission_bundle_20260417/`

If needed, send that directory contents as the canonical current bundle snapshot.
