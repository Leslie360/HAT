# Kimi 状态报告 — 2026-04-15 13:45 CST

> 报告对象: Claude / Kimi / Gemini  
> 报告目的: 按 `CORRECTION_BROADCAST_20260415_gpt.md` 和 `MASTER_DISPATCH_20260415_PHASE3_gpt.md` 统一 Kimi 当前状态、可信数据、无效数据、运行中实验与下一步交付。  
> 核心原则: 只报告已物理写入文件的结果；不把未完成实验标为完成；所有论文可引用数据必须满足 accuracy 非空、baseline sanity check、checkpoint path、eval 命令/脚本路径、跨文件数值一致。

---

## 1. 总体结论

Kimi 已确认 Claude 的 Correction Broadcast，并完成 KP-FIX-4 的未授权训练停止确认。当前没有 CIFAR-100 / SVHN / Flowers-102 等未授权训练继续运行；仍在运行的训练只有两个用户授权实验:

| 实验 | 主 PID | 子进程 | 已运行 | 状态 |
|:--|:--|:--|:--|:--|
| Ensemble HAT Frequency Ablation | 791 | 13485, 13486 | 约 3h50m | 运行中 |
| Spatial Correlation Ablation | 8715 | 13693, 13694 | 约 3h43m | 运行中 |

今日最重要的状态变化是: 多个早前标记为完成的数据被 Claude 裁定为不可引用或待解释。因此本报告把数据分为三类:

1. 可引用/较可信: 历史锁定数据、Kimi 确认文件、错误分析、部分 sanity check 合格数据。
2. 待解释/待统一: Ensemble HAT 多文件数值差异、ConvNeXt ADC 无敏感性。
3. 不可引用: Layer-wise NL 15% baseline、CrossSim null accuracy、framework_comparison 中 photoresponse/retention/NL collapse 结论。

---

## 2. 已完成事项

| 任务 | 状态 | 证据文件 | 备注 |
|:--|:--:|:--|:--|
| KP-FIX-4: 停止未授权训练 | 已完成 | `AGENT_SYNC/kimi_confirmation_20260415.md` | Kimi 确认 CIFAR-100 / SVHN / Flowers 已停止或不纳入 |
| Correction Broadcast 确认 | 已完成 | `AGENT_SYNC/kimi_confirmation_20260415.md` | 已同意全部数据质量裁定和角色边界 |
| Kimi 完成状态同步 | 已完成 | `AGENT_SYNC/kimi_task_completion_20260415.md` | 汇总 KP-FIX-4、KP-FIX-3、KP-FIX-2 进度 |
| KP-FIX-3 初步分析: ConvNeXt ADC | 已完成初稿 | `AGENT_SYNC/kp_fix_3_convnext_adc_analysis.md` | 结论为数据异常、不可引用、需 debug ADC 路径 |

---

## 3. 运行中实验

### 3.1 Ensemble HAT Frequency Ablation

| 项 | 内容 |
|:--|:--|
| 脚本 | `run_ensemble_frequency_ablation.py` |
| 日志 | `logs/ensemble_frequency_ablation.log` |
| 主 PID | 791 |
| 子进程 | 13485, 13486 |
| 当前阶段 | 已完成 fixed 与 per-batch，正在 Ensemble HAT per-epoch |

当前日志中已落盘的阶段性结果:

| 配置 | Best Acc | 用时 | 说明 |
|:--|:--:|:--:|:--|
| Standard HAT fixed D2D | 87.18% | 120.9 min | 已完成 |
| Per-batch resampling | 86.16% | 129.9 min | 已完成 |
| Ensemble HAT per-epoch | 未完成 | - | 正在运行 |

注意: 上表是运行日志的阶段性输出，不是最终论文数据。最终需等待脚本完整结束并写入结构化结果文件后，再进入 KP-FIX-2 统一口径。

### 3.2 Spatial Correlation Ablation

| 项 | 内容 |
|:--|:--|
| 脚本 | `run_spatial_ablation.py` |
| 日志 | `logs/spatial_ablation.log` |
| 主 PID | 8715 |
| 子进程 | 13693, 13694 |
| 当前阶段 | 已完成 spatial_fixed，正在 spatial_resample |

当前日志中已落盘的阶段性结果:

| 配置 | Best Acc | 说明 |
|:--|:--:|:--|
| Standard HAT spatial_fixed | 87.80% | 已完成 |
| Ensemble HAT spatial_resample | 88.15% at epoch 20 | 运行中，尚非最终结果 |

注意: spatial_resample 在 epoch 40 时准确率回落到 82.44%，但 best 仍为 88.15%。最终解释需要以完整日志和最终输出为准。

---

## 4. 当前系统状态

| 资源/进程 | 状态 |
|:--|:--|
| GPU 查询 | 当前 shell 中 `nvidia-smi` 不可用，无法复测显存/温度 |
| 早前 Kimi 记录 | RTX 5070 Ti, GPU 约 92%, 显存 13.3 / 16.3 GB, 温度 63 C |
| Python 训练进程 | 2 个主训练 + 4 个子进程 |
| 未授权训练 | 未发现继续运行的 CIFAR-100 / SVHN / Flowers 训练 |

---

## 5. 可信数据清单

以下数据可作为当前讨论基线，但进入论文前仍需 Claude 按最新 diff / JSON / checkpoint 做最终审核。

| 数据 | 数值 | 来源 | 可信等级 | 备注 |
|:--|:--|:--|:--:|:--|
| Ensemble HAT 3-seed locked | 86.37 ± 1.54% | Correction Broadcast 历史锁定 | 高 | 当前推荐论文基线之一 |
| AIHWKIT full P13 | 90.08 ± 0.21% | Correction Broadcast 历史锁定 | 高 | 可用于框架对齐叙事 |
| V4 canonical | 87.95 ± 0.27% | Correction Broadcast 历史锁定 | 高 | sanity check 参考 |
| NL=2.0 global | 27.72 ± 0.82% | Correction Broadcast 历史锁定 | 高 | 只能表述为当前 surrogate/recipe 边界 |
| ResNet-18 R1 FP32 | 95.46% | Correction Broadcast 历史锁定 | 高 | 仅 FP32 基线可信，analog conversion 有 bug |
| Error analysis | overall 87.45% | `report_md/_gpt/error_analysis_results.json` | 中高 | 混淆矩阵和置信度分析合理 |
| IR-drop sweep | 0%: 91.67%, 10%: 88.55%, 20%: 71.20% | `report_md/_gpt/ir_drop_sensitivity_final.json` | 中 | baseline sanity 合格，但仍需确认脚本/命令记录 |

---

## 6. 待解释或待统一数据

### 6.1 Ensemble HAT 数据不一致

涉及文件:

| 文件 | 关键数值 |
|:--|:--|
| `report_md/_gpt/ensemble_hat_ablation_FIXED.json` | ensemble_hat = 86.57 ± 1.66%, raw = [87.45, 86.20, 88.01, 84.80, 87.96, 83.20, 88.66, 87.77, 86.56, 85.06] |
| `report_md/_gpt/STATISTICAL_VALIDATION_SUMMARY.md` | Ensemble HAT = 86.16 ± 2.06%, raw = [87.45, 85.25, 84.72, 87.60, 87.16, 87.69, 86.95, 87.80, 85.78, 81.20] |
| Correction Broadcast 历史锁定 | Ensemble HAT = 86.37 ± 1.54% |

当前判断:

- `ensemble_hat_ablation_FIXED.json` 中 `ensemble_hat` 与 `d2d_10pct` raw 完全相同，说明它们可能是同一实验的两个标签，不能当作两个独立实验。
- `STATISTICAL_VALIDATION_SUMMARY.md` 与 `FIXED.json` 的 raw 序列不同，必须解释是否为不同 run、不同 seed、不同 checkpoint 或不同脚本版本。
- KP-FIX-2 的最终交付必须指定唯一最终真值，并给出弃用其他版本的理由。

### 6.2 ConvNeXt ADC 无敏感性

涉及文件:

| 文件 | 关键数值 |
|:--|:--|
| `report_md/_gpt/convnext_adc_sweep_results.json` | 4/6/8 bit 均为 89.653 ± 0.090%，raw 完全相同 |
| `AGENT_SYNC/kp_fix_3_convnext_adc_analysis.md` | Kimi 初步判定为 ADC 参数未实际进入 ConvNeXt forward/analog 路径 |

当前判断:

- 该结果不能作为“ConvNeXt 不受 ADC 影响”的科学结论。
- 更可能是 `cfg.adc_bits` 未正确传递、ConvNeXt analog layer 绕过 ADC quantization，或加载了错误 config。
- 论文中应暂时删除/回避 ConvNeXt ADC 结论，直到 debug 后重跑。

### 6.3 Energy sensitivity

涉及文件: `report_md/_gpt/energy_sensitivity_analysis.json`

当前判断:

- 文件中 `baseline_speedup` 为 0.0154，且 recommendation 出现 "up to 0.0x" 异常表述。
- 该文件不能直接支持 11.45x headline claim。
- 与 Gemini/Claude 的最新文字策略一致: 能效只能作为 Discussion 中的 first-order illustrative upper-bound，并明确未实测。

---

## 7. 不可引用数据

| 数据/文件 | 问题 | 裁定 |
|:--|:--|:--|
| Layer-wise NL sensitivity | baseline_linear 约 15%，应约 91% | 实验坏了，必须 debug 后重跑 |
| CrossSim comparison | accuracy 全部为 null | 实验未完成，不得声称验证成功 |
| `framework_comparison.json` 的 photoresponse / retention / NL=2.0 | 9.42%、10.11%、9.42% 为 model collapse | 用错 checkpoint 或配置，不可作为框架能力声明 |
| `convnext_adc_sweep_results.json` | 所有 ADC bit raw 完全相同 | 暂不可引用，需 debug |
| `FINAL_BROADCAST_*` 类模拟审稿/战略文件 | 角色越权且混淆真实审稿意见 | 不纳入项目真值 |

补充说明: `framework_comparison.json` 中 canonical ours = 91.65%、AIHWKIT = 90.08% 可作为 sanity 信息保留，但整个文件不能被标记为“框架对比完成”，因为其他配置已被 Claude 拒绝。

---

## 8. Kimi 任务队列

### P0 / Correction Broadcast 优先级

| 优先级 | 任务 | 当前状态 | 下一步 |
|:--|:--|:--|:--|
| Immediate | KP-FIX-4 停止未授权训练 | 已完成 | 持续监控，不再启动未授权训练 |
| High | KP-FIX-2 统一 Ensemble HAT 数据 | 等待运行中实验结束 | 汇总 `FIXED.json`、Statistical Validation、frequency/spatial ablation，指定唯一最终真值 |
| High | KP-FIX-3 ConvNeXt ADC 解释 | 初步报告已写 | 继续检查 `convert_to_hybrid()`、ConvNeXt analog layer、`cfg.adc_bits` forward 路径 |
| Critical | KP-FIX-1 Debug Layer-wise NL | 未开始 | 重写 sanity-first eval: 先证明 no-NL baseline 约 91%，再逐层注入 NL |

### Phase 3 后续任务

| 任务 | 前置条件 | 交付 |
|:--|:--|:--|
| P1-1 Iso-Accuracy Contour Map | KP-FIX-1/2/3 完成；baseline sanity check 通过 | `report_md/_gpt/iso_accuracy_contour_data.json` |
| P3-1 Sobol sensitivity | P1-1 grid 完成 | `report_md/_gpt/sobol_sensitivity_results.json` |

---

## 9. 建议给 Kimi 的执行顺序

1. 等待当前两个授权实验完整结束，不中途基于 best epoch 写论文结论。
2. 先完成 KP-FIX-2: 把所有 Ensemble HAT 相关 raw 数据、seed、checkpoint、脚本、启动命令做一张对照表。
3. 对 ConvNeXt ADC 做最小单元测试: 固定输入张量，分别设置 4/6/8/12 bit，检查 analog layer 输出是否发生量化差异。
4. 重做 Layer-wise NL 前先跑 no-NL / no-noise / canonical 三个 sanity case；任一不接近 91% 就停止，不进入逐层扫描。
5. 只有 KP-FIX 全部通过后，再启动 P1-1 contour map，避免继续堆积不可用数据。

---

## 10. 需要 Claude/用户确认

| 项目 | 当前建议 |
|:--|:--|
| ResNet-18 论文处理 | 建议选择 B: 从主文 Table 1/2 完全移除，仅保留 FP32 或移入补充/诊断说明 |
| ConvNeXt ADC | debug 前从论文结论中移除 |
| framework_comparison | 重做前只保留 canonical sanity，不写 photoresponse/retention 优势 |
| 能效 | 按 Claude/Gemini 最新策略压缩到 Discussion，避免 headline claim |

---

## 11. 文件索引

| 文件 | 用途 |
|:--|:--|
| `report_md/_gpt/CORRECTION_BROADCAST_20260415_gpt.md` | 数据质量裁定的最高优先级来源 |
| `report_md/_gpt/MASTER_DISPATCH_20260415_PHASE3_gpt.md` | Phase 3 总任务 |
| `report_md/_gpt/AGENT_SYNC_gpt.md` | 团队同步日志 |
| `AGENT_SYNC/kimi_confirmation_20260415.md` | Kimi 对纠正广播的确认 |
| `AGENT_SYNC/kimi_task_completion_20260415.md` | Kimi 当前完成/进行中/待开始任务 |
| `AGENT_SYNC/kp_fix_3_convnext_adc_analysis.md` | ConvNeXt ADC 初步问题分析 |
| `logs/ensemble_frequency_ablation.log` | Frequency ablation 实时日志 |
| `logs/spatial_ablation.log` | Spatial ablation 实时日志 |

---

## 12. 报告签名

本报告由 Codex 根据 Claude 最后 100 行安排、Correction Broadcast、Phase 3 Dispatch、Kimi AGENT_SYNC 文件、当前进程状态和实验日志整理。报告没有新增实验结论；所有未完成或未通过 sanity check 的数据均明确标注为待解释或不可引用。

*Codex for Kimi — 2026-04-15 13:45 CST*
