# Remote 105 Phase P6 Closure Tasklist

**Date:** 2026-05-09
**Owner:** Codex
**Purpose:** Close cross-architecture proportional HAT validation after server recovery.

## Required Return

Return one Markdown report plus CSV/JSON tables:

`REMOTE_105_PHASE_P6_DELIVERY_YYYYMMDD.md`

## Required Top Section

```text
Verdict: PASS / PARTIAL / FAIL
Use: supplement-candidate / future-only / exclude
Critical bugs found: yes/no
Git SHA: ...
Environment: ...
Exact artifact paths: ...
```

## Experiments / Tables

Complete seed789 where missing for:

- `deit`: digital, standard, ensemble, proportional
- `vit`: digital, standard, ensemble, proportional

For every row include:

- architecture
- HAT mode
- seed
- source definition = best epoch test accuracy
- source/best test accuracy
- fresh mean
- fresh std
- source-fresh delta
- checkpoint path
- exact train command
- exact fresh-eval command
- env packet

## Required Analysis

1. Same-architecture P vs D by seed.
2. Three-seed mean/std where complete.
3. Noise-off ablation only if same architecture and same seed.
4. Verdict:
   - strong validation if same-arch multi-seed P > D and fresh remains stable;
   - weak validation if mixed or inconsistent;
   - inconclusive if seed789 still missing;
   - exclude if source metric or split is wrong.

## Kill Criteria

- Do not compare across architecture.
- Do not use train accuracy as source.
- Do not fill missing rows by inference.
- Mark server-crash gaps explicitly.
