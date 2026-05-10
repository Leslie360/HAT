# Codex Phase P4 Final Acceptance

**Date:** 2026-05-09
**Owner:** Codex
**Scope:** Paper-1 submission bundle, provenance archive, post-audit mutation check

## Verdict

**P4 accepted.** The reviewer-facing submission bundle is now the active Paper-1 submission artifact.

Active submission bundle:

- `release_artifacts/paper1_submission_bundle_20260509_final/`
- `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`

Historical provenance archive:

- `release_artifacts/paper1_provenance_archive_20260509/`
- `release_artifacts/paper1_provenance_archive_20260509.tar.gz`

The provenance archive is not active claim material. It preserves deprecated/historical data only.

## Codex Final Checks

Codex independently re-ran the core guards after Kimi delivery and DS/Mimo PASS reports.

| Check | Result |
|---|---:|
| Submission stale-string scan | 0 hits |
| Main PDF stale text scan | 0 hits |
| Supplementary PDF stale text scan | 0 hits |
| Build/draft/checkpoint residue scan | 0 files |
| Files >10 MB inside submission bundle | 0 files |
| SHA256 verification | all OK |
| Submission file count | 133 files |
| Checksummed files | 132 files; `SHA256SUMS.txt` excludes itself |
| Compressed submission archive | 9.8 MiB |
| Compressed provenance archive | 38 MiB |

## Codex Corrections Applied

Two narrow corrections were applied during final acceptance.

1. **Release README cover-letter wording fixed.**
   - Old wording implied `cover_letter.tex` was source-only.
   - Actual P4 package includes `cover_letter.pdf`.
   - `RELEASE_README.md`, `MANIFEST_FILES.txt`, and `SHA256SUMS.txt` were refreshed.

2. **Post-audit Gemini drift mutation corrected in working source.**
   - Broadcast reported a post-audit change that standardized `Delta Drift` as `Fresh - 24h/1d`.
   - That definition is rejected for Paper-1.
   - Locked definition remains: `Delta Drift = retention-eval 0 s accuracy - retention-eval 24 h/1d accuracy`.
   - Working source `paper/latex_gpt/sections/05_results.tex` was restored to canonical values:
     - 8-bit PCM: `0.04 pp`
     - 6-bit PCM: `0.07 pp`
     - 4-bit PCM: `4.01 pp`
   - `paper/latex_gpt/main.pdf` was rebuilt and text-checked.

The final submission bundle already had the correct canonical drift values; the mutation primarily affected the working manuscript tree.

## Locked Canonical Numbers

| Precision | Fresh Acc. | 1 h Acc. | 24 h Acc. | Delta Drift | Role |
|---|---:|---:|---:|---:|---|
| 8-bit PCM | 77.60% | 77.49% | 77.57% | 0.04 pp | Drift-flat reference |
| 6-bit PCM | 68.55% | 68.57% | 68.46% | 0.07 pp | D2D-sensitive transition zone |
| 4-bit PCM | 76.68% | 74.04% | 72.64% | 4.01 pp | Drift-limited regime |

## Acceptance Conditions

P4 is accepted under these operating rules:

1. The active reviewer/submission artifact is `paper1_submission_bundle_20260509_final`, not older P2/P3 bundles.
2. Deprecated old-protocol data may be referenced only as provenance and must not re-enter active claims.
3. Any future edits to Paper-1 numbers, equations, or captions require a new Codex acceptance pass.
4. Gemini visual work may continue only under user direction; it must not alter scientific semantics.
5. DS/Mimo audits are considered valid for the final bundle after the README wording/hash refresh because no scientific content changed.

## Next Phase

Proceed to P5: post-audit lock, cold unpack verification, remote 105/107 task refresh, and long-horizon experiment governance.
