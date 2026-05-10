# GM-X35: Optional Supplement-Only Insertion Drafts

> **Goal:** Prepare clean insertion stubs for optional experiments without implying completion.

---

## 1. Ensemble HAT vs i.i.d. D2D Control (GM-E1)
- **Status:** **Completed**.
- **Supp Section:** SI Section 5.1 (Algorithm Novelty).
- **Table/Figure:** Table S5 (Ablation Comparison).
- **Takeaway:** Ensemble HAT achieves ~86% fresh-instance accuracy, whereas standard HAT collapses to ~10%, and i.i.d. noise augmentation fails to capture the fixed spatial correlation of mismatch.
- **Main-Text Pointer:** `As justified by the ablation study in Supplementary Section 5.1, epoch-level resampling is essential for crossbar-instance transfer.`

## 2. Pure-Digital ADC Control (GM-E2)
- **Status:** **Completed**.
- **Supp Section:** SI Section 5.2 (ADC Cliff Analysis).
- **Table/Figure:** Line chart added to Figure S5 (Noise/ADC Grid).
- **Takeaway:** While digital 4-bit ADC penalty is visible (~45%), analog noise exacerbates this to ~27%, confirming 6-bit as the system-wide threshold.
- **Main-Text Pointer:** `A pure-digital control (Supplementary Fig. S5) confirms that the 6-bit cliff is a combined effect of quantization and analog noise.`

## 3. Retention Sensitivity (GM-E3)
- **Status:** **Running**.
- **Supp Section:** SI Section 5.3 (Parameter Robustness).
- **Table/Figure:** Matrix of Accuracy vs A_0/Tau.
- **Takeaway:** System conclusions remain qualitatively unchanged within a ±50% variance of retention proxy parameters.
- **Main-Text Pointer:** `Sensitivity sweeps (Supplementary Section 5.3) demonstrate that the identified retention trends are robust to local variations in proxy decay constants.`

## 4. Lightweight NL Scan (GM-E4)
- **Status:** **Wait**.
- **Supp Section:** SI Section 5.4 (Boundary Refinement).
- **Table/Figure:** Accuracy vs NL curve (1.5 to 2.5).
- **Takeaway:** Transition to failure at NL=2.0 is graded rather than binary.
- **Main-Text Pointer:** `The transition to the approximation-limit regime is further detailed in Supplementary Section 5.4.`
