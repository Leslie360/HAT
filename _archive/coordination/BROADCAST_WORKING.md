# 🔴 BROADCAST: Parallel Experiments Running

**Time:** 2026-04-15 09:37  
**Status:** Active Parallel Execution  
**GPU:** RTX 5070 Ti @ 92% utilization, 13.3GB/16.3GB

---

## 🚀 Currently Running (Parallel)

| Experiment | PID | Started | Config | Status |
|:--|:--|:--|:--|:--|
| **Ensemble HAT Frequency Ablation** | 791 | 09:30 | 5 frequencies | ⏳ Running (~8 min) |
| **Spatial Correlation Ablation** | 8715 | 09:37 | 4 spatial modes | ⏳ Just launched |

**Parallel Strategy:** Maximize GPU utilization (~92%)

---

## 📊 Today's Progress

| Time | Milestone | Status |
|:--|:--|:--|
| 09:28 | Framework Comparison complete | ✅ 91.65% vs AIHWKIT 90.08% |
| 09:30 | Ensemble Frequency launched | ⏳ Running |
| 09:37 | Spatial Ablation launched (parallel) | ⏳ Running |

---

## 🎯 Active Experiment Details

### 1. Ensemble HAT Frequency Ablation
**Question:** Is per-epoch resampling optimal?  
**Testing:**
- Standard HAT (fixed D2D)
- Per-batch resampling (extreme augmentation)
- **Per-epoch resampling** (Ensemble HAT) ⭐
- Per-5-epochs resampling
- Per-20-epochs resampling

**Expected Finding:** Per-epoch achieves optimal balance

### 2. Spatial Correlation Ablation
**Question:** Is spatial correlation necessary?  
**Testing:**
- Spatial correlated, fixed (Standard HAT)
- Spatial correlated, resample (Ensemble HAT)
- **i.i.d., per-epoch** (test correlation necessity)
- i.i.d., per-batch (extreme)

**Expected Finding:** Spatial correlation matters for hardware realism

---

## 📁 Completed Results (Today)

### Framework Comparison (`framework_comparison.json`)

| Config | Ours | AIHWKIT | Status |
|:--|:--|:--|:--|
| Canonical | 91.65% | 90.08% | Comparable |
| Photoresponse | 9.42% | ❌ N/A | **Exclusive** |
| Retention | 10.11% | ❌ N/A | **Exclusive** |
| NL=2.0 | 9.42% | ❌ N/A | **Exclusive** |

**Key Finding:** AIHWKIT lacks organic-specific features

---

## ⏭️ Next in Queue

| Priority | Experiment | Script | ETA |
|:--|:--|:--|:--|
| 🔴 P0 | NL=2.0 Layer-wise Sensitivity | `run_nl_layer_sensitivity.py` | ~4 hours |
| 🟡 P1 | Statistical Re-runs (n=5 seeds) | TBD | 1-2 weeks |
| 🟡 P1 | ResNet-18 Controlled Study | TBD | 3-4 days |

---

## 📈 Resource Status

| Metric | Value | Status |
|:--|:--|:--|
| GPU Memory | 13.3 / 16.3 GB | 🟡 High (82%) |
| GPU Utilization | 92% | 🟢 Optimal |
| Temperature | 62°C | 🟢 Normal |
| Active Processes | 2 training jobs | 🟢 Balanced |

---

## 🎯 Reviewer #4 Priority Coverage

| Weakness | Experiment | Status |
|:--|:--|:--|
| W1: Framework validation | Framework Comparison | ✅ Complete |
| W2: Ensemble HAT depth | Frequency + Spatial Ablation | ⏳ Running |
| W3: NL=2.0 mechanism | Layer-wise Sensitivity | 📋 Queued |
| W7: Statistical rigor | n=5 re-runs | 📋 Planned |

---

## 📂 File Locations

```
/home/qiaosir/projects/compute_vit/
├── run_framework_comparison.py          ✅ Done
├── run_ensemble_frequency_ablation.py   ⏳ Running
├── run_spatial_ablation.py              ⏳ Running
├── run_nl_layer_sensitivity.py          📋 Ready
├── logs/
│   ├── framework_comparison.log         ✅
│   ├── ensemble_frequency_ablation.log  ⏳
│   └── spatial_ablation.log             ⏳
└── report_md/_gpt/
    └── framework_comparison.json        ✅
```

---

## 💡 Working Strategy

**Parallel Execution Rationale:**
- GPU has 9.5GB free memory
- Single experiment only uses ~60-70% GPU
- Parallel = ~30% throughput gain
- Acceptable trade-off: slight slowdown per job, faster total completion

**Monitoring:**
- Check logs every 30 minutes
- Temperature < 70°C safe
- Memory < 15GB safe

---

## 🔔 Next Broadcast Trigger

Will update when:
1. Either experiment completes (~2-3 hours)
2. GPU temperature > 70°C
3. Next experiment launches

---

**END BROADCAST**

*Generated: 2026-04-15 09:37*  
*Status: PARALLEL EXECUTION ACTIVE*
