# KIMI Red-Team Audit — 2026-04-19

Scope: hostile 8-minute editor pass over the current submission package (`outputs/submission_bundle_20260419/`).

## Verdict

- Recommendation: **send out, not desk-reject**, once user metadata is filled.
- CRITICAL issues: 1
- SHOULD-FIX issues: 2
- NICE issues: 2

## CRITICAL

1. **Bundle metadata placeholders are still visible.**
   - Evidence: `outputs/submission_bundle_20260419/README_SUBMISSION.txt` still contains `TBD` fields for corresponding author, email, and institution.
   - Why it matters: this is the one thing an editor can notice immediately and interpret as an unfinished submission package.
   - One-line patch: replace the three `TBD` fields after the user fills `USER_METADATA_REQUEST_20260420.md`.

## SHOULD-FIX

1. **The supplementary PDF page count increased after the correlated-D2D figure was added.**
   - Current machine-verified count: 23 pages.
   - Any text or checklist still quoting 22 pages should be treated as stale.
   - Patch: normalize future references to `17 / 23 / 2` for main / supplementary / cover.

2. **The Zenodo-ready archive exists but is not yet mentioned in the bundle README.**
   - Not a submission blocker, but it weakens the reproducibility story if someone audits both paths.
   - Patch: add one sentence in the internal submission notes pointing to `release_artifacts/zenodo_archive_v0/`.

## NICE

1. The cover letter could eventually be shortened by one paragraph if the editor demands a terser framing, but the current version is scientifically aligned and no longer contradictory.
2. A future revision could add a dual-curve correlated-D2D figure (standard-HAT collapse line + Ensemble-HAT robustness line), but the current single-curve supplementary figure is adequate because only the Ensemble-HAT correlated run was actually executed.

## Bottom line

The package no longer has scientific credibility gaps that would justify a desk rejection on presentation grounds. The remaining visible weakness is metadata completeness, which is user-owned rather than technical.
