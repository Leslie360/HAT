# Remote 107 Coordination Index

This branch is the clean communication and deliverable branch for Remote 107 analog KV-cache work.

## Branch Purpose

Use this branch for:

- lightweight task dispatch MD files
- result summary MD files
- portable reproduction scripts under `deliverable/code/`
- small JSON result files under `deliverable/results_*`
- audit notes and return templates

Do not use this branch for:

- checkpoints
- logs larger than a few MB
- datasets
- local paper-1/R11D source tree
- generated PDFs
- temporary tmux/nohup output dumps

## Current Files

- `coordination/REMOTE107_NEXT_TASKS_20260430.md` — next required task list from Codex.
- `coordination/RESULT_RETURN_TEMPLATE_107.md` — exact format for returning corrected results.
- `coordination/CODEX_REVIEW_107_CLEAN_20260430.md` — Codex audit of this clean branch.
- `RESULTS_SUMMARY.md` — current v2 numeric snapshot, still provisional until seed metadata reruns close.
- `deliverable/README.md` — deliverable tree overview.

## Operating Rule

Every remote result should be returned with:

1. Git branch and commit SHA.
2. Exact command line.
3. Exact code file paths used.
4. Environment packet.
5. JSON result path and a small MD summary.
6. Statement whether the result is canonical or provisional.

