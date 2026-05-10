# Remote 105 Phase P8 Final Ingestion Tasklist

Date: 2026-05-09
Issued by: Codex
Target: 105 server / multi-dataset validation lane
Status: Execute when 105 is available again. Not a Paper-1 submission blocker.

## 1. Goal

Close the 105 multi-dataset validation package cleanly so it can be used as supplement/defense evidence if it passes metadata and consistency gates.

## 2. Required Return Package

Return a Markdown report plus compact JSON/CSV summaries only. Do not send large checkpoints unless explicitly requested.

| Required item | Description |
|---|---|
| Exact git SHA | Commit used for all final runs. |
| Git status | Full `git status --short`; explain untracked files. |
| Environment | Python, PyTorch, CUDA, timm, GPU model, dataset path. |
| Exact commands | Train and fresh-eval commands for every final run. |
| Seed table | seed123/456/789 for each arch and HAT mode. |
| Fresh protocol | Number of fresh instances, MC runs, D2D/C2C semantics. |
| Source definition | Confirm source = best epoch test_acc, not train_acc. |
| JSON/log paths | For every run. |
| Failure log | If server crash lost any run, name it explicitly. |

## 3. Must-Finish Experiments

| Priority | Experiment | Seeds | Required output |
|---|---|---:|---|
| P0 | `deit_proportional` | 123/456/789 | source, fresh mean/std, exact command |
| P0 | `deit_digital` | 123/456/789 | same-arch digital baseline |
| P0 | `vit_proportional` | 123/456/789 | source, fresh mean/std |
| P0 | `vit_digital` | 123/456/789 | same-arch digital baseline |
| P1 | `deit_ensemble` | 123/456/789 if feasible | robustness comparison |
| P1 | `vit_ensemble` | 123/456/789 if feasible | robustness comparison |
| P2 | `standard` modes | optional | only if cheap; otherwise mark as known-collapse |

## 4. Decision Gates

| Gate | Pass condition |
|---|---|
| Naming | Source/test/train definitions unambiguous. |
| Same-arch digital | Every proportional claim compared to same architecture. |
| Multi-seed | At least 3 seeds for any supplement-level claim. |
| Fresh protocol | 10x5 or explicitly documented equivalent. |
| Reproducibility | Exact commands and git SHA present. |
| No Paper-1 contamination | State clearly this is validation/supplement, not changing locked Paper-1 values. |

## 5. Return Format

Use this top-level table:

| Arch | Mode | Seed | Source test_acc | Fresh mean | Fresh std | Delta fresh-source | Checkpoint path | JSON path | Status |
|---|---|---:|---:|---:|---:|---:|---|---|---|

Then provide aggregate table:

| Arch | Mode | n | Source mean +/- sd | Fresh mean +/- sd | Advantage vs digital | Verdict |
|---|---:|---:|---:|---:|---:|---|

## 6. Kill Criteria

Stop and report instead of continuing if:

| Condition | Action |
|---|---|
| Dataset path changed mid-run | Stop, mark runs invalid. |
| Source accidentally logged as train_acc | Stop, re-export summary. |
| Missing same-arch digital baseline | Do not claim proportional advantage. |
| Server crash corrupts checkpoint/log | Mark as invalid; do not average. |
