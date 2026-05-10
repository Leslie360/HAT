# Paper1 External Artifact Record — 2026-05-10

## Verdict

Paper1 release directory is tracked and internally manifest-clean. The compressed tarball is present locally but remains an external, untracked artifact.

## Current artifact

| Item | Value |
|---|---|
| Tarball path | `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` |
| Tarball size | 10,334,075 bytes |
| Tarball SHA256 | `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6` |
| Git tracking | not tracked |
| Release directory tracked files | 134 |
| Release `cover_letter.pdf` | tracked |
| Release manifest check | PASS |

## Evidence

- Audit log: `logs/external_artifact_record_20260510_155004_20260510.log`
- Manifest command run from release directory: `sha256sum -c SHA256SUMS.txt --quiet`

## Handling rule

Do not force-add the tarball unless the user explicitly requests tracking large external release bundles. Keep the release directory itself as the git-tracked reproducible payload.
