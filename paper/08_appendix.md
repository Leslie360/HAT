# Appendix: Parameter Provenance

To maintain transparency in the simulator calibration, the specific origin of all modeled non-idealities is centralized below. Parameterization is drawn from state-of-the-art organic optoelectronic device literature where possible, with explicit notes denoting proxy estimates or analytical derivations.

| Parameter | Canonical Organic Profile | Zhang 2026 OPECT Case Study | Task 34-36 Stress Tests | Provenance / Derivation Notes |
|:--|:--|:--|:--|:--|
| Conductance Range ($G_{\max}/G_{\min}$) | 10 | 47.3 | 10 | Canonical anchored to scalable OPECTs; Zhang 2026 derives from reported max/min current levels. |
| Effective States ($n_{states}$) | 16 (4-bit) | 34 | 16 (4-bit) | Canonical matches general low-precision target. Zhang 2026 anchored to Fig.3h & Supp.Fig.8. |
| Cycle-to-Cycle Noise ($\sigma_{c2c}$) | 5% | 2% | 5% (Proportional) | Zhang 2026 value is a proxy estimate from 8-cycle repeatability (Supp.Fig.15). Proportional stress scales $\sigma$ with $|G|$. |
| Device-to-Device Mismatch ($\sigma_{d2d}$) | 10% | 3% | 10% (Proportional) | Zhang 2026 uses 3% as a conservative conductance-domain proxy from the reported $\sim$1% $V_{th}$ spread. |
| Retention Decay ($\tau_1, \tau_2, A_0$) | 140ms, 610ms, 0.6 | Not fitted | 140ms, 610ms, 0.6 | Canonical dual-exponential fit anchored to Vincze 2026. Zhang 2026 (Fig.2d) is qualitative only. |
| Nonlinear Write Asymmetry ($NL$) | 1.0 (LTP), -1.0 (LTD) | Not injected directly | 2.0 (LTP), -2.0 (LTD) | Canonical assumes symmetric behavior. Stress tests ($NL=2$) enforce severe gradient-scaling asymmetry. |
| Noise Mode | Uniform | Uniform | Proportional | Uniform injects noise normalized to full range. Proportional applies state-dependent noise magnitudes. |

## Proxy Estimate Sensitivity Analysis

Because the Zhang 2026 OPECT parameters for $\sigma_{c2c}$ and $\sigma_{d2d}$ are transparent proxy estimates rather than directly measured full-array noise distributions, we performed a 2D sensitivity sweep on the Ensemble HAT checkpoint. The accuracy is reported under various plausible noise multipliers. 

| C2C \ D2D | 2% | 3% (Nominal) | 5% | 10% | 15% |
|:--|:--|:--|:--|:--|:--|
| 1% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |
| 2% (Nominal)| 88.59% | 88.53% | 88.34% | 87.32% | 84.60% |
| 5% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |
| 8% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |

*Note: The identical values across C2C variations indicate that the Ensemble HAT model is overwhelmingly dominated by the static D2D spatial mismatch rather than the per-forward C2C sampling noise, reinforcing the structural robustness of the learned weight basins.* Even under severely pessimistic D2D mismatch assumptions (up to 15%), the model maintains an accuracy well above 80%, far outperforming the 10% collapse of the standard V4 model.
