# GM-X34: Optional Experiment Gate Memo

> **Strategy Alignment:** Following 2026-04-13 "Strategy Reset". GPU time is now an open resource for defense and discovery.

## 1. Candidate Experiment Ranking

| Experiment | Reviewer Payoff | Scientific Payoff | Implementation Risk | Depends on Data? | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ensemble HAT Ablation** | **Extreme**. Differentiates algorithm from generic noise. | High | Low | No | **DONE** |
| **Pure-Digital ADC Scan** | **High**. Proves 6-bit cliff is a system bottleneck. | High | Low | No | **DONE** |
| **Retention Sensitivity** | **High**. Defends against "proxy parameter bias". | Med | Low | No | **RUNNING** |
| **Compound Stress Test** | **High**. Shows final robustness under "all non-idealities". | High | Low | No | **QUEUED** |
| **Lightweight NL Scan** | **Med**. Softens the NL=2.0 boundary. | High | Med | **Yes (Best)** | **WAIT** |

## 2. Rationale for Active Set

### ✅ Approved: Ensemble HAT vs i.i.d. D2D (GM-E1)
Proves that resampling the *static* mismatch each epoch is fundamentally required for fresh-instance transfer. Generic i.i.d. noise does not address spatial correlation.

### ✅ Approved: Pure-Digital ADC (GM-E2)
Isolates digital quantization from analog stochasticity. Confirms the 6-bit cliff is shared across regimes.

### ✅ Approved: Retention/Compound (GM-E3/E5)
Uses remaining GPU time to "over-engineer" the supplementary data, making the paper bulletproof against the "circular simulation" criticism.

## 3. Wait-List

- **NL Scan**: Better to wait for the PhD's actual $NL$ parameters from measured devices to ensure the sweep is centered on realistic physics.
