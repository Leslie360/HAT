# Claude Exact Commit-Prep Plan — 2026-05-10

## Status

No commit or push has been performed by Claude after takeover. Current `compute_vit` index already contains one staged rename:

```text
R100 thesis/cn/chapter_8_outlook.md -> archive/stale_thesis_markdown_20260510/thesis_cn_chapter_8_outlook_legacy_branch_a.md
```

This should be committed with workspace/thesis cleanup, not with Paper1 release.

## Current final artifact facts

- Paper1 release tarball path: `paper1/release/paper1_submission_bundle_20260509_final.tar.gz`
- Current tarball SHA256: `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`
- The tarball is ignored by `.gitignore` via `*.tar.gz`.
- Release `cover_letter.pdf` is ignored by `.gitignore` via `cover_letter.pdf`, but it is included in the release directory manifest/tarball.
- Release manifest check passes.
- Protected checkpoint/data paths are clean.
- `remote_reviews/107` is clean.
- Paper2/107 remains audit-only: `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`.

## Recommended commit groups

### 1. Root coordination commit

Repo: `/home/qiaosir/projects`

Stage:

```bash
git add BROADCAST.md TASKS.md
```

Message idea:

```text
chore: update workspace coordination state
```

### 2. compute_vit workspace hygiene commit

Repo: `/home/qiaosir/projects/compute_vit`

Stage:

```bash
git add .gitignore README.md
git add archive/stale_thesis_markdown_20260510/thesis_cn_chapter_8_outlook_legacy_branch_a.md
git add -u thesis/cn/chapter_8_outlook.md
```

This group should absorb the already-staged rename.

Message idea:

```text
chore: clean thesis workspace sidecars and stale drafts
```

### 3. Paper1 final release refresh commit

Stage:

```bash
git add tools/plotting/plot_paper_figures.py
git add paper1/reports/P8/CODEX_PAPER1_NARRATIVE_POLISH_20260510.md
git add paper1/manuscript/cover_letter.tex
git add paper1/manuscript/cover_letter_v3.tex paper1/manuscript/cover_letter_v3.pdf
git add paper1/manuscript/figures/figS3_ensemble_hat.pdf paper1/manuscript/figures/figS3_ensemble_hat.png
git add paper1/manuscript/figures/figS_corr_d2d.pdf paper1/manuscript/figures/figS_corr_d2d.png
git add paper1/manuscript/figures/fig_fresh_instance_ablation.pdf paper1/manuscript/figures/fig_fresh_instance_ablation.png
git add paper1/manuscript/main.pdf paper1/manuscript/supplementary_main.pdf
git add paper1/manuscript/sections/*.tex
git add paper1/manuscript/supplementary.tex paper1/manuscript/supplementary_main.tex
git add paper1/manuscript/supplementary/S_opect_distribution.tex paper1/manuscript/supplementary/S_reproducibility.tex
git add paper1/provenance/asset_archive/unused_figures_candidates/tikz/figS3_ensemble_hat.tex
git add paper1/release/paper1_submission_bundle_20260509_final
```

Optional force-add if git checkout of release directory must be self-contained:

```bash
git add -f paper1/release/paper1_submission_bundle_20260509_final/cover_letter.pdf
```

Only force-add tarball if user explicitly wants binary artifact tracked:

```bash
git add -f paper1/release/paper1_submission_bundle_20260509_final.tar.gz
```

Message idea:

```text
chore: refresh Paper1 release candidate
```

### 4. Thesis CN/EN sync commit

Stage:

```bash
git add thesis/cn/*.tex thesis/cn/main.pdf
git add thesis/en/*.tex thesis/en/README.md thesis/en/main.bbl thesis/en/main.pdf
```

Do not stage ignored sidecars unless explicitly requested:

```text
thesis/cn/main.blg
thesis/cn/main.toc
thesis/cn/main.xdv
thesis/en/main.toc
```

Message idea:

```text
chore: synchronize thesis CN and EN drafts
```

### 5. Paper2 / 107 audit-only commit

Stage:

```bash
git add paper2/README.md paper2/PROVENANCE_107_20260510.tsv
git add paper2/src/aggregate_107_results.py paper2/src/plot_107_results.py
git add paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv
git add paper2/results/METADATA_COMPLETENESS_107_20260510.tsv
git add paper2/results/fig_107_noise_sweep.pdf paper2/results/fig_107_noise_sweep.png
git add paper2/results/fig_107_selective_kv.pdf paper2/results/fig_107_selective_kv.png
git add paper2/results/fig_107_training_steps.pdf paper2/results/fig_107_training_steps.png
```

Message/body must say audit-only and not claim-locked.

Message idea:

```text
chore: add audit-only 107 metadata review artifacts
```

### 6. Coordination reports/tasks commit

Stage:

```bash
git add coordination/active/CODEX_CC_PARALLEL_WORKPLAN_20260510.md
git add coordination/active/CODEX_COMMAND_DASHBOARD_20260510.md
git add coordination/agent_reports/Claude
git add coordination/agent_reports/Codex
git add coordination/remote_tasks
```

Do not stage `coordination/active/AGENT_SYNC_gpt.md` unless user explicitly wants deprecated sync-log edits committed.

Message idea:

```text
docs: record final coordination and audit reports
```

## Checks before each commit or before final commit set

```bash
git -C /home/qiaosir/projects diff --check
git -C /home/qiaosir/projects/compute_vit diff --check
sha256sum /home/qiaosir/projects/compute_vit/paper1/release/paper1_submission_bundle_20260509_final.tar.gz
cd /home/qiaosir/projects/compute_vit/paper1/release/paper1_submission_bundle_20260509_final && sha256sum -c SHA256SUMS.txt
```

## Decisions needed before actual commits

1. Whether to force-add release `cover_letter.pdf` despite ignore, so the tracked release directory itself is manifest-complete.
2. Whether to force-add the ignored release tarball or keep it as an external artifact with SHA `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`.
3. Whether to include deprecated `coordination/active/AGENT_SYNC_gpt.md` changes or leave them unstaged.
