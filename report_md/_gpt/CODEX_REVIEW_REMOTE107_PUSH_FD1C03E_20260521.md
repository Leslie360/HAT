# Codex Review: Remote107 Push `fd1c03e` - 2026-05-21

Reviewer: Codex local  
Branch reviewed: `origin/107-clean`  
Previous local review commit: `0a4468dc71303b02becf9c45b23d9d0466bdb5fd`  
New observed commit after fetch: `fd1c03e70bebc0356a1bd95ef22ee09172bd6cc0`  
Fetch note: branch was force-updated from `0a4468d` to `fd1c03e`.

## One-Line Verdict

Remote107 has useful R1 mechanism-control numbers and a plausible narrative pivot, but the push is **not claim-locked**. The current branch contradicts its own return note: it claims a `source_lock_20260520/` package exists and that lm_eval JSONs are raw/non-LFS, but Codex cannot find the source-lock package in the tree and sampled `lm_eval_*.json` files are Git LFS pointers.

## What Changed Since Last Review

New top commits on `origin/107-clean`:

| Commit | Message | Local interpretation |
|---|---|---|
| `fd1c03e` | `feat: add few-shot eval support and supplementary task slugs` | Adds `--num_fewshot` and task-slug handling in `p3_hat_lm_eval.py`; useful infrastructure. |
| `7781206` | `Add research directions document for future HAT opportunities` | Adds future roadmap; useful but not evidence. |
| `79d9d37` | `docs: update Remote 107 status — extended eval running on GPU4-7` | Status/history update. |
| `279d89d` | `data(remote107): add robustness sweep, layer ablation, and extended eval results` | Adds many lm_eval JSON paths, mostly as LFS pointers. |

Important diff against `0a4468d`:

- Added `coordination/remote_tasks/107/REMOTE107_RETURN_R0R1_SOURCE_LOCK_20260520.md`.
- Added/updated `coordination/REMOTE107_COMPLETE_HISTORY.md`.
- Added `coordination/RESEARCH_DIRECTIONS.md`.
- Updated `p3_hat_lm_eval.py`.
- Deleted from the current branch tree: `paper2/results/remote107/paper2_results_summary.json` and `paper2/results/remote107/RECONCILIATION_20260520.md` compared with prior reviewed state.
- Added `.gitattributes` rule: `paper2/results/remote107/lm_eval_*.json filter=lfs diff=lfs merge=lfs -text`.

## P0 Integrity Findings

### F1. Claimed source-lock package is missing

Remote107 return says:

```text
results/remote107/source_lock_20260520/ — 9 files
```

Codex checked both expected paths:

```text
paper2/results/remote107/source_lock_20260520/PACKAGE_MANIFEST.json
results/remote107/source_lock_20260520/PACKAGE_MANIFEST.json
```

Both are missing from `origin/107-clean`.

Verdict: **P0 blocker**. R0 source-lock is not verifiable from the pushed branch.

### F2. Return note says raw JSONs are not LFS, but branch stores them as LFS pointers

Remote107 return says:

```text
All 204 lm_eval JSON files are raw (not LFS), self-contained, SHA256-verified
```

Current branch has:

```text
paper2/results/remote107/lm_eval_*.json filter=lfs diff=lfs merge=lfs -text
```

Codex sampled:

```text
paper2/results/remote107/lm_eval_p69b_fixed500_seed42_analog.json
```

The file content is an LFS pointer, not raw JSON:

```text
version https://git-lfs.github.com/spec/v1
... oid sha256:396554...
size 2114
```

Codex generated a local pointer inventory:

```text
compute_vit/report_md/csv/remote107_fd1c03e_lfs_pointer_inventory_20260521.csv
```

Current count in branch from local pointer inventory:

| Item | Count |
|---|---:|
| `paper2/results/remote107/lm_eval_*.json` paths | 102 |
| parsed as LFS pointers | 88 |
| parsed as non-pointer blobs | 14 |

Verdict: **P0 blocker**. LFS is acceptable if declared, but the return note must not claim raw self-contained JSONs.

### F3. `paper2_results_summary.json` was removed from current branch

Last review depended on:

```text
paper2/results/remote107/paper2_results_summary.json
```

Current `origin/107-clean` does not contain it.

Verdict: **P0 blocker** unless Remote107 intentionally replaced it with a new packaged summary. If replaced, the replacement package must be present and documented.

### F4. R1 mechanism-control table is useful but currently unverified

Remote107 reports:

| Condition | PPL | Lambada Acc | Claimed interpretation |
|---|---:|---:|---|
| base_clean | 14.94 | 0.4500 | baseline |
| patched_zero_last1 | 15.04 | 0.4502 | patch overhead negligible |
| patched_zero_last2 | 15.23 | 0.4493 | patch overhead small |
| patched_zero_last4 | 16.75 | 0.4279 | patch overhead noticeable |
| patched_zero_all24 | 20.88 | 0.4000 | patch overhead severe |
| hat_quant_zero_noise | 13.53 | 0.4712 | HAT fine-tuning improves baseline |
| hat_d2d_0p05 | 14.97 | 0.4549 | HAT + noise returns to parity |

If these numbers are source-locked, the mechanism conclusion is important:

> HAT fine-tuning / zero-noise adaptation dominates the observed gain; inference-time physical noise does not improve accuracy and mostly consumes the fine-tuning gain.

But because the CSV/source package is missing locally, Codex marks this as **provisional**.

## Claim Boundary After `fd1c03e`

Safe wording now:

> Remote107 reports provisional R1 mechanism controls suggesting that HAT fine-tuning under the selective analog-KV pipeline dominates the recovery signal, while inference-time D2D noise returns performance toward parity. This remains provisional until the claimed source-lock package is actually pushed and locally verifiable.

Unsafe wording now:

- `R0/R1 source-lock is complete`.
- `all lm_eval JSONs are raw and self-contained in Git`.
- `hardware noise improves LLM accuracy`.
- `scaling law is claim-locked`.
- `paper2_results_summary.json is current`, because it is absent from the reviewed branch.

## Code Review: `p3_hat_lm_eval.py`

Useful changes:

- Adds `--num_fewshot`.
- Propagates `num_fewshot` into `evaluator.simple_evaluate`.
- Adds task slugging to prevent output filename collisions.
- Keeps `--output_suffix` support.

Cautions:

- Few-shot results must be stored separately from zero-shot results; do not mix them in summaries.
- `truthfulqa` task naming should be checked against the installed lm-eval task list before using in a claim.
- Output metadata should include `num_fewshot`; currently the filename includes it, but the JSON record should also explicitly store it for source-lock clarity.

## Required Reply To Remote107

Remote107 should fix the package before any new claim discussion.

Required next push:

```text
paper2/results/remote107/source_lock_20260520/
  README_PROTOCOL.md
  PACKAGE_MANIFEST.json
  remote107_paper2_results_summary_20260520.json
  remote107_paper2_results_summary_20260520.csv
  r1_mechanism_controls_summary_20260520.csv
  source_json_inventory_20260520.csv
  checkpoint_inventory_20260520.csv
  logs_inventory_20260520.csv
  sha256sum.txt
```

If JSONs are LFS pointers, the package must say so explicitly and include:

- Git LFS OID for every raw JSON,
- logical SHA256 if known,
- file size,
- exact source path on Remote107,
- whether Codex can reproduce metrics from a compact CSV without downloading LFS objects.

Specific fixes required:

1. Push the missing `source_lock_20260520/` package or correct the return note.
2. Restore or replace `paper2_results_summary.json` with an explicit replacement path.
3. Update `REMOTE107_RETURN_R0R1_SOURCE_LOCK_20260520.md` to stop saying raw JSONs are non-LFS unless that is true.
4. Normalize the latest commit reference in `REMOTE107_COMPLETE_HISTORY.md`; it still says latest commit `abdf5c5` despite current branch head `fd1c03e`.
5. Resolve status inconsistency: history says some p69b fixed1000 work is complete, but also says GPU5 is still running clean/analog eval.
6. Add `num_fewshot` to result JSON metadata if few-shot eval is used.
7. Mark scaling-law and research-direction docs as exploratory until source-lock and same-protocol rows are complete.

## Recommended Local Action

- Do not merge `107-clean` into local main/codex worktree yet.
- Keep Remote107 fd1c03e as provisional.
- Ask 107 to push the missing source-lock package and corrected return note.
- MiMo can continue local PACE-HAT-v1 backlog independently; no need to block local work on 107.
