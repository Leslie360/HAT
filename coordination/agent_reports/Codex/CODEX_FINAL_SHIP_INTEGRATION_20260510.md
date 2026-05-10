# Codex Final Ship Integration — 2026-05-10

## Verdict

`paper1_release_ready_with_external_tarball_after_final_narrative_polish; thesis_content_locked_draft_metadata_pending; paper2_107_audit_only`

## Final Paper1 Artifact

| Artifact | Current state |
|---|---|
| Release directory | `paper1/release/paper1_submission_bundle_20260509_final/` |
| External tarball | `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` |
| Tarball SHA256 | `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6` |
| Manifest check | PASS: `sha256sum -c SHA256SUMS.txt` |
| Cold-unpack manifest check | PASS |

This SHA supersedes the earlier `10acca...`, `69fd3a3c...`, `2618fdce...`, and `a83a6d...` notes for the same local artifact path. The tarball remains ignored by `.gitignore`; force-adding it is a separate user decision.

Release-packaging note: the submission manifest contains 133 payload files. Ignored LaTeX sidecars may exist locally after rebuilds but are excluded from the manifest and tarball. `paper1/release/paper1_submission_bundle_20260509_final/cover_letter.pdf` is ignored by git but included in the manifest and tarball; force-add it only if a git checkout of the release directory must be self-contained.

## Final PDF State

| PDF | Pages | Size |
|---|---:|---:|
| `paper1/manuscript/main.pdf` | 13 | 263202 bytes |
| `paper1/manuscript/supplementary_main.pdf` | 40 | 2826341 bytes |
| `paper1/manuscript/cover_letter.pdf` | 2 | 64267 bytes |
| `paper1/manuscript/cover_letter_v3.pdf` | 1 | 57629 bytes |
| `paper1/release/paper1_submission_bundle_20260509_final/main.pdf` | 13 | 263202 bytes |
| `paper1/release/paper1_submission_bundle_20260509_final/supplementary_main.pdf` | 40 | 2826341 bytes |
| `paper1/release/paper1_submission_bundle_20260509_final/cover_letter.pdf` | 2 | 64267 bytes |
| `thesis/cn/main.pdf` | 102 | 1346437 bytes |
| `thesis/en/main.pdf` | 72 | 689060 bytes |

## Verification Summary

| Check | Result |
|---|---|
| Root and `compute_vit` `git diff --check` | PASS |
| Paper1 final narrative polish | PASS: Related Work, Methods, and Discussion no longer use one-paragraph micro-headings; only substantive Results subsections remain. |
| Paper1 active/release main build logs | PASS for scanned LaTeX errors, undefined refs/cites, rerun warnings, and `Overfull \hbox`. |
| CN/EN thesis LaTeX errors, undefined refs/cites, rerun warnings | PASS for scanned patterns |
| CN/EN thesis overfull hbox scan | PASS; no `Overfull \hbox` entries in current logs |
| Paper1 cover-letter future-tense/placeholder scan | PASS for `will be provided`, `will follow`, `To be provided`, `Corresponding author`, and bracketed thesis placeholder tokens |
| Active/release old-claim scan | PASS for active TeX/PDF claim-bearing artifacts; numeric JSON provenance still intentionally retains single-checkpoint historical values with explicit reporting notes |
| Paper2/107 | BLOCKED: `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED` |

PDF text scans still find `Nature Communications` only in bibliography/literature-reference contexts, not as the target journal in cover letters.

## Remaining Decisions

| Item | Decision needed |
|---|---|
| Thesis formal metadata | Advisor, department/college, official degree wording, university, and final submission/defense date require user or university confirmation. |
| Release tarball handling | Keep as external artifact with SHA above, or explicitly force-add despite `.gitignore`. |
| Release cover-letter PDF handling | Keep as tarball-only, or force-add `paper1/release/paper1_submission_bundle_20260509_final/cover_letter.pdf` so the tracked release directory itself passes its manifest check. |
| Git commits | Use exact path staging by logical group; no broad `git add -A`; no push without explicit user approval. |
