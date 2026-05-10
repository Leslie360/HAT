# Group Meeting PPT Prompt v2 — 2026-04-17

## 建议发给网页版 GPT 的文件

### 最小上传包

1. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf`
2. `/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md`
3. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig4_accuracy_comparison.png`
4. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig5_hat_recovery.png`
5. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_contour_map.png`
6. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_sobol_sensitivity.png`
7. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/figS3_ensemble_hat.png`
8. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig10_zero_shot_transferability.png`

### 可选增强包

9. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf`
10. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig7_retention_curve.png`
11. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_attention_maps.png`

### 不建议上传

- 训练日志
- `_gpt/` 目录下的大量中间审计文档
- 原始博士数据目录
- 历史版 PPT

原因：

- 网页版 GPT 容易被过量上下文带偏。
- 这次任务是组会汇报，不是结果溯源审计。

## 直接发给网页版 GPT 的 prompt

把下面整段原样发过去：

```md
你是我的学术汇报助手。请基于我上传的论文 PDF、补充材料和关键图片，帮我制作一份中文组会汇报 PPT，主题是“阶段性成果汇报”。汇报对象是导师和课题组，预期时长 12–15 分钟。

请严格遵守以下要求。

## 1. 汇报定位

- 这是“阶段性成果组会汇报”，不是投稿答辩。
- 重点是：我已经完成了什么、关键发现是什么、当前局限是什么、下一步准备做什么。
- 整体风格要像理工科组会，不要像商业路演或科普海报。

## 2. 信息来源优先级

如果不同文件之间有轻微差异，请按下面优先级取舍：

1. `CANONICAL_RESULT_LOCK_gpt.md`
2. `main.pdf`
3. `supplementary_main.pdf`
4. 我上传的关键图片

不要根据自己的想象补数字。

## 3. 必须遵守的硬约束

- 不允许编造实验结果、统计量、结论或未来计划。
- 不允许把“阶段性结果”写成“最终定论”。
- 不允许夸大 measured-profile、energy、CrossSim 等仍带边界条件的内容。
- 所有数值必须以我上传材料为准。
- 如果某个细节存在统计口径差异，请弱化为定性表述，不要强行写死数字。

## 4. 这份 PPT 的主线

请围绕这条主线组织整份 PPT：

1. 研究动机：
   现有有机光电/电化学器件工作多停留在器件级，缺少对现代视觉模型部署风险的系统级评估。

2. 我做了什么：
   搭建了一个 profile-driven、first-order behavioral simulation framework，
   将器件侧非理想性映射到任务级视觉精度，
   可以统一分析 photoresponse、retention、write nonlinearity、ADC、D2D/C2C noise、hardware-aware training。

3. 阶段性最重要发现：
   - ADC 分辨率是主瓶颈，6-bit 是明显门槛。
   - standard HAT 会过拟合单个固定 D2D instance，在 fresh hardware 上会崩到 chance level。
   - Ensemble HAT 可以显著改善 fresh-instance transferability。
   - severe nonlinear write 目前仍然是主要失败模式。
   - literature-calibrated / measured-profile substitution 路径已经打通，说明框架具备 profile 替换评估能力。

4. 这意味着什么：
   该框架可以作为 materials-to-system bridge，在真实阵列完全成熟前，先判断哪些器件特性真正限制 edge vision deployment。

5. 当前局限和下一步：
   目前仍是 first-order behavioral simulator，不是 chip-accurate array simulator；
   CrossSim 对比已经完成，但当前框架与 CrossSim 的建模语义并不完全相同；
   energy、measured-profile 扩展、更多实测器件数据接入仍需继续推进。

## 5. 请优先强调的锁定结果

请优先使用并突出下面这些结果：

- Tiny-ViT V4 HAT：
  - CIFAR-10: 91.94%
  - CIFAR-100: 65.48%
  - Flowers-102: 22.48%

- ConvNeXt C4 HAT：
  - CIFAR-10: 89.91%
  - CIFAR-100: 60.54%

- Tiny-ViT standard noisy deployment：
  - CIFAR-10: 89.54%
  - CIFAR-100: 44.06%

- ConvNeXt standard noisy deployment：
  - CIFAR-10: 70.48%
  - CIFAR-100: 23.86%

- Fresh-instance transfer：
  - standard HAT collapses to 10.00%
  - Ensemble HAT recovers to 86.37 ± 1.54%

- ADC / contour / Sobol：
  - accuracy cliff appears below 6-bit ADC
  - full-grid Sobol: S_ADC = 0.976, S_D2D = 0.018, S_interaction = 0.006
  - operational region (D2D <= 15%, ADC >= 6-bit): S_D2D = 0.922, S_ADC = 0.041, S_interaction = 0.038

- Literature-calibrated OPECT case：
  - zero-shot transfer accuracy = 88.53%

- Severe nonlinear write：
  - NL = 2.0 leads to 27.72 ± 0.82%

## 6. 需要避免的表述

- 不要把框架写成“通过 CrossSim 加速的主框架”。
  正确口径是：我的主框架是 first-order behavioral simulation framework，CrossSim 是对照基线和参考实现。

- 不要把 Tiny-ViT CIFAR-10 FP32 baseline 写成唯一锁死数字。
  如果需要写，优先写成“about 98% on CIFAR-10”，避免在组会上陷入统计口径争议。

- 不要把 retention 曲线混进 HAT recovery 图页。
  如果要讲 retention，请单独放在补充页，或者配合单独的 retention 图。

- 不要说“CrossSim 对齐尚未完成”。
  正确口径是：CrossSim comparison is completed, but the current simulator remains a first-order behavioral approximation rather than a chip-accurate array model.

- 不要把 zero-shot transfer 写成“所有实测 profile 都已经完整验证完毕”。
  更稳妥的口径是 literature-calibrated / selected measured-profile substitution has been demonstrated.

## 7. 推荐页数与结构

请做成 12 页左右，允许 11–13 页，不要超过 14 页。

推荐结构：

1. 标题页
2. 研究背景与问题定义
3. 为什么现有器件论文还不足以支撑部署判断
4. First-order behavioral simulation framework / workflow
5. 基线结果与 canonical deployment fragility
6. HAT recovery 与 cross-dataset 表现
7. ADC cliff + contour map + Sobol 解读
8. Fresh-instance transfer problem 与 Ensemble HAT
9. Zero-shot transfer to literature-calibrated / measured profiles
10. 当前局限：nonlinear write、first-order approximation、energy / profile 扩展边界
11. 阶段性总结：核心 takeaways
12. 下一步计划 / 希望组会讨论的问题

## 8. 版式要求

- 中文学术风格，简洁、克制、专业。
- 白底优先，配色使用深蓝、深灰和少量强调色。
- 全套字体统一，不要不同页不同字体。
- 不要用默认花哨模板，不要大面积渐变。
- 不要使用夸张动画或商业图标。
- 每页尽量控制在 3–5 个 bullet。
- 关键结果页优先使用我上传的原图；必要时可以裁剪、重排，但不要扭曲图意。
- 如果重绘示意图，请保持科研汇报风格，不要“AI 味”太重。
- 图片与文字不要互相遮挡，坐标轴、图例、标题必须清晰可读。

## 9. 输出形式

请按以下顺序输出：

1. 先给我一份“逐页 PPT 方案总表”
   - 页码
   - 页标题
   - 这一页的核心信息
   - 建议使用的图

2. 再给出“逐页详细内容”
   - 每页标题
   - 每页 bullet 文案
   - 讲解逻辑
   - 建议放哪张图、图怎么摆

3. 如果你支持直接生成 PPT / 演示文稿文件，请在内容确认后再生成。
   如果不能直接生成 PPT 文件，就给我一份可以直接复制到 PPT 里的终版逐页文案。

## 10. 特别提醒

- 这份汇报要保持“已完成 / 当前局限 / 下一步”的节奏。
- 不要把所有结果平均铺开，要形成主次关系。
- 导师看完之后，应该能直接抓住三件事：
  1. 我这段时间最核心完成了什么；
  2. 最有价值的技术发现是什么；
  3. 下一阶段最值得继续推进的方向是什么。
```

## 你自己操作时的建议

### 最省事的做法

先传“最小上传包”。

如果网页版 GPT 第一版已经把下面三件事讲清楚，就不要再补文件：

- 6-bit ADC cliff
- fresh-instance collapse vs Ensemble HAT recovery
- zero-shot transfer / profile substitution

只有在它明显讲不清下面内容时，再补“可选增强包”：

- retention
- attention maps
- supplement-specific supporting plots

### 你还可以补一句

如果你想让它更像导师组会，而不是论文答辩，可以在最后再补一句：

> 请让整份 PPT 更像“阶段性研究进展汇报”，弱化投稿措辞，强化“我已完成的模块、关键发现、当前卡点和下一步计划”。
