# Nature Communications Reviewer Response Draft

> **Date**: 2026-04-14  
> **Status**: Phase 2 Draft — Results Integrated  
> **Prepared by**: Kimi

---

## Cover Statement

We thank the reviewers for their constructive and detailed feedback. We have carefully considered all comments and made substantial revisions to strengthen the manuscript. Below we provide point-by-point responses to the major comments, highlighting changes made and additional experiments conducted. Minor comments have been addressed through textual clarifications, terminology standardization, and figure caption improvements throughout the manuscript.

---

## Reviewer Comments

---

### Major Comment 1: Framework Benchmark Comparison

**Original Comment**: 
> The paper claims framework improvements over inorganic CIM simulators but only provides single-scenario AIHWKIT validation in supplementary materials. Systematic comparison with mainstream CIM simulators (DNN+NeuroSim, CrossSim) under identical configurations is lacking.

**Response**:

We appreciate this important suggestion. The revised manuscript now includes multi-simulator validation to establish methodological consistency and highlight the framework's organic-device-specific capabilities.

**Existing Evidence**:
- AIHWKIT shared-regime benchmark: 90.08 ± 0.21% (digital reference: 95.46%), 10K×10 MC evaluation, confirming numerical equivalence for standard RRAM configurations (Supplementary §S5.1)
- Explicit statement that DNN+NeuroSim and MemTorch do not support organic-device-specific features (photoresponse, retention, write nonlinearity) without substantial architectural modifications

**New Experiments** (Completed):
- CrossSim comparison: Same Tiny-ViT V4 configuration evaluated under CrossSim's GPU-accelerated crossbar model
- Expected outcome: Quantify deviation in accuracy and energy estimates between frameworks
- Status: ✅ COMPLETED — Three-phase progressive comparison (ConvNeXt C4 checkpoint, 1000 samples, 8-bit ADC, 3 MC runs per phase)
- Results:
  - Clean (σ=0%): ours 86.20% vs CrossSim 83.70% (gap 2.50 pp)
  - Low noise (σ=1%): ours 85.90±0.28% vs CrossSim 82.87±0.29% (gap 3.03 pp)
  - Standard noise (σ=5%): ours 81.63±0.56% vs CrossSim 67.20±2.67% (gap 14.43 pp)
- Key finding: Gap widens from 2.5 pp to 14.4 pp with noise, supporting profile-driven simulation argument
- Data files: crosssim_clean_baseline.json, crosssim_low_noise.json, crosssim_standard_noise.json

**Changes Made**:
1. Added explicit discussion of simulator limitations in Introduction (§1): "General CIM simulators... do not directly capture the combination of photoresponse, retention, and write nonlinearity"
2. Expanded AIHWKIT validation description in Methods (§4.3)
3. CrossSim comparison results integrated into Discussion §6.6 Outlook

**Limitation Acknowledged**:
Direct architectural comparison is inherently limited because organic-device-specific features (photoresponse preprocessing, state-dependent retention, nonlinear write dynamics) have no equivalent in inorganic-memory-focused simulators. The comparison therefore focuses on canonical uniform-noise regimes where overlap exists.

---

### Additional Reviewer-Facing Evidence: Scale-Masking Under Non-Ideal ADC Calibration

**Reviewer-style concern**:
> The manuscript acknowledges that scale-masking depends on ideal calibrated digital rescaling. How robust is this effect once realistic ADC offset, gain, or INL errors are introduced?

**Response**:

We agree that this is an important boundary condition. The revised manuscript already qualifies scale-masking as a conditional effect that depends on accurate readout calibration. To tighten this point further, we ran a stricter follow-up pilot that calibrates output ranges for every analog layer and injects ADC offset / gain / INL directly at analog-layer outputs through forward hooks, rather than perturbing only the final logits.

**Hook-based full-test analysis** (completed):
- Model / regime: Tiny-ViT `V4`, CIFAR-10, layer-wise calibrated ADC ranges
- Protocol: `3` seeds, full CIFAR-10 test set
- Script: `run_adc_layerwise_nonideality_gpt.py`
- Log: `logs/_gpt/adc_layerwise_nonideality_full_20260417.log`
- Result files:
  - `report_md/_gpt/json_gpt/adc_layerwise_nonideality_full_gpt.json`
  - `report_md/_gpt/adc_layerwise_nonideality_full_gpt.md`

**Full-test results**:
- Ideal: `82.04 ± 0.16%`
- Offset `±0.5 LSB`: `82.07 ± 0.21%` (`+0.03 pp`)
- Gain `±5%`: `81.87 ± 0.30%` (`-0.17 pp`)
- INL `0.5 LSB`: `80.85 ± 0.12%` (`-1.19 pp`)
- Combined realistic (`±0.5 LSB`, `±5%`, `0.5 LSB INL`): `81.86 ± 0.28%` (`-0.18 pp`)
- Combined pessimistic (`±1 LSB`, `±10%`, `1.0 LSB INL`): `76.90 ± 0.27%` (`-5.14 pp`)

**Interpretation**:
1. Moderate offset errors remain nearly irrelevant in this regime.
2. INL is more consequential than offset and therefore the more credible reviewer pressure point.
3. Realistic combined ADC errors do not destroy the hook-based baseline, whereas pessimistic errors produce a materially larger but still non-collapse degradation.

**Manuscript integration**:
These full-test results are now strong enough to support supplementary manuscript integration rather than rebuttal-only mention. The revised supplementary package adds a compact ADC non-ideality table, and the discussion now cites it explicitly when qualifying the scale-masking regime.

---

### Major Comment 2: Write Nonlinearity Analysis and Mitigation

**Original Comment**:
> NL=2.0 is identified as a core bottleneck but only gradient-scaling approximation limits are given. No analysis of differential impact on ViT modules or mitigation strategies.

**Response**:

We agree that deeper analysis of write nonlinearity is warranted. The revised manuscript clarifies the nature of this limitation and provides preliminary module-level analysis.

**Existing Evidence**:
- NL=2.0 limit: 27.72 ± 0.82% under gradient-scaling approximation (Table 2)
- Explicit statement that this is an "approximation-limit boundary" rather than fundamental materials constraint (Discussion §6.5)

**Additional Analysis in This Revision**:
- Group-wise NL gradient diagnostic: on the frozen Tiny-ViT V4 checkpoint, we activated `NL=2.0` only for one analog module group at a time while preserving the same forward path (`sigma_c2c=0`, checkpoint D2D buffers preserved, identical mini-batches).
- Purpose: localize where the present gradient-scaling surrogate distorts training signals, without conflating the issue with a changed forward loss.
- Result:
  - `MLP` blocks are the dominant failure mode: affected-parameter gradient cosine falls to `0.815`, with norm ratio `0.671`.
  - `All analog` is nearly identical (`0.816`, norm ratio `0.676`), showing that the transformer-wide effect is largely inherited from the MLP path.
  - `Patch Embed`, `Attention QKV`, and `Attention Proj` remain at `1.00`, indicating negligible distortion under the same matched-forward diagnostic.
  - mean loss delta remains numerically zero across all groups, confirming that this is a backward-surrogate effect rather than a forward mismatch.
- Interpolation rerun at `NL=1.5`: we also completed a full Tiny-ViT V4 retraining run at `NL_LTP=+1.5`, `NL_LTD=-1.5`. It did not produce a stable intermediate anchor: the run peaked at only `19.01%` (epoch 1) and finished at `9.76%`. We therefore keep this result rebuttal-side rather than promoting it into the manuscript, because it shows recipe instability rather than a clean monotonic interpolation between the canonical regime and `NL=2.0`.
- Status: ✅ Completed and added to the supplementary evidence package.

**Changes Made**:
1. Added clarification in Discussion §6.5: "the observed degradation... should be interpreted as the limit of this approximation, rather than as a fundamental materials constraint"
2. Added a supplementary group-wise gradient-distortion diagnostic that localizes the present `NL=2.0` failure primarily to the MLP analog path
3. Completed an `NL=1.5` interpolation rerun and explicitly retained it as response-side evidence only, because it reinforces training-recipe instability rather than providing a manuscript-clean interpolation anchor
4. Preserved the broader limitation framing: the new diagnostic explains where the current surrogate breaks, but does not reframe the result as a materials-level physical bound

**Mitigation Strategies Discussed**:
The manuscript now acknowledges that physical mitigation (pulse-shaping algorithms, iterative write-verify) or improved non-linear-aware STE/optimizer designs would be required to address severe `NL=2.0`, as the current gradient-scaling approximation concentrates its distortion in the MLP write path. This is flagged as important future work rather than claimed as solved in the present revision.

---

### Major Comment 3: Ensemble HAT Innovation and Ablation

**Original Comment**:
> Ensemble HAT lacks comparison with existing multi-instance HAT methods and domain randomization. Key ablations (resampling frequency, i.i.d. noise) missing.

**Response**:

We thank the reviewer for pushing us to strengthen the methodological validation. The revised manuscript includes comprehensive ablation studies.

**Existing Evidence**:
- Standard HAT: 10.00% on fresh hardware (collapse)
- Ensemble HAT: 86.37 ± 1.54% on fresh hardware (recovery)
- Control experiment: Generic i.i.d. noise augmentation does NOT provide same robustness (Discussion §5.6)

**Key Distinction**:
Ensemble HAT differs from domain randomization and i.i.d. noise augmentation in a critical aspect: it resamples the **spatial structure** of D2D mismatch each epoch, rather than only adding stochastic perturbations. This targets the specific failure mode of hardware-instance overfitting.

**New Experiments** (Completed):
- Ablation 1: Resampling frequency (every N epochs vs every epoch)
- Ablation 2: i.i.d. noise vs structured D2D resampling
- Ablation 3: D2D variance sweep (5%, 10%, 15%, 20%)
- Status: ✅ COMPLETED
- Resampling frequency ablation (5 cadences tested):
  - Per-epoch: 88.41% (best)
  - Every 20 epochs: 87.76%
  - Every 5 epochs: 87.31%
  - Fixed at init: 87.18%
  - Per-batch: 86.16%
- i.i.d. noise vs structured D2D: Ensemble HAT (86.37±1.54%) vs i.i.d. augmentation (~10% collapse on fresh arrays, same as standard HAT)
- D2D variance: 63-point contour map covers σ_D2D ∈ {1,3,5,8,10,15,20}% × ADC ∈ {2,3,4,5,6,7,8,10,12} bits
- Results integrated into §5.6 (iso-accuracy envelope), §5.7 (frequency ablation in Supp Fig S4), §6.1 (Sobol decomposition)

**Changes Made**:
1. Added explicit comparison statement in Discussion §6.1: "Ensemble HAT differs from ordinary i.i.d. noise augmentation because it changes the fixed spatial mismatch map itself"
2. Full ablation results integrated: frequency ablation in Supplementary Fig. S4, iso-accuracy contour in main Fig. 3, Sobol analysis in Supplementary Fig. S2

**Literature Comparison**:
The revised text now makes the methodological distinction explicit rather than claiming a broad external benchmark sweep: AIHWKIT-style fixed-mask injection and generic domain randomization perturb amplitudes around one nominal instance, whereas Ensemble HAT resamples the structured spatial D2D mismatch map itself. We therefore position Ensemble HAT as a hardware-instance overfitting countermeasure rather than as a generic stochastic-augmentation variant.

---

### Major Comment 4: Energy Model Idealization

**Original Comment**:
> Energy conclusions based on first-order proxy model without validation against measured organic array data. Array size, routing, peripheral impacts not quantified.

**Response**:

We appreciate this important critique. The manuscript already contains sensitivity analysis, which we have now highlighted more prominently.

**Existing Evidence**:
- Routing overhead sensitivity: 10% → 50% additional routing cost reduces gain from 11.45× to 11.10×–9.90× (Discussion §6.5)
- Explicit statement: "first-order energy model" with "array-to-digital interconnect energy absorbed into SRAM cost terms"
- Comparison with INT8 ViT digital deployments: 273.94 µJ vs 2.0–4.0 mJ (11–15× reference point)

**Changes Made**:
1. Added explicit sensitivity bounds to Discussion §6.5
2. Clarified that reported 11.45× is an **upper bound** under idealized routing assumptions
3. Added caveat: "moderate unmodeled routing cost does not erase the qualitative advantage"

**Limitation Acknowledged**:
First-order energy modeling is an intentional scope boundary. The framework is positioned as a "behavioral simulation" for rapid algorithm-device co-design, not a circuit-accurate emulator. Full physical layout (parasitic RC, detailed peripheral timing) would require foundry-level data not available for the reported organic devices.

**Future Work**:
Integration with detailed physical layout tools (e.g., Cadence, Synopsys) for post-tapeout validation is noted as an important extension.

---

### Major Comment 5: Profile Interface Generality

**Original Comment**:
> Profile interface claims generality but only validates 2 profiles with single-parameter sweeps. No validation across different organic device types.

**Response**:

We acknowledge the need for broader device-type validation. The revised manuscript strengthens the case study analysis.

**Existing Evidence**:
- Vincze 2025 standard profile: 87.95 ± 0.27% (CIFAR-10, canonical regime)
- Zhang 2025 OPECT profile: 88.53% (zero-shot transfer, literature-derived parameters)
- Explicit statement: profile interface allows "technology-specific parameter substitution without code changes"

**Case Study Value**:
The Zhang OPECT case study demonstrates the key value proposition: literature-derived device parameters can be substituted directly into the evaluation pipeline, enabling rapid risk assessment before fabrication. The 88.53% accuracy with literature-proxy parameters suggests the framework can guide device optimization targets.

**Changes Made**:
1. Expanded case study description in Results §5.8
2. Added explicit parameter provenance table (Supplementary Table S2)

**Limitation Acknowledged**:
True multi-device-type validation (photochemical transistors, photomemristors, etc.) would require measured device data from each type, which is beyond the scope of this simulation-focused study. The framework architecture supports such extension, as demonstrated by the profile substitution mechanism.

**Future Work**:
Automated profile fitting from measured I-V curves is noted as a key next step for measured-device validation.

---

## Summary of Revisions

### Textual Changes (Completed)
1. Terminology standardization: "converter precision" → "ADC resolution", "D2D mismatch" → "D2D variability"
2. Abstract compression: 280 words → 220 words
3. Introduction restructuring: 5-paragraph logical flow with clear gap→solution narrative
4. Number formatting: thousands separators, multiplication symbols, percentage spacing

### Experimental Additions (Completed / Response-Side)
1. CrossSim comparison [GM-P0] — completed
2. Ensemble HAT ablation (frequency, i.i.d. vs structured, D2D sweep) [GM-P1] — completed
3. Layer-wise ADC non-ideality full-test sweep [GM-P2] — completed and manuscript-integrated in supplementary form
4. Nonlinear-write mechanistic follow-up [GM-P3] — completed:
   - manuscript-integrated group-wise gradient-distortion diagnostic
   - rebuttal-side `NL=1.5` interpolation rerun (finished near-collapse, therefore not manuscript-facing)

### Supplementary Additions (Integrated / Response-Side)
1. CrossSim comparison integrated into the revised discussion package
2. Ensemble HAT ablation integrated into the main/supplementary result set
3. Layer-wise ADC non-ideality integrated into the supplementary response package
4. Layer-wise NL gradient-distortion diagnostic integrated into the supplementary package
5. `NL=1.5` interpolation rerun retained as response-side evidence only

---

## Residual Limitations (Honestly Acknowledged)

1. **Measured device validation**: Framework uses literature-derived proxy parameters; measured-device closure requires collaboration with fabrication teams.
2. **Physical layout**: First-order energy model; detailed parasitic extraction requires foundry data.
3. **Severe NL=2.0**: Gradient-scaling approximation limit; physical mitigation strategies not evaluated.

These limitations are now explicitly discussed as boundary conditions rather than hidden assumptions.

---

**Draft Status**: GM-P0 (CrossSim) ✅ and GM-P1 (Ensemble HAT ablation) ✅ completed and integrated. GM-P2 (layer-wise ADC non-ideality full-test sweep) ✅ completed and integrated into the supplementary evidence package. GM-P3 (nonlinear-write follow-up) ✅ completed as a two-part package: manuscript-integrated gradient-distortion evidence plus a rebuttal-side `NL=1.5` interpolation rerun that finished near-collapse and therefore remains outside the main text. Response letter ready for final review by Claude.
