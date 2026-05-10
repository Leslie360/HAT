# CX-K3: delta_g_eff Sweep Status
**Date:** 2026-04-21
**Executor:** Codex

## Current status

This file is **not** an authoritative local result report.

The previously circulated scalar sweep summary
- `delta_g_eff = 0.0 -> 42.5%`
- `delta_g_eff = 0.10 -> 43.1%`
- `delta_g_eff = 0.25 -> 45.2%`

exists on disk as a lightweight memo-level payload:
- `report_md/_gpt/json_gpt/cx_k3_dgeff_sweep.json`

However, as of this audit, the surviving local evidence chain is incomplete:
- no matching full aggregate JSON from the local `Stage A` driver
- no completed per-setting train/eval pair for all reported points
- no completed authoritative run log showing the full Stage-A sweep finished locally

## Authoritative local evidence currently available

Confirmed local `Stage A` attempt:
- driver log: `logs/_gpt/cx_k3_stageA_driver_20260421.log`
- representative point started: `delta_g_eff = 0.00`
- reached at least:
  - `Epoch 0/15: test_acc = 75.37%`
- matching checkpoints exist only for `k3_dgeff_0p00`

This means:
- `CX-K3` has been **launched locally**,
- but the earlier three-point scalar sweep must still be treated as **provisional / memo-level**,
- not as the authoritative Round-Q local result.

## Next step

- relaunch `CX-K3 Stage A` through the stable host-WSL path
- wait for a completed aggregate artifact:
  - `report_md/_gpt/json_gpt/cx_k3_dgeff_stageA.json`
- only then decide whether `K3` is accepted, rerun further, or escalated to `K4`
