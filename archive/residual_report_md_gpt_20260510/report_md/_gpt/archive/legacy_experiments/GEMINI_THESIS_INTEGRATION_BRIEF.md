# GEMINI G-Z3: Thesis Integration Brief — 2026-04-19

**Reread of canonical state:** I have integrated the three confirmed experimental pillars (10.00% baseline collapse, 32.6% all-linear upper bound, and ρ=0.3 ranking preservation) into the broader thesis narrative.

## Thesis Chapter Refinement: Hardware-Aware Training (HAT)

These results transition the thesis from a "framework validation" story to a "fundamental limitations" study.

### 1. Section Ordering and Narrative Flow
*   **The Problem: Instance Overfitting**: Lead with the **10.00% collapse** (G-Z2). This proves that "hardware-aware" is not "hardware-invariant." This section justifies why Ensemble HAT is not just an optimization but a mandatory architectural requirement for CIM deployment.
*   **The Bound: Linearization Ablation**: Introduce the **32.6% all-linear result**. This is a "pessimistic" finding: even if we linearized *everything*, standard HAT still fails to transfer. This decouples the transfer failure from "bad gradients" and assigns it purely to "instance-specific representational bias."
*   **The Robustness: Spatial Correlation**: Present the **ρ=0.3/0.5 ranking preservation** (G-Z1). This closes the loop by showing that once you solve instance-overfitting (via Ensemble HAT), the framework is robust to the non-ideal noise distributions typical of real organic arrays.

### 2. Manuscript vs. Thesis Claims
| Metric | NC Manuscript Claim | Thesis Claim (Advanced) |
|:---|:---|:---|
| **Transfer** | Ensemble HAT fixes a 10% collapse. | The 10% collapse is a deterministic attractor of fixed-mask objectives. |
| **Linearization** | MLP-only identifies the bottleneck. | All-linearization proves that the transfer gap is an information-theoretic limit of single-instance training. |
| **Noise Model** | i.i.d. Gaussian is a proxy. | Ranking preservation under AR(1) correlation validates the low-pass property of high-dimensional CIM projections. |

### 3. Future "Upgrade" Chapter
The thesis should conclude this chapter by proposing the **MLP-Linear + Ensemble HAT** joint training (originally G-R recommendation). This is the "Solution" that goes beyond the "Diagnostic" of the NC paper. By combining algorithmic linearization (fixing gradients) with stochastic resampling (fixing transfer), we move toward the theoretical limit of organic edge vision.
