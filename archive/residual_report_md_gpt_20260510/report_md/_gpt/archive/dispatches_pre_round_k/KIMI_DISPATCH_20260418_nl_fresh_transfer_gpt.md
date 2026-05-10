<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Dispatch — NL Fresh-Instance Interpretation (2026-04-18)

## Objective

Update the severe-NL interpretation using the **new fresh-instance results**, not just the source-domain training numbers.

## Locked facts to use

### Source-domain lanes

- baseline severe `NL=2.0`: `27.72 ± 0.82%`
- `MLP-only` linear compensation: best `87.79%`, final `86.22%`
- `QKV-only` linear compensation: best `18.72%`, final `10.15%`
- `all-linear` compensation: best `87.49%`, final `84.81%`

### Fresh-instance lanes

- canonical fixed-HAT: `10.00 ± 0.00%`
- canonical epoch-resampled Ensemble HAT: `86.33 ± 1.61%`
- canonical batch-resampled control: `89.48 ± 0.36%`
- `MLP-only` severe-NL mitigation: `32.12 ± 7.72%`
- `QKV-only` severe-NL mitigation: `10.01 ± 0.10%`
- `all-linear` severe-NL mitigation: still pending; do not assume a number

## What I need from you

Produce one file:

- `report_md/_gpt/KIMI_NL_FRESH_TRANSFER_INTERPRETATION_20260418.md`

with 3 short sections:

1. **Mechanistic interpretation**
   - Explain why `MLP-only` can strongly rescue source-domain accuracy but still fail to generalize across fresh D2D draws.
   - Explain why `QKV-only` collapse strengthens the `MLP-localized` hypothesis.

2. **Editorial implication**
   - Should this remain a supplementary mechanistic ablation rather than a main-text headline?
   - Give a direct yes/no answer and a 4–6 sentence justification.

3. **Drop-in prose**
   - Give one paragraph for supplementary results/discussion.
   - Give one paragraph for reviewer response.
   - Both must be conservative and must not claim deployment-stable recovery unless the data actually support it.

## Hard constraints

- Do **not** invent literature baselines.
- Do **not** assume `all-linear` fresh-instance succeeded.
- Do **not** rewrite the manuscript around a new contribution.
- Treat this as an interpretation task, not a new experiment proposal.
