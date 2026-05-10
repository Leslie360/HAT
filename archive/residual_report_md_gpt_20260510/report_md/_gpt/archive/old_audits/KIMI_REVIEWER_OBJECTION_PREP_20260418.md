# Reviewer Objection Prep — Top 5 (Claude pre-draft)

**Status:** Pre-draft for Kimi K-M refinement. Covers the five most likely post-revision objections given the locked manuscript state (15pp main, 21pp supp, Option B NL framing).

---

## 1. "Why no ImageNet? CIFAR-10/100 and Flowers-102 are too small to claim general vision-task viability."

**Manuscript counter-evidence:**
- §1 explicitly scopes to "edge vision" where model sizes (ResNet-18, ConvNeXt-Tiny, Tiny-ViT-5M) and dataset scales match the organic-device memory capacity assumed in the literature (~10⁴–10⁶ conductance states).
- §6 Limitations notes: "ImageNet-scale validation is deferred until larger organic arrays or hierarchical tiling strategies are demonstrated."
- The framework architecture supports ImageNet (dataset loader hook exists), but the physical array size assumed in the present profiles does not yet accommodate ResNet-50–class parameter counts.

**Strongest counter:** The paper does not claim general vision viability; it claims "materials-to-system risk ranking" for edge-scale deployment. The gap is scope, not evidence.

**Residual exposure:** MEDIUM. A determined reviewer can still push on ImageNet as a de facto standard.

**Mitigation if pushed:** Offer a pre-registered ImageNet pilot as a response-side commitment (not a promise to add to this revision). The existing code path already supports it; only GPU time is missing.

---

## 2. "The energy model is unvalidated first-order placeholder. Without measured organic-array data, the ~11× claim is unsubstantiated."

**Manuscript counter-evidence:**
- §3 and §6 repeatedly qualify energy as "first-order analytical model" and "system-level upper bounds under placeholder constants."
- §6: "Energy parameters are placeholders; parasitic ranges derive from ReRAM literature until measured organic-array data become available."
- Cover letter: "we state energy advantages only as first-order system-level upper bounds prior to routed-chip implementation."

**Strongest counter:** The manuscript never claims the energy number is measured. It is explicitly framed as a relative ranking tool, not an absolute prediction.

**Residual exposure:** LOW-MEDIUM. Reviewers who skip the caveats may still fixate on the headline number.

**Mitigation if pushed:** Add one additional sentence in §6.5 tightening the caveat to "not suitable for direct watt-per-inference comparison with silicon CMOS." This is a 5-word edit with no experimental cost.

---

## 3. "NL=2.0 limitation reflects your gradient-scaling approximation, not a materials bound. This weakens the severe-NL bottleneck claim."

**Manuscript counter-evidence:**
- §6.5: "the observed degradation... should be interpreted as the limit of this approximation, rather than as a fundamental materials constraint."
- Supplementary gradient-distortion diagnostic (Fig S10) localizes the failure to the MLP analog path, providing mechanistic grounding.
- Group-wise ablation (Table SX.N) shows MLP-linearization recovers to ~87%, confirming the bottleneck is path-specific, not universal.

**Strongest counter:** The paper already admits this is an approximation limit. The value of the result is that it *localizes* the approximation failure, which guides future pulse-shaping or write-verify algorithm design.

**Residual exposure:** LOW. An honest reviewer who reads §6.5 will see the disclosure.

**Mitigation if pushed:** None needed. The text is already reviewer-honest. If pushed further, note that pulse-shaping algorithms are orthogonal to the present simulation scope and are flagged as future work.

---

## 4. "Ensemble HAT lacks direct comparison with existing multi-instance or domain-randomization methods."

**Manuscript counter-evidence:**
- §6.1: "Ensemble HAT differs from ordinary i.i.d. noise augmentation because it changes the fixed spatial mismatch map itself."
- Reviewer response (Major Comment 3) provides literature comparison: Zhu et al. DATE 2020 and Liu et al. DAC 2015 sample device parameters statistically but do not resample complete spatial hardware-instance maps.
- Internal controls: fixed-mask standard HAT (10.00%), per-batch perturbation, epoch-level structured resampling — these isolate the causal contribution without an external apples-to-apples baseline.

**Strongest counter:** No prior open-source baseline implements exactly the same epoch-level resampling of full spatial D2D mismatch maps. The internal-control design is therefore the best available causal evidence.

**Residual exposure:** MEDIUM. A reviewer may still demand an external baseline sweep.

**Mitigation if pushed:** Offer to add AIHWKIT-style i.i.d. noise augmentation as a response-side control if the editor insists. The existing codebase already supports it (see `train_tinyvit.py` `--noise_mode=iid`).

---

## 5. "Why fixed Gaussian C2C/D2D? Real devices exhibit spatially correlated D2D and heavy-tailed conductance distributions."

**Manuscript counter-evidence:**
- §6 Limitations explicitly lists: "Spatially correlated D2D and heavy-tailed conductance distributions are also absent."
- §6 Outlook: "circuit-aware layer explicitly deferred" to prioritize "materials-to-system risk ranking before full hardware closure."
- The profile interface is replaceable; the framework architecture supports arbitrary noise-law substitution without code changes.

**Strongest counter:** The paper is a first-order behavioral study. Adding spatial correlation and heavy tails is acknowledged as important but requires measured spatial maps that do not yet exist in the open literature for organic arrays.

**Residual exposure:** LOW. The limitation is honestly disclosed and framed as scope boundary, not hidden assumption.

**Mitigation if pushed:** None needed. If pushed hard, cite the unpublished measured-device data (`数据_博士/`) as the reason spatial correlation was not modeled: the raw data lack sufficient spatial resolution to fit a variogram.

---

## Honorable mentions (lower probability)

| # | Objection | Exposure | Mitigation |
|:--|:--|:--:|:--|
| 6 | "Why best-checkpoint reporting?" | LOW | Already disclosed in §5.1. Standard practice for noisy training. |
| 7 | "Why 4-bit quantization? Why not 2-bit or 8-bit?" | LOW | ADC sweep (Fig 3, Fig S2) covers 2–12 bits; 4-bit is the operational sweet spot. |
| 8 | "CrossSim gap (14.43 pp) suggests your noise model is wrong." | LOW-MEDIUM | Response draft already frames this as "profile-driven simulation argument" — different noise-to-conductance mapping. |
| 9 | "The OPECT profile uses proxy estimates (2% C2C, 3% D2D), not measured full-array statistics." | LOW | Supplementary sensitivity sweep (4×5 grid) shows conclusion is insensitive to exact proxy choice. |
| 10 | "Why no measured-device validation?" | LOW | Explicitly scoped as "prospective simulation" in abstract, intro, cover letter. |

---

**Next step:** Kimi K-M should refine this pre-draft, add citation support, and assess which objections warrant pre-emptive text hardening vs. response-only treatment.
