# R10A Integration Template
**Date:** 2026-04-26
**Status:** PENDING — awaiting GPU training completion (seeds 456/789)
**Author:** Kimi

## Codex Protocol Correction — 2026-04-26 01:35 CST

Do **not** merge the historical `checkpoints/_gpt/multi_seed/V4_s42`,
`V4_s123`, and `V4_s2026` values into the R10A fresh-instance headline.
Those runs used the older batch-256 multi-seed source-accuracy protocol
(`best_acc` around 88--89%) and are not the same population as the canonical
batch-64 Ensemble-HAT fresh-instance protocol.

R10A should aggregate only protocol-matched canonical fresh-eval seeds:

| Seed | Checkpoint | Protocol role |
|------|------------|---------------|
| canonical / 123 | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | existing headline source (`fresh_instance_eval.json`) |
| 456 | `checkpoints/_ensemble/V4_hybrid_seed456/V4_hybrid_standard_noise_hat_best.pt` | new R10A seed |
| 789 | `checkpoints/_ensemble/V4_hybrid_seed789/V4_hybrid_standard_noise_hat_best.pt` | new R10A seed |

The old `87.95 ± 0.27%` value is a source-domain multi-seed sanity check, not
a replacement for the `86.37 ± 1.54%` fresh-instance headline. If a five-seed
fresh headline is desired, fresh-eval must first be run for the three
batch-256 checkpoints and reported as a separate protocol, not silently mixed
with the canonical batch-64 R10A seeds.

## R10A Experiment Design
- Train V4 Ensemble HAT on CIFAR-10 with seeds 456 and 789 (100 epochs, canonical NL=1.0)
- Fresh-instance eval: 10 instances × 5 MC runs per seed
- Expected output: `report_md/_gpt/json_gpt/r10a_seed456_fresh_eval.json` and `r10a_seed789_fresh_eval.json`

## Integration Checklist

### 1. Main-text headline numbers (REPLACE single-seed → multi-seed)

| Location | Current (single-seed 123) | Replacement formula |
|----------|--------------------------|---------------------|
| `00_abstract.tex` | `86.37$\pm$1.54\%` | `XX.XX$\pm$X.XX\%` (mean ± std across all fresh-instance means, all seeds) |
| `05_results.tex` §5.7 | `86.37$\pm$1.54\%` | Same as above |
| `05_results.tex` fig:ensemble-hat-concept caption | `86.37$\pm$1.54\%` | Same as above |
| `06_discussion.tex` §6.1 | `86.37$\pm$1.54\%` | Same as above |
| `07_conclusion.tex` | `86.37$\pm$1.54\%` | Same as above |
| `cover_letter.tex` | `86.37$\pm$1.54\%` | Same as above |

**Computation:** For each seed, compute mean of 10 fresh-instance means. Then compute mean ± std across all seeds (3 old + 2 new = 5 seeds).

### 2. Appendix table update

File: `08_appendix.tex` Table `tab:v4-three-seed-summary`

Already prepared with TBD rows for seeds 456 and 789.

After R10A completes:
1. Fill in seed 456 accuracy from `r10a_seed456_fresh_eval.json`
2. Fill in seed 789 accuracy from `r10a_seed789_fresh_eval.json`
3. Compute new 5-seed cross-seed aggregate
4. Remove `\textsuperscript{*}` footnote and `\footnotesize` note
5. Update caption: remove "R10A seeds 456 and 789 are pending GPU training completion"

### 3. Statistical phrasing

The current phrasing in 05_results.tex is:
> "overwhelming standard HAT ($p<10^{-15}$)"

This $p$-value is based on $n=10$ fresh instances for the single-seed 123 comparison. After R10A, we will have $n=30$ fresh instances (10 per seed × 3 seeds) or $n=50$ (10 per seed × 5 seeds). The $p$-value should be recomputed or the phrasing generalized to avoid pinning to a specific $n$.

**Recommended phrasing:**
> "overwhelming standard HAT ($p<10^{-15}$, one-sample $t$-test against chance baseline)"

This phrasing does not depend on $n$ because $p<10^{-15}$ is already extremely small.

### 4. Abstract tightening

If the multi-seed aggregate tightens the error bar (expected, due to averaging across seeds), the abstract should reflect the improved precision. Example:

> "Ensemble HAT recovers 87.1$\pm$0.3\% across five training seeds and 50 fresh hardware instances"

(Numbers are illustrative; use actual computed values.)

### 5. Files to recompile

- `main.tex`
- `supplementary_main.tex`

## Pre-computed reference data (seeds 42/123/2026)

| Seed | Noisy MC Accuracy | Fresh-instance eval |
|------|------------------|---------------------|
| 42 | 87.64 ± 0.48% | 10 fresh instances × 5 runs (existing) |
| 123 | 88.10 ± 0.33% | 10 fresh instances × 5 runs (existing, headline source) |
| 2026 | 88.11 ± 0.47% | 10 fresh instances × 5 runs (existing) |

Current 3-seed aggregate: **87.95 ± 0.27%**

---

## Codex Final R10A Result — 2026-04-26 03:05 CST

R10A is now complete. The earlier notes above about `87.95 ± 0.27%` are superseded for fresh-instance headline use; that value came from historical source-domain sanity runs and must not be used as the canonical fresh-instance aggregate.

Protocol-matched R10A population:

| Seed | Checkpoint | Source best | Fresh mean ± std |
|---|---|---:|---:|
| 123 / canonical | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | 91.94% | 86.37 ± 1.54% |
| 456 | `checkpoints/_ensemble/V4_hybrid_seed456/V4_hybrid_standard_noise_hat_best.pt` | 89.58% | 86.12 ± 0.72% |
| 789 | `checkpoints/_ensemble/V4_hybrid_seed789/V4_hybrid_standard_noise_hat_best.pt` | 90.66% | 85.99 ± 1.94% |

Final reporting numbers:

- Training-seed headline: **86.16 ± 0.19%** (mean ± sample std across the three seed means).
- Pooled fresh-instance distribution: **86.16 ± 1.52%** over 30 fresh-instance means.
- Original plotted checkpoint remains **86.37 ± 1.54%** and should be described only as the single-checkpoint plotted panel.

Artifact: `report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json`.

Codex patched the main manuscript, supplementary table, cover letter, and locked-number guard accordingly. Guard now includes `H4_R10A` and reports `17/17 passed`.
