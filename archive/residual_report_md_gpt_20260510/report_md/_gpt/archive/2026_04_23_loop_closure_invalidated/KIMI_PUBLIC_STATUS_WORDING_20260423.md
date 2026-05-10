<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# KIMI Public Status Wording
**Date:** 2026-04-23

## User-facing one paragraph summary
We have identified and resolved two fundamental bugs in the physical simulation engine (a branch-swap in update difficulty and a redundant coefficient in the Taylor expansion). These issues inverted the simulated hardware physics, invalidating our recent experimental results including K4R. We have executed an atomic fix to the codebase and are now preparing a minimal, clean rerun to establish the true baseline performance under corrected physics.

## Remote-facing one paragraph hold message
Please pause all active GPU runs and parity checks. We have discovered critical theoretical bugs in the `analog_layers.py` implementation that invalidate the current baseline. Do not sync code or launch new experiments until we push the atomic fix and provide a new, verified local parity anchor.

## Internal one paragraph "why nothing current is canonical"
All experiments prior to the dual-bug fix (including K4R, P1-C, and earlier 86% results) were executed on a physically flawed engine that either swapped LTP/LTD difficulty or artificially inflated second-order penalties. Because the optimization landscape was fundamentally distorted, no absolute metrics from these runs can be cited as canonical evidence of the hardware's true limitations or capabilities.
