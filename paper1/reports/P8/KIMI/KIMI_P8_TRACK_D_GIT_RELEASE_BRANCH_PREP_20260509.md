# Kimi P8 Track D: Git Release Branch Preparation

Date: 2026-05-09
Scope: Git status, commit/exclude/user-decision categorization, branch/commit/push plan
Status: COMPLETE — command-ready, no push executed

## 1. Current git metadata

| Item | Value |
|---|---|
| Current branch | `paper1-release-20260501` |
| Current HEAD | `934c1f1a7334ff8df67a9b0fd9ddcbb7c90080d1` |
| Main branch target | `main` |
| `git status --short` count | 442 entries after cleanup/quarantine/report generation |

## 2. Commit-scope categories

### Commit candidates

| Category | Paths |
|---|---|
| Active manuscript source/PDF | `paper/latex_gpt/main.tex`, `main.pdf`, `supplementary_main.tex`, `supplementary_main.pdf`, `cover_letter.tex`, `cover_letter.pdf`, `sections/*.tex`, `supplementary.tex`, `supplementary/*.tex`, `refs_gpt.bib` |
| Active figures/source data | `paper/latex_gpt/figures/*`, `paper/figures/*`, `paper/latex_gpt/source_data/*.csv`, active canonical JSON under `paper/latex_gpt/source_data/canonical_json/` |
| Validation scripts | `scripts/_gpt/check_local_pcm_precision_ladder.py`, plotting scripts required for source-data provenance |
| Release bundle | `release_artifacts/paper1_submission_bundle_20260509_final/` and final tarball, if repository policy accepts tarball artifacts |
| P8 reports | `report_md/_gpt/KIMI_P8_TRACK_*_20260509.md`, `KIMI_P8_SELF_AUDIT_20260509.md` |
| Coordination | `broadcast.md`, `report_md/_gpt/AGENT_SYNC_gpt.md`, `CLAUDE_TASK_gpt.md` if the repo tracks coordination state |

### Exclude from commit by default

| Category | Paths/reasons |
|---|---|
| Large data/checkpoints | `checkpoints/`, `data/`, `paper2_aihwkit_baseline/checkpoints/`, any `.pt`, `.pth`, `.ckpt` |
| Raw local experiment tree | most untracked `paper2_aihwkit_baseline/*` scripts/figures unless separately approved for Work-2 |
| Review clones | `/home/qiaosir/projects/remote_reviews/105/`, `/home/qiaosir/projects/remote_reviews/107/` are outside commit scope |
| Quarantine | `archive/cleanup_candidates_20260509/` should normally stay uncommitted unless Codex wants a cleanup record committed |
| Legacy bundles | `release_artifacts/paper1_reviewer_bundle_20260501_1645*`, `paper1_release_candidate_*`, provenance tarballs unless explicitly desired |
| Local Claude settings | `.claude/` |
| Raw device data | `数据_博士/` and archives (`.zip`, `.qivd`, raw CSV) should not be swept into Paper-1 commit without a data-policy decision |

### User/Codex decision required

| Item | Decision |
|---|---|
| Final tarball commit | Commit only if repository intentionally stores release artifacts; otherwise keep local/upload-only |
| Thesis edits | `thesis/en/ (compat: paper/thesis/)` and `thesis/cn/ (compat: paper/thesis_cn/)` changed; include only if this branch is also meant to update thesis drafts |
| `report_md/` older untracked reports | Many historical report files are untracked; include only the P8 files and essential acceptance/audit files unless Codex wants a full report import |
| Chinese PPT | Leave untouched until user decides |
| Deprecated old-protocol canonical archive | Keep for provenance, but commit only if Codex wants old protocol archived in git |

## 3. Large/private/checkpoint guard

Status scan still shows source-data JSON, release tarballs, and raw data candidates. No `.pt`, `.pth`, `.ckpt`, dataset, raw huge log, or private credential should be included in the default staging command.

## 4. Proposed branch

Recommended branch:

`paper1-final-freeze-20260509`

If the current branch already serves as the release branch, safer alternative:

`paper1-final-freeze-p8-20260509`

## 5. Conservative command block

Do not run this without user/Codex approval.

```bash
git switch -c paper1-final-freeze-p8-20260509

# Stage only active manuscript, source data, final bundle, and P8 reports.
git add \
  paper/latex_gpt/main.tex \
  paper/latex_gpt/main.pdf \
  paper/latex_gpt/supplementary_main.tex \
  paper/latex_gpt/supplementary_main.pdf \
  paper/latex_gpt/cover_letter.tex \
  paper/latex_gpt/cover_letter.pdf \
  paper/latex_gpt/refs_gpt.bib \
  paper/latex_gpt/sections \
  paper/latex_gpt/supplementary.tex \
  paper/latex_gpt/supplementary \
  paper/latex_gpt/source_data \
  paper/latex_gpt/figures \
  paper/figures \
  scripts/_gpt/check_local_pcm_precision_ladder.py \
  scripts/_gpt/plot_paper1_decision_map.py \
  scripts/_gpt/plot_paper1_spine.py \
  release_artifacts/paper1_submission_bundle_20260509_final \
  release_artifacts/paper1_submission_bundle_20260509_final.tar.gz \
  report_md/_gpt/KIMI_P8_TRACK_A_NARRATIVE_DESLOP_REWRITE_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md \
  report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md \
  report_md/_gpt/KIMI_P8_SELF_AUDIT_20260509.md

git diff --cached --stat
git diff --cached --name-only | grep -E '\.(pt|pth|ckpt)$|(^|/)checkpoints/|(^|/)data/|\.env|credential|secret' && echo 'STOP: unsafe staged file' && exit 1 || true

git commit -m "docs: finalize Paper-1 P8 submission bundle"

git push -u origin paper1-final-freeze-p8-20260509
```

## 6. Hard prohibitions

- No `git reset --hard`.
- No `git checkout --` or destructive restore.
- No force push.
- No broad `git add -A`.
- No checkpoint/data/raw-device sweep into commit scope.

## 7. Verdict

Track D COMPLETE. Git path is command-ready and conservative; push not executed.
