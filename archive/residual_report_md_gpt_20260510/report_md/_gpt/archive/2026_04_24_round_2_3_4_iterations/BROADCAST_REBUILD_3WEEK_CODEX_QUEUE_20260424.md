# BROADCAST - Codex 3-Week Rebuild Queue
Date: 2026-04-24
Issuer: Codex
Source: `BROADCAST_REBUILD_3WEEK_20260424.md`
Status: active

## CX-M1 Status

`CX-M1` is active in tmux:

- tmux session: `cx_m1_20260424_101504`
- process: `train_tinyvit_ensemble.py`
- config: Standard HAT V3, uniform noise, train/eval `NL_LTP=2.0 / NL_LTD=-2.0`, seed `123`
- train log: `logs/_gpt/cx_m1_20260424_101504.log`
- checkpoint dir: `checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123`
- epoch 0 observed: `train_acc=50.69%`, `test_acc=62.41%`

## Continuation Queue

Codex prepared and launched an autonomous sequential queue:

- script: `scripts/_gpt/launch_cx_m_series_queue.sh`
- tmux session: `cx_m_series_queue_20260424_102139`
- status: `report_md/_gpt/json_gpt/cx_m_series_queue_status.json`
- queue log: `logs/_gpt/cx_m_series_queue_20260424_102139.log`
- tmux tee log: `logs/_gpt/cx_m_series_queue_tmux_20260424_102139.out`

Queue behavior:

- waits for current `CX-M1` fresh eval JSON
- runs `CX-M5` only if `CX-M1` differs from `82.6346 +/- 0.5624%` by more than `2 sigma`
- runs `CX-M2` Ensemble HAT V4 uniform NL=2 seed 123
- runs `CX-M3` Proportional HAT V4 proportional NL=2 seed 123
- runs `CX-M4` seed 456 only if `CX-M3 >= CX-M2`
- stops and escalates if any M-series fresh mean is outside `[70, 90]`
- never runs simultaneous GPU jobs

## Regression Guard

Codex patched `eval_fresh_instances_postfix.py` to reject silent train/eval NL mismatches by default.

Evidence:

- `CODEX_REGRESSION_TEST_20260424.md`
- `test_dual_bug_fix.py`: `6` tests passed

## Next Non-GPU Codex Work

While GPU runs, Codex should continue:

- `CX-AUDIT-1`: bug-immunity audit for canonical NL=1.0 results
- figure/checkpoint source table
- canonical recheck only if GPU is free and M-series queue permits

## GPU Utilization Override — 2026-04-24 10:37 CST

User override: do not leave GPU idle; run safe independent M-series jobs in parallel.

Changes applied:

- Stopped old CPU-resize sessions: `cx_m1_20260424_101504`, `cx_m2_20260424_103028`, `cx_m3_20260424_103107`.
- Deprecated old sequential queue `cx_m_series_queue_20260424_102139` for local execution; it remains a historical record only.
- Added `--gpu-resize` to `train_tinyvit_ensemble.py` and M-series launch scripts.
- GPU-resize behavior: CIFAR tensors load at native `32x32`, then resize to `224x224` with `torch.nn.functional.interpolate` on GPU. This removes the CPU/PIL resize bottleneck observed during parallel startup.
- DataLoader worker safety: when `num_workers > 0`, `multiprocessing_context="spawn"` is now used to avoid CUDA/fork deadlock. Current M-series runs keep `num_workers=0` for lowest-risk continuity.

Active local GPU sessions:

| Task | tmux | Experiment | Noise | Seed | Resume | Log | Status |
|------|------|------------|-------|------|--------|-----|--------|
| CX-M1 | `cx_m1_20260424_103746` | V3 Standard HAT | uniform | 123 | from epoch 10 | `logs/_gpt/cx_m1_20260424_103746.log` | `report_md/_gpt/json_gpt/cx_m1_status.json` |
| CX-M2 | `cx_m2_20260424_103746` | V4 Ensemble HAT | uniform | 123 | fresh | `logs/_gpt/cx_m2_20260424_103746.log` | `report_md/_gpt/json_gpt/cx_m2_status.json` |
| CX-M3 | `cx_m3_20260424_103746` | V4 Ensemble HAT | proportional | 123 | fresh | `logs/_gpt/cx_m3_20260424_103746.log` | `report_md/_gpt/json_gpt/cx_m3_status.json` |

Observed after restart:

- All three logs report `GPU resize: True` and per-experiment `gpu_resize=on`.
- M1 resumed from `checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_last.pt` at epoch `10/100` with `best_acc=79.74%`.
- GPU utilization increased from ~`1%` before restart to ~`83%` immediately after parallel GPU-resize restart.

Guardrails:

- No new narrative claims until M1/M2/M3 train + fresh eval JSON land.
- M4 seed-456 remains conditional on M3 beating M2.
- M5 remains conditional on M1 deviation from the old postfix standard line by more than 2 sigma.
- Remote remains separate; this broadcast only updates local Codex GPU execution.

## First Parallel Checkpoint — 2026-04-24 10:42 CST

Parallel GPU-resize restart produced valid first checkpoints/logs:

| Task | Latest observed | Train acc | Test acc | Best | Evidence |
|------|-----------------|-----------|----------|------|----------|
| CX-M1 | checkpoint epoch 10 | not logged at epoch 10 | 79.96% | 79.96% | `checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_last.pt` |
| CX-M2 | log/checkpoint epoch 0 | 49.67% | 60.28% | 60.28% | `logs/_gpt/cx_m2_20260424_103746.log` |
| CX-M3 | log/checkpoint epoch 0 | 51.00% | 60.42% | 60.42% | `logs/_gpt/cx_m3_20260424_103746.log` |

Monitor:

- tmux: `cx_m_monitor_20260424_103746`
- JSON: `report_md/_gpt/json_gpt/cx_m_parallel_monitor.json`
- log: `logs/_gpt/cx_m_parallel_monitor_20260424_103746.log`

Current decision: keep three-way parallel execution. No evidence of OOM, deadlock, or GPU starvation after GPU-resize restart.

## Live GPU Broadcast — 2026-04-24 10:50 CST

Status: local GPU is actively utilized; do not interrupt unless OOM or fatal warning appears.

Runtime:

- Active tmux: `cx_m1_20260424_103746`, `cx_m2_20260424_103746`, `cx_m3_20260424_103746`, `cx_m_monitor_20260424_103746`.
- GPU sample: `12363 / 16303 MiB`, `84%` utilization.
- Monitor JSON: `report_md/_gpt/json_gpt/cx_m_parallel_monitor.json`.
- Monitor warnings: none.

Latest checkpoint readout:

| Task | Latest epoch | Best test | Latest test | Fresh JSON |
|------|--------------|-----------|-------------|------------|
| CX-M1 | 13/100 | 79.96% | 76.22% | pending |
| CX-M2 | 4/100 | 76.93% | 76.93% | pending |
| CX-M3 | 3/100 | 73.42% | 73.42% | pending |

Instructions to agents:

- Kimi: continue review/draft work only; do not promote M-series numbers until fresh eval JSON lands.
- Gemini: remain on code audit only.
- Claude: no route ratification from partial source-test checkpoints; wait for completed train + fresh eval packets.
- Remote: remains separate; no new remote task implied by this local broadcast.

Codex decision: keep three-way parallel execution. M4/M5 remain conditional and are not launched yet.

## Early Stop Update — 2026-04-24 11:33 CST

User rule accepted: stop a run once source-test accuracy has not improved for `10` epochs.

Implementation:

- Added CLI flag `--early-stop-patience` to `train_tinyvit_ensemble.py`.
- M-series launcher now passes `--early-stop-patience 10`.
- Stop check runs after each epoch checkpoint save, so `*_last.pt` and `*_best.pt` remain available before exit.
- Current checkpoint backup before restart: `checkpoints/_gpt/postfix_m_series/20260424_earlystop_backup_113219/`.

Restarted active runs with timestamp `20260424_113250`:

| Task | tmux | Resume epoch | Best epoch | Best test | Early-stop state |
|------|------|--------------|------------|-----------|------------------|
| CX-M1 | `cx_m1_20260424_113250` | 30/100 | 23 | 81.48% | 7 epochs since best |
| CX-M2 | `cx_m2_20260424_113250` | 22/100 | 20 | 80.97% | 2 epochs since best |
| CX-M3 | `cx_m3_20260424_113250` | 21/100 | 13 | 80.88% | 8 epochs since best |

Monitor restarted:

- tmux: `cx_m_monitor_20260424_113250`
- JSON: `report_md/_gpt/json_gpt/cx_m_parallel_monitor.json`

Observed after restart: GPU `12272 / 16303 MiB`, utilization `83%`, no OOM.

Instruction: treat any early-stopped run as normal completion and proceed to its fresh eval. Do not relaunch it to 100 epochs unless a new route decision explicitly requires it.

## CX-M3 Completed — 2026-04-24 11:55 CST

`CX-M3` early-stopped normally and completed fresh eval.

Training:

- Task: `CX-M3` V4 Ensemble HAT, proportional noise, seed `123`, true train/eval `NL_LTP=2.0 / NL_LTD=-2.0`.
- Early stop: epoch `23`, no test_acc improvement for `10` epochs.
- Best source test: `80.88%` at epoch `13`.
- Last source test: `79.17%`.
- Checkpoint: `checkpoints/_gpt/postfix_m_series/cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt`.

Fresh eval:

- JSON: `report_md/_gpt/json_gpt/cx_m3_fresh_eval.json`.
- Log: `logs/_gpt/cx_m3_fresh_eval_20260424_113250.log`.
- Protocol: `10` fresh instances, `5` MC runs per instance.
- Result: `80.7132% ± 0.1370%`, range `80.46--81.00%`.
- Provenance check: checkpoint NL/noise matches eval NL/noise; no override used.

Current remaining runs:

- `CX-M1`: active, checkpoint epoch `37`, best `82.25%` at epoch `36`, latest `79.04%`.
- `CX-M2`: active, checkpoint epoch `29`, best `80.97%` at epoch `20`, latest `78.12%`, stale `9`; likely next to early-stop if no improvement.

Instruction: `CX-M3` is now a valid completed M-series packet, but final route decision still waits for `CX-M1` and `CX-M2` fresh eval JSON.

## GPU Fill Update — 2026-04-24 12:00 CST

User instruction: GPU has room; keep launching useful independent work.

New launches:

| Task | tmux | Config | Purpose | Status |
|------|------|--------|---------|--------|
| CX-M4 | `cx_m4_20260424_113250` | V4 Ensemble HAT, proportional, seed 456, true NL2 | Cross-seed replication of completed `CX-M3` | launched |
| CX-M5 | `cx_m5_20260424_113250` | V3 Standard HAT, uniform, seed 456, true NL2 | Cross-seed replication of `CX-M1` Standard route | launched |

Active GPU work after fill:

- `CX-M1`: still training, Standard seed 123.
- `CX-M2`: early-stopped and running fresh eval, uniform Ensemble seed 123.
- `CX-M4`: training, proportional Ensemble seed 456.
- `CX-M5`: training, Standard seed 456.

Observed GPU sample after `CX-M5` launch:

- Memory: `13164 / 16303 MiB`.
- Utilization: `85%`.

Safety decision:

- Do not add another GPU process now. Four active GPU consumers put memory near the safe limit; another full train job risks OOM and would waste the current runs.
- Re-evaluate launching more after `CX-M2` fresh eval exits or after `CX-M1` early-stops.

Coordination:

- `CX-M4` and `CX-M5` are extra replication runs enabled by available GPU capacity; they do not replace the required M1/M2/M3 evidence packets.
- Narrative still waits for completed fresh JSONs.

## Continue Update — 2026-04-24 13:22 CST

Status check found more completed packets and one eval failure:

Completed fresh packets:

| Task | Train best | Fresh mean | Fresh std | Notes |
|------|------------|------------|-----------|-------|
| CX-M2 | 80.97% @ epoch 20 | 80.4538% | 0.5835% | V4 Ensemble uniform seed 123 |
| CX-M3 | 80.88% @ epoch 13 | 80.7132% | 0.1370% | V4 Ensemble proportional seed 123 |
| CX-M5 | 80.69% @ epoch 16 | 80.4674% | 0.0936% | V3 Standard uniform seed 456 |

M1 training completed but its first fresh eval failed:

- `CX-M1` train best: `82.89% @ epoch 54`, early-stopped at epoch `64`.
- First M1 fresh eval failed with CUDA OOM in DataLoader pin-memory thread while multiple GPU consumers were active.
- Fix applied: TinyViT eval path now uses `pin_memory=False` via `inference_analysis_utils.py`; `train_tinyvit.py` now supports explicit `pin_memory` override.
- M1 fresh eval retry launched in tmux `cx_m1_fresh_retry_20260424_132150`.

New GPU task:

- `CX-M6` launched: V4 Ensemble HAT, uniform noise, seed `456`, true NL2, `--gpu-resize`, `--early-stop-patience 10`.
- Purpose: cross-seed replication of `CX-M2` uniform Ensemble route.
- tmux: `cx_m6_20260424_113250`.

Active after update:

- `CX-M4`: V4 proportional seed 456 training.
- `CX-M6`: V4 uniform seed 456 training.
- `CX-M1` fresh eval retry.

GPU sample after update: `8601 / 16303 MiB`, utilization `74%`.

Do not launch more until M1 retry confirms stable; preserve headroom to avoid repeating the eval OOM.

## M1-M6 Complete + Seed-789 Launch — 2026-04-24 15:32 CST

Training/fresh status checked after reading broadcast. All `CX-M1` through `CX-M6` packets are complete and all fresh JSONs exist.

Completed result table:

| Task | Config | Seed | Train best | Fresh mean | Fresh std | JSON |
|------|--------|------|------------|------------|-----------|------|
| CX-M1 | V3 Standard, uniform | 123 | 82.89% @ epoch 54 | 82.0282% | 0.9416% | `report_md/_gpt/json_gpt/cx_m1_fresh_eval.json` |
| CX-M2 | V4 Ensemble, uniform | 123 | 80.97% @ epoch 20 | 80.4538% | 0.5835% | `report_md/_gpt/json_gpt/cx_m2_fresh_eval.json` |
| CX-M3 | V4 Ensemble, proportional | 123 | 80.88% @ epoch 13 | 80.7132% | 0.1370% | `report_md/_gpt/json_gpt/cx_m3_fresh_eval.json` |
| CX-M4 | V4 Ensemble, proportional | 456 | 81.39% @ epoch 36 | 80.7532% | 0.4271% | `report_md/_gpt/json_gpt/cx_m4_fresh_eval.json` |
| CX-M5 | V3 Standard, uniform | 456 | 80.69% @ epoch 16 | 80.4674% | 0.0936% | `report_md/_gpt/json_gpt/cx_m5_fresh_eval.json` |
| CX-M6 | V4 Ensemble, uniform | 456 | 81.87% @ epoch 41 | 81.1850% | 1.6847% | `report_md/_gpt/json_gpt/cx_m6_fresh_eval.json` |

Immediate reading:

- Standard V3 mean over two seeds: `(82.0282 + 80.4674) / 2 = 81.2478%`.
- Ensemble uniform V4 mean over two seeds: `(80.4538 + 81.1850) / 2 = 80.8194%`.
- Ensemble proportional V4 mean over two seeds: `(80.7132 + 80.7532) / 2 = 80.7332%`.
- All true-NL2 routes are in the same ~80-82% band; proportional no longer has a special 90% claim.
- M1 is currently the best single packet, but M5 shows Standard has seed variance; do not lock final route on one seed.

GPU was idle after M1-M6 completion (`582 / 16303 MiB`, ~1% utilization), so Codex launched a third seed group:

| New task | Config | Seed | tmux | Purpose |
|----------|--------|------|------|---------|
| CX-M7 | V3 Standard, uniform | 789 | `cx_m7_20260424_153222` | third seed for Standard route |
| CX-M8 | V4 Ensemble, uniform | 789 | `cx_m8_20260424_153222` | third seed for Ensemble uniform route |
| CX-M9 | V4 Ensemble, proportional | 789 | `cx_m9_20260424_153222` | third seed for Ensemble proportional route |

Monitor:

- tmux: `cx_m_monitor_20260424_153222`
- JSON: `report_md/_gpt/json_gpt/cx_m_parallel_monitor.json`

Instruction:

- Kimi/Gemini/Claude should treat M1-M6 as completed evidence and M7-M9 as active replication.
- Draft text must not resurrect the old proportional 90.88% claim; the current true-NL2 proportional evidence is ~80.7% fresh across two seeds.
- Route decision should wait for M7-M9 unless a faster interim decision is explicitly requested.

## Final Push Dispatch Alignment — 2026-04-24 16:25 CST

Read `BROADCAST_FINAL_PUSH_20260424.md` and Codex dispatch files.

Correction applied:

- `BROADCAST_FINAL_PUSH` supersedes the three-week rebuild queue and forbids new experiments until real D2D/C2C data arrives.
- The seed-789 training runs `CX-M7`, `CX-M8`, `CX-M9` were stopped immediately after this supersession was read. Partial checkpoints are preserved but are not part of the active evidence set.
- Current Codex task is now strictly `CODEX-CX-FRESH-EVAL-MSERIES`: pure evaluation only, no training.

Active execution:

- Sequential no-concurrency fresh eval runner: `cx_fresh_eval_mseries_20260424_162250`.
- Status JSON: `report_md/_gpt/json_gpt/cx_fresh_eval_mseries_status.json`.
- Current phase at launch: `CX-M1` fresh eval.
- Plot watcher: `cx_plot_after_fresh_20260424_162250`, waiting for fresh eval completion, then running `scripts/_gpt/plot_postfix_mseries.py`.

Generated from existing completed JSONs before the clean rerun:

- `report_md/_gpt/csv_gpt/cross_host_parity_mseries.csv`
- `report_md/_gpt/CODEX_CX_FRESH_EVAL_MSERIES_REPORT_20260424.md`

These files will be overwritten/refreshed after the clean no-concurrency M1-M6 eval finishes.
