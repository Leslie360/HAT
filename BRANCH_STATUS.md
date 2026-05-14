# Branch Status

Date: 2026-05-14
Owner: Codex
Purpose: keep GitHub branch roles explicit so future work does not keep adding ambiguous lanes.

## Canonical remote branches

- `master`
  - historical canonical base
- `107-clean`
  - active Remote107 review / source-data lane
- `105-remote-results`
  - active Remote105 review mirror

## Active exchange branch

- `codex-exchange-20260511`
  - dedicated Codex app / exchange / local-results handoff branch
  - preferred place for in-progress synced artifacts that should not pollute canonical remote-review branches

## Frozen release branch

- `paper1-release-20260501`
  - historical Paper1 release lane
  - treat as frozen unless release packaging must be re-opened

## Historical remote branches

- `main`
- `main-clean-20260429`
- `backup-master-before-clean-20260429`
- `remote-exploration`
- `remote-107-kv-20260429`

These should be treated as historical until someone shows an active dependency.

## Working rule

For new synced work, prefer exactly one of:

1. the relevant canonical branch, or
2. `codex-exchange-20260511`

Do not open another temporary remote branch unless there is a concrete coordination reason.

## Deletion rule

Remote branch deletion is destructive and must be confirmed explicitly, branch by branch.
