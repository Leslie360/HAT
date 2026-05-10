
---
## [2026-04-23] CX-K2 Bimodality Test Complete — CODEX

| Field | Value |
|-------|-------|
| Task | CX-K2 Hartigan's Dip Test |
| N | 30 |
| Dip statistic | 0.041493 |
| p-value | **0.979643** |
| Bimodal (α=0.05) | **NO** |
| GMM means | 30.12%, 44.37% (canonical, from analyze_cx_k2_bimodality.py) |
| KDE mode | 39.7% |
| Recommendation | **Branch B (structural limit fallback)** |
| Output JSON | `report_md/_gpt/json_gpt/cx_k2_bimodality_test.json` |
| Output memo | `report_md/_gpt/CODEX_CX_K2_BIMODALITY_TEST_20260423.md` |
| Script | `scripts/_gpt/run_hartigans_dip.py` |

**Note:** Despite visual suggestions of two clusters, Hartigan's dip test does not reject unimodality (p ≈ 0.98). The distribution is statistically consistent with a broad unimodal density centered near ~39%. Work 1 closure should proceed via Branch B unless additional evidence overrides. **Erratum:** Earlier intercom entry listed stale GMM means (32.1%, 45.9%) from run_hartigans_dip.py; canonical values are 30.12%/44.37% from analyze_cx_k2_bimodality.py. GMM is diagnostic only; the branch decision rests on Hartigan p=0.9796.
