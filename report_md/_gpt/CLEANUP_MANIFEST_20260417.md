# CLEANUP_MANIFEST_20260417

## Scope
- Dispatch: `CODEX_DISPATCH_20260417_cleanup_gpt.md`
- Execution mode: filesystem hygiene only; no deletions; no code/LaTeX content edits outside allowed manifest/sync files and outer-root `.gitignore`.
- Repo layout note: `/home/qiaosir/projects` and `/home/qiaosir/projects/compute_vit` are separate git roots, so status verification is reported for both.

## TX-17

| Source | Destination | Size (bytes) | Reason |
| --- | --- | ---: | --- |
| `/home/qiaosir/projects/cover_letter.aux` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/cover_letter.aux` | 786 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/cover_letter.fdb_latexmk` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/cover_letter.fdb_latexmk` | 8112 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/cover_letter.fls` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/cover_letter.fls` | 30423 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/cover_letter.log` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/cover_letter.log` | 12530 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/cover_letter.out` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/cover_letter.out` | 0 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/cover_letter.pdf` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/cover_letter.pdf` | 64238 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/main.aux` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/main.aux` | 662 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/main.fdb_latexmk` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/main.fdb_latexmk` | 10980 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/main.fls` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/main.fls` | 46080 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/main.log` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/main.log` | 17644 | stray root-level LaTeX build artifact |
| `/home/qiaosir/projects/main.out` | `/home/qiaosir/projects/tmp/stale_latex_root_20260417/main.out` | 0 | stray root-level LaTeX build artifact |

## TX-18

| Source | Destination | Size (bytes) | Reason |
| --- | --- | ---: | --- |
| `/home/qiaosir/projects/tunnel` | `/home/qiaosir/projects/tmp/garbage_root_20260417/tunnel` | 0 | zero-byte root-level garbage file |
| `/home/qiaosir/projects/proxy_sensitivity_sweep_gpt.py` | `/home/qiaosir/projects/tmp/garbage_root_20260417/proxy_sensitivity_sweep_gpt.py` | 0 | zero-byte root-level garbage file |
| `/home/qiaosir/projects/•` | `/home/qiaosir/projects/tmp/garbage_root_20260417/•` | 0 | zero-byte root-level garbage file |

## TX-19 (resolved 2026-04-17 by Claude per user decision — option A)

| Source | Destination | Size (bytes) | Reason |
| --- | --- | ---: | --- |
| `/home/qiaosir/projects/home/qiaosir/projects/compute_vit/KIMI_KM1_KM7_REPORTS.md` | `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_KM1_KM7_REPORTS.md` | 4210 | rescued authored Kimi KM1–KM7 proofreading report to canonical `_gpt/` location |
| `/home/qiaosir/projects/home/` (now empty mirror tree) | `/home/qiaosir/projects/tmp/unknown_home_subtree_20260417/home/` | — | stray WSL-style nested path; preserved under tmp/ for reversibility |

## TX-20

| Source | Destination | Size (bytes) | Reason |
| --- | --- | ---: | --- |
| `/home/qiaosir/projects/compute_vit/append_batch3.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_batch3.py` | 2225 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_kimi_km14.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_kimi_km14.py` | 4303 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_kimi_km14_part2.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_kimi_km14_part2.py` | 2266 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_kimi_km14_v2.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_kimi_km14_v2.py` | 4268 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_kimi_part2.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_kimi_part2.py` | 4266 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_sync.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_sync.py` | 1850 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_sync_batch4.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_sync_batch4.py` | 1880 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_sync_final.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_sync_final.py` | 1398 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_sync_k5.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_sync_k5.py` | 834 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/append_sync_kimi.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/append_sync_kimi.py` | 1510 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/check_resnet_keys.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/check_resnet_keys.py` | 719 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/check_resnet_weights.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/check_resnet_weights.py` | 833 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/debug_ensemble_deep.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/debug_ensemble_deep.py` | 5205 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/debug_nl_baseline.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/debug_nl_baseline.py` | 1963 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/debug_resnet18_load.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/debug_resnet18_load.py` | 1482 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/debug_resnet_issue.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/debug_resnet_issue.py` | 4417 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/debug_train_eval_mismatch.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/debug_train_eval_mismatch.py` | 6738 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_asymmetry_stats.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_asymmetry_stats.py` | 1496 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_ensemble_issue.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_ensemble_issue.py` | 5914 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_resnet18_cifar100.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_resnet18_cifar100.py` | 4568 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_resnet18_deep.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_resnet18_deep.py` | 9065 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_resnet18_final.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_resnet18_final.py` | 6162 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_tinyvit_noise.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_tinyvit_noise.py` | 8308 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/diagnose_tinyvit_retention.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/diagnose_tinyvit_retention.py` | 8565 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/watch_convnext_task21_stage1_completion_gpt.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/watch_convnext_task21_stage1_completion_gpt.py` | 3771 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/watch_convnext_task21_stage2_completion_gpt.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/watch_convnext_task21_stage2_completion_gpt.py` | 6356 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/watch_convnext_task21_stage2_then_launch_task23_task24_gpt.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/watch_convnext_task21_stage2_then_launch_task23_task24_gpt.py` | 8050 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/watch_noise_sweep_completion_gpt.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/watch_noise_sweep_completion_gpt.py` | 3595 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/experiment_asymmetry_gemini.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/experiment_asymmetry_gemini.py` | 3215 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/experiment_asymmetry_simple.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/experiment_asymmetry_simple.py` | 7639 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/experiment_asymmetry_sweep.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/experiment_asymmetry_sweep.py` | 7813 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/experiment_asymmetry_sweep_v2.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/experiment_asymmetry_sweep_v2.py` | 8266 | one-shot helper/archive per cleanup dispatch |
| `/home/qiaosir/projects/compute_vit/experiment_nonideality_gemini.py` | `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/experiment_nonideality_gemini.py` | 3364 | one-shot helper/archive per cleanup dispatch |

## TX-21

| Source | Destination | Size (bytes) | Reason |
| --- | --- | ---: | --- |
| `/home/qiaosir/projects/compute_vit/paper/latex_gpt/pdflatex51394.fls` | `/home/qiaosir/projects/tmp/stale_latex_paper_20260417/pdflatex51394.fls` | 139 | stale pdflatex scratch artifact |
| `/home/qiaosir/projects/compute_vit/paper/latex_gpt/pdflatex52112.fls` | `/home/qiaosir/projects/tmp/stale_latex_paper_20260417/pdflatex52112.fls` | 139 | stale pdflatex scratch artifact |

## TX-22

| Source | Destination | Size (bytes) | Reason |
| --- | --- | ---: | --- |
| `/home/qiaosir/projects/.gitignore` | `/home/qiaosir/projects/.gitignore` | 344 | appended LaTeX/python/tmp/log ignore patterns at outer project root only |

## Not Moved / Ambiguities

- `TX-19` was initially blocked and is now resolved: the authored report was rescued to `compute_vit/report_md/_gpt/KIMI_KM1_KM7_REPORTS.md`, and the remaining empty mirror tree was archived to `tmp/unknown_home_subtree_20260417/home/`.
- `TX-22` verification note: the new outer-root `.gitignore` applies only to `/home/qiaosir/projects`. The live manuscript files are inside the nested git repo `/home/qiaosir/projects/compute_vit`, so they are unaffected by this ignore expansion.
- Tracking state observed in `/home/qiaosir/projects/compute_vit`: `paper/latex_gpt/main.pdf` and the section `.tex` files are tracked; `paper/latex_gpt/cover_letter.pdf` and `paper/latex_gpt/supplementary_main.pdf` currently exist but were not already tracked before this cleanup pass. No index changes were made for those PDFs because dispatch scope was hygiene only.

## Git Status

### Outer Root Repo (`/home/qiaosir/projects`)
```text
?? .gitignore
?? home/
```

### `compute_vit` Repo (`/home/qiaosir/projects/compute_vit`)
```text
 M report_md/_gpt/AGENT_SYNC_gpt.md
 M report_md/_gpt/CLAUDE_TASK_gpt.md
RM append_sync.py -> scripts/archive_20260417/append_sync.py
R  diagnose_tinyvit_noise.py -> scripts/archive_20260417/diagnose_tinyvit_noise.py
R  diagnose_tinyvit_retention.py -> scripts/archive_20260417/diagnose_tinyvit_retention.py
R  watch_convnext_task21_stage1_completion_gpt.py -> scripts/archive_20260417/watch_convnext_task21_stage1_completion_gpt.py
R  watch_convnext_task21_stage2_completion_gpt.py -> scripts/archive_20260417/watch_convnext_task21_stage2_completion_gpt.py
R  watch_convnext_task21_stage2_then_launch_task23_task24_gpt.py -> scripts/archive_20260417/watch_convnext_task21_stage2_then_launch_task23_task24_gpt.py
R  watch_noise_sweep_completion_gpt.py -> scripts/archive_20260417/watch_noise_sweep_completion_gpt.py
?? report_md/_gpt/CLEANUP_MANIFEST_20260417.md
?? scripts/archive_20260417/append_batch3.py
?? scripts/archive_20260417/append_kimi_km14.py
?? scripts/archive_20260417/append_kimi_km14_part2.py
?? scripts/archive_20260417/append_kimi_km14_v2.py
?? scripts/archive_20260417/append_kimi_part2.py
?? scripts/archive_20260417/append_sync_batch4.py
?? scripts/archive_20260417/append_sync_final.py
?? scripts/archive_20260417/append_sync_k5.py
?? scripts/archive_20260417/append_sync_kimi.py
?? scripts/archive_20260417/check_resnet_keys.py
?? scripts/archive_20260417/check_resnet_weights.py
?? scripts/archive_20260417/debug_ensemble_deep.py
?? scripts/archive_20260417/debug_nl_baseline.py
?? scripts/archive_20260417/debug_resnet18_load.py
?? scripts/archive_20260417/debug_resnet_issue.py
?? scripts/archive_20260417/debug_train_eval_mismatch.py
?? scripts/archive_20260417/diagnose_asymmetry_stats.py
?? scripts/archive_20260417/diagnose_ensemble_issue.py
?? scripts/archive_20260417/diagnose_resnet18_cifar100.py
?? scripts/archive_20260417/diagnose_resnet18_deep.py
?? scripts/archive_20260417/diagnose_resnet18_final.py
?? scripts/archive_20260417/experiment_asymmetry_gemini.py
?? scripts/archive_20260417/experiment_asymmetry_simple.py
?? scripts/archive_20260417/experiment_asymmetry_sweep.py
?? scripts/archive_20260417/experiment_asymmetry_sweep_v2.py
?? scripts/archive_20260417/experiment_nonideality_gemini.py
```

### Tracking Verification Snapshot
```text
compute_vit repo tracked latex outputs
paper/latex_gpt/main.pdf
paper/latex_gpt/main.tex
paper/latex_gpt/sections/00_abstract.tex
paper/latex_gpt/sections/01_introduction.tex
paper/latex_gpt/sections/02_related_work.tex
paper/latex_gpt/sections/03_methodology.tex
paper/latex_gpt/sections/04_experimental_setup.tex
paper/latex_gpt/sections/05_results.tex
paper/latex_gpt/sections/06_discussion.tex
paper/latex_gpt/sections/07_conclusion.tex
paper/latex_gpt/sections/08_appendix.tex

root repo tracked latex outputs
```

## PDF / Count Checks

- `paper/latex_gpt/main.pdf` exists: yes (`/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf` | `248645|2026-04-17 03:04:03.274799656 +0800`); log check: `711:Output written on main.xdv (16 pages, 547876 bytes).`
- `paper/latex_gpt/cover_letter.pdf` exists: yes (`/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.pdf` | `22590|2026-04-17 01:56:13.481864569 +0800`); log check: `268:Output written on cover_letter.xdv (2 pages, 39804 bytes).`
- `paper/latex_gpt/supplementary_main.pdf` exists: yes (`/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf` | `10019617|2026-04-17 03:04:44.063809282 +0800`); log check: `503:Output written on supplementary_main.xdv (16 pages, 305808 bytes).`
- Dispatch expected supplementary_main to be 15 pages; the current compiled artifact is 16 pages according to the live log, so this was recorded rather than normalized.
- `compute_vit/run_*.py` count unchanged: `44` before -> `44` after

## Outcome Summary

- TX-17, TX-18, TX-20, TX-21, TX-22 executed successfully.
- TX-19 intentionally blocked from moving because the subtree contains authored material.
- TX-23 completed by this manifest; no commit was made.
