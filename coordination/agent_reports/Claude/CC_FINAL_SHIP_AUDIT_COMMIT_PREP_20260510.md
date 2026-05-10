# Final Ship Audit and Commit-Prep Report — 2026-05-10

## Verdict

`ship_candidate_with_artifact_note`

Paper1 active/release bundle and CN/EN thesis outputs are internally consistent and pass the checks run in this final audit. Paper2/107 remains audit-only and claim-lock blocked. No commit or push was performed.

## Verified deliverables

| Deliverable | Path | Status | Evidence |
|---|---|---|---|
| Paper1 release directory | `paper1/release/paper1_submission_bundle_20260509_final/` | PASS | `sha256sum -c SHA256SUMS.txt` passed for all 133 manifest-covered entries; log `logs/final_ship_release_sha_20260510.log`. |
| Paper1 release tarball | `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` | PRESENT / EXTERNAL ARTIFACT | Current SHA256 `a83a6d5e9f6c1e36f5a70c7ab0bd1c95005ea22d7d35d23782abe124fb828f10`; supersedes earlier final-audit SHA after the later corrected-D2D tarball refresh. |
| Paper1 cold-unpack check | same tarball | PASS | Cold-unpacked tarball and re-ran `sha256sum -c SHA256SUMS.txt`; log `logs/final_ship_cold_unpack_sha_20260510.log`. |
| Paper1 active/release TeX stale scan | active/release main + Supplementary TeX | PASS | No active/release TeX hits for `86.37`, `1.54`, `Data establish`, `notrun`, `n.e.`, `AIHWKIT`, `completely collapses`, `Future Directions`, `68.55`, `0.07 pp`; log `logs/final_ship_paper1_active_release_tex_stale_scan_20260510.log`. |
| Paper1/Thesis PDF stale scan | Paper1 active/release PDFs, CN thesis PDF, EN thesis PDF | PASS | No PDF text hits for the same stale patterns; log `logs/final_ship_pdf_stale_scan_20260510.log`. |
| CN thesis | `thesis/cn/main.pdf` | PRESENT | Size log `logs/final_ship_artifact_sizes_20260510.log`. |
| EN thesis | `thesis/en/main.pdf` | PRESENT | Size log `logs/final_ship_artifact_sizes_20260510.log`; prior style build log `logs/cc_thesis_en_style_build_20260510.log`. |
| Paper2/107 gate | `coordination/remote_tasks/107/CODEX_107_EVIDENCE_GATE_LEDGER_20260510.md` | BLOCKED / AUDIT-ONLY | Ledger verdict is `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`; current 107 tables/figures are audit-only. |
| Paper1 release isolation from 107 | final release directory | PASS | `find` for Paper2/107 artifacts under release returned no hits. |
| Protected paths | `checkpoints`, `data`, `paper2_aihwkit_baseline/checkpoints`, `paper2_aihwkit_baseline/data` | PASS | `git status --short -- ...` returned no entries. |
| Diff whitespace | root and `compute_vit` repos | PASS | `git diff --check` passed in both repositories. |
| Remote review clone | `remote_reviews/107` | CLEAN | `git status --short` returned no entries. |

## Important artifact note

The release tarball is ignored by `.gitignore` (`*.tar.gz`) and is not tracked by git:

- `paper1/release/paper1_submission_bundle_20260509_final.tar.gz`
- Current SHA256 after the later corrected-D2D tarball refresh: `a83a6d5e9f6c1e36f5a70c7ab0bd1c95005ea22d7d35d23782abe124fb828f10`

This supersedes earlier broadcast and intermediate final-audit SHA notes. The directory manifest and cold-unpack manifest checks pass for the current tarball, so the final tarball is internally consistent. If this tarball must be versioned in git, it needs an explicit decision because it is currently ignored.

## Git status summary

### Root repository `/home/qiaosir/projects`

Tracked changes:

- `BROADCAST.md`
- `TASKS.md`

Root diff check passed.

### Nested repository `/home/qiaosir/projects/compute_vit`

Major tracked-change groups:

1. Paper1 active manuscript/release refresh
   - `paper1/manuscript/**`
   - `paper1/release/paper1_submission_bundle_20260509_final/**`
   - `tools/plotting/plot_paper_figures.py`

2. Thesis CN/EN synchronization and builds
   - `thesis/cn/*.tex`, `thesis/cn/main.pdf`
   - `thesis/en/*.tex`, `thesis/en/main.pdf`, `thesis/en/main.bbl`

3. Paper2/107 audit-only documentation
   - `paper2/README.md`
   - `paper2/PROVENANCE_107_20260510.tsv`

4. Coordination and agent reports
   - `coordination/agent_reports/Claude/*`
   - `coordination/agent_reports/Codex/*`
   - `coordination/remote_tasks/**`
   - `coordination/active/*`

Untracked/generated items that need handling before commit:

- Keep/commit as coordination evidence if desired:
  - `coordination/agent_reports/Claude/*.md`, `*.tsv`
  - `coordination/agent_reports/Codex/*.md`
  - `coordination/remote_tasks/**`
  - `paper1/reports/P8/CODEX_PAPER1_NARRATIVE_POLISH_20260510.md`
- Keep/commit as Paper2 audit-only artifacts if desired:
  - `paper2/src/aggregate_107_results.py`
  - `paper2/src/plot_107_results.py`
  - `paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv`
  - `paper2/results/METADATA_COMPLETENESS_107_20260510.tsv`
  - `paper2/results/fig_107_*`
- Usually do not commit build sidecars unless project policy says otherwise:
  - `thesis/cn/main.blg`
  - `thesis/cn/main.toc`
  - `thesis/cn/main.xdv`
  - `thesis/en/main.toc`

The final-audit logs under `compute_vit/logs/final_ship_*_20260510.log` are not shown as untracked in `git status --short` because the logs path is ignored. They exist locally and support this report.

## Recommended commit grouping

Do not use `git add -A`. Stage exact paths by group.

1. Root coordination commit
   - Root repo only: `BROADCAST.md`, `TASKS.md`.
   - Purpose: cross-agent coordination history and task state.

2. Paper1 release refresh commit in `compute_vit`
   - Active manuscript + release directory + plotting source/report.
   - Include `paper1/release/paper1_submission_bundle_20260509_final/**`.
   - Decide separately whether to force-add the ignored tarball; if not, publish it as an external artifact with SHA `a83a6d5e...`.

3. Thesis CN/EN sync commit in `compute_vit`
   - `thesis/cn/*.tex`, `thesis/cn/main.pdf`
   - `thesis/en/*.tex`, `thesis/en/README.md`, `thesis/en/main.pdf`, `thesis/en/main.bbl`
   - Exclude `.toc`, `.blg`, `.xdv` unless intentionally tracked.

4. Paper2/107 audit-only commit in `compute_vit`
   - `paper2/README.md`, `paper2/PROVENANCE_107_20260510.tsv`
   - `paper2/src/aggregate_107_results.py`, `paper2/src/plot_107_results.py`
   - `paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv`
   - `paper2/results/METADATA_COMPLETENESS_107_20260510.tsv`
   - `paper2/results/fig_107_*`
   - Commit message/body must state: audit-only, not claim-locked.

5. Coordination reports/tasks commit in `compute_vit`
   - `coordination/agent_reports/**`
   - `coordination/remote_tasks/**`
   - `coordination/active/CODEX_*`
   - Consider whether to include or retire `coordination/active/AGENT_SYNC_gpt.md`, since broadcast now says root `BROADCAST.md` is canonical and deprecated sync logs are ignored.

## Remaining blockers / non-ship items

| Item | Status | Required next step |
|---|---|---|
| Paper2/107 claim lock | BLOCKED | Signed manifest or minimal corrected-noise rerun with per-row metadata envelope and checkpoint SHA-256. |
| Release tarball git handling | DECISION NEEDED | Keep external with SHA in report, or explicitly force-add despite `.gitignore`. |
| Build sidecars | DECISION NEEDED | Leave untracked/ignored cleanup for `.toc`, `.blg`, `.xdv`, or intentionally track if thesis policy requires. |
| GitHub cleanup | READY FOR COMMIT-PREP | Use exact path staging by the groups above; do not push until user approves. |

## Scope note

This final audit was read-only with respect to project source artifacts. It created local verification logs and this report only. No training, checkpoint/data movement, commit, push, or destructive cleanup was performed.
