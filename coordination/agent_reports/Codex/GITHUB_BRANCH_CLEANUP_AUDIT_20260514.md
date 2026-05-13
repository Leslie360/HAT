# GitHub Branch Cleanup Audit — 2026-05-14

Date: 2026-05-14 00:40 CST
Owner: Codex
Scope: non-destructive branch hygiene review only. No remote branch deletion performed.

## Current remote branches

- `origin/master`
- `origin/main`
- `origin/main-clean-20260429`
- `origin/backup-master-before-clean-20260429`
- `origin/paper1-release-20260501`
- `origin/remote-107-kv-20260429`
- `origin/105-remote-results`
- `origin/107-clean`
- `origin/remote-exploration`
- `origin/codex-exchange-20260511`

## Current local branches

- active exchange lane:
  - `codex-exchange-20260511`
- active remote review mirrors:
  - `105-remote-results`
  - `107-clean`
- likely historical or dispatch-only branches:
  - `backup/pre-slim-9e6e62f`
  - `remote-107-kv-20260429`
  - `paper1-release-20260501`
- local-only worktree/dispatch branches:
  - `remote-dispatch-20260507`
  - `remote105-dispatch-20260507`
  - `remote107-dispatch-20260507`
  - `worktree-agent-abb5677aa6a460fef`

## Immediate reading

The GitHub state is messy mainly because the repo currently mixes:

1. long-lived canonical branches (`master`, `107-clean`, `105-remote-results`);
2. one release lane (`paper1-release-20260501`);
3. one exchange lane (`codex-exchange-20260511`);
4. several historical or dispatch branches that no longer communicate their status clearly.

The highest-value cleanup is therefore **labeling and narrowing**, not deletion-first cleanup.

## Safe actions now

1. Keep using:
   - `107-clean` for Remote107 review
   - `codex-exchange-20260511` for Codex app / local exchange handoff
2. Treat `paper1-release-20260501` as frozen historical release lane.
3. Treat `remote-dispatch-*` and `worktree-agent-*` as local execution debris unless someone can show an active dependency.
4. Prefer new work to land on either:
   - the canonical working branch, or
   - the explicit exchange branch,
   instead of opening more temporary lanes.

## Not safe without explicit user confirmation

Do **not** do these automatically:

- delete any remote branch
- rename `master` / `main`
- force-push anything
- collapse `105-remote-results` or `107-clean` into other branches

These are cleanup actions with irreversible coordination cost.

## Recommended next GitHub cleanup sequence

### Phase 1: zero-risk

1. Keep `codex-exchange-20260511` up to date as the dedicated exchange branch.
2. Add one short branch-status note in repo docs so future agents know:
   - what is canonical,
   - what is exchange-only,
   - what is historical.

### Phase 2: low-risk, after user confirms

1. Remove or archive local-only dispatch/worktree branches.
2. Keep remote canonical lanes untouched.

### Phase 3: destructive remote cleanup, user-confirmed only

Candidate remote branches for deletion or archival discussion:

- `origin/main-clean-20260429`
- `origin/backup-master-before-clean-20260429`
- `origin/remote-exploration`
- possibly `origin/remote-107-kv-20260429`

But only after checking whether any document, automation, or collaborator still references them.

## Recommendation

The best immediate GitHub cleanup is not branch deletion. It is:

- stabilize `codex-exchange-20260511` as the app/data handoff lane,
- keep `107-clean` and `105-remote-results` as canonical remote-review lanes,
- then later prune the dispatch/historical clutter with explicit confirmation.
