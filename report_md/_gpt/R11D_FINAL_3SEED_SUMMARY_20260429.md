# R11D PCM Multi-Seed — Final 3-Seed Summary

**Date:** 2026-04-29
**Status:** COMPLETE. All 6 runs (3 seeds x 2 configs) trained, fresh-evaluated, drift-evaluated.

---

## Complete Results Table

| run_id | seed | bit | best_test | final_test | fresh_mean | fresh_std | drift_0s | drift_1h | drift_24h |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|
| r11d_7_pcm_4bit_seed123 | 123 | 4-bit | 76.74% | 76.33% | 76.6512% | 0.0427% | 76.68% | 74.74% | 72.28% |
| r11d_7_pcm_4bit_seed456_clean | 456 | 4-bit | 77.15% | 76.86% | 77.0724% | 0.0562% | 77.02% | 73.09% | 72.18% |
| r11d_7_pcm_4bit_seed789 | 789 | 4-bit | 76.23% | 76.23% | 76.3300% | 0.0400% | 76.23% | 74.29% | 73.45% |
| r11d_5a_pcm_seed123 | 123 | 8-bit | 77.00% | 77.00% | 76.9974% | 0.0454% | 76.86% | 77.07% | 77.01% |
| r11d_5a_pcm_seed456 | 456 | 8-bit | 78.36% | 77.98% | 78.2690% | 0.0471% | 78.46% | 78.07% | 78.22% |
| r11d_5a_pcm_seed789 | 789 | 8-bit | 77.56% | 77.35% | 77.5200% | 0.0400% | 77.52% | 77.33% | 77.49% |

---

## 3-Seed Statistics

### 4-bit PCM
| Metric | Mean | Std |
|:---|---:|---:|
| Source best | 76.71% | 0.46pp |
| Fresh eval | 76.6845% | 0.37pp |
| Drift @ 0s | 76.64% | 0.40pp |
| Drift @ 1h | 74.04% | 0.85pp |
| Drift @ 24h | 72.64% | 0.71pp |
| **Drift drop (0s->24h)** | **4.01pp** | — |

### 8-bit PCM
| Metric | Mean | Std |
|:---|---:|---:|
| Source best | 77.64% | 0.68pp |
| Fresh eval | 77.5955% | 0.64pp |
| Drift @ 0s | 77.61% | 0.80pp |
| Drift @ 1h | 77.49% | 0.52pp |
| Drift @ 24h | 77.57% | 0.61pp |
| **Drift drop (0s->24h)** | **0.04pp** | — |

### 4-bit vs 8-bit Gap
| Comparison | Gap |
|:---|---:|
| Source best | 0.93pp |
| Fresh eval | 0.91pp |
| Drift @ 24h | **4.94pp** |

---

## Narrative Verdict

**STRONG NARRATIVE CONFIRMED**

> "PCM device physics enable 4-bit training that pure quantization cannot."

**Evidence:**
- 4-bit PCM 3-seed mean = 76.71%, std = 0.46pp — cross-seed stable
- 8-bit PCM 3-seed mean = 77.64%, std = 0.68pp — cross-seed stable
- 4-bit vs 8-bit fresh gap only 0.91pp — minimal precision penalty
- 4-bit pure baseline all collapse (~10%) — catastrophic failure

**Key Caveat (must discuss in paper):**
- 4-bit drift @ 24h = -4.01pp, 8-bit drift = -0.04pp
- Precision-drift trade-off is the main cost of 4-bit PCM
- Paper must explicitly quantify and discuss this trade-off

---

## Invalid/Excluded Data

| Run | Reason |
|:---|:---|
| r11d_7_pcm_4bit_seed456 partial | Killed @ epoch 46, pipefail bug, no training_history.json |
| T1-3 PCMPresetDevice (first) | Killed @ epoch 12, Bug #3 silent fallback |
| T1-3 PCMPresetDevice (second) | Path bug, files saved to nested directory |
| T1-4 Oracle | Provenance caveat (extended script), diagnostic only |

---

*All corrected checkpoints verified: PCMPresetUnitCell + AnalogSGD + canonical script SHA.*
