# Remote 107 Phase P8 Corrected-Noise Report — Strict-Review Draft

**Date:** 2026-05-10
**Status:** DRAFT / candidate index only; not claim-bearing and not locked.

## Strict-review verdict

This file supersedes the earlier Gemini claim-lock text. The raw JSON results are useful, but the current local package does not satisfy the P8 evidence-lock requirements yet.

Do not cite these tables as Paper2 claims until the metadata and comparison gates below are closed.

## Why the prior claim-lock table was rejected

- The prior aggregation grouped runs only by broad labels such as `last1`, `last2`, and `all24`, which mixed distinct checkpoints and experiment conditions.
- Its own table contradicted its conclusion: several rows had standard deviations far above 0.1 PPL, yet the conclusion claimed `<0.1 PPL` variance.
- Raw JSON count inspected: 993 usable files; bad JSON files: 0.
- Files missing `d2d_seed`: 54.
- Required metadata missing from every inspected JSON: `commit` (993), `command` (993), `config` (993), `dataset` (993), `eval_protocol` (993), `checkpoint_sha256` (993).

## Candidate Fresh-D2D index

The companion TSV `paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv` is now grouped by checkpoint, exact analog-layer list, eval C2C, and eval D2D. It is an audit index, not a claim-bearing table. The per-file metadata audit is `paper2/results/METADATA_COMPLETENESS_107_20260510.tsv`.

| checkpoint | layers | eval C2C | eval D2D | n seeds | mean PPL | std PPL | min PPL | max PPL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `combined_layerall_v2_seed42` | `all24` | 0 | 0.02 | 5 | 25.985 | 0.165 | 25.731 | 26.182 |
| `combined_layerall_v2_seed42` | `all24` | 0 | 0.05 | 5 | 59.055 | 1.800 | 56.301 | 60.914 |
| `combined_layerall_v2_seed42` | `all24` | 0.01 | 0.02 | 5 | 27.032 | 0.134 | 26.805 | 27.144 |
| `410m_last1_v2_seed42` | `last1_24l` | 0 | 0.02 | 5 | 18.781 | 0.026 | 18.745 | 18.806 |
| `410m_last1_v2_seed42` | `last1_24l` | 0 | 0.05 | 5 | 18.963 | 0.039 | 18.918 | 19.000 |
| `410m_last1_v2_seed42` | `last1_24l` | 0.01 | 0.02 | 5 | 18.804 | 0.020 | 18.773 | 18.819 |
| `combined_layerlast1_v2_seed42` | `last1_24l` | 0 | 0.02 | 5 | 18.781 | 0.026 | 18.745 | 18.806 |
| `combined_layerlast1_v2_seed42` | `last1_24l` | 0 | 0.05 | 5 | 18.963 | 0.039 | 18.918 | 19.000 |
| `combined_layerlast1_v2_seed42` | `last1_24l` | 0.01 | 0.02 | 5 | 18.803 | 0.015 | 18.781 | 18.816 |
| `hat_d2d002_500_freshd2d_last1_seed42` | `last1_24l` | 0 | 0.02 | 5 | 18.420 | 0.019 | 18.399 | 18.446 |
| `hat_d2d002_500_freshd2d_last1_seed42` | `last1_24l` | 0 | 0.04 | 5 | 18.553 | 0.027 | 18.518 | 18.578 |
| `hat_d2d002_500_freshd2d_last1_seed42` | `last1_24l` | 0 | 0.05 | 5 | 18.601 | 0.030 | 18.559 | 18.629 |
| `combined_layerlast2_v2_seed42` | `last2_24l` | 0 | 0.02 | 5 | 18.594 | 0.016 | 18.575 | 18.610 |
| `combined_layerlast2_v2_seed42` | `last2_24l` | 0 | 0.05 | 5 | 19.018 | 0.028 | 18.973 | 19.042 |
| `combined_layerlast2_v2_seed42` | `last2_24l` | 0.01 | 0.02 | 5 | 18.640 | 0.013 | 18.628 | 18.659 |
| `hat_d2d002_500_freshd2d_last2_seed42` | `last2_24l` | 0 | 0.02 | 5 | 18.707 | 0.021 | 18.686 | 18.740 |
| `hat_d2d002_500_freshd2d_last2_seed42` | `last2_24l` | 0 | 0.04 | 5 | 19.068 | 0.039 | 19.033 | 19.127 |
| `hat_d2d002_500_freshd2d_last2_seed42` | `last2_24l` | 0 | 0.05 | 5 | 19.207 | 0.038 | 19.167 | 19.261 |
| `410m_last4_v2_seed42` | `last4_24l` | 0 | 0.02 | 5 | 20.402 | 0.078 | 20.287 | 20.488 |
| `410m_last4_v2_seed42` | `last4_24l` | 0 | 0.05 | 5 | 21.535 | 0.057 | 21.481 | 21.626 |
| `410m_last4_v2_seed42` | `last4_24l` | 0.01 | 0.02 | 5 | 20.517 | 0.064 | 20.416 | 20.573 |
| `combined_layerlast4_v2_seed42` | `last4_24l` | 0 | 0.02 | 5 | 20.402 | 0.078 | 20.287 | 20.488 |
| `combined_layerlast4_v2_seed42` | `last4_24l` | 0 | 0.05 | 5 | 21.535 | 0.057 | 21.481 | 21.626 |
| `combined_layerlast4_v2_seed42` | `last4_24l` | 0.01 | 0.02 | 5 | 20.522 | 0.060 | 20.435 | 20.583 |

## Gates still required before Paper2 claim use

1. Identify the exact corrected-noise code path and Git SHA used by the remote 107 run.
2. Attach exact training/eval commands, dataset split, context length, stride, batch size, analog-layer list, and seed semantics for every result row.
3. Add checkpoint paths plus hashes without copying checkpoints into Paper1 or GitHub payloads.
4. Produce the old-vs-corrected comparison table and mark whether the qualitative trend is preserved.
5. Re-run metadata completeness after the JSON sidecars are patched or a signed manifest is provided.

## Safe current use

Use this report only to plan the next Paper2/107 audit and drafting tasks. Do not promote it into Paper1 source-data paths, and do not describe the 107 evidence as locked.
