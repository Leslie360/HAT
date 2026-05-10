<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# KIMI Minimal Rerun Requirements
**Date:** 2026-04-23
**Scope:** Gating spec for the canonical anchor.

## Exact artifact set
- 1x Full training run log (`100 epochs`).
- 1x Training best/final JSON.
- 1x Fresh-instance evaluation JSON (`10x5` runs).

## Exact metrics that must be returned
- Training best accuracy.
- Training final accuracy.
- Fresh-instance mean accuracy.
- Fresh-instance standard deviation.
- Fresh-instance min/max range.

## Exact provenance fields
- Commit hash of the atomic dual-bug fix.
- Command-line arguments used for launch.
- Confirming tags: `group=all`, `delta_g_eff=0.0` (for first-order anchor) or corrected `alpha` (for SO2).

## What cannot be omitted
- The 10x5 fresh-instance evaluation. A same-instance train best is meaningless under the current physical regime.
