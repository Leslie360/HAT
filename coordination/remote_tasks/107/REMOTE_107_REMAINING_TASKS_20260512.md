# Remote 107 Remaining Tasks for Paper 2 Full Closure

Date: 2026-05-12
Status: Extended eval in progress; 5 queued or blocked items remain

## Why this task exists

The user asked for a gap analysis of what remains incomplete before the Paper 2 experiment loop on Remote 107 can be considered fully closed. This file tracks those gaps.

## Task inventory

| # | Task | Status | Blocker / Note |
|---|---|---|---|
| 1 | Extended downstream eval (MMLU, Winogrande, PIQA, BoolQ) on p28b clean/analog and p69b clean/analog | **In Progress** | Running on GPUs 4/5/6/7 since ~09:51. p69b clean runs without MMLU due to `datasets` cache corruption. ETA 3-4h. |
| 2 | Retention noise sweep on p28b and p69b | **Queued** | Script ready at `/tmp/run_retention_sweep_queue.py`. 8 tasks (0.001, 0.01, 0.1, 1.0 × 2 models). Blocked by #1 (needs GPUs 4/5). |
| 3 | Layer ablation training (last2 / last4) on p28b and p69b | **Queued** | Script ready at `/tmp/run_layer_ablation_training.py`. 4 training jobs, 500 steps each. Blocked by #2. |
| 4 | p69b clean MMLU eval (single task) | **Blocked** | Requires fixing `datasets` cache corruption first, or running in a clean cache env. Skipped during #1 to avoid repeated crash. |
| 5 | Qwen3-VL 5000-step checkpoint eval | **Pending** | Training completed at `vlm_hat_last1_seed42` but evaluation was never run. Needs clean vs analog PPL/QA validation. |
| 6 | Qwen3-VL claim-lock metadata | **Pending** | Generate source-backed manifest + JSON sidecars for the 5000-step VLM checkpoint. Depends on #5. |
| 7 | Generate Paper 2 figures and update conclusions | **Pending** | User explicitly deferred: "图表不用你画了，只做1就行". Kept here for completeness. |

## Execution order (user-confirmed priority)

1. Wait for #1 to finish.
2. Launch #2 immediately after GPUs 4/5 free.
3. Launch #3 immediately after #2 finishes.
4. #4 can be attempted in parallel with #2 or #3 if cache issue is resolved.
5. #5 and #6 can run on any idle GPU (e.g., GPU 3) in parallel with #2/#3.

## Required scripts

- `/tmp/run_retention_sweep_queue.py` — retention sweep automation
- `/tmp/run_layer_ablation_training.py` — layer ablation training automation
- `/tmp/run_extended_lm_eval_v2.sh` — extended downstream eval launcher (already running)

## Acceptance criteria for full closure

- All rows in the table above are marked **Completed**.
- p69b clean MMLU result exists (even if run manually).
- Qwen3-VL 5000-step checkpoint has eval JSONs for both clean and analog configs.
- All new JSONs follow the corrected filename format including `n_states` (e.g. `eval_*_ns256_*.json`).
