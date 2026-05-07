# Remote GPU Exploration — Wave 1 (2026-05-07)

**Executor:** Claude (HAT KV-cache robustness track)  
**GPUs:** 8x A100 (remote107)  
**Status:** Complete — 7 new models trained + 133 evals (0 failures)

---

## 1. Motivation

Two open questions after the baseline sweep (34 models, 578 evals):

1. **Scale effect on selective KV:** 410M last2 is optimal, but 1B last1 is optimal. Does "fewer layers = better" hold at 410M too?
2. **Training noise tolerance at 1B last1:** 1B last1 shows remarkably low degradation (clean=13.9, D2Ds=14.1, delta=0.2). How high can training sigma_d go before clean performance collapses?

---

## 2. Experiments

| Tag | Model | sigma_d | sigma_c | Layers | Seed | Description |
|:---|:---|---:|---:|:---|---:|:---|
| 410m_last1 | Pythia-410M | 0.02 | 0.01 | [23] | 42 | 410M last1 ablation |
| 410m_last4 | Pythia-410M | 0.02 | 0.01 | [20,21,22,23] | 42 | 410M last4 ablation |
| p1b_last1_e10 | Pythia-1B | 0.10 | 0.01 | [15] | 42 | 1B last1 sigma_d=0.10 |
| p1b_last1_e15 | Pythia-1B | 0.15 | 0.01 | [15] | 42 | 1B last1 sigma_d=0.15 |
| p1b_last1_e20 | Pythia-1B | 0.20 | 0.01 | [15] | 42 | 1B last1 sigma_d=0.20 |
| p1b_last1_d2d | Pythia-1B | 0.02 | 0.00 | [15] | 42 | 1B last1 D2D-only |
| p1b_last1_c2c | Pythia-1B | 0.00 | 0.01 | [15] | 42 | 1B last1 C2C-only |

Training: 500 steps each. Eval: 5 scenarios (clean, C2C, D2D_weak, D2D_strong, combined), with 1-5 seeds per scenario.

---

## 3. Results

### 3.1 Pythia-1B last1 extreme sigma (main finding)

| Training config | clean | C2C | D2Dw | D2Ds | comb | delta_clean->D2Ds |
|:---|---:|---:|---:|---:|---:|---:|
| Baseline sigma_d=0.02 | 13.9 | 13.9 | 13.9 | 14.1 | 13.9 | 0.2 |
| **sigma_d=0.10** | **14.0** | **14.0** | **14.0** | **14.1** | **14.0** | **0.1** |
| **sigma_d=0.15** | **14.1** | **14.1** | **14.1** | **14.2** | **14.1** | **0.1** |
| **sigma_d=0.20** | **14.3** | **14.3** | **14.3** | **14.3** | **14.3** | **0.0** |

**Key observation:** Training sigma_d can be pushed to 0.20 on 1B last1 with only +0.4 clean-PPL degradation. At sigma_d=0.20, clean and noisy performance completely converge (delta=0). This is the opposite of 410M behavior, where sigma_d=0.20 causes catastrophic clean degradation (clean=20.8, vs 18.1 baseline).

### 3.2 410M last1 ablation

| Config | clean | C2C | D2Dw | D2Ds | comb |
|:---|---:|---:|---:|---:|---:|
| last2 baseline | 18.1 | 18.4 | 18.6 | 19.0 | 18.6 |
| **last1** | **18.6** | **18.7** | **18.8** | **19.0** | **18.8** |
| last4 | 19.1 | 19.8 | 20.4 | 21.5 | 20.5 |

**Key observation:** At 410M, last1 is *worse* than last2 (clean 18.6 vs 18.1). The "fewer layers = better" rule does **not** generalize down to 410M. Last2 remains the 410M optimum.

### 3.3 1B last1 noise decomposition

| Config | clean | C2C | D2Dw | D2Ds | comb |
|:---|---:|---:|---:|---:|---:|
| D2D-only | 13.9 | 13.9 | 13.9 | 14.1 | 13.9 |
| C2C-only | 13.9 | 13.9 | 13.9 | 14.1 | 13.9 |
| Combined | 13.9 | 13.9 | 13.9 | 14.1 | 13.9 |

**Key observation:** D2D-only and C2C-only are individually sufficient at 1B last1. Both match the combined baseline exactly.

---

## 4. Narrative Implications

1. **Scale unlocks extreme noise tolerance.** 1B last1 can absorb sigma_d=0.20 training with negligible clean degradation. This suggests the performance ceiling is not structural at 1B scale — it is a limitation of the training recipe at smaller scales.

2. **Layer selectivity is scale-dependent.** "Minimize analog layers" is true at 1B (last1 > last2 > last4 > all), but false at 410M (last2 > last1). There may be a critical model size below which a minimum number of analog layers is required for the noise signal to propagate usefully.

3. **Noise type interchangeability at 1B.** D2D and C2C are fully substitutable when applied to a single layer at 1B scale. This simplifies deployment: either noise source can be used for HAT training.

---

## 5. Recommended Local Reproduction Target

**Priority 1:** Reproduce `p1b_last1_e20` locally. If confirmed, this is a strong paper claim: *"At 1B scale, HAT training with sigma_d=0.20 on a single KV layer yields clean/noisy PPL convergence with <3% clean degradation."*

**Priority 2:** Reproduce `410m_last1` locally to confirm the last1-last2 inversion at 410M.

---

## 6. Code Edits

None. All experiments used existing `p3_hat_train.py` and `p3_hat_eval.py` with standard arguments.

Script used: `overnight_extreme.py` (committed in session).
