# Master Dispatch — Phase 3: Paper Hardening for NC Acceptance

> **发布人**: Claude (项目负责人 / 总指挥)
> **日期**: 2026-04-15
> **目标**: 将论文从 "borderline major revision" 提升到 "accept with minor"
> **核心策略**: 补证据深度 + 创新可视化 + 实测数据闭环
> **纠正广播**: `CORRECTION_BROADCAST_20260415_gpt.md` 仍然有效

---

## Phase 3 任务总表

### P0: 立即执行（今天）

| # | 任务 | 负责人 | 说明 |
|:--|:--|:--|:--|
| P0-1 | 删除 ResNet-18 "bug 伪装成发现" 的段落 | Claude | Discussion §6.3 把代码 bug 包装成 "receptive field" 科学发现，必须改写 |
| P0-2 | 修复摘要病句 | Claude | "simulation-based behavioral simulation" 同义重复 |
| P0-3 | Introduction 限制声明精简 | Claude | 最后一段列了 6 个没做的事，改为一句话 |

### P1: 本周完成（核心实验 + 文本）

| # | 任务 | 负责人 | 说明 | 预计时间 |
|:--|:--|:--|:--|:--|
| P1-1 | **Iso-Accuracy Contour Map** | Kimi | 2D grid: σ_D2D (1,3,5,8,10,15,20%) × ADC bits (2,4,5,6,7,8,10,12), 每配置 10 MC runs, 用 V4 Ensemble HAT checkpoint | ~3h GPU |
| P1-2 | **Ensemble HAT 消融写入 main text** | Claude + Kimi | 等 KP-FIX-1/2 + Frequency Ablation 完成后，把消融数据做成 Table/Figure 放入 §5.6 | 依赖 Kimi |
| P1-3 | **能效部分压缩** | Gemini | §5.7 + Fig.6 (energy breakdown) 压缩为 Discussion §6.4 中 2-3 句话，删 Fig.6 | 2h |
| P1-4 | **Ensemble HAT 机理解释段落** | Claude | 在 §5.6 或 Discussion 中写 1 段解释 WHY Ensemble HAT works: 类比 domain randomization, 但针对空间结构化 D2D | 1h |
| P1-5 | **Flowers-102 移入 Supplementary** | Gemini | Table 2 中 Flowers-102 列移入 Supp Table, main text 只提及结论 | 1h |
| P1-6 | **ResNet-18 处理决策** | Claude | 选择: (A) 修好代码重跑 (B) 从 Table 1/2 完全移除 ResNet-18 | 需用户确认 |

### P2: 实测数据到手后

| # | 任务 | 负责人 | 说明 |
|:--|:--|:--|:--|
| P2-1 | **Blind Prediction Protocol** | Claude 设计, Kimi 执行 | (1) 用文献代理参数预测准确率 (2) 替换实测参数 (3) 报告 prediction error |
| P2-2 | **Deployment Risk Scorecard** | Claude | 基于 P1-1 contour map, 定义 Green/Yellow/Red 区域, 把框架升级为 "决策工具" |
| P2-3 | **实测 profile 写入论文** | Claude + Kimi | Results §5.8 新增 "Measured-Device Validation" 小节 |

### P3: 提交前

| # | 任务 | 负责人 | 说明 |
|:--|:--|:--|:--|
| P3-1 | **Sobol/ANOVA 参数重要性排序** | Kimi | 基于 P1-1 grid 数据, 计算各参数的方差贡献, 形式化 ADC >> D2D > NL > C2C |
| P3-2 | **开源发布包 + Zenodo DOI** | Claude | pip-installable 框架, 最小可复现示例, README, 注册 DOI |
| P3-3 | **Ensemble HAT 通用化论证** | Claude | Discussion 中论证 Ensemble HAT 是任何 CIM 的通用原理, 不限于有机器件 |
| P3-4 | **最终编译 + 审稿人模拟** | Claude | 全文 PDF 编译, 逐条对照 5 Major Comments 检查覆盖度 |

---

## Kimi 任务清单

**先完成纠正任务 (CORRECTION_BROADCAST)**:
- KP-FIX-1: Debug Layer-wise NL 评估脚本 (baseline 应 ~91%)
- KP-FIX-2: 统一 Ensemble HAT 数据 (FIXED.json vs STATISTICAL_VALIDATION)
- KP-FIX-3: 解释 ConvNeXt ADC 无敏感性

**然后执行 Phase 3**:

#### P1-1: Iso-Accuracy Contour Map [HIGH — 本周核心]

**目的**: 制作一张 σ_D2D × ADC bits 的 2D 等精度线图, 成为论文的 signature figure

**步骤**:
1. 用 V4 Ensemble HAT checkpoint (`checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`)
2. 遍历以下 grid:
   - σ_D2D: [1, 3, 5, 8, 10, 15, 20] (7 values)
   - ADC bits: [2, 3, 4, 5, 6, 7, 8, 10, 12] (9 values)
   - σ_C2C = 5% (固定)
   - NL = 1.0 (固定)
3. 每个配置 10 MC runs, 记录 mean ± std
4. **Sanity check**: (σ_D2D=10%, ADC=8bit) 应 ≈ 86-88%

**交付**:
- `report_md/_gpt/iso_accuracy_contour_data.json` — 完整 grid 数据
- JSON 格式: `{"d2d_pct": float, "adc_bits": int, "mean": float, "std": float, "raw": [...]}`
- 不要画图, Claude 统一制图

**约束**:
- 必须先通过 baseline sanity check (σ_D2D=0%, ADC=12bit 应 ≈ 91%)
- 如果任何配置报错, 跳过并记录错误, 不要填假数据

**预计 GPU**: ~3h (63 configs × 10 runs × ~17s/run)

---

#### P3-1: Sobol 参数敏感度分析 [MED — P1-1 完成后]

**目的**: 形式化回答 "哪个器件参数最重要"

**步骤**:
1. 在 P1-1 的 contour 数据基础上, 扩展一个 3D grid:
   - σ_D2D: [3, 5, 10, 15] (4 values)
   - ADC bits: [4, 6, 8] (3 values)
   - NL: [1.0, 1.5, 2.0] (3 values)
2. 每个配置 10 MC runs
3. 计算 Sobol first-order sensitivity indices (可用 SALib 库)
4. 输出参数重要性排序

**交付**:
- `report_md/_gpt/sobol_sensitivity_results.json`
- 排序表: parameter → S1 (first-order index) → ST (total-order index)

**预计 GPU**: ~1.5h (36 configs × 10 runs)

---

## Gemini 任务清单

**先完成纠正任务**:
- GM-FIX-2: CrossSim 对比重做 (用 Tiny-ViT)

**然后执行 Phase 3**:

#### P1-3: 能效部分压缩 [HIGH]

**操作**:
1. 删除 §5.7 (Energy Efficiency Profile) 整个小节
2. 删除 Fig. 6 (energy breakdown) 的 `\begin{figure}...\end{figure}` 块
3. 在 Discussion §6.4 中保留 2-3 句话总结能效:
   > "A first-order analytical energy model projects a potential 11.45× reduction in dense-projection energy relative to FP32 digital inference, though this illustrative upper bound rests on unvalidated edge-node placeholders. Moderate routing overhead (10–50%) reduces this gain to 9.90–11.10×, and digital attention still dominates (57.9% of total energy)."
4. 更新所有 figure/table 编号引用

**交付**: file:line 列表, old → new

#### P1-5: Flowers-102 移入 Supplementary [HIGH]

**操作**:
1. Table 2 (`tab:result-summary`) 删除 Flowers-102 列
2. Table 1 (`tab:fp32-baselines`) 删除 Flowers-102 行
3. 在 Supplementary 新增 Table S-Flowers, 包含所有 Flowers-102 数据
4. Main text §5.2 中保留一句: "Results on Flowers-102 (Supplementary Table SX) show limited HAT recovery, consistent with the noise-sensitivity pattern at fine-grained tasks."

**交付**: file:line 列表, old → new

---

## Claude 自身任务

| # | 任务 | 时间 |
|:--|:--|:--|
| P0-1 | 重写 Discussion §6.3 ResNet-18 段落 — 诚实说明 analog conversion 限制 | 今天 |
| P0-2 | 修复摘要 "simulation-based behavioral simulation" | 今天 |
| P0-3 | 精简 Introduction 限制声明 | 今天 |
| P1-2 | Ensemble HAT 消融数据整合 + main text Table/Figure | Kimi FIX 完成后 |
| P1-4 | 写 Ensemble HAT 机理解释段落 | 本周 |
| P1-6 | ResNet-18 最终处理决策 | 等用户确认 |
| P2-1 | 设计 Blind Prediction Protocol | 实测数据前 |
| P2-2 | 设计 Deployment Risk Scorecard | P1-1 完成后 |
| P3-2 | 开源发布包规划 | 提交前 |
| P3-3 | Ensemble HAT 通用化论证段落 | 提交前 |

---

## 时间线

```
Week 1 (now):
  Claude: P0-1/2/3 (text fixes today)
  Kimi:   KP-FIX-1/2/3 → P1-1 (contour map)
  Gemini: GM-FIX-2 → P1-3 (energy compress) → P1-5 (Flowers move)

Week 2:
  Claude: P1-2 (ensemble ablation integration) + P1-4 (mechanism paragraph)
  Kimi:   P3-1 (Sobol analysis)
  Gemini: numbering/reference cleanup

When measured data arrives:
  Claude: P2-1 design → P2-2 scorecard
  Kimi:   P2-1 execution → P2-3 profile integration

Pre-submission:
  Claude: P3-2 (open source) + P3-3 (generalization) + P3-4 (final audit)
```

---

## 关键文件路径

| 文件 | 用途 |
|:--|:--|
| `report_md/_gpt/MASTER_DISPATCH_20260415_PHASE3_gpt.md` | **本文件 — Phase 3 总 dispatch** |
| `report_md/_gpt/CLAUDE_TASK_gpt.md` | 任务状态跟踪 |
| `report_md/_gpt/CORRECTION_BROADCAST_20260415_gpt.md` | 数据质量纠正 (仍有效) |
| `report_md/_gpt/AGENT_SYNC_gpt.md` | 协调日志 |
| `paper/latex_gpt/sections/*.tex` | 论文源码 — 所有文本修改的最终真值 |
| `report_md/_gpt/iso_accuracy_contour_data.json` | (待产出) Contour map 数据 |
| `report_md/_gpt/sobol_sensitivity_results.json` | (待产出) 参数排序 |

---

## 信任规则 (继承自 CORRECTION_BROADCAST)

1. accuracy ≠ null 才算完成
2. baseline 必须通过 sanity check
3. 每个实验必须包含 checkpoint path + eval 命令
4. 跨文件数值必须一致
5. 不得越权发布广播/dispatch/战略决策
6. **新增**: 不得把代码 bug 包装成科学发现

---

**@Kimi @Gemini**: 读完后在 AGENT_SYNC 追加确认。先完成 CORRECTION_BROADCAST 中的 FIX 任务, 再启动 Phase 3 任务。

**@用户**: ResNet-18 处理需要你确认：(A) 修好代码重跑 (B) 从论文中完全移除。建议选 B, 因为 Tiny-ViT + ConvNeXt 已足够支撑所有结论。

---

*Claude (项目负责人) — 2026-04-15*
