# Codex Commit-Prep Exact Paths — 2026-05-10

No commit or push has been performed. This file records safe staging groups for a later explicit `提交` instruction.

## Current Index State

| Repo | Current staged changes |
|---|---|
| `/home/qiaosir/projects` | none |
| `/home/qiaosir/projects/compute_vit` | `thesis/cn/chapter_8_outlook.md` is staged as a rename to `archive/stale_thesis_markdown_20260510/thesis_cn_chapter_8_outlook_legacy_branch_a.md` |

Do not use `git add -A`. If the staged rename should not be in the next `compute_vit` commit, explicitly unstage it before committing; do not silently mix it into an unrelated commit.

## Root Repo

```bash
cd /home/qiaosir/projects
git add BROADCAST.md TASKS.md
```

## Compute-Vit Workspace Hygiene

```bash
cd /home/qiaosir/projects/compute_vit
git add .gitignore README.md
```

The already-staged thesis-markdown archive rename belongs with this group if accepted.

## Paper1 Release Refresh

```bash
cd /home/qiaosir/projects/compute_vit
git add tools/plotting/plot_paper_figures.py
git add paper1/reports/P8/CODEX_PAPER1_NARRATIVE_POLISH_20260510.md
git add paper1/manuscript paper1/provenance/asset_archive/unused_figures_candidates/tikz/figS3_ensemble_hat.tex
git add paper1/release/paper1_submission_bundle_20260509_final
```

The release directory is locally self-consistent only with its ignored `cover_letter.pdf` present. Choose one:

```bash
# External-artifact route: do not add ignored binaries; cite tarball SHA only.
# Git-self-contained release route:
git add -f paper1/release/paper1_submission_bundle_20260509_final/cover_letter.pdf
```

Only force-add the tarball if the user explicitly wants the binary artifact in git:

```bash
git add -f paper1/release/paper1_submission_bundle_20260509_final.tar.gz
```

Current tarball SHA256:

```text
343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6
```

## Thesis CN/EN Sync

```bash
cd /home/qiaosir/projects/compute_vit
git add thesis/cn/*.tex thesis/cn/main.pdf
git add thesis/en/*.tex thesis/en/README.md thesis/en/main.bbl thesis/en/main.pdf
```

Ignored build sidecars should remain untracked unless university policy requires them:

```text
thesis/cn/main.blg
thesis/cn/main.toc
thesis/cn/main.xdv
thesis/en/main.toc
```

## Paper2 / 107 Audit-Only Artifacts

```bash
cd /home/qiaosir/projects/compute_vit
git add paper2/README.md paper2/PROVENANCE_107_20260510.tsv
git add paper2/src/aggregate_107_results.py paper2/src/plot_107_results.py
git add paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv
git add paper2/results/METADATA_COMPLETENESS_107_20260510.tsv
git add paper2/results/fig_107_noise_sweep.pdf paper2/results/fig_107_noise_sweep.png
git add paper2/results/fig_107_selective_kv.pdf paper2/results/fig_107_selective_kv.png
git add paper2/results/fig_107_training_steps.pdf paper2/results/fig_107_training_steps.png
```

Commit message/body must state: audit-only; not claim-locked; blocked pending signed manifest or minimal rerun.

## Coordination Reports And Tasks

```bash
cd /home/qiaosir/projects/compute_vit
git add coordination/active/CODEX_CC_PARALLEL_WORKPLAN_20260510.md
git add coordination/active/CODEX_COMMAND_DASHBOARD_20260510.md
git add coordination/agent_reports/Claude
git add coordination/agent_reports/Codex
git add coordination/remote_tasks
```

Do not stage `coordination/active/AGENT_SYNC_gpt.md` for current coordination unless the user explicitly wants to preserve the deprecated sync file changes.

## Pre-Commit Checks

```bash
cd /home/qiaosir/projects
git diff --check
cd /home/qiaosir/projects/compute_vit
git diff --check
sha256sum paper1/release/paper1_submission_bundle_20260509_final.tar.gz
cd paper1/release/paper1_submission_bundle_20260509_final
sha256sum -c SHA256SUMS.txt
```
