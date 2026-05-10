# K-S2: Figure Caption Audit

**Scope:** All `.tex` files in `compute_vit/paper/latex_gpt/` (main body, appendix, and supplementary).
**Criteria:** (a) standalone readability, (b) cross-reference to dependent equations/tables, (c) explicit error-bar / MC protocol where applicable.

---

## Main Manuscript

### Table 1: `tab:exp-notation`
- **Standalone:** NO — does not state the evaluated task, the canonical profile, or the hardware-aware training context; out of context the IDs are unexplained abbreviations.
- **Cross-ref:** NO — cites no equation or table.
- **Error-bar protocol:** N/A
- **Patch:** *"Notation and experiment-ID mapping for the Tiny-ViT hardware-aware training family under the canonical organic-device profile (4-bit quantization, 5% C2C, 10% D2D; see Section~\\ref{sec:experimental-setup})."*

### Fig 1: `fig:accuracy-comparison`
- **Standalone:** NO — omits the architectures (ResNet-18, ConvNeXt-Tiny, Tiny-ViT-5M) and datasets (CIFAR-10, CIFAR-100, Flowers-102) that are plotted.
- **Cross-ref:** NO — uses regime shorthand but does not cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** YES — explicitly defines "±1 standard deviation" and explains missing error bars.
- **Patch:** *"Cross-dataset accuracy (CIFAR-10, CIFAR-100, Flowers-102) for ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M under canonical deployment (4-bit quantization, 5% C2C, 10% D2D variability; regimes defined in Table~\\ref{tab:exp-notation}). Error bars denote ±1 standard deviation where Monte Carlo (MC) statistics are available; bars without visible error bars indicate deterministic baselines or currently available point estimates."*

### Fig 2: `fig:hat-recovery`
- **Standalone:** NO — does not name the datasets, the full set of architectures, or the canonical profile context.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — "10-run MC" is stated but the caption does not say what the error bars represent (±std? ±sem?); ConvNeXt is explained.
- **Patch:** *"Accuracy degradation from FP32 to noisy deployment and hardware-aware training (HAT) recovery for ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M on CIFAR-10 and CIFAR-100 (regimes defined in Table~\\ref{tab:exp-notation}). Tiny-ViT shows mean ± standard deviation over 10 Monte Carlo forward-pass evaluations; ConvNeXt and ResNet results are single-run deterministic estimates."*

### Fig 3: `fig:contour-map`
- **Standalone:** YES — specifies model, sweep axes, and key takeaway.
- **Cross-ref:** NO — should cite Eq.~\\ref{eq:sobol-first-order} (the Sobol definition used to interpret the sweep) and Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** YES — "10 MC runs per point".
- **Patch:** *"Iso-accuracy contour map for the Ensemble HAT Tiny-ViT model under joint σ_D2D and ADC precision sweep (σ_C2C=5%, NL=1.0, 10 Monte Carlo runs per point; model defined in Table~\\ref{tab:exp-notation}). The 6-bit ADC cliff and the D2D-dominated degradation in the operational regime are visible."*

### Fig 4: `fig:ensemble-hat-concept`
- **Standalone:** YES — explains the concept and the generalization gap clearly.
- **Cross-ref:** NO — should cite Eqs.~\\ref{eq:hat-standard}--\\ref{eq:hat-ensemble}, which formally define the two protocols shown.
- **Error-bar protocol:** N/A
- **Patch:** *"Ensemble HAT concept (Eqs.~\\ref{eq:hat-standard}--\\ref{eq:hat-ensemble}). Standard HAT reuses one fixed D2D mismatch map throughout training, whereas Ensemble HAT resamples the mismatch map each epoch. The fresh-instance transfer panel highlights the resulting generalization gap between the two training protocols."*

### Fig 5: `fig:case-study-transfer`
- **Standalone:** YES — detailed description of what the bars show.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for the C4/V4 identifiers.
- **Error-bar protocol:** NO — the ± spread in the surrounding text is absent from the caption; no n=... or std-dev definition is given.
- **Patch:** *"Zero-shot transfer across alternative device profiles. Bars report the accuracy of standard-HAT checkpoints (ConvNeXt C4, Tiny-ViT V4; see Table~\\ref{tab:exp-notation}) when evaluated on literature-calibrated or measured alternative device profiles without profile-specific retraining. ConvNeXt C4 retains partial transfer on the OPECT and idealized profiles but degrades sharply on PCM and RRAM, whereas Tiny-ViT V4 collapses to chance level (10.00%) across all shown alternatives. Dashed vertical lines mark the source-profile best accuracy, and unavailable combinations are labeled as n/a. Error bars (where present) show ±1 standard deviation over 10 fresh-instance Monte Carlo evaluations."*

---

## Main Manuscript — Appendix

### Table A1: `tab:v4-three-seed-summary`
- **Standalone:** NO — omits model, dataset, and what "V4" means.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — the ± symbols are explained in the table body but the caption itself does not state the MC protocol.
- **Patch:** *"Three-seed reproducibility summary for the canonical Tiny-ViT V4 hardware-aware training regime on CIFAR-10 (Table~\\ref{tab:exp-notation}). Each seed shows mean ± standard deviation over 10 Monte Carlo forward-pass evaluations; the cross-seed aggregate is mean ± standard deviation of the three seed means."*

### Table A2: `tab:provenance`
- **Standalone:** NO — no mention of which profiles, parameters, or framework.
- **Cross-ref:** NO — cites no supporting table or equation.
- **Error-bar protocol:** N/A
- **Patch:** *"Parameter provenance tracking matrix for the canonical organic profile, the Zhang 2025 OPECT case-study profile, and the Task 34-36 stress-test profiles. Literature-anchored values are distinguished from proxy estimates."*

### Table A3: `tab:sensitivity`
- **Standalone:** NO — does not specify model, dataset, or what the cell values represent (accuracy % on CIFAR-10?).
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — mentions "Monte Carlo averaging" but gives no n=... or statistic type.
- **Patch:** *"Ensemble HAT Tiny-ViT accuracy (%) on CIFAR-10 under varied Zhang-proxy C2C/D2D noise assumptions (Table~\\ref{tab:exp-notation}). Each cell reports the mean over 10 Monte Carlo forward-pass evaluations; repeated rows reflect scale-masking because static D2D spatial variability dominates the deployment accuracy budget."*

### Table A4: `tab:sensitivity-ci`
- **Standalone:** NO — omits model and dataset.
- **Cross-ref:** YES — cites Table~\\ref{tab:sensitivity}.
- **Error-bar protocol:** YES — "normal approximation over the 10 Monte Carlo runs" is stated.
- **Patch:** *"Statistical summary of the C2C-insensitivity trend in Table~\\ref{tab:sensitivity} for Ensemble HAT Tiny-ViT on CIFAR-10. The confidence interval uses a normal approximation over the 10 Monte Carlo forward-pass runs recorded for the nominal C2C =2% row."*

### Table A5: `tab:retention-comparison`
- **Standalone:** NO — omits model, dataset, and retention-model details.
- **Cross-ref:** NO — cites no equation or table.
- **Error-bar protocol:** N/A
- **Patch:** *"Retention accuracy comparison for Ensemble-HAT Tiny-ViT on CIFAR-10: uniform double-exponential decay versus state-dependent decay in which high-conductance states decay 20% faster (Section~\\ref{subsec:retention-drift})."*

---

## Supplementary

### Table S1: `tab:supp-operator-mapping`
- **Standalone:** NO — does not name the architecture or the hybrid deployment context.
- **Cross-ref:** NO — should cite Section~\\ref{subsec:hybrid-deployment}.
- **Error-bar protocol:** N/A
- **Patch:** *"Analog/digital operator mapping rationale for the hybrid organic-CIM inference stack (Section~\\ref{subsec:hybrid-deployment})."*

### Fig S1: `fig:supp-weight-mapping`
- **Standalone:** YES — describes the pipeline clearly.
- **Cross-ref:** NO — should cite Eq.~\\ref{eq:scale-recovery}, which defines the weight-to-conductance math illustrated.
- **Error-bar protocol:** N/A
- **Patch:** *"Behavioral weight-to-conductance mapping pipeline (Eq.~\\ref{eq:scale-recovery}). Floating-point weights are split into differential branches, mapped to a bounded conductance window, quantized, and perturbed by the selected device profile before differential readout."*

### Fig S2: `fig:supp-system-architecture`
- **Standalone:** YES — clear.
- **Cross-ref:** NO — should cite Table~\\ref{tab:supp-operator-mapping} for the operator-level details.
- **Error-bar protocol:** N/A
- **Patch:** *"Hybrid organic-CIM inference stack (operator mapping detailed in Table~\\ref{tab:supp-operator-mapping}). Dense weight-stationary operators execute on analog crossbars, whereas dynamic attention and control-heavy operators remain in the digital path."*

### Table S2: `tab:supp-fp32-baselines`
- **Standalone:** YES — self-explanatory.
- **Cross-ref:** N/A — no dependencies.
- **Error-bar protocol:** N/A
- **Patch:** None needed.

### Table S3: `tab:supp-result-summary`
- **Standalone:** YES — the table body supplies datasets; caption is sufficient.
- **Cross-ref:** NO — uses V3/V4/C3/C4 shorthand without citing Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — "entries with ± denote stochastic physical-extension evaluations" is vague; no n=... or statistic type.
- **Patch:** *"Summary of classification accuracy (%) across architectures and physical regimes on CIFAR-10 and CIFAR-100 (experiment IDs defined in Table~\\ref{tab:exp-notation}). Cross-dataset deployment rows report locked best-checkpoint values; entries with ± show mean ± standard deviation over 10 Monte Carlo forward-pass evaluations."*

### Table S4: `tab:v4-three-seed-summary`
- **Standalone:** NO — omits model, dataset, and MC protocol.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — ± meaning is not stated in the caption.
- **Patch:** *"Three-seed reproducibility summary for the canonical Tiny-ViT V4 uniform-noise HAT regime on CIFAR-10 (Table~\\ref{tab:exp-notation}). Each seed shows mean ± standard deviation over 10 Monte Carlo forward-pass evaluations; the cross-seed aggregate is mean ± standard deviation of the three seed means."*

### Table S5: `tab:provenance`
- **Standalone:** NO — same issue as Appendix Table A2.
- **Cross-ref:** NO.
- **Error-bar protocol:** N/A
- **Patch:** *"Parameter provenance tracking matrix for the canonical organic profile, the Zhang 2025 OPECT case-study profile, and the nonlinear-write stress-test profiles. Literature-anchored values are distinguished from proxy estimates."*

### Fig S3: `fig:supp-contour-map`
- **Standalone:** NO — omits model and dataset.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** YES — "10 Monte Carlo evaluations" stated.
- **Patch:** *"Zhang-proxy C2C/D2D sensitivity sweep for Ensemble HAT Tiny-ViT on CIFAR-10 (Table~\\ref{tab:exp-notation}). Cell annotations report mean accuracy over 10 Monte Carlo forward-pass evaluations at each operating point. The nominal proxy point (σ_C2C=2%, σ_D2D=3%) is outlined. Accuracy changes are driven almost entirely by D2D mismatch, while the C2C axis remains flat to within Monte Carlo uncertainty."*

### Table S6: `tab:sensitivity`
- **Standalone:** NO — omits model, dataset, and what the cells represent.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — no n=... or MC protocol.
- **Patch:** *"Ensemble HAT Tiny-ViT accuracy (%) on CIFAR-10 under a Zhang-proxy C2C/D2D sensitivity sweep (Table~\\ref{tab:exp-notation}). Each cell reports the mean over 10 Monte Carlo forward-pass evaluations."*

### Table S7: `tab:sensitivity-ci`
- **Standalone:** NO — omits model and dataset.
- **Cross-ref:** YES — cites Table~\\ref{tab:sensitivity}.
- **Error-bar protocol:** NO — unlike the appendix version, the caption does not state the normal-approximation method or the 10-run count.
- **Patch:** *"Confidence intervals for the Zhang-proxy sensitivity sweep in Table~\\ref{tab:sensitivity} (Ensemble HAT Tiny-ViT, CIFAR-10). The 95% confidence interval uses a normal approximation over the 10 Monte Carlo forward-pass runs recorded for the nominal C2C =2% row."*

### Table S8: `tab:adc-nonideality`
- **Standalone:** YES — names model, deployment, and dataset.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V4.
- **Error-bar protocol:** NO — "Std." column present but caption gives no run count or protocol.
- **Patch:** *"Hook-based ADC non-ideality check for the canonical Tiny-ViT V4 deployment (Table~\\ref{tab:exp-notation}). Offset, gain, and INL are injected at calibrated analog-layer outputs during full-test inference on CIFAR-10. Mean and standard deviation are computed over 10 Monte Carlo forward-pass evaluations."*

### Fig S4: `fig:supp-sobol`
- **Standalone:** YES — describes what the two groups show.
- **Cross-ref:** NO — should cite Eq.~\\ref{eq:sobol-first-order} and Fig.~\\ref{fig:contour-map}.
- **Error-bar protocol:** N/A
- **Patch:** *"First-order Sobol sensitivity indices (Eq.~\\ref{eq:sobol-first-order}) derived from the 7×9 D2D--ADC contour sweep (Fig.~\\ref{fig:contour-map}). The left group reports indices over the full grid, where ADC resolution dominates the variance budget. The right group restricts the analysis to the deployment-relevant operating region (ADC≥ 6 bits, σ_D2D≤ 15%), where residual variance is driven primarily by D2D mismatch after readout precision has saturated."*

### Table S9: `tab:retention-comparison`
- **Standalone:** NO — same issue as Appendix Table A5.
- **Cross-ref:** NO.
- **Error-bar protocol:** N/A
- **Patch:** *"Retention accuracy comparison for Ensemble-HAT Tiny-ViT on CIFAR-10: uniform double-exponential decay versus state-dependent decay in which high-conductance states decay 20% faster."*

### Table S10: `tab:supp-flowers-results`
- **Standalone:** YES — clear.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V3/V4.
- **Error-bar protocol:** NO — ± entries lack an n=... or statistic definition.
- **Patch:** *"Classification accuracy (%) on Flowers-102 across physical regimes (experiment IDs defined in Table~\\ref{tab:exp-notation}). The asterisk marks a single-run ConvNeXt boundary estimate. Stochastic entries show mean ± standard deviation over 10 Monte Carlo forward-pass evaluations."*

### Fig S5: `fig:supp-noise-sensitivity`
- **Standalone:** YES — explains both panels.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V4.
- **Error-bar protocol:** N/A — heatmap/sweep of means, no error bars shown.
- **Patch:** *"Continuous noise sensitivity and ADC sweep for the Tiny-ViT V4 checkpoint (Table~\\ref{tab:exp-notation}). Left: mean accuracy heatmap under a continuous joint sweep of σ_C2C and σ_D2D in the uniform-noise regime. Right: ADC-bit sweep highlighting the 6-bit knee and subsequent saturation. Only the model with available continuous-sweep data is shown."*

### Fig S6: `fig:supp-zero-shot-transfer`
- **Standalone:** YES — detailed.
- **Cross-ref:** NO — should cite Eqs.~\\ref{eq:hat-standard}--\\ref{eq:hat-ensemble} and Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — "86.37±1.54%" is given but the caption does not define the ± as cross-instance standard deviation over 10 fresh arrays with 5 MC passes each.
- **Patch:** *"Fresh-instance robustness and D2D-resampling ablation for Tiny-ViT (Eqs.~\\ref{eq:hat-standard}--\\ref{eq:hat-ensemble}, Table~\\ref{tab:exp-notation}). Left: evaluation on 10 unseen fixed D2D realizations. Standard HAT collapses to chance on every fresh array (10.00%), whereas Ensemble HAT preserves 86.37±1.54% (standard deviation across 10 fresh instances, 5 Monte Carlo forward passes per instance) accuracy across the same deployment set. Right: exploratory held-out-accuracy scan under different D2D-resampling cadences during a 50-epoch training ablation."*

### Fig S7: `fig:supp-attention-maps`
- **Standalone:** YES — very detailed row/column description.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V1/V3/V4/V6.
- **Error-bar protocol:** N/A
- **Patch:** *"Attention heatmaps for three representative CIFAR-10 samples across the main deployment regimes (experiment IDs defined in Table~\\ref{tab:exp-notation}). Columns show cat, truck, and automobile. Rows show the original input image, the V1 digital baseline, the V3 fixed-mask noisy deployment, the V4 hardware-aware trained deployment, and the V6 front-end-compensated deployment. Color intensity denotes normalized head-averaged attention response."*

### Fig S8: `fig:supp-retention-curve`
- **Standalone:** YES — names models and takeaway.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for C9/V4 and Eq.~\\ref{eq:scale-recovery} for the recalibration.
- **Error-bar protocol:** N/A
- **Patch:** *"Retention decay under programmed weight drift for ConvNeXt C9 and Tiny-ViT V4 (Table~\\ref{tab:exp-notation}) under dynamic scale recalibration (Eq.~\\ref{eq:scale-recovery}) with co-decay of the retained D2D buffers. Both models exhibit a rapid early drop followed by a broad plateau, indicating partial long-horizon viability under the present uniform double-exponential retention model."*

### Table S11: `tab:supp-frontend-gamma-scan`
- **Standalone:** YES — clear.
- **Cross-ref:** NO — should cite Eqs.~\\ref{eq:inverse-gamma}--\\ref{eq:frontend-photoresponse}.
- **Error-bar protocol:** N/A
- **Patch:** *"ResNet-18 HAT accuracy (%) under inverse-gamma compensation (Eqs.~\\ref{eq:inverse-gamma}--\\ref{eq:frontend-photoresponse}). Each cell reports compensated / raw accuracy and the gain in percentage points."*

### Fig S9: `fig:supp-frontend-compensation`
- **Standalone:** NO — omits model, dataset, axes, and what the curves represent.
- **Cross-ref:** NO — should cite Eqs.~\\ref{eq:inverse-gamma}--\\ref{eq:frontend-photoresponse}.
- **Error-bar protocol:** N/A
- **Patch:** *"Impact of front-end nonlinearity and dark current on ResNet-18 HAT accuracy (Eqs.~\\ref{eq:inverse-gamma}--\\ref{eq:frontend-photoresponse}). Inverse-gamma compensation restores accuracy for γ_phys > 1 but amplifies shot-noise variance when γ_phys < 1."*

### Fig S10: `fig:supp-snr-curves`
- **Standalone:** NO — does not state what is plotted (SNR vs. what?), for which parameters, or over what domain.
- **Cross-ref:** NO — should cite Eq.~\\ref{eq:frontend-photoresponse}.
- **Error-bar protocol:** N/A
- **Patch:** *"Analytical signal-to-noise ratio (SNR) trends under inverse-gamma compensation (Eq.~\\ref{eq:frontend-photoresponse}) as a function of normalized input intensity for varying γ_phys and I_dark."*

### Fig S11: `fig:supp-pareto`
- **Standalone:** NO — omits model, dataset, and energy-model context.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V2--V7 and the Supplementary Methods for the energy model.
- **Error-bar protocol:** N/A
- **Patch:** *"Energy--accuracy placement of the digital baseline and hybrid V2--V7 family (Table~\\ref{tab:exp-notation}) for Tiny-ViT on CIFAR-10, estimated with the first-order analytical energy model described in the Supplementary Methods."*

### Table S12: `tab:retention-sensitivity`
- **Standalone:** NO — omits model, dataset, and retention model.
- **Cross-ref:** NO — should cite Section~\\ref{subsec:retention-drift}.
- **Error-bar protocol:** N/A
- **Patch:** *"Retention sensitivity to the persistent fraction A_0 across time scales for Ensemble-HAT Tiny-ViT on CIFAR-10 under the uniform double-exponential retention model (Section~\\ref{subsec:retention-drift})."*

### Table S13: `tab:asymmetry-sensitivity`
- **Standalone:** YES — names model, dataset, and test.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V4 and the supplementary asymmetry equation.
- **Error-bar protocol:** NO — "Std Dev" column exists but the caption gives no run count.
- **Patch:** *"Differential-pair asymmetry sensitivity for Tiny-ViT V4 on CIFAR-10 (Table~\\ref{tab:exp-notation}). Accuracy degradation under systematic branch mismatch α (Supplementary Methods). Mean and standard deviation are computed over 10 Monte Carlo forward-pass evaluations."*

### Fig S12: `fig:supp-asymmetry-concept`
- **Standalone:** YES — concept and quantitative takeaway are clear.
- **Cross-ref:** NO — should cite Table~\\ref{tab:asymmetry-sensitivity} for the quantitative bounds quoted.
- **Error-bar protocol:** N/A
- **Patch:** *"Differential-pair asymmetry concept. Systematic mismatch between positive and negative branches (asymmetry factor α) degrades the effective differential signal. Quantitative sensitivity analysis (Table~\\ref{tab:asymmetry-sensitivity}) shows tolerance up to 1% asymmetry with <2% accuracy degradation, but nonlinear collapse beyond 2%."*

### Table S14: `tab:nonideality-sensitivity`
- **Standalone:** YES — names model, dataset, and effects.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V4 and the supplementary IR/sneak equations.
- **Error-bar protocol:** NO — "Mean Accuracy" is given but no MC protocol is stated.
- **Patch:** *"Physical non-ideality sensitivity for Tiny-ViT V4 on CIFAR-10 (Table~\\ref{tab:exp-notation}). Accuracy degradation under IR drop and sneak-path effects (Supplementary Methods). Mean accuracy is computed over 10 Monte Carlo forward-pass evaluations."*

### Fig S13: `fig:supp-nonideality`
- **Standalone:** YES — clear concept and quantitative summary.
- **Cross-ref:** YES — explicitly cites Table~\\ref{tab:nonideality-sensitivity}.
- **Error-bar protocol:** N/A
- **Patch:** None needed.

### Table S15: `tab:parameter-risk`
- **Standalone:** NO — no model, dataset, or framework named.
- **Cross-ref:** NO — should cite Tables~\\ref{tab:sensitivity}--\\ref{tab:sensitivity-ci}, Supplementary Fig.~\\ref{fig:supp-nl-gradient}, and Section~\\ref{subsec:retention-sensitivity}.
- **Error-bar protocol:** N/A
- **Patch:** *"Core parameter risk and robustness assessment for the organic optoelectronic CIM simulation framework, referencing the sensitivity sweeps in Tables~\\ref{tab:sensitivity}--\\ref{tab:sensitivity-ci}, Supplementary Fig.~\\ref{fig:supp-nl-gradient}, and Section~\\ref{subsec:retention-sensitivity}."*

### Fig S14: `fig:supp-nl-gradient`
- **Standalone:** YES — detailed diagnostic description.
- **Cross-ref:** NO — should cite Eq.~\\ref{eq:supp-nl-surrogate} and Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** N/A — deterministic diagnostic.
- **Patch:** *"Group-wise gradient distortion under severe nonlinear write (Eq.~\\ref{eq:supp-nl-surrogate}) on the frozen Tiny-ViT V4 checkpoint (Table~\\ref{tab:exp-notation}). The NL=1.0 baseline is compared against matched forward passes where NL=2.0 is activated for one analog module group at a time. Results aggregate eight CIFAR-10 train batches with preserved checkpoint D2D buffers and σ_C2C=0 so that only the backward surrogate changes."*

### Table S16: `tab:supp-nl-ablation`
- **Standalone:** PARTIAL — does not specify model or dataset.
- **Cross-ref:** NO — should cite Eq.~\\ref{eq:supp-nl-surrogate} and Table~\\ref{tab:exp-notation}.
- **Error-bar protocol:** NO — baseline row has ±0.27 but no n=... or statistic is given.
- **Patch:** *"Group-wise nonlinearity ablation under global NL=2.0 for Tiny-ViT on CIFAR-10 (Eq.~\\ref{eq:supp-nl-surrogate}, Table~\\ref{tab:exp-notation}). Each row reports best and final test accuracy when the specified analog module group is protected at NL=1.0 while all other analog layers remain at NL=2.0. The baseline NL=1.0 row shows mean ± standard deviation of the canonical uniform-noise HAT configuration over 10 Monte Carlo forward-pass evaluations."*

### Fig S15: `fig:supp-corr-d2d`
- **Standalone:** YES — detailed.
- **Cross-ref:** NO — should cite Table~\\ref{tab:exp-notation} for V4 and Eq.~\\ref{eq:hat-ensemble} for Ensemble HAT.
- **Error-bar protocol:** YES — "cross-instance standard deviation over 10 fresh arrays, with 5 Monte Carlo evaluations per array" is fully explicit.
- **Patch:** *"Fresh-instance robustness under spatially correlated D2D mismatch for the canonical Tiny-ViT V4 Ensemble HAT checkpoint (Table~\\ref{tab:exp-notation}, Eq.~\\ref{eq:hat-ensemble}). Error bars show cross-instance standard deviation over 10 fresh arrays, with 5 Monte Carlo evaluations per array. The i.i.d. baseline reaches 86.33±1.61%, while separable AR(1)-style correlation degrades the mean to 84.57±2.39% at ρ=0.3 and 82.12±3.95% at ρ=0.5. The dashed horizontal line marks the canonical standard-HAT collapse baseline (10.00%) to emphasize that ranking is preserved despite bounded degradation."*

---

## Summary Statistics

| Document Region | Total Audited | Standalone NO | Cross-ref NO | Error-bar NO |
|-----------------|---------------|---------------|--------------|--------------|
| Main Manuscript | 6 | 3 | 5 | 2 |
| Main — Appendix | 5 | 4 | 4 | 2 |
| Supplementary | 30 | 17 | 26 | 8 |
| **Total** | **41** | **24** | **35** | **12** |

**Top patterns:**
1. **Cross-reference gap:** The vast majority of captions (35/41) fail to cite the equations or tables that define the plotted quantities (e.g., `tab:exp-notation` for V1--V8 IDs, `eq:scale-recovery` for the mapping pipeline, `eq:sobol-first-order` for Sobol figures).
2. **Standalone gap:** 24/41 captions omit model, dataset, or profile context needed to interpret the figure out of context.
3. **Error-bar gap:** 12/41 captions with statistical spreads omit the explicit n=... or "mean ± std over N MC runs" wording.

**Best-practice example:** Supplementary Fig. S15 (`fig:supp-corr-d2d`) provides a model caption: it names the checkpoint, states the exact error-bar construction (10 fresh arrays × 5 MC passes), and describes every visual element.
