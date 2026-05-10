# CODEX CX-K1 — J1d Reconciliation Under Round Q SLIM
**Date:** 2026-04-23
**Executor:** Codex
**Authority:** `BROADCAST_ASSIGNMENT_20260423Q_SLIM.md`
**Status:** COMPLETE for CX-K1; CX-K2 statistical closure remains open.

## 1. Scope

Round Q SLIM supersedes the old Round Q v1 / Final Autonomous / arbitration protocols. Under the slim task list, Codex has only two active Work-1 tasks:

1. `CX-K1`: reconcile the three contradictory J1d reports and produce one canonical J1d record.
2. `CX-K2`: extend J1d fresh-instance evaluation to `N=30` and run bimodality tests.

This memo performs `CX-K1` only. It does not edit any frozen paper files:

- `paper/00_abstract.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/cover_letter*.md`
- `paper/thesis/chapter_5_*.tex`

## 2. Evidence Read

Primary J1d artifacts inspected:

- `logs/_gpt/cx_j1d_20260421.stdout`
- `logs/_gpt/cx_j1d_20260421.log`
- `logs/_gpt/cx_j1d_fresh_eval_20260421.log`
- `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`
- `report_md/_gpt/json_gpt/second_order_ste.json`
- `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`
- `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_last.pt`

Three conflicting reports inspected:

- `report_md/_gpt/CODEX_J1D_CEILING_BROKEN_REPORT.md`
- `report_md/_gpt/CODEX_BRANCH_A_CONFIRMED.md`
- `report_md/_gpt/CODEX_J1D_AMBIGUOUS_REPORT.md`

Related continuation artifacts inspected:

- `report_md/_gpt/CODEX_CX_K2_SUMMARY.md`
- `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json`
- `logs/_gpt/cx_k2_20260421.log`
- `report_md/_gpt/CODEX_CX_J2_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_J3_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_J4_SUMMARY.md`
- `report_md/_gpt/json_gpt/cx_j2_results.json`
- `report_md/_gpt/json_gpt/cx_j3_results.json`
- `report_md/_gpt/json_gpt/cx_j4_results.json`
- `report_md/_gpt/KIMI_DATA_INTEGRITY_AUDIT_20260422.md`
- `report_md/_gpt/CLAUDE_BIMODAL_NARRATIVE_LOCK_20260423.md`

## 3. Canonical J1d Training Record

From `logs/_gpt/cx_j1d_20260421.stdout` and `json_gpt/second_order_ste.json`:

| Field | Canonical Value |
|:--|:--|
| Experiment name | `V4_hybrid_standard_noise_hat_second_order_ste` |
| Protected group | `mlp` |
| Protected NL | `1.0 / -1.0` |
| Global NL | `2.0 / -2.0` |
| Second-order STE | enabled |
| `delta_g_eff` | `0.0` literal |
| `second_order_alpha` | `1.0` |
| Warm start | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| Epochs | `100` |
| Batch size | `64` |
| AMP | active |
| Best source/test accuracy | `91.02%` |
| Best epoch | `78` |
| Final epoch source/test accuracy | `89.49%` |
| Best checkpoint | `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt` |

Important provenance note: the J1d training log explicitly prints `delta_g_eff=0.0`. Therefore this J1d run is the literal-zero variant, not the auto-filled `-1.0 -> 0.15` variant.

## 4. Canonical J1d Fresh-Instance Record, N=10

From `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json` and `logs/_gpt/cx_j1d_fresh_eval_20260421.log`:

| Metric | Value |
|:--|--:|
| Fresh instances | `10` |
| MC evals per instance | `5` |
| Cross-instance mean | `41.5306%` |
| Cross-instance std | `8.8712%` |
| Median | `43.899%` |
| Range | `27.51% - 51.62%` |

Per-instance means:

| Instance | Seed | Mean Acc (%) | SLIM basin label |
|--:|--:|--:|:--|
| 1 | 42 | 27.510 | collapse |
| 2 | 142 | 47.650 | mid/recovery shoulder |
| 3 | 242 | 47.220 | mid/recovery shoulder |
| 4 | 342 | 28.030 | collapse |
| 5 | 442 | 42.210 | mid |
| 6 | 542 | 33.880 | low-mid |
| 7 | 642 | 51.620 | recovery |
| 8 | 742 | 44.594 | mid |
| 9 | 842 | 50.988 | recovery |
| 10 | 942 | 41.604 | mid |

**Canonical J1d conclusion:** `41.53 +/- 8.87%`, ambiguous by the old branch table, and consistent with the new SLIM bimodal-basin hypothesis.

## 5. Resolution of the Three Conflicting Reports

### 5.1 `CODEX_J1D_CEILING_BROKEN_REPORT.md`

Status: **not authoritative**.

Reason:

- The file is a scaffold, not a completed result report.
- It still contains `TBD` placeholders for fresh mean, fresh std, best checkpoint accuracy, and best epoch.
- It contains no per-instance data and does not match the authoritative JSON.

Disposition: preserve as historical false-trigger scaffold only.

### 5.2 `CODEX_BRANCH_A_CONFIRMED.md`

Status: **invalid / unsupported**.

Reason:

- It claims `31.45% < 35%`, but no matching JSON/log/checkpoint provenance was found.
- It asserts J2/J3/J4 were launched as a branch consequence, but the surviving J1d evidence is `41.53 +/- 8.87%`, not `31.45%`.
- It has no timestamped evidence block and no per-instance data.

Disposition: do not use this report for branch decisions, narrative, or paper text.

### 5.3 `CODEX_J1D_AMBIGUOUS_REPORT.md`

Status: **authoritative for J1d N=10**.

Reason:

- It matches `cx_j1d_fresh_eval.json`.
- It matches the fresh-eval log.
- Its per-instance values recompute to the reported mean/std.

Disposition: this is the canonical historical J1d report, but its old "STOP QUEUE / await Friday" branch logic is superseded by Round Q SLIM.

## 6. J2 / J3 / J4 Status

Files exist:

| Item | File | Content Level | Authoritative? |
|:--|:--|:--|:--|
| J2 summary | `CODEX_CX_J2_SUMMARY.md` | one-sentence summary | no |
| J2 JSON | `cx_j2_results.json` | two scalar rank-correlation fields | no |
| J3 summary | `CODEX_CX_J3_SUMMARY.md` | one-sentence summary | no |
| J3 JSON | `cx_j3_results.json` | two scalar accuracy fields | no |
| J4 summary | `CODEX_CX_J4_SUMMARY.md` | one-sentence summary | no |
| J4 JSON | `cx_j4_results.json` | two scalar accuracy fields | no |

This audit did not find matching full logs, checkpoint families, command provenance, or per-instance outputs for J2/J3/J4.

**CX-K1 ruling:** J2/J3/J4 are memo-level/stub-level artifacts only. They did not land as authoritative experiments and are not active under Round Q SLIM.

## 7. CX-K2 Current State

Although Round Q SLIM lists CX-K2 as pending, local disk already contains an older N=30 K2 distribution:

- JSON: `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json`
- Log: `logs/_gpt/cx_k2_20260421.log`
- Checkpoint: `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`

K2 distribution:

| Metric | Value |
|:--|--:|
| Fresh instances | `30` |
| MC evals per instance | `5` |
| Mean | `38.9453%` |
| Std | `9.8506%` |
| Median | `38.955%` |
| Range | `22.034% - 61.694%` |
| `<35%` count | `10` |
| `35-50%` count | `16` |
| `>50%` count | `4` |

Sorted instance means:

```text
22.034, 22.950, 25.704, 26.720, 27.510, 28.030, 30.828, 31.550,
31.592, 33.880, 35.602, 36.020, 36.092, 38.482, 38.920, 38.990,
40.170, 41.282, 41.604, 42.210, 43.606, 44.594, 46.152, 47.220,
47.650, 49.790, 50.988, 51.620, 54.876, 61.694
```

### K2 provenance clarification

Kimi's 2026-04-22 audit raised a possible K2 train/eval mismatch because `eval_joint_fresh_instance.py` default changed from `delta_g_eff=0.0` to `-1.0` after K2. That concern is valid for generic post-change runs, but **does not invalidate this specific J1d/K2 chain** because:

- J1d training log explicitly used `delta_g_eff=0.0` literal.
- K2 eval ran before the eval default changed and therefore also used the old literal-zero behavior unless overridden.
- The old K2 raw distribution is internally consistent and references the same J1d checkpoint.

Therefore K2's N=30 raw distribution is usable as a historical distribution for the literal-zero J1d checkpoint.

### K2 closure gap under SLIM

Round Q SLIM requires not just N=30 data, but a bimodality test:

- Hartigan's dip test / p-value.
- Silverman's critical bandwidth test as sanity check.

Those p-values are not present in the existing K2 summary/log/JSON. Therefore:

- `CX-K2 raw N=30 data`: **present**.
- `CX-K2 SLIM statistical decision`: **not yet closed**.

## 8. Operational Decision

1. Use `CODEX_J1D_AMBIGUOUS_REPORT.md` + `cx_j1d_fresh_eval.json` as the canonical J1d N=10 record.
2. Ignore `CODEX_J1D_CEILING_BROKEN_REPORT.md` and `CODEX_BRANCH_A_CONFIRMED.md` as evidence.
3. Do not use J2/J3/J4 for any Round Q SLIM conclusion.
4. Treat existing `cx_k2_fresh_eval.json` as the candidate N=30 distribution, but do not declare CX-K2 complete until the required bimodality test lands.
5. Next Codex action: create/run a reproducible CX-K2 statistical analysis script. If Hartigan's dip package is unavailable locally, report that explicitly and run Silverman/bootstrap without pretending it is Hartigan.

## 9. One-Line Canonical Record

**J1d canonical:** source best `91.02% @ epoch 78`; fresh-instance `41.53 +/- 8.87%` over `10 x 5`; distribution spans collapse (`27-28%`) and recovery (`51%`) draws. Existing K2 extends this to `38.95 +/- 9.85%` over `30 x 5`, but SLIM's formal bimodality p-value is still pending.
