# Codex Paper1 Post-Broadcast Release Refresh — 2026-05-10

## Verdict

release_refreshed_final_after_final_narrative_polish

## Integrated Inputs

| Input | Outcome |
|---|---|
| `CC_PAPER1_AUTHOR_REVIEW_20260510.md` | Integrated. Verdict was `minor_edits`. |
| User final narrative concern | Integrated. Paper1 was not treated as closed until text-level author polishing was completed. |
| Table 1 caption phrase `Data establish...` | Rewritten in active and release sources. |
| Supplement `\notrun{}` / `n.e.` wording | Replaced with explicit `not evaluated` wording. |
| Stale single-checkpoint `86.37±1.54` in active/release plotted figures | Replaced with the current `86.16±0.19` three-seed framing in `fig_fresh_instance_ablation` and `figS3_ensemble_hat`. |

## Files Updated

| Area | Summary |
|---|---|
| Active Paper1 manuscript | Rebuilt `main.pdf`, `supplementary_main.pdf`, and `cover_letter_v3.pdf`. |
| Active Paper1 figures | Regenerated `fig_fresh_instance_ablation` from the current three-seed source and refreshed `figS3_ensemble_hat`. |
| Cover letter | Removed future-tense availability phrasing from the release cover letter and refreshed the active/release PDF artifact. |
| Final release bundle | Synced active accepted sources/PDFs, refreshed manifest/checksums, and rebuilt tarball after the cover-letter closeout. |
| Final narrative de-heading pass | Related Work, Methods, Discussion, and the Results tail were rewritten as continuous prose rather than one-heading/one-paragraph blocks. |
| Plotting script | Updated `plot_fig_fresh_instance_ablation` to use the current three-seed canonical JSON for Ensemble HAT reporting. |

## Verification

| Check | Status |
|---|---|
| `paper1/manuscript/main.pdf` build | PASS; 13 pages, 263202 bytes. |
| Release `main.pdf` build | PASS; 13 pages, 263202 bytes. |
| `paper1/manuscript/supplementary_main.pdf` build | PASS; 40 pages, 2826341 bytes. |
| `paper1/manuscript/cover_letter.pdf` build | PASS; 2 pages, 64267 bytes. |
| Release `SHA256SUMS.txt` | PASS. |
| Release cold-unpack SHA check | PASS. |
| Active/release claim-bearing TeX stale scan | PASS for `86.37`, `1.54`, `Data establish`, `notrun`, `n.e.`, `AIHWKIT`, `completely collapses`, `Future Directions`, `68.55`, `0.07 pp`. Numeric JSON provenance intentionally retains historical single-checkpoint values with explicit reporting notes. |
| Active/release PDF stale scan | PASS for the same patterns across main, Supplementary, and refreshed figure PDFs. |

## Release Artifact

| Artifact | SHA256 |
|---|---|
| `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` | `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6` |

This final SHA supersedes the earlier `10acca...`, `69fd3a3c...`, `2618fdce...`, and `a83a6d...` notes for the same local artifact path.

## Logs

| Log | Purpose |
|---|---|
| `logs/paper1_main_post_broadcast_fix_20260510.log` | Main manuscript rebuild. |
| `logs/paper1_supplementary_post_figure_fix_20260510.log` | Supplementary rebuild after figure refresh. |
| `logs/paper1_cover_letter_v3_post_broadcast_fix_20260510.log` | Cover letter v3 rebuild. |
| `logs/paper1_release_sha_check_after_figfix_20260510.log` | Release checksum verification. |
| `logs/paper1_release_cold_unpack_sha_after_figfix_20260510.log` | Cold-unpack checksum verification. |
| `/tmp/paper1_release_sha_coverletter_20260510.log` | Release checksum verification after cover-letter closeout. |
| `/tmp/paper1_release_cold_coverletter_20260510.log` | Cold-unpack checksum verification after cover-letter closeout. |
