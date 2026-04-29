# R11D Fresh+Drift Combined Eval — Final Summary

**Date:** 2026-04-29
**Status:** COMPLETE. All 6 checkpoints evaluated (5 fresh instances × 3 MC repeats × 3 drift times).

---

## Per-Run Results

| run_id | bit | seed | t=0s | t=1h | t=1d |
|:---|:---|---:|---:|---:|---:|
| r11d_7_pcm_4bit_seed123 | 4-bit | 123 | 76.66% | 74.41% | 72.22% |
| r11d_7_pcm_4bit_seed456_clean | 4-bit | 456 | 77.05% | 73.78% | 72.34% |
| r11d_7_pcm_4bit_seed789 | 4-bit | 789 | 76.31% | 74.44% | 73.47% |
| r11d_5a_pcm_seed123 | 8-bit | 123 | 76.95% | 77.00% | 76.86% |
| r11d_5a_pcm_seed456 | 8-bit | 456 | 78.28% | 78.19% | 78.21% |
| r11d_5a_pcm_seed789 | 8-bit | 789 | 77.55% | 77.51% | 77.46% |

---

## 3-Seed Statistics

### 4-bit PCM
| Metric | Mean | Std |
|:---|---:|---:|
| Fresh+drift @ 0s | 76.67% | 0.37pp |
| Fresh+drift @ 1h | 74.21% | 0.38pp |
| Fresh+drift @ 1d | 72.68% | 0.69pp |
| **Drift drop (0s→1d)** | **3.99pp** | — |

### 8-bit PCM
| Metric | Mean | Std |
|:---|---:|---:|
| Fresh+drift @ 0s | 77.59% | 0.66pp |
| Fresh+drift @ 1h | 77.57% | 0.60pp |
| Fresh+drift @ 1d | 77.51% | 0.67pp |
| **Drift drop (0s→1d)** | **0.08pp** | — |

### 4-bit vs 8-bit Gap
| Comparison | Gap |
|:---|---:|
| Fresh (0s) | 0.92pp |
| Drift @ 1h | 3.36pp |
| Drift @ 1d | **4.83pp** |

---

## Consistency Check

Comparison with extended drift eval (single-instance, no fresh rebuild):

| Metric | Extended Drift | Fresh+Drift | Diff |
|:---|---:|---:|---:|
| 4-bit @ 0s | 76.64% | 76.67% | +0.03pp |
| 4-bit @ 1h | 74.04% | 74.21% | +0.17pp |
| 4-bit @ 1d | 72.64% | 72.68% | +0.04pp |
| 8-bit @ 0s | 77.61% | 77.59% | -0.02pp |
| 8-bit @ 1h | 77.49% | 77.57% | +0.08pp |
| 8-bit @ 1d | 77.57% | 77.51% | -0.06pp |

All differences < 0.2pp. Two eval pipelines are consistent.

---

## GPU Status

**Current:** GPU idle. No processes. 398MB/16GB used.

All eval tasks completed at 20:31. No further GPU load unless new tasks are launched.
