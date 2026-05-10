# 5. Results

## 5.1 The Failure of Pure Quantization and Algorithmic Rescue

We first establish the behavior of the tested AIHWKit IdealDevice quantization/noise baseline. At 8-bit precision the baseline remains stable, achieving 87.28 ± 0.13% fresh-instance accuracy; at 4-bit precision it collapses to 14.64 ± 0.11%. This demonstrates that standard fixed-instance hardware-aware training fails to generalize under fresh hardware instance shifts at extreme low precision.

To address this, we apply Ensemble Hardware-Aware Training (HAT). By resampling the device-to-device (D2D) variation patterns during the forward pass, Ensemble HAT rescues the tested 4-bit pure-quantization regime where the AIHWKit IdealDevice baseline collapses. The model recovers to 86.16 ± 0.19% fresh-instance accuracy, effectively closing the gap with the 8-bit baseline and demonstrating robust cross-instance transfer.

## 5.2 Realistic PCM Training and the Precision-Retention Frontier

While Ensemble HAT solves the algorithmic generalization problem in a pure-quantization context, realistic analog deployment must account for complex device physics, particularly conductance drift. We evaluate our approach using the `PCMPresetUnitCell` model in AIHWKit, which incorporates non-linear update physics, finite dynamic range, and time-dependent drift.

Under the tested PCM UnitCell simulation regime, the implicit noise and update characteristics enable 4-bit and 6-bit convergence where pure quantization baselines collapse. As shown in Table 1, training is viable across 4-bit, 6-bit, and 8-bit precisions. However, the results reveal a precision-retention deployment frontier for the tested PCM simulation regime.

**Table 1: PCM Precision Ladder and Deployment Frontier**

| Precision | Source Best Mean | Fresh-Instance Mean | 1-Day Drift Drop | Deployment Role |
| :--- | :--- | :--- | :--- | :--- |
| **8-bit PCM** | 77.64 ± 0.68% | 77.60 ± 0.64% | 0.04pp | Drift-flat reference |
| **6-bit PCM** | 77.88 ± 0.58% | 77.86 ± 0.56% | 0.10pp | Pareto midpoint |
| **4-bit PCM** | 76.71 ± 0.46% | 76.68 ± 0.37% | 4.01pp | Drift-limited |

*(Note: We found that canonical PCM precision-ladder comparisons require full-schedule training: a 6-bit seed that appeared to plateau under patience-based early stopping recovered late in the schedule, so all reported 6-bit PCM statistics use the matched full 100-epoch protocol.)*

## 5.3 Deployment Guidance

The precision ladder clearly separates the algorithmic challenge of cross-instance robustness from the device-level precision-retention tradeoff.

8-bit PCM serves as a highly stable reference, remaining effectively drift-flat over the tested 24-hour retention window. Conversely, while 4-bit PCM achieves significant memory compression and remains highly trainable (76.68 ± 0.37% fresh accuracy), it incurs a measurable time-dependent drift, dropping by ~4.01pp over one day.

Crucially, 6-bit is the best tested Pareto midpoint in our PCM UnitCell experiments. It maintains 8-bit-like drift stability (dropping only 0.10pp over one day) while achieving a fresh accuracy of 77.86 ± 0.56%, comparable to or slightly exceeding the 8-bit aggregate. Within the tested PCM UnitCell setting, 6-bit therefore provides the best observed balance between model compression and long-term inference reliability.

## 5.4 Future Directions

Extending the same hardware-aware training principles to memory-bound inference components such as analog KV-cache is an important future direction.
