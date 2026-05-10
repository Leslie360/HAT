# Group Meeting PPT Prompt — 2026-04-17

## 建议发给网页版 GPT 的文件

### 最小上传包

这 7 个文件足够让网页版 GPT 做一版可靠的组会 PPT：

1. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf`
2. `/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md`
3. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig4_accuracy_comparison.png`
4. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig5_hat_recovery.png`
5. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_contour_map.png`
6. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/figS3_ensemble_hat.png`
7. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig10_zero_shot_transferability.png`

### 建议增强包

如果你想让网页版 GPT 更好地做“阶段性成果 + 补充结果 + 后续计划”，再额外上传这 3 个文件：

8. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf`
9. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_sobol_sensitivity.png`
10. `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_attention_maps.png`

### 不建议上传

- 原始训练日志
- 太多中间 markdown
- doctor 原始数据文件夹
- 很多版本的历史 PPT / 草稿

原因很简单：网页版 GPT 很容易被过量上下文带偏。你现在要的是“组会阶段性成果汇报”，不是“项目全历史归档”。

## 你发给网页版 GPT 的 prompt

把下面整段原样发过去即可：

```md
你是我的学术汇报助手。请基于我上传的论文 PDF、补充材料和关键图，直接帮我制作一份中文组会汇报 PPT，主题是“阶段性成果汇报”。汇报对象是导师和课题组，预期时长 12–15 分钟。

请严格遵守以下要求：

## 1. 任务目标

- 这是“阶段性成果组会汇报”，不是投稿答辩，也不是面向外行的科普。
- 汇报要突出：我已经做成了什么、核心发现是什么、当前局限是什么、接下来准备做什么。
- PPT 风格要像理工科组会，不要像产品发布会，也不要像花哨商业模板。

## 2. 信息来源优先级

请按以下优先级使用信息：

1. `CANONICAL_RESULT_LOCK_gpt.md`
2. `main.pdf`
3. `supplementary_main.pdf`
4. 我上传的关键图片 PNG

如果不同文件里出现表述差异，请优先服从 `CANONICAL_RESULT_LOCK_gpt.md` 和 `main.pdf`，不要自己发明新数字。

## 3. 必须遵守的硬约束

- 不允许编造实验结果、统计量、对比结论或未来计划。
- 不允许把“阶段性结果”包装成“已经最终定稿的结论”。
- 不允许过度夸大能耗、CrossSim、measured-profile 等仍然带限定语的内容。
- 所有数值必须以我上传材料为准。
- 如果你不确定某个细节，就弱化表述，不要乱补。

## 4. 这份组会 PPT 的核心叙事

请围绕下面这条主线组织内容：

1. 研究动机：
   现有有机光电/电化学器件论文很多停留在器件级，缺少面向现代视觉模型部署风险的系统级评估框架。

2. 我做了什么：
   搭建了一个 profile-driven、first-order behavioral simulation framework，
   把器件侧参数映射到任务级视觉精度，
   能统一分析 photoresponse、retention、write nonlinearity、ADC、D2D/C2C noise、hardware-aware training。

3. 阶段性最重要发现：
   - ADC 分辨率不是小问题，而是主瓶颈：6-bit 是明显门槛。
   - standard HAT 会过拟合单个固定 D2D instance，在 fresh hardware 上会崩。
   - Ensemble HAT 可以显著改善 fresh-instance transferability。
   - severe nonlinear write 目前仍然是主要失败模式。
   - literature-calibrated / measured-profile 路径已经打通，说明框架能做 profile substitution。

4. 这意味着什么：
   这个框架可以作为 materials-to-system bridge，在真实阵列完全成熟前，先评估哪些器件特性真正限制 edge vision deployment。

5. 当前局限和下一步：
   还不是 chip-accurate simulator；
   对 energy、CrossSim 对齐、measured-profile 扩展、更多器件数据接入仍需继续推进。

## 5. 请优先强调的锁定结果

请在 PPT 中优先使用并突出这些结果：

- Tiny-ViT V4 HAT：
  - CIFAR-10: 91.94%
  - CIFAR-100: 65.48%
  - Flowers-102: 22.48%

- ConvNeXt C4 HAT：
  - CIFAR-10: 89.91%
  - CIFAR-100: 60.54%

- Fresh-instance transfer：
  - standard HAT 在 fresh arrays 上崩到 10.00%
  - Ensemble HAT 恢复到 86.37 ± 1.54%

- ADC / contour / Sobol：
  - 6-bit 以下出现明显 accuracy cliff
  - 全局 Sobol：S_ADC ≈ 0.98
  - operational region：S_D2D ≈ 0.92

- Literature-calibrated OPECT case study：
  - zero-shot transfer accuracy = 88.53%

- Severe nonlinear write：
  - NL=2.0 时仅 27.72 ± 0.82%

## 6. 推荐页数与结构

请做成 12 页左右，允许 11–13 页，但不要超过 14 页。

推荐结构如下：

1. 标题页
2. 研究背景与问题定义
3. 为什么现有器件论文还不够支撑部署判断
4. 我提出的 simulation framework / workflow
5. 基线结果与 canonical deployment fragility
6. HAT recovery 与 cross-dataset 表现
7. ADC cliff + contour map + Sobol 解读
8. Fresh-instance transfer problem 与 Ensemble HAT
9. Zero-shot transfer to literature-calibrated / measured profiles
10. 当前局限：nonlinear write、energy 近似、非 chip-accurate 边界
11. 阶段性总结：核心 takeaways
12. 下一步计划 / 希望组会讨论的问题

## 7. 版式要求

- 中文学术风格，简洁、克制、专业。
- 白底优先，深蓝 / 深灰配色即可。
- 全套字体统一，不要不同页不同字体。
- 不要大面积渐变、炫技动画、花哨图标。
- 每页尽量 3–5 个 bullet，避免大段文字堆砌。
- 每页必须有清楚的标题。
- 关键结果页优先使用我上传的原图，必要时你可以裁剪或重排，但不要扭曲图意。
- 如果你重绘示意图，请保持科研汇报风格，不要“AI 味”太重。

## 8. 输出形式

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

3. 如果你支持直接生成 PPT / 演示文稿文件，请在内容确认后直接帮我生成。
   如果你不能直接生成 PPT 文件，就给我一份可以直接复制进 PPT 的最终版逐页文案。

## 9. 特别提醒

- 这份汇报是“阶段性成果”，请保留“已完成 / 当前局限 / 下一步”的节奏。
- 不要把所有结果平均铺开，要形成主次关系。
- 整个 PPT 要让导师一眼看出：我这段时间最核心的工作完成了什么、最有价值的发现是什么、接下来最值得继续推进的是什么。
```

## 你自己操作时的建议

### 最省事的做法

先只传“最小上传包”那 7 个文件，先让网页版 GPT 出第一版结构。

如果第一版已经顺，就不用再加文件。

如果它对：

- Sobol / supplementary 讲不清
- attention map 想补一页
- 下一步计划不够具体

再补传增强包里的 3 个文件，让它迭代第二版。

### 你可以再补一句口头要求

如果你希望更像“导师组会”而不是“论文答辩”，可以在 prompt 最后再补一句：

> 请让整份 PPT 更像“阶段性研究进展汇报”，弱化投稿措辞，强化“我已经完成的模块、关键发现、当前卡点、下阶段计划”。
