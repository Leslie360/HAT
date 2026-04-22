# Thesis Narrative Arc — 2026-04-20

Integration guide for Ch.1–Ch.8.

---

## Ch.1 — Introduction

**Hook:** Organic optoelectronic CIM promises efficient edge inference, yet single-array benchmarking masks distributional deployment risk. This chapter states the gap and the four contributions that close it.

**Forward pointer:** The next chapter builds the compute-ViT framework hosting every subsequent experiment.

**Backward pointer:** *(origin).*

---

## Ch.2 — Framework Architecture

**Hook:** This chapter presents compute-ViT’s operator mapping, profile interface, and energy model as the modular, auditable substrate for every subsequent claim.

**Forward pointer:** With the instrument built, the next chapter maps the HAT design space and exposes instance overfitting.

**Backward pointer:** Turns Ch.1’s motivation into a traceable simulation backend.

---

## Ch.3 — HAT Taxonomy

**Hook:** Decomposed along cadence and noise-profile axes, HAT reveals deterministic single-instance collapse to 10.00 ± 0.00%. That failure is representational bias, not noise variance.

**Forward pointer:** The taxonomy surfaces five distinct failure modes, which the next chapter names and ranks.

**Backward pointer:** Applies the Ch.2 framework to training, turning a tool into a diagnostic engine.

---

## Ch.4 — Failure Mode Atlas

**Hook:** Without consistent nomenclature, mitigation is whack-a-mole; here the five canonical modes—overfitting, QKV collapse, MLP bound, correlated D2D, and retention—are defined, reproduced, and cross-mapped to layers and physical mechanisms.

**Forward pointer:** Named failures demand named remedies; the next chapter tests four mitigations against this exact atlas.

**Backward pointer:** Systematizes the pathologies first observed in the Ch.3 taxonomy.

---

## Ch.5 — Mitigation Case Studies

**Hook:** Ensemble HAT rescues transfer to 86.37%, MLP-linear retraining isolates the severe-NL bottleneck, and all-linearization caps recovery at 32.60%—proving the gap is instance bias, not gradient corruption.

**Forward pointer:** These mitigations assume i.i.d. noise; the next chapter reintroduces physical realism.

**Backward pointer:** Every case study targets a specific entry from the Ch.4 atlas.

---

## Ch.6 — Physical-Realism Extensions

**Hook:** This chapter reranks mitigations under spatial correlation, heavy-tailed drift, IR-drop, and temperature, showing Ensemble HAT preserves ranking to ρ = 0.3 while heavy tails widen the variance budget.

**Forward pointer:** With physical realism restored, the next chapter draws the deployment envelope.

**Backward pointer:** Stress-tests the Ch.5 mitigations against non-idealities absent from the original training model.

---

## Ch.7 — Deployment Envelope

**Hook:** This chapter constructs the ranking-preservation map, architect decision diagram, and CNN-versus-ViT surface to yield a data-driven go/no-go boundary.

**Forward pointer:** The final chapter steps outside the envelope to propose the next-generation theory and hardware roadmap.

**Backward pointer:** Compresses the Ch.6 findings into actionable deployment rules.

---

## Ch.8 — Outlook + Conclusion

**Hook:** This chapter distills failure-mode lessons into a theory agenda—analytical bounds, learnable exponents, joint co-optimization—and a hardware roadmap toward fabricated-array calibration.

**Forward pointer:** *(terminus).*

**Backward pointer:** Generalizes the Ch.7 boundary into the research directions required to push it outward.

---

## Boundary Sentences

1. **Ch.1 → Ch.2:** *To make those claims falsifiable, the thesis now introduces the simulation framework every subsequent experiment inherits.*
2. **Ch.2 → Ch.3:** *With the instrument in place, the first question is how HAT behaves when training and deployment instances differ.*
3. **Ch.3 → Ch.4:** *The taxonomy reveals symptoms, but symptoms are not diagnoses; the next section names the diseases.*
4. **Ch.4 → Ch.5:** *Each named failure now receives its remedy, with recovery ceilings explicitly measured.*
5. **Ch.5 → Ch.6:** *These recoveries assume idealized noise; the next chapter reintroduces the physical world.*
6. **Ch.6 → Ch.7:** *Surviving physical realism is necessary but not sufficient; the thesis now translates survival into deployment rules.*
7. **Ch.7 → Ch.8:** *The envelope is where the thesis ends and the next project begins.*

---

*Preserve boundary sentences verbatim during integration.*
