# Codex Review of Kimi T6/T7 Drafts

**Date:** 2026-04-23 17:56 CST
**Reviewer:** Codex
**Scope:** Review `T6_SNEAK_PATH_LIMITATIONS_DRAFT_20260423.md` and `T7_DIGITAL_QUANTIZATION_LITREVIEW_20260423.md` for correctness and paper-safety.

## Executive Verdict

T6 is directionally useful but contains one unsafe quantitative claim. T7 has useful source material, but one named-method description is wrong and the comparison to our TinyViT/CIFAR-10 result is currently too strong.

Do not paste either draft into the manuscript unchanged.

## T6 Review: Sneak Path / Circuit-Level Omissions

### What Is Correct

- It is correct to describe our simulator as a first-order behavioral model rather than a circuit-level crossbar simulator.
- It is correct that the current code does not model sneak paths, full spatial IR-drop networks, selector behavior, detailed peripheral nonidealities, or interconnect/data-marshaling energy.
- It is correct to frame reported accuracy/energy as optimistic relative to fabricated CIM hardware.
- It is appropriate to reference circuit-level tools such as NeuroSim / DNN+NeuroSim / RxNN as complementary rather than competing frameworks.

### Required Fix

The phrase claiming sneak paths can introduce `5-15% additional error` is not safe as written. I did not find that exact range in the checked primary/near-primary sources. Replace it with a supported, broader statement:

> Prior resistive-crossbar studies report that circuit/device nonidealities such as interconnect parasitics, peripheral circuits, sneak paths, and process variation can produce material DNN accuracy degradation; for example, RxNN reports `9.6%-32%` degradation across large-scale DNNs under modeled crossbar nonidealities.

### Suggested T6 Replacement Wording

> Our framework should be interpreted as a first-order behavioral simulator, not a circuit-level crossbar emulator. It captures quantization, programmed conductance noise, device-to-device mismatch, cycle-to-cycle noise, nonlinearity, and retention at the behavioral level, but it does not solve the full crossbar circuit equations. In particular, it omits sneak-path leakage, spatial IR-drop through word/bit-line resistance, selector-device behavior, detailed peripheral DAC/ADC nonidealities, and dedicated routing/interconnect costs. Prior resistive-crossbar simulation frameworks such as RxNN and DNN+NeuroSim show that these effects can materially degrade DNN accuracy and chip-level energy/latency estimates. Therefore, our reported accuracy and energy should be treated as optimistic architecture-level estimates; tape-out-oriented predictions would require coupling this behavioral model to circuit-level simulators.

## T7 Review: Digital Quantization Baseline

### Source Checks

| Draft claim | Review |
|---|---|
| FQ-ViT reports DeiT-B `81.20%` with all modules 8-bit and `80.85%` with 4-bit attention maps | Correct. FQ-ViT says DeiT-B full precision is `81.85%`, FQ-ViT gets `81.20%` at `8/8/8`, and `80.85%` with attention maps compressed to 4-bit. |
| PTQ4ViT has `<0.5%` drop at 8-bit | Correct. The abstract and results state less than `0.5%` drop at W8A8. |
| PTQ4ViT has about `2.1%` average drop at 6-bit | Correct. The paper states PTQ4ViT has `2.1%` average drop at 6-bit, while base PTQ is much worse. |
| PTQ4ViT 4-bit is poor without mixed precision / correction | Correct. Their Table 2 shows DeiT-B W4A4 PTQ4ViT is `60.91%`; with bias correction `64.39%`; mixed-precision Liu baseline is `75.94%`. |
| Q-ViT uses an information rectification module | Incorrect. The checked Q-ViT paper describes head-wise bit-width allocation and switchable scale, not an information rectification module. |
| Q-ViT pushes ViT quantization to 3-bit | Correct directionally, but describe it as QAT/mixed bit-width learning, not PTQ. |

### Required T7 Fixes

1. Replace the Q-ViT sentence with:

> Q-ViT (Li et al., 2022) is a quantization-aware training method that learns quantization scales and bit-widths, using head-wise bit-width allocation and switchable scale to improve low-bit ViT quantization; it reports improvements at 3- and 4-bit settings relative to LSQ+.

2. Soften the comparison between our TinyViT/CIFAR-10 result and ImageNet DeiT/Swin literature. Do not say our result is "comparable to or better than" those PTQ baselines. The datasets, models, and quantization protocols differ.

3. Replace the final inference with a narrower claim:

> These ViT quantization papers provide context that low-bit transformer quantization is itself a hard problem. Our same-instance TinyViT/CIFAR-10 result shows that, in our controlled setting, the additional analog C2C/D2D perturbations do not dominate the source-domain accuracy loss. It does not by itself establish cross-instance robustness, which R1 shows remains weak.

## Revised T7 Paragraph Candidate

> Digital quantization provides an important baseline for interpreting the degradation observed in our analog CIM setting. Prior ViT quantization work shows that transformer architectures are sensitive to low-bit deployment: FQ-ViT reports DeiT-B top-1 accuracy of `81.20%` when all modules are quantized to 8-bit and `80.85%` when attention maps are compressed to 4-bit, compared with `81.85%` full precision; PTQ4ViT reports near-lossless 8-bit PTQ but still around `2.1%` average degradation at 6-bit and much poorer fully 4-bit PTQ without mixed precision or correction; Q-ViT further shows that pushing ViTs to 3- or 4-bit typically requires quantization-aware training with component-wise bit allocation. These results suggest that low-bit transformer deployment is already a nontrivial baseline even before analog device noise is introduced. In our TinyViT/CIFAR-10 source-domain setting, the small drop from FP32 to 4-bit noisy inference indicates that C2C/D2D perturbations are not the dominant same-instance bottleneck. Cross-instance transfer remains a separate failure mode and must be evaluated with fresh D2D realizations rather than inferred from source accuracy.

## Sources Checked

- FQ-ViT, IJCAI 2022: `https://www.ijcai.org/proceedings/2022/0164.pdf`
- PTQ4ViT, arXiv 2111.12293 / ECCV 2022: `https://arxiv.org/abs/2111.12293`
- Q-ViT, arXiv 2201.07703: `https://arxiv.org/abs/2201.07703`
- RxNN, arXiv 1809.00072 / TCAD 2020: `https://arxiv.org/abs/1809.00072`
- DNN+NeuroSim V2.0, arXiv 2003.06471: `https://arxiv.org/abs/2003.06471`
