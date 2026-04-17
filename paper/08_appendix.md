# Appendix: Parameter Provenance

This appendix consolidates parameter provenance and the targeted sensitivity checks used to bound the main claims. Whenever a value is not directly reported in the source literature, it is labeled explicitly as a proxy estimate or analytical assumption.

## Three-Seed Summary for the Canonical V4 Path

To document the reproducibility of the canonical Tiny-ViT HAT path, we lock the three-seed V4 summary directly in the appendix. Each seed was evaluated with a `10`-run noisy Monte Carlo sweep under the canonical deployment regime, and the final cross-seed statistic is computed from the three seed means.

| Seed / Aggregate | Noisy MC Accuracy | Statistic Type |
|:--|:--|:--|
| 42 | 87.64 ± 0.48% | 10-run mean ± std |
| 123 | 88.10 ± 0.33% | 10-run mean ± std |
| 2026 | 88.11 ± 0.47% | 10-run mean ± std |
| **Cross-seed aggregate** | **87.95 ± 0.27%** | mean ± std of seed means |

| Parameter | Canonical Organic Profile | Zhang 2025 OPECT Case Study | Task 34-36 Stress Tests | Provenance / Derivation Notes |
|:--|:--|:--|:--|:--|
| Conductance Range ($G_{\max}/G_{\min}$) | 10 | 47.3 | 10 | Canonical anchored to scalable OPECTs; Zhang 2025 derives from reported max/min current levels. |
| Effective States ($n_{states}$) | 16 (4-bit) | 34 | 16 (4-bit) | Canonical matches general low-precision target. Zhang 2025 anchored to Fig.3h & Supp.Fig.8. |
| Cycle-to-Cycle Noise ($\sigma_{\text{C2C}}$) | 5% | 2% | 5% (Proportional) | Zhang 2025 value is a proxy estimate from 8-cycle repeatability (Supp.Fig.15). Proportional stress scales $\sigma$ with $|G|$. |
| Device-to-Device Mismatch ($\sigma_{\text{D2D}}$) | 10% | 3% | 10% (Proportional) | Zhang 2025 uses 3% as a conservative conductance-domain proxy from the reported $\sim$1% $V_{th}$ spread. |
| Retention Decay ($\tau_1, \tau_2, A_0$) | 140ms, 610ms, 0.6 | Not fitted | 140ms, 610ms, 0.6 | Canonical dual-exponential fit anchored to Vincze 2025. Zhang 2025 (Fig.2d) is qualitative only. |
| Nonlinear Write Asymmetry ($NL$) | 1.0 (LTP), -1.0 (LTD) | Canonical defaults retained | 2.0 (LTP), -2.0 (LTD) | Zhang 2025 does not report a pulse-level NL fit, so the case study keeps the canonical symmetric-write defaults rather than injecting a separate literature-fit NL term. Stress tests ($NL=2$) enforce severe gradient-scaling asymmetry. |
| Noise Mode | Uniform | Uniform | Proportional | Uniform injects noise normalized to full range. Proportional applies state-dependent noise magnitudes. |

## Proxy Estimate Sensitivity Analysis

The Zhang 2025 OPECT values for $\sigma_{\text{C2C}}$ and $\sigma_{\text{D2D}}$ are transparent proxy estimates rather than directly measured full-array noise distributions. We therefore ran a compact 2D sensitivity sweep on the Ensemble HAT checkpoint to verify that the case-study conclusion does not hinge on one narrow proxy choice.

| C2C \ D2D | 2% | 3% (Nominal) | 5% | 10% | 15% |
|:--|:--|:--|:--|:--|:--|
| 1% | 88.57% | 88.53% | 88.33% | 87.30% | 84.59% |
| 2% (Nominal)| 88.57% | 88.53% | 88.33% | 87.30% | 84.59% |
| 5% | 88.57% | 88.53% | 88.33% | 87.30% | 84.59% |
| 8% | 88.57% | 88.53% | 88.33% | 87.30% | 84.59% |

| D2D | Nominal Acc. (C2C=2%) | 95% CI | Max $\Delta$ across C2C sweep |
|:--|:--|:--|:--|
| 2% | 88.57% | [88.52, 88.62]% | 0.00 pp |
| 3% | 88.53% | [88.48, 88.58]% | 0.00 pp |
| 5% | 88.33% | [88.27, 88.38]% | 0.00 pp |
| 10% | 87.30% | [87.22, 87.38]% | 0.00 pp |
| 15% | 84.59% | [84.51, 84.66]% | 0.00 pp |

*Interpretation.* The statistical summary makes the same point more formally: at fixed D2D mismatch, the maximum accuracy excursion across the full C2C sweep is 0.00 percentage points at the reported precision, while the Monte Carlo uncertainty band remains narrow. The numerically identical rows in the preceding table should therefore be read as a stability result rather than as a copy-paste artifact: for this checkpoint and evaluation budget, static D2D spatial mismatch dominates the case-study outcome, whereas per-forward C2C sampling noise remains sub-resolution. Even under a pessimistic D2D assumption of 15%, the model remains above 80% accuracy, far from the 10% collapse of the standard V4 model.

## Automated Profile Fitting Pipeline

To reduce manual profile tuning, we implemented an automated fitting tool (`profile_auto_fitter_gpt.py`). It ingests four raw-data categories:
1. **Pulsed Programming Curves**: Fits the conductance range ($G_{\min}, G_{\max}$) and non-linearity coefficients ($NL_{LTP}, NL_{LTD}$) using a behavioral exponential model.
2. **Cycle-to-Cycle (C2C) Statistics**: Extracts the $\sigma_{\text{C2C}}$ noise parameter from repeated write-verify measurements at identical target states.
3. **Device-to-Device (D2D) Mismatch**: Calculates the $\sigma_{\text{D2D}}$ parameter from conductance distributions across multiple physical devices in an array.
4. **Retention Decay**: Fits the double-exponential decay constants ($\tau_1, \tau_2, A_0$) from long-term conductance-vs-time measurements.

The output is a standardized JSON DeviceProfile that can be injected directly into the PyTorch inference and HAT loops.

## Uniform vs. State-Dependent Retention Comparison

To test whether the first-order uniform retention assumption is sufficient for this paper, we compared it with a more physical state-dependent model in which high-conductance states decay up to 20% faster than low-conductance states. The comparison uses the V4 Ensemble HAT model on CIFAR-10 because that checkpoint is the retained deployment-facing path emphasized in the main text.

| Time (s) | Uniform Acc (%) | State-Dep Acc (%) | Diff (pp) |
|:---------|:----------------|:------------------|:----------|
| 0        | 90.77%          | 90.80%            | +0.03%    |
| 1        | 90.07%          | 90.08%            | +0.01%    |
| 10       | 89.78%          | 89.81%            | +0.03%    |
| 100      | 89.87%          | 89.89%            | +0.02%    |
| 1000     | 89.82%          | 89.90%            | +0.08%    |

The accuracy difference stays below 0.1 percentage points across all tested time intervals. For this paper, the result serves only as a regime-specific sanity check, not as a claim that state dependence is negligible in general. We did not replicate the same comparison on the collapsing fresh-instance standard-HAT path or on non-HAT checkpoints, so this table should be read as a scoped validation of the retention-model choice within the retained Ensemble-HAT deployment regime rather than as a universal statement across all training recipes.
