# Remote 107 Task: Commit Per-Row Claim-Lock JSON Artifacts

Date: 2026-05-11
Requester: Claude Code local audit
Branch target: `origin/107-clean`
Priority: blocking archive completeness for selective-KV claim-lock packet

## Context

Commit `8565bbd` on `origin/107-clean` added:

- `coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_LOCK_REPORT_20260511.md`
- `coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_LOCK_MANIFEST_20260511.tsv`

The report states that 41/41 required rows are claim-lockable and that the per-row JSON artifacts exist at:

```text
/home/lisq753/projects/HAT_kv107/paper2/results/remote107/claim_lock_recovery_20260511/
```

However, local audit of `origin/107-clean` found zero committed files under `paper2/results/remote107/claim_lock_recovery_20260511/`. The manifest/report are useful, but the packet is not fully archived until the original per-row JSONs are visible in GitHub.

## Required action

On the remote 107 machine, commit and push the original 41 JSON files into `origin/107-clean` at exactly:

```text
paper2/results/remote107/claim_lock_recovery_20260511/
```

Expected contents:

- 41 per-row claim-lock JSON files corresponding one-to-one with `REMOTE_107_SELECTIVE_KV_LOCK_MANIFEST_20260511.tsv` rows.
- If an index file already exists in that directory, include it too.
- Do not rewrite PPL values or regenerate different run IDs unless the old files are unavailable; if regeneration is necessary, explicitly state that in a note.

## Verification commands

After pushing, run and report these commands:

```bash
git fetch origin 107-clean
git ls-tree -r --name-only origin/107-clean paper2/results/remote107/claim_lock_recovery_20260511 | wc -l
git ls-tree -r --name-only origin/107-clean paper2/results/remote107/claim_lock_recovery_20260511 | head
```

The count should be at least 41. If an index file is included, the count may be 42+.

## Acceptance criteria

This task is complete only when:

1. `origin/107-clean` contains the JSON artifact directory.
2. The JSON file count is at least 41.
3. Every manifest `run_id` has one corresponding JSON artifact.
4. The pushed commit hash is reported back.

## Local fallback note

Local audit generated manifest-derived JSON backups under:

```text
paper2/results/remote107/claim_lock_recovery_manifest_derived_20260511/
```

These are explicitly marked as manifest-derived backups and are not a replacement for the original remote JSONs.
