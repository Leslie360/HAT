# Kimi 任务单 — 2026-04-14 Phase 2 NC Reviewer Response

> **协调员**: Claude (总指挥)
> **你的角色**: 论文文本 + 审稿回应信 + 文献调研
> **硬约束**: 不编造数字或文献，不改 locked numbers，所有文本修改标注 path:line

---

## 先读这些文件

1. `report_md/_gpt/PROJECT_MASTER_SUMMARY_FOR_AGENTS_gpt.md` — 项目真值
2. `report_md/_gpt/NC_REVIEWER_FEEDBACK_ANALYSIS_20260414.md` — NC 审稿意见
3. `report_md/_gpt/RESNET_DEBUG_FINDINGS_20260414.md` — ResNet 问题诊断
4. `paper/latex_gpt/sections/06_discussion.tex` — 当前 Discussion
5. `paper/latex_gpt/sections/05_results.tex` — 当前 Results

---

## KP-1: Discussion 补充 ResNet-18 CIFAR-100 说明 [IMMEDIATE]

**Claude 决策**: ResNet-18 CIFAR-100 数据无效，采用"声明为发现"策略

**操作**:
在 `06_discussion.tex` §6.3 (Task Complexity and Data Starvation) 末尾追加一段：

**要点**:
- ResNet-18 在 CIFAR-100 上的 R3/R4 实验未能收敛（ADC 扫描全 1.00%）
- Root cause: 标准训练流水线中 train/eval 噪声配置不一致导致分布偏移
- Tiny-ViT 和 ConvNeXt 不受影响（它们的 HAT 训练逻辑在训练时即启用噪声）
- 这揭示了一个架构-训练-部署交互效应：不同架构对 HAT 流水线配置的敏感度不同
- 修复并重跑是未来工作的一部分

**语气**: NC 论文风格 — 直接陈述事实，不道歉，框架为一个有意义的发现

**交付**: 写好的 LaTeX 段落（不要直接写入文件，写到 AGENT_SYNC 中等 Claude 审核）

---

## KP-2: 审稿回应信初稿 [HIGH]

**操作**: 撰写 point-by-point 回应信骨架

**格式** (NC 标准):
```
We thank the reviewers for their constructive feedback...

## Reviewer 1

### Major Comment 1: [原文摘要]

**Response**: [回应]

**Changes made**: [改动列表]
```

**5 个 Major Comments 回应策略**:

| # | 问题 | 回应策略 |
|:--|:--|:--|
| 1 | 基准对比不足 | 已有 AIHWKIT (90.08±0.21%)；CrossSim 对比实验正在进行（Gemini GM-P0）；引用 DNN+NeuroSim 但指出其不支持有机器件特有的 photoresponse/retention/NL |
| 2 | NL=2.0 分析不充分 | 层级消融实验正在进行（Gemini GM-P2）；当前的 27.72±0.82% 是 gradient-scaling approximation 的极限，不是材料极限 |
| 3 | Ensemble HAT 创新性 | 消融实验正在进行（Gemini GM-P1）；与 i.i.d. 噪声增强对比；D2D resampling 处理的是空间结构化 mismatch，不是简单随机噪声 |
| 4 | 能效模型假设 | 已有 routing sensitivity bounds (10-50% overhead → 11.10x-9.90x)；一阶模型的定位在论文中明确声明 |
| 5 | Profile 普适性 | 已有 Zhang 2025 OPECT case study (88.53%)；profile interface 设计允许直接替换实测参数 |

**对每个回应**:
- 先写"已有证据"部分
- 再标注"等待实验结果后补充"的占位符
- 保持诚实 — 不要回避真实局限

**交付**: `report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md`

---

## KP-3: Ensemble HAT 文献调研 [HIGH — 为 Major #3 准备]

**操作**: 调研以下主题，为 Ensemble HAT 的创新性论证提供支撑

**调研问题**:
1. CIM 领域有哪些 multi-instance/variability-aware 训练方法？
2. Domain Randomization 在 CIM/analog 领域的应用？
3. 与 Ensemble HAT 最接近的方法是什么？区别在哪？
4. 标准 HAT (AIHWKIT 的 InjectAnalogNoise) 的训练策略是什么？与我们的有何不同？

**交付**:
- `report_md/_gpt/ENSEMBLE_HAT_LITERATURE_SURVEY_gpt.md`
- 包含 5-10 篇关键文献的简要分析
- 明确写出 Ensemble HAT 相对于每种方法的差异化

**约束**: 只引用真实存在的论文，给出完整引用信息（作者、年份、venue）

---

## KP-4: ConvNeXt ADC 扫描结果写入 [MED — Minor #1]

**背景**: 审稿要求补充 ConvNeXt 的 ADC 扫描。检查是否已有数据。

**操作**:
1. 检查 `logs/_gpt/` 和 `report_md/_gpt/json_gpt/` 是否有 ConvNeXt ADC 扫描数据
2. 如果有，写一段补充文本放入 Results 或 Supplementary
3. 如果没有，报告给 Claude，标记为需要 Gemini 跑实验

**交付**: 数据状态报告 + 写入建议（写到 AGENT_SYNC）

---

## KP-5: Supplementary 扩展准备 [MED]

**背景**: Phase 2 实验完成后需要更新 Supplementary

**操作**: 在 `supplementary.tex` 中预留 3 个新 section 的框架（注释状态）：

1. `§S6: CrossSim Comparison` — 等 Gemini GM-P0 结果
2. `§S7: Ensemble HAT Ablation` — 等 Gemini GM-P1 结果
3. `§S8: Layer-Wise NL Sensitivity` — 等 Gemini GM-P2 结果

**交付**: 预留框架（注释状态），写到 AGENT_SYNC 等 Claude 审核后统一写入

---

## 输出规则

1. **每个任务完成后在 AGENT_SYNC 追加一个 `[Kimi]` block — 只写一次**
2. **不要直接修改 .tex 文件** — 所有文本建议写到 AGENT_SYNC，由 Claude 审核后落地
3. 不确定的内容写方案+选项，不要自行决定
4. 不编造文献 — 文献调研必须可验证
5. **按 KP-1 → KP-2 → KP-3 → KP-4 → KP-5 顺序执行**
