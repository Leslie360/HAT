# DISPATCH — Kimi Local GPU Queue, Controlled Not Overloaded

Date: 2026-05-07 15:35 +08
Owner: Kimi
Coordinator: Codex
Resource: local RTX 5070 Ti 16GB, currently idle

## Executive Ruling

Do **not** flood Kimi with many GPU jobs. This is a single 16GB local GPU, not the 8-card remote server. The correct policy is:

1. Keep GPU non-idle with a short, prioritized queue.
2. Run at most **one training job** at a time.
3. A lightweight eval may run only if it does not materially slow the training job.
4. Every job must have a kill criterion and exact provenance.
5. No exploratory long run without a clear decision it can change.

The goal is to support the newly locked Paper-1 narrative:

> Ensemble HAT solves algorithmic cross-instance robustness; PCM precision-retention physics selects the deployable bit point; 6-bit is the observed Pareto midpoint.

## Current Inputs

From Kimi hostile review:

- Do not headline real PCM as “4-bit rescue”.
- IdealDevice 4-bit 86.16% is algorithmic ablation only.
- PCM deployment claim is a precision-retention frontier.
- 4-bit PCM fresh is trainable but drift-limited.
- 6-bit PCM is currently the observed Pareto midpoint.

From local/remote state:

- Local GPU is idle.
- 105 is blocked until new seed results return.
- 107 K107 P0/EPSC is promising but should be cited only from locked metadata snapshots.
- Paper polish is being handled separately by user/Gemini; shared-agent priority is experiments/data integrity.

## Queue Policy

### Hard Limits

- Max active training jobs: 1
- Max active eval jobs: 1, only if GPU memory stays below safe threshold and training throughput is not harmed
- No more than 3 queued GPU jobs before reporting back
- If a run is expected to exceed 8 hours, ask/flag before launch unless it is a continuation of an already approved canonical run

### Early Stop Rules

Use whichever is supported by the script; if not supported, manually monitor logs:

- Stop training if validation/source metric has no meaningful improvement for 10 epochs.
- Stop immediately if source/fresh is clearly inconsistent with previous canonical range and logs indicate code/config mismatch.
- Stop if checkpoint/preset path silently falls back or metadata is incomplete.
- Stop if the job only reproduces an already locked result without adding a missing seed, missing precision, missing drift point, or missing provenance.

## P0 — Frontier Consistency Audit and Missing-Cell Fill

### K-GPU-P0.1: Checkpoint and Result Inventory

Before launching training, produce a table of all local PCM frontier artifacts:

- precision: 4-bit / 5-bit / 6-bit / 8-bit
- seed: 123 / 456 / 789 or available seeds
- source/fresh/drift metrics
- checkpoint path
- train log path
- fresh eval log path
- drift eval log path
- exact command if available
- git SHA / dirty status if available

Output:

- `report_md/_gpt/KIMI_LOCAL_PCM_FRONTIER_INVENTORY_20260507.md`

Decision impact:

- If 5-bit already has complete 3-seed fresh+drift, do not retrain it. Just summarize.
- If 5-bit is incomplete but near completion, finish only the missing eval/train cells.
- If 6-bit or 4-bit canonical data is missing provenance, prioritize provenance repair over new experiments.

### K-GPU-P0.2: 5-bit PCM Multi-Seed Closure

Rationale: The manuscript currently says 6-bit is the Pareto midpoint. If 5-bit exists and is strong, it may refine the frontier curve. This is the only immediately useful new local GPU direction.

Run only missing cells for 5-bit PCM:

- seeds: 123, 456, 789 if not already complete
- required metrics: source, fresh, drift at 24h or canonical drift horizon
- use strict preset mode; no fallback allowed
- record exact commands and logs

Kill criteria:

- If inventory shows all 5-bit cells already complete, do not rerun.
- If the first missing 5-bit seed is clearly below 4-bit/6-bit in both fresh and drift, stop remaining 5-bit training and report it as non-frontier.
- If 5-bit is between 4-bit and 6-bit, finish all missing seeds because it may alter the Pareto plot.

Output:

- `report_md/_gpt/KIMI_LOCAL_5BIT_PCM_CLOSURE_20260507.md`

Required verdict:

- Does 5-bit change the “6-bit Pareto midpoint” statement?
- If yes, propose corrected manuscript language.
- If no, explain why 6-bit remains the deployable point.

## P1 — Reproducibility Repair, Not New Science

### K-GPU-P1.1: Canonical 4/6/8-bit Re-eval If Metadata Is Weak

Only run if P0 inventory finds missing or weak provenance.

For each canonical precision, re-run evaluation from existing checkpoint only:

- 4-bit PCM: fresh + 24h drift
- 6-bit PCM: fresh + 24h drift
- 8-bit PCM: fresh + 24h drift

Do not retrain unless checkpoint is missing and the result is manuscript-critical.

Output:

- `report_md/_gpt/KIMI_LOCAL_PCM_CANONICAL_REEVAL_20260507.md`

Required verdict:

- Are the current paper numbers traceable to logs/checkpoints?
- Are the 1 pp SLA and 4-bit drift-limited claim still valid?

## P2 — Optional Only If GPU Still Idle

### K-GPU-P2.1: IdealDevice 4-bit Ablation Smoke Replay

Purpose: Confirm the algorithmic ablation did not break under current code after narrative edits.

Run a short smoke replay or eval-only validation for:

- Standard/fixed-mask HAT 4-bit IdealDevice collapse
- Ensemble HAT 4-bit IdealDevice rescue

Do not launch full 3-seed training unless existing logs/checkpoints are missing or inconsistent.

Output:

- `report_md/_gpt/KIMI_IDEALDEVICE_4BIT_ABLATION_SMOKE_20260507.md`

Required verdict:

- Is the IdealDevice 4-bit rescue claim safe as an algorithmic ablation?
- Does it remain clearly separated from PCM deployment in the manuscript?

## Reporting Format

Every report must start with this table:

| Task | Status | New GPU hours | Changed manuscript claim? | Verdict |
|---|---:|---:|---:|---|

Then include:

1. exact command lines
2. git SHA and git status summary
3. checkpoint paths
4. log paths
5. result table with source/fresh/drift
6. kill/continue decision
7. one-sentence manuscript implication

## Codex Position

The GPU should not sit idle, but overloading Kimi with many jobs is counterproductive. The only high-value local GPU work right now is frontier closure and provenance repair. New broad exploration should wait until 105/107 return or until a specific claim is blocked.
