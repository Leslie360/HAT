# Physical Noise Injection Sweep Results

## Experiment Design

Two-path comparison:
- **Compensated**: X → InverseGamma(γ) → PhotocurrentSim → Network
- **Raw**: X → PhotocurrentSim → Network (control)

**Clean baseline (no physical preprocessing):** 10.00%

## Delta Accuracy (Compensated − Raw)

Positive values = compensation helps.


### Shot noise: ON

| γ_phys \ I_dark | 100pA | 1nA |
|:---:|:---:|:---:|
| 0.7 | +0.01% | +0.01% |
| 1.0 | +0.00% | +0.00% |

## Full Results

| Mode | γ_phys | I_dark | Shot | Accuracy |
|:-----|:------:|:------:|:----:|:--------:|
| clean | — | — | — | 10.00% |
| compensated | 0.7 | 100pA | on | 10.01% |
| raw | 0.7 | 100pA | on | 10.00% |
| compensated | 0.7 | 1nA | on | 10.01% |
| raw | 0.7 | 1nA | on | 10.00% |
| compensated | 1.0 | 100pA | on | 10.01% |
| raw | 1.0 | 100pA | on | 10.01% |
| compensated | 1.0 | 1nA | on | 10.01% |
| raw | 1.0 | 1nA | on | 10.01% |
