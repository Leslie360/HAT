# KIMI R10G: Novelty Contrast Paragraph for §2.1

**Date:** 2026-04-25
**Task:** Write a novelty contrast paragraph for §2.1 (Related Work — Hardware-Aware Training) that differentiates Ensemble HAT from Tobin 2017 domain randomization and AIHWKit / Rasch 2023 per-batch analog noise injection.

---

## Drafted Paragraph (inserted at end of §2.1, before §2.2)

> The connection to domain randomization~\citep{tobin2017domain} is deliberate, but the analogy is superficial. Domain randomization treats perturbations as i.i.d.\ simulation parameters; organic optoelectronic CIM exhibits spatially structured D2D mismatch, C2C noise, and nonlinear write that are fixed per hardware instance. Ensemble HAT therefore resamples complete structured mismatch \emph{maps} per epoch rather than i.i.d.\ noise per batch---a granularity choice that is empirically load-bearing (88.41\% epoch-level versus 86.16\% per-batch and 87.18\% fixed-mask). Supplementary Note~S-Theory shows this acts as a structural analogue to SAM along the D2D direction. Moreover, unlike domain-randomization studies that do not diagnose instance-level overfitting, we explicitly measure it: Standard HAT collapses to 10.00\% on fresh instances, whereas Ensemble HAT recovers to 86.37\%. AIHWKIT~\citep{rasch2021aihwkit} injects per-batch analog noise; our epoch-level resampling of full D2D maps yields [PENDING_R10E_NUMBER] in a direct head-to-head comparison.

---

## Rationale

1. **Acknowledges domain randomization openly:** The opening sentence confirms the reviewer is right that a conceptual link exists ("deliberate"), but immediately downgrades it ("superficial"). This prevents the appearance of hiding the connection.

2. **Substrate differentiation (Point 1):** Explicitly contrasts i.i.d. simulation parameters with spatially structured D2D + C2C + nonlinear write fixed per hardware instance. This is the core physical distinction.

3. **Granularity + empirical evidence (Point 2):** Cites the three ablation numbers from the 50-epoch cadence scan: 88.41% (epoch), 86.16% (per-batch), 87.18% (fixed). The dash construction makes the hierarchy immediately readable.

4. **Theoretical interpretation (Point 3):** Invokes Supplementary Note S-Theory and the SAM analogue. This provides a principled, non-empirical pillar of novelty.

5. **Diagnosis of hardware-instance overfitting (Point 4):** Contrasts domain-randomization papers (which do not diagnose instance-level overfitting) with our explicit measurement: 10.00% Standard HAT collapse → 86.37% Ensemble HAT recovery. This frames the contribution as methodological (diagnosis + treatment) rather than purely algorithmic.

6. **vs AIHWKit (Point 5):** Distinguishes AIHWKIT's per-batch analog noise injection from our epoch-level resampling of *full structured D2D mismatch maps*. The placeholder `[PENDING_R10E_NUMBER]` is inserted for the head-to-head comparison number that R10E will produce.

7. **Length:** ~132 words (TeX source), comfortably near the ~120-word target.

## Files Modified

- `compute_vit/paper/latex_gpt/sections/02_related_work.tex` — paragraph inserted between the AIHWKIT discussion and §2.2.

## Citations Verified

- `tobin2017domain` — exists in `refs_gpt.bib` (Tobin et al., ICRA 2017).
- `rasch2021aihwkit` — exists in `refs_gpt.bib` (Rasch et al., 2021). Note: The dispatch spec mentioned "Rasch 2023," but the actual bib entry is `rasch2021aihwkit` (2021). The paragraph uses the correct key.
