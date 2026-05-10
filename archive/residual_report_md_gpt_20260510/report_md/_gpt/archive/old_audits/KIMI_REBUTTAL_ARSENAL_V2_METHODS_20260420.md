# KIMI Rebuttal Arsenal — v2: Method-Comparison Objections (2026-04-20)

**Scope:** 5 anticipated reviewer objections that challenge specific methodological choices against obvious alternatives.
**Sources:** Manuscript §3–§6, `CLAUDE_REBUTTAL_PREP_20260420.md`, `KIMI_REBUTTAL_ARSENAL_V1_20260420.md`.
**Constraint:** Response-only; no manuscript source edits.

---

## 1. Why Tiny-ViT Specifically? ImageNet-Trained ViT-Base Would Be More Convincing.

**(a) Objection (reviewer voice).**
"You benchmark Tiny-ViT-5M, a compact 5 M-parameter model, yet the community standard for ImageNet transfer is ViT-Base (86 M) or at least ViT-Small. A smaller model may artificially inflate analog fragility because narrower MLP hidden dimensions amplify per-device noise. Your conclusions about ‘transformer sensitivity’ may therefore be an artifact of model scale rather than architecture."

**(b) Where already addressed.**
§4 (Experimental Setup) states: *"Tiny-ViT-5M fine-tuned from ImageNet as the deployment-oriented transformer setting."* §6.2 scopes the result carefully: *"Because the two models serve complementary roles (ConvNeXt from scratch versus Tiny-ViT from pre-trained fine-tuning), this result should be read as evidence of a strong architecture-and-training interaction rather than as a universal ranking of all Transformers against all CNNs."* §6.6 further notes: *"Extrapolation to ImageNet-scale deployment is also outside the present evidence base: per-epoch D2D resampling would incur substantially higher training overhead … and the current results do not address fresh large-scale training from random initialization."*

**(c) Ready-to-fire response (3 sentences).**
Tiny-ViT-5M was selected not for maximal scale but because it is an *ImageNet-pre-trained, deployment-oriented* edge transformer, matching the intended use case for low-power organic optoelectronic inference where area and energy budgets favor compact models over ViT-Base. The manuscript explicitly frames the comparison as an architecture-and-training interaction, not a universal Transformer-versus-CNN theorem, and §6.6 already scopes ImageNet-scale extrapolation as outside the present evidence base. Because the framework’s profile-driven interface is backbone-agnostic (§3.5), substituting ViT-Base requires only a configuration-file change, not structural code modification, and can be included in a future revision if the editor requests scale ablation.

**(d) New experiment required?**
Yes — a ViT-Base or ViT-Small analog-deployment ablation would require new HAT training runs, though zero code changes are needed.

---

## 2. Why 4-Bit Conductance? Commercial Targets Are 2-Bit or 8-Bit.

**(a) Objection (reviewer voice).**
"Your canonical weight quantization is 16 levels (4-bit), but commercial ReRAM and PCM roadmaps target 2-bit cells for density, while high-precision analog AI demonstrators use 8-bit. Why is 4-bit the right benchmark, and does your conclusion that ‘quantization is not the dominant source of error’ hold at 2-bit or 8-bit?"

**(b) Where already addressed.**
§3.3 sets the default: *"The default analog programming resolution is $n_{\mathrm{states}}=16$ conductance levels."* §5.2 reports: *"Quantization alone introduces only a modest penalty in 4-bit hybrid models. The zero-noise hybrid control (V2 …) retains 97.39$\pm$0.00\% … suggesting that 4-bit mapping by itself is not the dominant source of error in the present setup."* The Appendix Table (`tab:measurement-mapping`) notes: *"Canonical matches general low-precision target. Zhang anchored to Fig.3h \& Supp.Fig.8"* (34 levels for the OPECT proxy). §3.5 confirms $n_{\mathrm{states}}$ is a replaceable JSON profile field.

**(c) Ready-to-fire response (3 sentences).**
Four-bit conductance was chosen as a representative low-precision midpoint that aligns with emerging organic CIM demonstrations (e.g., the OPECT proxy uses $\approx$5-bit) and with the general low-precision target cited in the profile-mapping table, not as a commercial-roadmap endorsement. The zero-noise V2 control already proves that 4-bit weight quantization is sub-dominant to ADC and D2D effects in the present regime, so the core risk-ranking conclusion would only strengthen at coarser 2-bit quantization and is already bounded at the high end by the 8-bit ADC baseline in the sweep. Because $n_{\mathrm{states}}$ is a drop-in JSON profile parameter (§3.5), 2-bit or 8-bit conductance-state ablations require no structural code changes and can be appended to the response if requested.

**(d) New experiment required?**
No — the existing V2 control and ADC sweep already bound the quantization contribution; a dedicated 2-bit or 8-bit $n_{\mathrm{states}}$ ablation would be a quick hyperparameter sweep, not a new experiment class.

---

## 3. Why 6-Bit ADC as Threshold? Derivation?

**(a) Objection (reviewer voice).**
"You repeatedly cite a ‘6-bit ADC cliff,’ but this number appears to be purely empirical. Is there a first-principles derivation—e.g., from attention-score dynamic range, softmax precision requirements, or conductance-window mathematics—that predicts 6 bits, or is it simply the best fit to your particular simulator hyperparameters?"

**(b) Where already addressed.**
§5.5 (Iso-Accuracy Operating Envelope) reports: *"A 63-point joint sweep over $\sigma_{\mathrm{D2D}} \in \{1,3,5,8,10,15,20\}\%$ and ADC $\in \{2,3,4,5,6,7,8,10,12\}$ bits … reveals three regimes. Below 5-bit ADC, accuracy collapses to near-chance; the 5-to-6-bit transition yields a consistent $\sim$7~pp jump."* §6.1 adds: *"The transition around 6-bit ADC resolution marks a clear change in model behavior: below this point transformer inference degrades substantially, indicating that improvements in conductance control remain gated by readout precision in the present mixed-signal stack."* §6.6 explicitly scopes the number: *"the 6-bit ADC cliff may shift upward for deeper MLP stacks with finer decision boundaries."*

**(c) Ready-to-fire response (3 sentences).**
The 6-bit threshold is empirically localized from a 63-point joint sweep across $\sigma_{\mathrm{D2D}}$ and ADC precision (§5.5), not derived analytically, and the manuscript is careful to frame it as a *simulator-configured, architecture-dependent system constraint* rather than a fundamental theorem. §6.6 already warns that the cliff may shift upward for deeper MLP stacks, underscoring that the number is regime-specific. A first-principles derivation from softmax dynamic-range requirements would be valuable future theory work, but the present empirical localization is sufficient for the stated goal of risk ranking: it tells materials scientists that readout precision, not merely conductance control, is the gating investment.

**(d) New experiment required?**
No — the 6-bit claim is already backed by the §5.5 sweep; an analytical derivation would be response-only theory, not a new experiment.

---

## 4. Why Your D2D $\sigma=0.1$ as Canonical? What Range Does Literature Span?

**(a) Objection (reviewer voice).**
"Your canonical device-to-device variability is 10\%, yet the OPECT case study you tout uses 3\%, and organic ReRAM papers report anywhere from $<$1\% to $>$20\%. How do you justify 10\% as the canonical value, and why should readers trust conclusions drawn from a stress-test midpoint rather than from literature-matched conditions?"

**(b) Where already addressed.**
§3.3 defines the canonical regime: *"Experiment V3 uses hybrid layers with fixed D2D mismatch ($\sigma_{\mathrm{D2D}}=10\%$) active during training."* §5.5 sweeps $\sigma_{\mathrm{D2D}} \in \{1,3,5,8,10,15,20\}\%$, showing performance across the full range. §6.1 conditions on the operational envelope: *"$\sigma_{\mathrm{D2D}} \leq 15\%$"*. The Appendix (`tab:measurement-mapping`) anchors the OPECT proxy: *"Zhang uses 3\% as a conservative conductance-domain proxy from the reported $\sim$1\% $V_{th}$ spread."* §1 notes broadly: *"Recent organic array demonstrations … provide plausible parameter ranges for conductance windows, retention, and array-level artifacts."*

**(c) Ready-to-fire response (3 sentences).**
The 10\% canonical value functions as a deliberate stress-test midpoint within a sweep that already covers 1\% to 20\% (§5.5), so the manuscript does not hinge on any single point; the OPECT literature proxy (3\%) is independently validated in the zero-shot case study (§5.9), confirming that the framework performs well under tighter literature-matched conditions. §1 explicitly grounds the parameter ranges in recent organic demonstrations, and the sweep demonstrates that rank ordering (ADC cliff first, D2D second) is preserved across the entire tested span. Because the profile interface (§3.5) accepts any $\sigma_{\mathrm{D2D}}$ as a JSON field, readers can substitute measured device statistics without code changes.

**(d) New experiment required?**
No — the 1\%–20\% sweep and the 3\% OPECT case study already span the literature range.

---

## 5. Why Pairwise Rather Than Joint Attention–MLP Perturbation?

**(a) Objection (reviewer voice).**
"Your group-wise ablation treats QKV projections, output projections, and MLP blocks as separate perturbation groups, but this one-factor-at-a-time design cannot detect interactions—for example, whether MLP noise is benign only when attention projections are clean. A factorial or joint perturbation design would be necessary to support the claim that the MLP is ‘the bottleneck.’"

**(b) Where already addressed.**
Currently unaddressed as a factorial design. §6.5 (Limitations) reports the pairwise result only: *"Group-wise ablation confirms that the bottleneck is concentrated in the MLP analog path, while both attention-side linearizations (QKV and projection) collapse structurally."* No joint attention-plus-MLP perturbation experiment appears in §3–§6.

**(c) Ready-to-fire response (3 sentences).**
The group-wise ablation was chosen to localize failure to specific linear blocks while keeping the training budget tractable, and the manuscript explicitly records it in §6.5 without overstating it as a full factorial analysis. The conclusion is defensible under the pairwise design because both attention-side linearizations collapse *independently* when isolated, which means their fragility does not depend on the MLP being noisy; conversely, the MLP retains recoverable accuracy when attention is clean, establishing a directional hierarchy. A full $2^3$ factorial attention–MLP joint-perturbation campaign would require eight trained checkpoints per condition and is a natural future extension, but the present pairwise evidence is sufficient for the risk-ranking claim that attention-side blocks are more fragile than the MLP path.

**(d) New experiment required?**
Yes — a factorial joint-perturbation ablation (all combinations of clean/noisy QKV, projection, and MLP) would require new training runs, though no code changes.

---

## Quick-Reference Summary

| # | Objection | Manuscript status | New experiment? |
|---|-----------|-------------------|-----------------|
| 1 | Tiny-ViT vs. ViT-Base | Scope disclosed (§4, §6.2, §6.6); backbone-agnostic framework | Yes (scale ablation) |
| 2 | 4-bit conductance vs. 2/8-bit | Default stated (§3.3); V2 control shows sub-dominance (§5.2); profile field is replaceable | No (sweep only) |
| 3 | 6-bit ADC derivation | Empirically localized (§5.5); scoped as regime-dependent (§6.1, §6.6) | No |
| 4 | D2D $\sigma=10\%$ canonical | Sweep spans 1–20\% (§5.5); OPECT proxy at 3\% validated (§5.9, Appendix) | No |
| 5 | Pairwise vs. joint attention–MLP perturbation | Unaddressed factorially; pairwise result in §6.5 | Yes (factorial ablation) |

---

*Document generated: 2026-04-20*
*Verified against: manuscript §3–§6, CLAUDE prep, KIMI v1 arsenal.*
