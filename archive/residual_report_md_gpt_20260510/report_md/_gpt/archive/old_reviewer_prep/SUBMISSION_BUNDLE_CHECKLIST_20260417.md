# Submission Bundle Checklist — 2026-04-17

## Scope

This checklist records the current upload-facing manuscript package and the minimum consistency checks that have already been verified locally.

Canonical lightweight bundle directory:

- [outputs/submission_bundle_20260417](/home/qiaosir/projects/compute_vit/outputs/submission_bundle_20260417)

## Ready Now

### Core PDFs

1. Main manuscript
   - [main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf)
   - last modified: `2026-04-17 01:43:37 +0800`
   - current page count from log: `16`

2. Supplementary information
   - [supplementary_main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf)
   - last modified: `2026-04-17 01:44:22 +0800`
   - current page count from log: `15`

3. Cover letter
   - [cover_letter.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.pdf)
   - last modified: `2026-04-17 01:43:36 +0800`
   - current page count from log: `2`

### Reviewer-facing text artifacts

4. Submission handoff packet
   - [SUBMISSION_PACKET_gpt.md](/home/qiaosir/projects/compute_vit/paper/latex_gpt/SUBMISSION_PACKET_gpt.md)

5. Current reviewer response draft
   - [REVIEWER_RESPONSE_DRAFT_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md)

6. Final alignment memo
   - [FINAL_ALIGNMENT_CHECKLIST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/FINAL_ALIGNMENT_CHECKLIST_20260417.md)

7. External-review synthesis memo
   - [EXTERNAL_REVIEW_SYNTHESIS_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_20260417.md)

8. Table-2 provenance response
   - [TX14_TABLE2_RESPONSE_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md)

## Verified Consistency Checks

### Title

- Main title in [main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex) and cover-letter submission line match:
  - `Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision`

### Page counts

- Cover letter now matches the currently compiled manuscript package:
  - main manuscript: `16 pages`
  - supplementary information: `15 pages`

### Figure source directory

- Template migration and submission package should use:
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/`

### Compile state

- `main.log`, `supplementary_main.log`, and `cover_letter.log` are currently clean for:
  - `undefined reference`
  - `multiply defined`
  - `Overfull \hbox`
  - `Underfull \hbox`

## Current Bundle Contents

The lightweight canonical bundle directory currently exposes symlinks to:

- `main.pdf`
- `supplementary_main.pdf`
- `cover_letter.pdf`
- `reviewer_response_draft.md`
- `final_alignment_checklist.md`
- `external_review_synthesis.md`
- `tx14_table2_response.md`
- `submission_packet.md`

## Before Actual Upload

These items are still packaging tasks, not manuscript-writing tasks:

1. Decide whether the reviewer response will be uploaded as Markdown, PDF, or pasted into the portal.
2. Freeze the reviewer archive described in [REVIEWER_ARCHIVE_MANIFEST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/REVIEWER_ARCHIVE_MANIFEST_20260417.md).
3. If the submission portal asks for source-data files separately, collate the figure/source-data files from the manifest into one archive.
4. Recheck portal metadata:
   - title
   - article type
   - data-availability wording
   - code-availability wording
   - page counts

## Known Tracked Caveat

One manuscript-wide statistic-family caveat remains documented but intentionally unchanged in this pass:

- Tiny-ViT CIFAR-10 FP32 appears as `98.06%` in the current main-results baseline presentation, while [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md) separately preserves `97.48%` for another locked statistic family.
- This is already tracked in [TX14_TABLE2_RESPONSE_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md) and was not changed in this bundle pass.

## Outcome

The manuscript package itself is submission-ready in structure. The remaining work is archive assembly and portal-facing packaging, not additional paper editing.
