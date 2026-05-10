# GEMINI E6 THESIS CHAPTER OUTLINE — 2026-04-18

## 1. Chapter Title & Motivation
**Title:** Synergistic Mitigation of Optoelectronic Inference Bottlenecks: Joint Optimization of Read-Side and Write-Side Non-idealities

**Motivation:**
The transition from idealized digital models to physical organic optoelectronic arrays exposes two distinct but potentially interacting failure modes: sublinear photoresponse at the read-side optical frontend ($\gamma_{\text{phys}}$) and severe asymmetric non-linearity during write-side updates (NL). While our previous investigations isolated these mechanisms—demonstrating inverse-gamma compensation for frontend fidelity and MLP-localized linear scaling for write-side recovery—it remains unknown whether these read and write mitigations interact synergistically. This chapter investigates the $\gamma \times \text{NL}$ joint parameter space, evaluating whether frontend compensation provides an implicit regularizing effect that alleviates write-side non-linearity, or if the two mitigations operate orthogonally and must be explicitly co-optimized for successful edge-vision deployment.

## 2. Hypothesis Grid
The joint sweep covers $\gamma_{\text{phys}} \in \{1.0, 2.0\}$ and $\text{NL (LTP/LTD)} \in \{0, 1.0, 1.5, 2.0\}$, evaluating 16 combinations of mitigation states (No Compensation / Inverse-Gamma Only / MLP-Linear Mitigation Only / Both) on a HAT-trained Tiny-ViT (CIFAR-10).

| $\gamma_{\text{phys}}$ | NL (LTP/LTD) | Mitigation Applied | Predicted Outcome (Accuracy) | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | 0 (Linear) | None | ~92-95% (Baseline) | Idealized linear baseline. |
| 1.0 | 0 (Linear) | Both | ~92-95% | Mitigations have minimal impact on linear baseline. |
| 1.0 | 2.0 | None | ~27% (Severe Collapse) | Pure write-side non-linearity collapse. |
| 1.0 | 2.0 | MLP-Linear Only | ~87% (Recovered) | Targeted write-side mitigation succeeds. |
| 2.0 | 0 (Linear) | None | ~84% (Frontend Degraded) | Pure read-side sublinear degradation. |
| 2.0 | 0 (Linear) | Inv-Gamma Only | ~89-90% (Recovered) | Targeted read-side mitigation succeeds. |
| 2.0 | 2.0 | None | < 20% (Compounded Failure) | Both failure modes compound destructively. |
| 2.0 | 2.0 | Inv-Gamma Only | ~27-30% | Read-side mitigation alone cannot save write-side collapse. |
| 2.0 | 2.0 | MLP-Linear Only | ~80-84% | Write-side recovered, but limited by uncompensated frontend. |
| 2.0 | 2.0 | Both | ~87-89% (Joint Recovery) | Full mitigation restores near-baseline performance. |
*(Note: Intermediate cells for NL=1.0 and 1.5 follow interpolated trajectories to map the severity onset curve.)*

## 3. Analysis Plan
- **Performance Evaluation:** Plot iso-accuracy contour maps across the $\gamma \times \text{NL}$ grid for each of the four mitigation configurations.
- **Statistical Significance:** Conduct two-way ANOVA to test for significant interaction terms between $\gamma_{\text{phys}}$ and NL severity, determining if their compounded degradation is strictly additive or non-linear.
- **Gradient/Attention Diagnostics:**
  - Compare the gradient cosine similarity of the MLP layers (affected by NL) under the presence vs. absence of inverse-gamma compensation.
  - Evaluate attention map fragmentation (utilizing the `visualize_attention.py` logic) across the joint failure cells to determine if write-side noise exacerbates read-side attention scattering.
- **Matrix Decomposition:** Evaluate whether the joint accuracy matrix exhibits rank-1 separability (indicating orthogonal failure mechanisms) or higher-rank complexity (indicating synergistic or interfering effects between the read and write paths).

## 4. Contribution Beyond the NC Paper
The Nature Communications manuscript scopes its narrative to demonstrating the individual feasibility and identification of these physical bounds (e.g., establishing the 6-bit ADC cliff and introducing Ensemble HAT). Presenting the full 16-cell joint mitigation sweep in the main paper would overwhelm the narrative and dilute the primary message of framework viability. This chapter elevates the thesis by moving from the *identification* of isolated mechanisms to the *co-optimization* of a complete, end-to-end analog-optical system. It answers the critical systems-engineering question of whether these mitigations stack linearly, providing a comprehensive design guide that a thesis format can deeply and rigorously explore.

## 5. Fallback Plan (Minimum Viable Reduction)
If the full ~200 GPU-hour budget is unavailable, the 16-cell $\times$ 3-seed grid will be aggressively reduced to a 4-cell critical interaction square (12 runs total, ~50 GPU-hours):
- **Cell 1:** $\gamma=1.0$, NL=0, No Mitigation (Idealized Baseline Control)
- **Cell 2:** $\gamma=2.0$, NL=0, Inv-Gamma Only (Isolated Frontend Success)
- **Cell 3:** $\gamma=1.0$, NL=2.0, MLP-Linear Only (Isolated Write Success)
- **Cell 4:** $\gamma=2.0$, NL=2.0, Both Mitigations (Joint Success Verification)

This minimal 4-cell framework still proves that the two mitigations are architecturally compatible and can simultaneously rescue the network from compounded physical extremes, preserving the core mechanistic narrative of the chapter.
