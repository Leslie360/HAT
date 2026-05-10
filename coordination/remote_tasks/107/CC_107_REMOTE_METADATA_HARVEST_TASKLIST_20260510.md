# CC Tasklist: Remote 107 Metadata Harvest

Date: 2026-05-10
Issued by: Codex
Target agent: separate CC model
Write scope: `compute_vit/coordination/agent_reports/Claude/` only

## Purpose

The current Paper2/107 candidate tables are not claim-bearing because the raw JSON files lack required provenance fields. Your task is to determine whether that missing metadata can be recovered from the remote 107 clone, without changing any experiment files.

## Read-only inputs

- `/home/qiaosir/projects/remote_reviews/107/`
- `/home/qiaosir/projects/remote_reviews/107/results/paper2/*.json`
- `/home/qiaosir/projects/remote_reviews/107/results/d2d_seed_ablation/*.json`
- `/home/qiaosir/projects/remote_reviews/107/RESULTS_SUMMARY.md`
- any scripts, shell launchers, logs, state files, or docs inside the remote 107 clone
- `compute_vit/coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md`
- `compute_vit/coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_20260510.md`

## Do not touch

- Do not edit files inside `/home/qiaosir/projects/remote_reviews/107/`.
- Do not edit `compute_vit/paper2/src/` or `compute_vit/paper2/results/`.
- Do not edit Paper1 files.
- Do not move, hash-copy, or stage checkpoints. If checkpoint hashes are available from existing files, report them; otherwise mark blocked.
- Do not run training or GPU jobs.
- Do not push.

## Required report

Write:

`compute_vit/coordination/agent_reports/Claude/CC_107_REMOTE_METADATA_HARVEST_20260510.md`

Use this structure:

1. Executive verdict: `claim_lock_possible_now`, `claim_lock_blocked`, or `partial_metadata_recovered`.
2. Remote git state: branch, HEAD SHA, dirty status.
3. Corrected-noise code path: file, function, and relevant line ranges.
4. Command recovery: exact commands found, source file/log path, and which result families they cover.
5. Protocol recovery: dataset split, context length, stride, batch size, analog-layer list, seed semantics.
6. Checkpoint provenance: path strings, hashes if available, and missing-hash blockers.
7. Old-vs-corrected map: rows that can be compared safely, rows that cannot.
8. Metadata completeness verdict by result family.
9. Recommended next action for Codex.

Optional TSV outputs under the same directory:

- `CC_107_OLD_VS_CORRECTED_MAP_20260510.tsv`
- `CC_107_COMMAND_AND_CODE_PATHS_20260510.tsv`

## Acceptance criteria

- Every recovered fact must cite a local path.
- Do not infer a command or protocol if no source file/log supports it.
- If metadata is not recoverable, say `blocked` and name the missing artifact.
- Keep Paper2/107 separate from Paper1.
