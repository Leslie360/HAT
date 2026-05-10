# CX-K2: Bimodality Test Result

**Date:** 2026-04-23
**Data:** `cx_k2_fresh_eval.json` (N=30 fresh instances)
**Test:** Hartigan's dip test (`diptest` package)

## Result

| Statistic | Value |
|-----------|-------|
| Dip statistic | 0.0415 |
| p-value | **0.9796** |
| Bimodal (p < 0.05)? | **NO** |

## Interpretation

The N=30 distribution is **not statistically bimodal**. The p-value of 0.98 strongly supports the unimodal null hypothesis.

**Visual clustering vs. statistical significance:**
- GMM-2 fit finds two components: mean=44.4 (weight 0.62) and mean=30.1 (weight 0.38)
- Histogram shows visual separation between low (<35%) and mid-high (>40%) instances
- However, the dip test indicates this separation is **not significant at N=30**

**Likely explanation:** The apparent "two clusters" in the N=10 J1d data (41.53±8.87%) was a **small-sample artifact**. With N=30, the distribution smooths into a single broad mode centered at ~39%.

## Decision

**Recommend Branch B: Structural-Limit Narrative**

The ~30% fresh-instance ceiling under severe NL remains the correct claim. The bimodal narrative, while visually appealing in small samples, is not supported by the extended N=30 dataset.

## Implications for Paper-1

- Revert to original "~30% structural ceiling" language
- Remove bimodal figure spec (G-SLIM-2)
- Keep K-SLIM-1 (中文 Ch.5) but reframe from "双模态吸引子" to "结构性极限"
- K-SLIM-2 diff: use Branch B (minimal changes to frozen files)

## Files

- `report_md/_gpt/json_gpt/cx_k2_bimodality_test.json`
