# GitHub Cleanup Executed — 2026-05-14

Date: 2026-05-14
Owner: Codex
Scope: destructive cleanup approved by user

## GitHub remote actions

Changed GitHub default branch:

- from `remote-exploration`
- to `master`

Deleted remote branches:

- `backup-master-before-clean-20260429`
- `main-clean-20260429`
- `remote-107-kv-20260429`
- `remote-exploration`

Remaining remote branches:

- `origin/master`
- `origin/main`
- `origin/107-clean`
- `origin/105-remote-results`
- `origin/paper1-release-20260501`
- `origin/codex-exchange-20260511`

## Local cleanup actions

Removed local dispatch/historical branches:

- `remote-dispatch-20260507`
- `remote105-dispatch-20260507`
- `remote107-dispatch-20260507`
- `remote-107-kv-20260429`
- `backup/pre-slim-9e6e62f`

Removed prunable temporary worktrees under `/tmp/` and pruned worktree metadata.

Kept local active worktrees:

- `/home/qiaosir/projects/compute_vit`
- `/home/qiaosir/projects/HAT_105_results_review`
- `/home/qiaosir/projects/HAT_107_clean_review`
- `/home/qiaosir/projects/compute_vit/.claude/worktrees/agent-abb5677aa6a460fef` (locked)

## Remaining intentional mess

Two non-deleted items are intentional:

1. `origin/main`
   - kept as compatibility branch because it points to the same base commit line as `origin/master`
2. `worktree-agent-abb5677aa6a460fef`
   - left in place because it is locked and may still be referenced by the local Codex/Claude workflow

## Recommendation

The GitHub branch layout is now materially cleaner.

If you want the repo even stricter later, the only likely next destructive step is:

- decide whether `origin/main` should also be deleted or kept permanently as a compatibility alias for `master`
