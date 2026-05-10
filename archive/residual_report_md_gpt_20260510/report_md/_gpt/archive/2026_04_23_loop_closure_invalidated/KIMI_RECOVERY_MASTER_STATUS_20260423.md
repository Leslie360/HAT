<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# KIMI Recovery Master Status
**Date:** 2026-04-23
**Role:** Lead Recovery Owner

## What is invalid
- K4R (alpha=0.25) fresh-instance results (contaminated by dual-bugs).
- P1-C and P1-C2 results.
- All pre-`ab56c2d` K-series and J-series results involving severe NL.

## What survives
- V4 baseline (CIFAR-10, ~97%).
- The theoretical formulations of the surrogate and its first derivative (as ruled by Gemini).
- The project structure, evaluation scripts, and non-GPU artifacts.

## What is frozen
- The code in `analog_layers.py` after the atomic dual-bug fix (branch swap + second-order coefficient/sign).
- No new theoretical explorations until a clean rerun validates the physics.

## What the next minimal rerun must prove
- A clean parity anchor (`group=all`, no SO2) full rerun with 10x5 fresh eval to establish the absolute baseline of the corrected physical engine.
- A corrected SO2 comparison rerun to evaluate if the negative brake (with the correct coefficient and branch logic) stabilizes or shatters the loss landscape.
