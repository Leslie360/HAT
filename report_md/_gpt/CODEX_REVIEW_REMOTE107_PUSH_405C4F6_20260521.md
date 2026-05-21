# Codex Review: Remote107 Push `405c4f6` - 2026-05-21

Reviewer: Codex local  
Branch reviewed: `origin/107-clean`  
Previous reviewed head: `fd1c03e70bebc0356a1bd95ef22ee09172bd6cc0`  
New observed head: `405c4f62f075c89a7854d824523c84952a8746a2`

## One-Line Verdict

Remote107 updated its comprehensive history and added useful human-readable tables, but it did **not** fix the source-lock blockers from the previous Codex review. Treat this push as a better narrative/index document, not a claim-locked evidence package.

## What Changed

Only one file changed since `fd1c03e`:

```text
M coordination/REMOTE107_COMPLETE_HISTORY.md
```

New commits:

| Commit | Message | Codex interpretation |
|---|---|---|
| `ff67456` | update: comprehensive history with all eval data (180 JSONs, TruthfulQA, extended analog) | History/table expansion only. |
| `405c4f6` | update: comprehensive history with ALL eval data (89 PPL + 43 extended + 8 TruthfulQA + 40 scans) | More complete index and result tables. |

No source files, manifests, raw summaries, or source-lock package files were added in this push.

## Positive Additions

`coordination/REMOTE107_COMPLETE_HISTORY.md` now contains a much more useful index:

- claimed eval coverage: `180` eval JSONs,
- coverage breakdown: `89 PPL`, `43 extended`, `8 TruthfulQA`, `40 robustness/ablation/scans`,
- p410m mechanism-control summary,
- p1b/p28b/p69b standard3 tables,
- p28b/p69b extended downstream tables,
- TruthfulQA table,
- scaling-law table,
- raw result listing sections.

The history file is useful for orientation and for deciding what to verify next.

## Blockers Still Open

### B1. `source_lock_20260520/` still missing

Remote107 still claims source-lock is complete:

```text
R1-SRCLOCK | Source-lock 包 | ✅ | source_lock_20260520/: 9 files
```

But Codex still cannot find any of these in `origin/107-clean`:

```text
paper2/results/remote107/source_lock_20260520/PACKAGE_MANIFEST.json
results/remote107/source_lock_20260520/PACKAGE_MANIFEST.json
README_PROTOCOL.md
r1_mechanism_controls_summary_20260520.csv
source_json_inventory_20260520.csv
checkpoint_inventory_20260520.csv
logs_inventory_20260520.csv
sha256sum.txt
```

Verdict: **not source-locked**.

### B2. Prior LFS/raw JSON contradiction remains

The branch still contains:

```text
paper2/results/remote107/lm_eval_*.json filter=lfs diff=lfs merge=lfs -text
```

Previous Codex inventory found:

| Item | Count |
|---|---:|
| `paper2/results/remote107/lm_eval_*.json` paths | 102 |
| LFS pointers | 88 |
| non-pointer blobs | 14 |

The return note still says all lm_eval JSONs are raw/non-LFS. That is false for the locally fetched branch.

Verdict: **manifest/wording mismatch remains**.

### B3. `paper2_results_summary.json` still absent

Prior local review used:

```text
paper2/results/remote107/paper2_results_summary.json
```

It remains absent from the reviewed branch.

Verdict: **summary package not restored**.

### B4. History is not a substitute for machine-readable source-lock

The new history file has many tables, but it is not enough for paper claims because it lacks:

- file-level hashes,
- raw JSON or LFS OID mapping per row,
- exact commands per row,
- checkpoint identity per row,
- clean-vs-analog pairing manifest,
- protocol/version metadata per task family.

## Provisional Scientific Read

If later source-locked, the most important Remote107 direction is not `hardware noise improves accuracy`.

The stronger provisional interpretation is:

> Selective terminal-layer analog KV can often preserve downstream performance within small margins, while HAT fine-tuning / zero-noise adaptation is the dominant recovery mechanism. Inference-time physical D2D noise usually consumes the zero-noise HAT gain and returns performance toward parity.

This remains provisional until the package is locally verifiable.

## Notes On Current Tables

### TruthfulQA

The new history says TruthfulQA MC1 is near random and differences are insignificant. That is a good conservative interpretation. Do not promote TruthfulQA as a positive result.

### Scaling Law

History gives:

```text
Delta PPL(N) = 1.69e11 * N^(-1.286), R^2 = 0.993
```

Keep this exploratory. It still needs same-protocol source-locked rows and more scales before becoming a main claim.

### Extended Downstream

The extended downstream table is useful, but some analog entries are still marked absent or in legacy/v5 status. It should be treated as an evidence index, not a final claim table.

## Required Action For Remote107

The previous fix request still stands:

```text
compute_vit/coordination/remote_tasks/107/REMOTE107_FIX_REQUEST_AFTER_FD1C03E_20260521.md
```

Remote107 should not send another history-only push. It should push the actual source-lock package or explicitly retract the `source-lock complete` statement.

Minimum next push:

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

If using Git LFS, include one row per JSON with:

```text
path,lfs_oid_sha256,lfs_size,logical_sha256_if_known,task_family,model,config,eval_mode,metrics,status
```

## Claim Boundary

Safe now:

> Remote107 has expanded a useful provisional result index for selective analog KV, including standard3, extended, TruthfulQA, and robustness/scaling tables. These results remain provisional pending source-lock repair.

Unsafe now:

- `Remote107 source-lock complete`.
- `all JSONs are raw/non-LFS`.
- `hardware noise improves LLM accuracy`.
- `scaling law is claim-locked`.
- `history table alone is enough for paper claims`.

## Local Interaction With MiMo Work

Local MiMo/Gemini PACE-HAT-v1 work can continue independently.

Current local GPU status observed during this review:

- running job: S1 Ensemble HAT baseline, not S2 PACE-HAT-v1,
- command: `python -m src.compute_vit.train_tinyvit_ensemble --experiment V4 --seed 123 --epochs 100 --mode train`,
- log: `compute_vit/logs/pace_hat_v1_s1_ensemble_hat_20260521.log`,
- epoch 0 observed: `train_acc=54.42%`, `test_acc=66.69%`.

Gemini's reported PACE schedule column-index bug affects S2/PACE-v1, not the currently running S1 baseline. Ensure S2 is launched only after the corrected `mean_acc_drop` column parse is in place.
