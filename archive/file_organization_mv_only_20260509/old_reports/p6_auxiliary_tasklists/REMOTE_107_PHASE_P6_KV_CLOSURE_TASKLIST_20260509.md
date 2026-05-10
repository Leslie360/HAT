# Remote 107 Phase P6 KV-Cache Closure Tasklist

**Date:** 2026-05-09
**Owner:** Codex
**Purpose:** Make analog KV-cache Work-2 evidence decisive after corrected-noise rerun.

## Required Return

Return one Markdown report plus CSV/JSON tables:

`REMOTE_107_PHASE_P6_DELIVERY_YYYYMMDD.md`

## Required Top Section

```text
Verdict: PASS / PARTIAL / FAIL
Use: Work-2 separate paper / appendix pilot / reject
Critical bugs found: yes/no
Git SHA: ...
Environment: ...
Exact artifact paths: ...
```

## Required Sections

1. Corrected-noise rerun report:
   - old vs corrected absolute values;
   - trend-preservation verdict;
   - superseded claims list.
2. Core math/code packet:
   - KV quantization equation;
   - conductance mapping;
   - C2C injection point;
   - D2D injection point;
   - retention equation;
   - seed handling;
   - sliding-window PPL scoring;
   - train/test split proof.
3. HAT effectiveness matrix:
   - D2D, C2C, combined;
   - ctx=512 and ctx=1024 where available;
   - pre-HAT and post-HAT;
   - 3-seed stability.
4. Selective-layer route:
   - last1, last2, last4, all24;
   - pre/post HAT PPL;
   - terminal-layer deployment verdict.
5. Generalization matrix:
   - train D2D=0.04, eval D2D 0.00--0.05;
   - train C2C=0.01, eval C2C 0.00--0.02;
   - combined D2D+C2C if compute permits.
6. Decision:
   - separate paper / appendix pilot / reject;
   - minimal next experiment if not decisive.

## Kill Criteria

- Stop if base+patch PPL is far from clean baseline and unexplained.
- Stop if train/test split is ambiguous.
- Stop if sliding-window scoring double-counts or drops tokens.
- Do not transfer any result into Paper-1.
