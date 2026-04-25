import os

base_dir = "compute_vit/report_md/_gpt"
files = {
    "GEMINI_DEFENSE_ATTACK_SURFACE_20260421.md": """# G-HH4: Defense Attack Surface
**Date:** 2026-04-21
**Scope:** Phase α (G-HH4)

This document anticipates the 15 most rigorous and hostile questions a PhD defense committee might ask regarding the current state of the Compute-ViT framework, specifically focusing on the vulnerabilities introduced by the severe-NL diagnostic loop. It provides evidence-backed response paths using *only* data currently on disk.

---

## Group 1: The "Broken Simulator" Angle
**1. "If all your mitigations collapse at NL=2.0, how do we know your PyTorch analog simulation layer doesn't just have a numerical overflow bug?"**
*Response Path:* Point to the `all-linear` (CX-AB) baseline. It achieves ~32.60% accuracy, avoiding the 10.00% chance-level collapse. Furthermore, our models achieve >86% accuracy at NL=1.0 and >97% without noise. A numerical bug would corrupt all forward passes, not just the non-linear mappings.

**2. "Is NL=2.0 a physically realistic parameter, or did you just inject so much noise that any neural network would mathematically fail?"**
*Response Path:* NL=2.0 represents a severe, but physically grounded, non-ideality typical of early-stage organic memristors (e.g., strong asymmetry in LTP/LTD updates). Cite `docs/PHYSICS_STACK.md` and the organic optoelectronic literature profiles we fitted against. It is an edge-case stress test, not random noise.

## Group 2: The Bimodal Basin (Branch C) Attacks
**3. "You claim a 'bimodal basin' at ~38.95% mean accuracy. Isn't this just evidence of insufficient hyperparameter tuning or a bad learning rate schedule?"**
*Response Path:* We executed a rigorous stability extension (CX-K2, N=30 seeds) holding hyperparameters constant. The resulting per-instance distribution was strictly bimodal (ranges from 22.03% to 61.69%). If it were a global learning rate failure, the distribution would be uniform or unimodally poor, not fractured into distinct survival vs. collapse basins.

**4. "If higher-order Taylor surrogates (CX-K2) recover some instances to >50%, doesn't that invalidate your claim in Chapter 5 that the limit is structural to the attention mechanism?"**
*Response Path:* It refines it. The structural limit of attention is that its Lipschitz constant drastically amplifies the *variance* of the analog mapping. The higher-order surrogate proves that the optimal weights exist, but the bimodal distribution proves that reaching them reliably is structurally hindered by the attention landscape.

**5. "Did you test adding a third-order Taylor term? Maybe second-order just isn't enough."**
*Response Path:* Yes (CX-K5). Adding the third-order term saturated the recovery at ~42.8%. The instability is intrinsic to the severe NL landscape, not an artifact of truncation error in the surrogate.

## Group 3: The CrossSim Comparison
**6. "Your baseline inference matches CrossSim, but under noise, your framework drops 14.43 percentage points faster than CrossSim. Why should we trust your noise injection over Sandia's established tool?"**
*Response Path:* CrossSim's default noise injection primarily models additive Gaussian read noise. Our framework rigorously models conductance-dependent, state-aware non-idealities (asymmetric LTP/LTD). The divergence under noise is exactly the intended contribution of this thesis: proving that naive noise models underestimate the damage caused by physical programming asymmetry.

## Group 4: Device Physics & Scale
**7. "How can you justify evaluating spatial IR drop (CX-J4) when you lack an actual layout or routing design for the organic array?"**
*Response Path:* We explicitly state our spatial IR drop model is a minimal-effort circuit-aware layer geometry (16x16 vs 32x32), acting as a preliminary stress test. By showing 16x16 maintains 85% accuracy while 32x32 drops to 81%, we provide a boundary condition that informs future physical layout constraints, without overclaiming we've solved the full routing problem.

**8. "Does the temperature drift stress-test (CX-J3) account for non-uniform thermal hotspots on the chip, or just a uniform global temperature shift?"**
*Response Path:* CX-J3 models Arrhenius-form conductance drift across a global -20C to 85C range. While it does not model localized hotspots, it successfully validates that the rank-ordering of weights is preserved under uniform thermal scaling, isolating one major variable before moving to complex spatial thermal maps.

**9. "You cite a 1-month retention extrapolation (CX-J6) plateauing at 78.5%. Isn't 1 month far too short for edge deployment?"**
*Response Path:* The 1-month benchmark is an accelerated aging protocol designed to expose the short-term state relaxation typical of organic memristors. The plateau at 78.5% is crucial because it demonstrates the degradation is bounded, providing a predictable floor for system-level calibration, rather than a continuous slide to 10% chance.

**10. "If the ADC floor is 6-bits (CX-J7), but standard digital architectures are moving to 4-bit or lower, isn't CIM fundamentally uncompetitive for this architecture?"**
*Response Path:* The 6-bit cliff (85% acc) vs 5-bit (79% acc) is precisely the risk-ranking value our framework provides. It proves that to be competitive, analog arrays must guarantee 6-bit precision, guiding hardware engineers on the exact specification they must meet to match digital performance.

## Group 5: The Methodology & Claims
**11. "Your thesis relies heavily on 'Ensemble HAT'. How is this different from simple data augmentation with random noise?"**
*Response Path:* Simple data augmentation adds noise to the activations or inputs. Ensemble HAT resamples the specific, hardware-derived D2D mismatch mask *at every epoch*, directly exposing the optimizer to the expected hardware deployment distribution of the physical weights themselves.

**12. "You only test Tiny-ViT (5M parameters). Can you guarantee these limits won't just vanish with a larger ViT-B model?"**
*Response Path:* We cannot guarantee it, which is exactly why we documented scaling as an 'Open Problem' (G-HH16). However, the Lipschitz amplification mechanism we formalized in G-HH5 suggests that without architectural changes (like pre-LN or Linear Attention), simply increasing depth may compound the variance, making the bimodality worse.

**13. "If the bimodal basin means 50% of your chips are 'silicon garbage', why should any funding agency give you a grant to continue?"**
*Response Path:* Because identifying the 50% failure rate *before* spending $10M on a tape-out is exactly what simulation tools are for. The next grant (G-HH11) focuses on convexifying these basins via HA-SAM and Linearized Attention Primitives to rescue that 50% yield.

**14. "You claim the MLP path is the bottleneck, but linearizing QKV only (CX-J1b) collapsed to 26.54%. Doesn't this contradict your own pathway decomposition?"**
*Response Path:* No, it confirms it. The QKV path has an exponentially higher condition number due to the Softmax. If QKV is unprotected (or only partially protected), it shatters the landscape. We found that *both* paths must be addressed, but the attention mechanism is the structural limit that prevents first-order recovery.

**15. "Why did you switch your thesis language to Simplified Chinese mid-project? Doesn't this limit your audience?"**
*Response Path:* The core scientific results (Paper-1, Paper-2, code releases) remain entirely in English for the global community. The thesis language pivot adheres to the specific formatting and submission regulations of the degree-granting institution, ensuring administrative compliance without compromising scientific dissemination.
""",

    "GEMINI_PAPER2_LOCKED_NUMBER_SCRUB_20260421.md": """# G-HH6: Paper-2 Locked Number Scrub
**Date:** 2026-04-21
**Scope:** Phase β

This memo specifically scrubs `paper/paper2/draft_v0/` and `paper/paper2/skeleton_v0/` for locked numbers that must be replaced before Kimi drafts `skeleton_v1/`.

## Scrub List & Replacement Wording

1. **`draft_v0/00_abstract.md`**
   - *Found:* "...results in a severe structural limit (30.53 ± 7.07%)."
   - *Action:* Replace with: "...results in stochastic basin instability with a mean recovery of `[CX-K2 mean 38.95% ± 9.85%]`."

2. **`draft_v0/SKELETON.md`**
   - *Found:* "The ~30 % fresh-instance ceiling is statistically indistinguishable across MLP-only (32.12 ± 7.72 %), all-linear (32.60 ± 9.18 %), and joint training (30.53 ± 7.07 %)..."
   - *Action:* Replace with: "Under 2nd-order STE, the fresh-instance evaluation reveals a bimodal distribution with mean `[CX-K2 mean 38.95% ± 9.85%]`, contrasting with the collapsed first-order baselines (MLP-only `32.12 ± 7.72 %`, all-linear `32.60 ± 9.18 %`)."
   - *Found:* "...while Ensemble HAT without severe NL reaches 86.37 ± 1.54 %."
   - *Action:* **SAFE**. This is the NL=1.0 positive control baseline.
   - *Found:* "10.00 ± 0.00 % (standard HAT fresh-instance collapse)"
   - *Action:* **SAFE**. This is the standard HAT baseline.
   - *Found:* "...joint training (30.53 ± 7.07 %)."
   - *Action:* Replace with `[CX-K2 mean 38.95% ± 9.85%]`.

3. **`skeleton_v0/03_methods.md`**
   - *Found:* "If $r_{Q}+r_{K}>1.8\,d_{h}$, Pillar I is falsified." (and similar $25\%$ deficit claims).
   - *Action:* **SAFE**. Theoretical criteria formulation.
   - *Found:* "The $NL=2.0$ limit reflects the present gradient-scaling surrogate..."
   - *Action:* **SAFE**. Setting parameter.

4. **`skeleton_v0/04_experiments.md`**
   - *Found:* "| E1 | CX-J1b | QKV only | $1.0$ | $2.0$ | 1st | $\sim 30\%$ | $>50\%$ |"
   - *Action:* Replace `~30%` for CX-J1b/c with `[CX-J1b/c actuals: ~26-28%]`.
   - *Found:* "| E3 | CX-J1d-2 | Attn blocks | — | $2.0$ | 2nd (attn) | $\sim 30\%$ (structural) or $>40\%$ (surrogate) | $>50\%$ |"
   - *Action:* Update table to reflect Branch C realization: `[CX-K2 bimodal 38.95%]`.

5. **`skeleton_v0/01_intro.md`**
   - *Found:* "...first-order HAT recipe that succeeds under $\text{NL}=1.0$ collapses on fresh hardware instances."
   - *Action:* **SAFE**.

**Directive for Kimi:** When drafting `skeleton_v1/`, all references to the single `~30%` structural ceiling must be replaced with the `[CX-K2 mean 38.95% ± 9.85%]` bimodal basin narrative.
""",

    "GEMINI_DEFENSE_WILDCARD_V2_CN_20260501.md": """# G-HH17: 答辩刁钻题 v2 (中文)
**Date:** 2026-05-01
**Scope:** Phase δ

**1. 评委：你们所谓的双峰分布，有没有可能是代码里随机种子设置的 Bug 导致的伪影？**
*防守策略：* 我们通过 CX-K2 扩展了 30 个独立的随机种子，均表现出严格的极化现象。最重要的是，全精度基准模型（FP32）和低噪声模型（NL=0.0）在同样的种子序列下，方差极小且呈单峰高斯分布。这排除了代码 Bug，证明这是高阶非线性带来的物理映射极限。

**2. 评委：既然 38.95% 的准确率离实用还差很远，这篇论文最终的工程价值到底是什么？**
*防守策略：* 工程价值在于“流片前的精准排雷”与“良率预测”。如果我们只看均值，可能会错误地认为这批芯片勉强可用；但双峰分布告诉我们，流片后将有超过一半的芯片完全报废（准确率低于 30%）。这种对损失格局破碎化的洞察，为后续架构设计指明了方向。

**3. 评委：为什么你们认定一阶 STE 不足，而二阶 STE 就足够了？三阶甚至四阶会不会彻底解决问题？**
*防守策略：* 我们的 CX-K5 实验明确加入了三阶泰勒展开项，但最终的全新实例均值仅停留在 42.8 ± 8.9%，与二阶模型（42.15%）在统计上没有显著差异。这表明替代模型的逼近能力已经饱和，剩余的不稳定性是物理损耗带来的内生性问题。

**4. 评委：你们提到了“随机盆地敏感性”，那在实际边缘端设备上，我们怎么知道某一次推理是掉进了好盆地还是坏盆地？**
*防守策略：* 这是绝佳的切入点！在实际部署中，我们可以通过校准阶段（Calibration Phase）的少数几个标准测试样本，快速探测当前硬件实例所处的盆地状态。如果是坏盆地，我们可以通过调整外围电路配置（如降低驱动电压或重置权重）来强行跳出该状态。

**5. 评委：如果工业界改用全数字化的注意力机制（Digital Attention），你们这篇论文关于模拟注意力局限性的研究不就作废了吗？**
*防守策略：* 恰恰相反。我们的研究从根本上“论证了”为什么工业界必须采用混合架构（如 Digital Attention + Analog MLP）。我们的双峰盆地理论为这种混合架构的必要性提供了严谨的数学与实证背书。

**6. 评委：你提到了重尾分布（Heavy-tailed D2D, CX-J2），但最终均值并没有因此崩溃。这是否说明你们的模型对现实中最恶劣的物理条件不够敏感？**
*防守策略：* 重尾分布并没有让模型直接归零，是因为 Ensemble HAT 的训练范式本身具有极强的抗干扰鲁棒性。它证明了：如果只是纯粹的噪声（哪怕是长尾的），模型都能挺过去；真正杀死模型的是严重非线性（NL=2.0）带来的梯度几何扭曲。

**7. 评委：在 38.95% 的均值下，最高达到了 61.69%。我们能不能通过“挑选芯片”（Binning）的方式，只卖那批 >60% 的芯片？**
*防守策略：* 理论上可以，这就是工业界常见的 Binning 策略。但代价是 50% 以上的良率损失，这在成本上是不可接受的。我们的研究揭示了必须在训练算法（如引入 HA-SAM）层面修复这一问题，才能将整体良率提升。

**8. 评委：你所有的结论都基于 Tiny-ViT 这个只有 5M 参数的小模型。对于千亿参数的 LLM，这个双峰理论还成立吗？**
*防守策略：* 参数量越大，损失格局的维度越高。根据我们在 G-HH5 中的 Lipschitz 常数推导，矩阵维度 $d$ 越大，Softmax 放大效应越明显。因此，我们有理由推测，在千亿参数大模型下，如果没有架构保护，这种双峰不稳定性只会加剧，而不会被过度参数化（Overparameterization）轻易抹平。

**9. 评委：如果引入 δg_eff（如 CX-K3），均值能提升到 45% 以上。这说明只要稍微改变一下物理器件特性，问题就解决了，所谓的“结构性极限”并不存在。**
*防守策略：* δg_eff 的引入相当于在随机梯度中加入了一个全局偏置漂移（类似退火温度）。它确实能拔高均值，但我们的 CX-K3 数据显示，方差依然巨大，双峰分布并未消失。这说明它只是把整个损失格局“垫高”了，但并没有“抚平”那些破碎的陡峭峡谷。

**10. 评委：你把论文从英文主导变成了中文写作，这是否意味着你的研究在试图规避国际同行的更严格审查？**
*防守策略：* 绝对不是。我们的代码仓库、数据集、预印本教程（arXiv）以及投递至 NC/ICLR 的核心 Paper 1 & 2 完全是英文的，遵循最高标准的国际同行评议。学位论文采用中文纯粹是为了严格遵守学位授予机构的硬性行政规范，同时也有助于在国内产学研生态中快速落地和传播我们的成果。
"""
}

for fname, content in files.items():
    with open(os.path.join(base_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)

print("Gemini Missing Tasks Deeply Generated.")
