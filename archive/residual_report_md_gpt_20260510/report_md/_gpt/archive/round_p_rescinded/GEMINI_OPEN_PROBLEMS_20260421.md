# Open Problems After This Paper

Under severe nonlinear-write dynamics, analog ViTs hit a ~30 % fresh-instance ceiling no existing mitigation fully breaks. That ceiling is a signpost, not an endpoint. Here are eight questions most likely to move the field from diagnosis to cure.

---

## 1. Higher-Order NL Surrogates
Can second- or third-order conductance-update models raise the ~30 % ceiling, or is the bound structural for any smooth nonlinearity? If the ceiling is only a first-order artifact, the limit narrative shifts from physics to model error. We know power-law surrogates miss curvature near filament saturation, which dominates the conductance tail. We do not know whether curvature-corrected gradients enable transferable compensations across independent instances. *First experiment:* train Tiny-ViT with a second-order surrogate (κ = 0.5) at NL = 2.0; ≥ 50 % fresh-instance accuracy falsifies the bound, ≤ 35 % confirms it.

## 2. Attention-Free Architectures
Can Mamba or pooling backbones replace softmax attention under severe crossbar nonlinearity? If the bottleneck is softmax’s exponential sensitivity to QK noise, removing it may sidestep collapse. We know linearizing QKV or attn_proj under NL = 2.0 causes immediate collapse, implicating the mechanism itself. We do not know whether state-space models merely shift fragility to a different path. *First experiment:* run the identical device-profile sweep on Mamba-Tiny and PoolFormer-S12; compare fresh-instance curves head-to-head against the ViT baseline.

## 3. Hardware-in-the-Loop Validation
Does the ~30 % ceiling survive contact with physical RRAM, PCM, or FeFET arrays? All current evidence rests on simulation; real silicon can reveal spatial correlations and programming dynamics that surrogates miss. We know CrossSim reproduces measured single-device I-V curves, but not full-array parasitics. We do not know whether on-chip noise tightens the ceiling further or behaves more benignly than worst-case models. *First experiment:* port a small pre-trained analog ViT (≤ 1 M weights) to a 130 nm RRAM or 22 nm FeFET test chip; report CIFAR-10 accuracy across ten fresh programming cycles.

## 4. Temperature + Retention Joint Model
How do thermal drift and conductance retention interact on the same Arrhenius-enabled device? Real deployments experience both simultaneously; treating them independently may underestimate combined distortion. We know retention follows a double-exponential envelope and temperature modulates conductance via an Arrhenius prefactor. We do not know whether temperature-accelerated retention loss creates a time-dependent accuracy cliff. *First experiment:* evaluate Ensemble HAT under a joint profile (−20 °C, 25 °C, 85 °C) at 1 s, 1 h, and 1 d retention ages; fit a bivariate degradation surface.

## 5. Full-Array IR Drop + Sneak Paths
Do line resistance and sneak paths modify the ~30 % ceiling, or merely add uniform bias? Array-level parasitics dominate large crossbars; if they reshape the attention distribution, the limit tightens. We know static IR-drop matrices on 128 × 64 preserve ranking (Kendall’s τ ≥ 0.95), but sneak paths are neglected. We do not know the geometry at which parasitics become non-rank-preserving. *First experiment:* integrate a SPICE-extracted sneak-path surrogate; sweep geometry from 64 × 64 to 512 × 512 and locate the τ = 0.95 threshold.

## 6. Language-Model CIM
Do the same nonlinear-write limits apply to LLM inference on analog arrays? LLMs drive accelerator roadmaps; if the limits transfer, analog CIM may be relegated to shallow CNNs. We know LLM transformers share the same QK-softmax structure as ViTs, but operate at far larger scale. We do not know whether billion-parameter averaging suppresses device noise or whether higher dynamic-range weights exacerbate saturation. *First experiment:* simulate a 125 M–1 B parameter layer on the nonlinear-write surrogate; measure perplexity degradation versus NL and locate the cliff.

## 7. Optimal ADC Design
Can custom ADC architectures mitigate the observed 6-bit cliff? Relaxing the floor would halve ADC area and power while preserving throughput. We know the cliff arises because softmax requires ~10 effective quantization levels per standard deviation of QK scores. We do not know whether dynamic range adaptation or learned codebooks can recover necessary precision with fewer raw bits. *First experiment:* replace uniform ADC quantization with a per-head Lloyd-Max codebook at 4–6 bits; compare attention-map KL divergence and downstream accuracy.

## 8. Process-Variation-Aware Training
Can foundry statistical data improve Ensemble HAT beyond Gaussian Monte-Carlo resampling? If the training prior matches true fabrication distributions, the ensemble can regularize toward physically realizable weights. We know real arrays exhibit spatially correlated, heavy-tailed variation that Gaussian resampling smooths over. We do not know whether measured wafer maps reduce fresh-instance variance. *First experiment:* replace Gaussian D2D draws with spatially correlated heavy-tailed samples from foundry kits; retrain Tiny-ViT and measure fresh-instance mean and variance.

---

These problems form a web, not a list. A breakthrough in ADC design may be nullified by IR drop; an attention-free architecture may buy headroom that variation-aware training then seals. The ceiling is either real or removable—but it will yield only to disciplined, cross-layer inquiry.
