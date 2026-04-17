# GM-X47: Next-Generation Experiment Proposals (0412 Reviewer Response)

> **Objective:** Direct response to the most penetrating critiques from the 0412 mock reviews (Doubao, Nemotron, Sonar, ds-tenxun). These experiments are designed to close the final scientific gaps and transform the paper from "promising simulation" to "bulletproof methodology."

---

## 1. GM-E6: Comprehensive 2D Noise Robustness Frontier
**Criticism Addressed:** ds-tenxun asked if Ensemble HAT sacrifices standard C2C robustness to achieve its D2D fresh-instance generalizability. Sonar asked for performance boundaries under different D2D variances.
**Experiment Design:** 
Evaluate three models (V3 Standard Noise, V4 Standard HAT, V4 Ensemble HAT) across a 2D grid:
- $\sigma_{C2C} \in [0.0, 0.02, 0.05, 0.08, 0.10]$
- $\sigma_{D2D} \in [0.0, 0.03, 0.05, 0.10, 0.15]$
**Scientific Payoff:** Proves that Ensemble HAT strictly dominates Standard HAT across all D2D mismatch regimes without sacrificing fundamental C2C stability, closing the theoretical gap between domain randomization and spatial-correlation awareness.

## 2. GM-E7: State-Dependent Retention Simplification Validation
**Criticism Addressed:** Doubao pointed out that the assumption "uniform retention is a sufficient approximation for state-dependent retention" was only validated on the best-case Ensemble HAT checkpoint, leaving its applicability in non-HAT or standard HAT regimes unproven.
**Experiment Design:**
Evaluate V3 (No HAT) and V4 (Ensemble HAT) under both uniform and state-dependent retention models at $t \in [1, 100, 1000, 10000]$ seconds.
**Scientific Payoff:** Confirms that the physical simplification holds across all deployment regimes, preventing reviewers from attacking the framework's fundamental retention physics approximations.

## 3. GM-E8: Layer-Wise Non-Linear Write (NL) Ablation
**Criticism Addressed:** Sonar and ds-tenxun criticized the $NL=2.0$ limit as an empirical cliff without a mechanistic explanation. They asked which specific modules (Attention QKV vs MLP vs Patch Embedding) are actually breaking down.
**Experiment Design:**
Inject severe non-linear write ($NL=2.0$ and $NL=2.5$) into only one layer group at a time during inference:
- Group A: Attention QKV Projections
- Group B: Attention Output Projections
- Group C: MLP (fc1 + fc2)
- Group D: Patch Embeddings
**Scientific Payoff:** Pinpoints the exact structural vulnerability of Transformers to non-linear write. This not only explains the cliff but provides actionable guidance for future hybrid mapping (e.g., "keep QKV linear, allow MLP to be non-linear").