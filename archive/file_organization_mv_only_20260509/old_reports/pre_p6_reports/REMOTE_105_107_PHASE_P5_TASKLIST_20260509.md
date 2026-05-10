# Remote 105/107 Phase P5 Tasklist

**Date:** 2026-05-09
**Owner:** Codex
**Use:** copy to GitHub or server agents as the current remote task list.

## Global Rules

1. Return Markdown/CSV/JSON only; do not return checkpoints unless explicitly requested.
2. Every table must include seed, command, git SHA, metric definition, and split.
3. Separate Paper-1 validation from Work-2 KV-cache.
4. If a bug is found, label old results superseded before giving corrected numbers.
5. Do not alter Paper-1 final claims from remote results without Codex acceptance.

## Server 105 — Cross-Architecture / Multi-Dataset Validation

### Objective
Validate whether proportional HAT generalizes across architecture and seed. This is candidate supplementary/future evidence, not a Paper-1 main claim.

### Required Results

Return a complete table for:

- architectures: `deit`, `vit`
- modes: `digital`, `standard`, `ensemble`, `proportional`
- seeds: all completed seeds, including seed789 when server recovers

Required columns:

- architecture
- HAT mode
- seed
- source definition (`best_epoch_test_acc`, not train accuracy)
- source/best test accuracy
- fresh mean
- fresh std
- fresh-source delta
- checkpoint path
- exact command
- environment packet

### Required Analyses

1. Same-architecture proportional-vs-digital by seed.
2. Three-seed mean/std where complete.
3. Noise-off ablation interpretation only when same architecture and same seed are controlled.
4. Verdict: strong validation / weak validation / inconclusive.
5. Placement recommendation: supplement candidate / future-only / exclude.

### Kill Criteria

- Reject any proportional advantage claim if it mixes architecture or seed.
- Reject any row where source means train accuracy instead of best test accuracy.
- Mark missing seed789 rows as missing; do not interpolate.

## Server 107 — Analog KV-Cache Work-2

### Objective
Build a corrected and reproducible Work-2 evidence base for analog KV-cache HAT.

### Required Results

1. Corrected-noise rerun report after the noise-algorithm bug.
2. Old-vs-corrected comparison table:
   - which absolute values shifted;
   - which trends survived;
   - which claims are superseded.
3. Core math/code reproducibility packet:
   - KV quantization equation;
   - conductance mapping;
   - C2C injection point;
   - D2D injection point;
   - retention equation;
   - seed handling;
   - exact sliding-window PPL definition;
   - train/test split proof.
4. HAT effectiveness matrix:
   - pre/post HAT PPL for D2D, C2C, and combined noise;
   - 3-seed stability for key settings;
   - ctx=512 vs ctx=1024 where available.
5. Selective-layer evidence:
   - last1, last2, last4, all24;
   - pre-HAT and post-HAT PPL;
   - one verdict on terminal-layer analog KV as a practical route.
6. Generalization evidence:
   - train D2D=0.04, eval D2D 0.00--0.05;
   - train C2C=0.01, eval C2C 0.00--0.02;
   - combined D2D+C2C if compute permits.

### Kill Criteria

- Stop if base+patch PPL is far from clean baseline and unexplained.
- Stop if train/test split is ambiguous.
- Stop if sliding-window scoring double-counts or omits tokens.
- Do not claim Work-2 paper readiness unless corrected-noise results preserve the qualitative story.

## Return Format

Each server returns one Markdown report plus optional CSV/JSON tables:

- `REMOTE_105_DELIVERY_YYYYMMDD.md`
- `REMOTE_107_DELIVERY_YYYYMMDD.md`

Top section must be:

```text
Verdict: PASS / PARTIAL / FAIL
Use: supplement-candidate / future-only / Work-2 / exclude
Critical bugs found: yes/no
Exact artifact paths: ...
Git SHA: ...
Environment: ...
```
