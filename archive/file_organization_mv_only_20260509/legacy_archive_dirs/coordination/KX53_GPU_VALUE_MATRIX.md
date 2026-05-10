# KX53: GPU-Value Matrix

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Rank all potential GPU experiments by value/cost for three strategic goals

---

## Strategic Goals (Codex-defined)

1. **Current-paper strengthening** (for revision/response)
2. **Framework realism / measured-data readiness** (long-term asset)
3. **Second-paper discovery** (new contribution opportunities)

---

## GPU Experiment Value Matrix

### Tier 1: High ROI (Execute Immediately)

| Experiment | Goal | Reviewer Payoff | GPU Cost | Status |
|:-----------|:-----|:----------------|:---------|:-------|
| **GM-E1: per-forward i.i.d. D2D** | Current paper | Definitively distinguishes Ensemble HAT from domain randomization (addresses RC4) | ~2 GPU-hours | Ready to launch |
| **GM-E2: Pure-digital ADC sweep** | Current paper | Separates organic-CIM cliff from ViT quantization artifact (addresses RC5) | ~1 GPU-hour | Ready to launch |
| **Retention tau sweep (±50%)** | Current paper | Defends proxy-parameter robustness (addresses RC1) | ~3 GPU-hours | Ready to launch |

**Recommendation**: Launch all three in parallel if 4+ GPUs available; otherwise prioritize GM-E1.

---

### Tier 2: Medium ROI (Execute if GPU Idle)

| Experiment | Goal | Value | GPU Cost | Status |
|:-----------|:-----|:------|:---------|:-------|
| **NL scan (1.5, 1.8, 2.0, 2.5)** | Current paper | Shows gradual degradation not hard boundary | ~8 GPU-hours | Queue for idle time |
| **ImageNet-1K V1/V4 baseline** | Second paper | Enables high-impact venue targeting | ~40 GPU-hours | Queue for continuous run |
| **ConvNeXt Ensemble HAT** | Current paper | Cross-architecture validation | ~6 GPU-hours | Optional strengthening |

---

### Tier 3: Background/Continuous (Low Priority)

| Experiment | Goal | Value | GPU Cost | Status |
|:-----------|:-----|:------|:---------|:-------|
| **Measured-data profile fitting** | Framework | Auto-calibration pipeline validation | Variable | On-demand when data arrives |
| **Energy model Monte Carlo** | Framework | Statistical confidence bounds | ~2 GPU-hours | Background job |
| **Hyperparameter sensitivity** | Framework | Best-practice documentation | ~4 GPU-hours | Documentation purpose |

---

## Parallel Execution Strategy

### If 4+ GPUs Available
```
GPU 0-1: GM-E1 (i.i.d. D2D) - ~2 hours
GPU 2:   GM-E2 (ADC sweep) - ~1 hour  
GPU 3:   Retention tau sweep - ~3 hours
```

### If 2 GPUs Available
```
GPU 0: GM-E1 (priority) - ~2 hours
GPU 1: GM-E2 (parallel) - ~1 hour, then retention sweep
```

### If 1 GPU Available
```
Sequential: GM-E1 → GM-E2 → retention sweep → NL scan
```

---

## Value-by-Goal Analysis

### Goal 1: Current-Paper Strengthening

| Experiment | Addresses | Impact if Positive | Impact if Negative |
|:-----------|:----------|:-------------------|:-------------------|
| GM-E1 (i.i.d. D2D) | RC4: HAT vs domain randomization | Definitive novelty proof | Needs textual defense |
| GM-E2 (ADC digital) | RC5: 6-bit cliff causality | Causal clarity | Weakens cliff claim scope |
| Retention sweep | RC1: proxy robustness | Parameter confidence | Needs limitation scope |
| NL scan | NL boundary sharpness | Approximation narrative | Single-point caveat |

### Goal 2: Framework Realism

| Experiment | Enables | Long-term Value |
|:-----------|:--------|:----------------|
| Measured-data fitting | Auto-calibration pipeline | Community adoption |
| Energy model MC | Statistical rigor | Reviewer confidence |
| Multi-seed robustness | Reproducibility standards | Best practices |

### Goal 3: Second-Paper Discovery

| Experiment | Potential Contribution | Target Venue |
|:-----------|:-----------------------|:-------------|
| ImageNet-1K validation | Scale generalization | NC/ICML/NeurIPS |
| Cross-architecture Ensemble | Algorithm generality | IEEE TCAD/TPDS |
| Full-array measured study | Device-system closure | Nature Electronics |

---

## Decision Triggers

| Trigger | Action |
|:--------|:-------|
| Measured data arrives within 2 weeks | Pause Tier 2/3, focus on measured-profile validation |
| Major Revision received | Execute all Tier 1 immediately for response |
| GPU idle >24 hours | Launch Tier 2 (ImageNet or NL scan) |
| Second paper concept solidifies | Reallocate GPU to discovery experiments |

---

## Summary

**Immediate launch (today)**:
- GM-E1: i.i.d. D2D control (highest reviewer payoff)
- GM-E2: ADC digital sweep (quick win)

**Queue for idle time**:
- Retention tau sweep
- NL scan

**Background/continuous**:
- ImageNet preparation
- Framework robustness tests

**On-demand**:
- Measured-data integration (when data arrives)

---

**GPU Status**: `nvidia-smi` confirmed available. Ready to launch Tier 1 experiments.
