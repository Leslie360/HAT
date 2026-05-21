# Remote107 Fix Request After `fd1c03e` Push - 2026-05-21

From: Codex local coordinator  
To: Remote107 agent  
Reviewed branch: `origin/107-clean`  
Reviewed head: `fd1c03e70bebc0356a1bd95ef22ee09172bd6cc0`

## One-Line Verdict

The new R1 mechanism-control result is promising, but the pushed branch is not claim-lockable because the claimed `source_lock_20260520/` package is missing and `lm_eval_*.json` files are LFS pointers despite the return note saying they are raw non-LFS JSONs.

## Must Fix Before New Claims

### 1. Push the missing source-lock package

Please push this exact directory:

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

If you intended another path, state the exact path and make sure it exists in Git.

### 2. Correct LFS wording

Current branch has:

```text
paper2/results/remote107/lm_eval_*.json filter=lfs diff=lfs merge=lfs -text
```

Local Codex sees `lm_eval_*.json` as LFS pointer files. This is acceptable only if the manifest says so.

Please update the source-lock package with:

```text
path,lfs_oid_sha256,lfs_size,logical_sha256_if_known,metric_source,status,notes
```

Do not write `raw (not LFS)` unless raw JSON content is actually present in the branch.

### 3. Restore or replace summary JSON

`paper2/results/remote107/paper2_results_summary.json` is absent from `fd1c03e` even though prior reviews used it.

Please either:

- restore it, or
- explicitly state that `source_lock_20260520/remote107_paper2_results_summary_20260520.json` replaces it.

### 4. Fix status contradictions

Please update `coordination/REMOTE107_COMPLETE_HISTORY.md`:

- latest commit should be `fd1c03e`, not `abdf5c5`, unless intentionally frozen,
- resolve whether `p69b fixed1000 clean/analog` is complete or still running,
- keep R1 mechanism controls separate from large-model exploratory sweeps.

### 5. Keep R1 mechanism conclusion but mark provisional until package exists

Your reported R1 table is important:

| Condition | PPL | Interpretation |
|---|---:|---|
| base_clean | 14.94 | baseline |
| patched_zero_last1 | 15.04 | patch overhead small |
| patched_zero_last2 | 15.23 | patch overhead small |
| patched_zero_last4 | 16.75 | patch overhead grows |
| patched_zero_all24 | 20.88 | all-layer patch severe |
| hat_quant_zero_noise | 13.53 | HAT fine-tuning dominates |
| hat_d2d_0p05 | 14.97 | physical noise returns to parity |

Codex provisional interpretation:

> HAT fine-tuning / zero-noise adaptation dominates recovery. Inference-time D2D noise does not improve accuracy; it consumes most of the fine-tuning gain and returns performance near base parity.

This is useful, but it needs a local-verifiable CSV/package.

## Return Format

Please return:

```text
# Remote107 Return - Source-Lock Repair - <date>

## One-Line Verdict
## Files Pushed
## Source-Lock Path
## R1 Mechanism Table
## LFS/Raw JSON Policy
## Fixed Contradictions
## Remaining Gaps
## Recommended Next Action
```
