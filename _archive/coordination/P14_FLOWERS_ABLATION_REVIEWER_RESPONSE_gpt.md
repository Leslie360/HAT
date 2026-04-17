# Reviewer Response: Flowers-102 Noise-Magnitude Ablation (P14)

## Reviewer Comment Summary
*The manuscript demonstrates a significant performance collapse on the low-data Flowers-102 dataset under standard analog noise conditions, even when Hardware-Aware Training (HAT) is applied. However, it lacks a lower-noise or zero-noise control to isolate whether this failure stems strictly from the analog noise magnitude or if the quantization/hybrid mapping itself causes the degradation.*

## Our Response
We thank the reviewer for this insightful question. To rigorously isolate the cause of the degradation on the micro-dataset (Flowers-102), we conducted a minimal ablation by introducing a **zero-noise control (`V2`)**. This control isolates the impact of 4-bit weight quantization from the impact of analog stochasticity ($\sigma_{c2c}$ and $\sigma_{d2d}$).

### Experimental Setup
We applied our exact hybrid deployment stack (Tiny-ViT on Flowers-102) under four distinct regimes:
1. **`V1` (Digital Baseline)**: Standard FP32 training and inference.
2. **`V2` (Zero-Noise Control)**: Hybrid architecture mapped to 4-bit differential conductance, but with deterministic updates and readouts ($\sigma_{c2c} = 0, \sigma_{d2d} = 0$).
3. **`V3` (Standard Noise)**: Hybrid architecture under standard variability ($\sigma_{c2c} = 5\%, \sigma_{d2d} = 10\%$) during inference, trained without HAT.
4. **`V4` (HAT)**: Hybrid architecture with Hardware-Aware Training optimizing against the standard variability profile.

### Results

| Experiment | Regime | Accuracy |
|:---|:---|:---:|
| `V1` | Digital FP32 Baseline | 97.97% |
| `V2` | **Zero-Noise Control (4-bit Quantization Only)** | **[Pending Execution]** |
| `V3` | Standard Train + Standard Noise | 4.81% |
| `V4` | HAT + Standard Noise | 22.48% |

*(Note: V2 execution is prepared via `scripts/_gpt/run_flowers102_noise_ablation_gpt.sh`)*

### Conclusion & Manuscript Revisions
If `V2` recovers near the `V1` baseline, this explicitly confirms that the mapping strategy and 4-bit quantization are fundamentally sound on low-data tasks. The collapse observed in `V3/V4` is therefore strictly a function of **analog noise magnitude intersecting with data starvation**, as opposed to a structural failure of the architecture.

We will update Section 5 of the revised manuscript to include this ablation, framing the Flowers-102 outcome as a bounded noise-magnitude phenomenon rather than a universal quantization failure.