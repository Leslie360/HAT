# Codex Superphase P3 Final Review

Date: 2026-05-09
Owner: Codex
Scope: Kimi Superphase P3 final delivery, DS P3 audit, Mimo P3 audit, clean bundle inspection

## Verdict

**P3 is accepted as an operational milestone, but the current clean bundle is not yet the final submission-grade bundle.**

Kimi completed all five P3 tracks and DS/Mimo both passed the package. Codex independently verified the major scientific and source-data guards. The active Paper-1 science is still frozen and valid. However, final journal/submission packaging needs one more hardening pass.

## What Passes

- Clean bundle exists: `release_artifacts/paper1_release_candidate_20260509_clean/`
- File count: 207 files
- Draft/backup/temp patterns: 0 hits
- Checkpoint patterns `.pt/.pth/.ckpt`: 0 hits
- Files >10 MB: 0
- SHA256 verification: all files OK
- Main PDF and supplementary PDF exist
- Core source files exist: `main.tex`, `supplementary.tex`, `supplementary_main.tex`, `refs_gpt.bib`, canonical source data
- PDF stale scans: no visible old 6-bit claims
- Clean-room logs inspected by Codex: no actual `undefined` warnings found by grep in generated logs

## Remaining Submission-Grade Issues

These are packaging/professionalism issues, not scientific-result blockers:

1. `RELEASE_README.md` still mentions old `77.86%` in explanatory context. This is historically correct, but it makes naive stale guards fail and may confuse a reviewer.
2. `MANIFEST_FILES.txt` and `SHA256SUMS.txt` include deprecated `seed456_full100` paths because deprecated old-protocol JSON is still bundled.
3. `figures/deprecated_20260424/` is still included in the clean bundle.
4. `figures/tikz/*.aux` and `figures/tikz/*.log` build artifacts are still included.
5. The bundle still includes more figures than strictly needed; this is not fatal, but a final submission bundle should be minimal and intentional.
6. Cover letter remains source-only. Acceptable for internal review, but final package should attempt a cover-letter PDF or explicitly classify it as source-only in a separate submission checklist.

## Decision

Do not call `paper1_release_candidate_20260509_clean/` the final submission package. Treat it as a valid release candidate and base for P4.

Next phase: create separate artifacts:

- `paper1_submission_bundle_20260509_final/` — reviewer/submission-facing only, zero deprecated paths, zero old 6-bit numbers, zero aux/log build products.
- `paper1_provenance_archive_20260509/` — historical provenance, deprecated old-protocol data allowed and clearly documented.

## Locked Science State

No scientific changes are authorized in P4 unless a hard guard failure is found.

Locked PCM ladder:

| Precision | Fresh | 1 h | 24 h | Drift | Role |
|---|---:|---:|---:|---:|---|
| 8-bit PCM | 77.60% | 77.49% | 77.57% | 0.04 pp | Drift-flat reference |
| 6-bit PCM | 68.55% | 68.57% | 68.46% | 0.07 pp | D2D-sensitive transition zone |
| 4-bit PCM | 76.68% | 74.04% | 72.64% | 4.01 pp | Drift-limited regime |

## Codex Recommendation

Proceed to P4: final submission-grade packaging, citation/reference zero-warning check, and provenance split. Kimi should execute; DS/Mimo should audit; Codex will final-accept.
