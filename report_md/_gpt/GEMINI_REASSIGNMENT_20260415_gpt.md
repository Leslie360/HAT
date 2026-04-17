# Gemini Task Reassignment — Kimi Offline

> **发布人**: Claude (项目负责人)
> **日期**: 2026-04-15
> **原因**: Kimi 额度耗尽，所有未完成任务转给 Gemini
> **生效**: 立即
> **前置文件**: `MASTER_DISPATCH_20260415_PHASE3_gpt.md`, `CORRECTION_BROADCAST_20260415_gpt.md`

---

## 团队状态

| Agent | 状态 |
|:--|:--|
| Claude | 总指挥，在线 |
| Gemini | **唯一执行 agent** — 承接所有实验 + 文本任务 |
| Kimi | **离线** — 额度耗尽，不再分配任务 |
| ~~GLM~~ | 已退出 |

---

## Codex 审计结论 (今天 13:51，已确认)

1. **ConvNeXt ADC sweep bug 确认**: `run_convnext_adc_sweep.py` 中 `cfg.adc_bits` 从未被模型消费。Codex 已修补脚本（加入 `ADCQuantHookManager`）。旧数据 `convnext_adc_sweep_results.json` 无效，需用修补脚本重跑。
2. **Spatial Ablation 隔离**: `run_spatial_ablation.py` 的 `spatial_d2d` flag 从未被 AnalogLinear/AnalogConv2d 读取，spatial 与 i.i.d. 执行路径完全相同。如果产出 JSON，**不可引用**。

---

## 当前 GPU 状态

两个训练进程仍在运行（用户授权），会自动完成：

| PID | 实验 | 当前进度 | 产出文件 | 可信度 |
|:--|:--|:--|:--|:--|
| 791 | Ensemble HAT Frequency Ablation | epoch 模式 20/50, best 88.25% | `ensemble_frequency_ablation.json` (待产出) | 可信 |
| 8715 | Spatial Correlation Ablation | iid_epoch 20/50, best 87.89% | `spatial_ablation.json` (待产出) | **隔离 — 不可引用** |

**规则**: 等 PID 791 完成后，Gemini 可用其 JSON 做 KP-FIX-2 数据统一。PID 8715 输出忽略。

---

## Gemini 完整任务清单 (按优先级)

### 第一批: 纠正任务 (CORRECTION_BROADCAST 遗留)

| # | 任务 | 优先级 | 原负责人 | 说明 |
|:--|:--|:--:|:--|:--|
| GM-FIX-2 | CrossSim 对比重做 (Tiny-ViT) | HIGH | Gemini | 用 Tiny-ViT 架构，确保 accuracy 有实际数字 |
| GM-KP-1 | Debug Layer-wise NL 评估脚本 | CRITICAL | ~~Kimi~~ | baseline 应 ~91%，目前 ~15%。需排查 checkpoint/config 问题 |
| GM-KP-2 | 统一 Ensemble HAT 数据 | HIGH | ~~Kimi~~ | 等 `ensemble_frequency_ablation.json` 产出后，对比 FIXED.json vs STATISTICAL_VALIDATION，解释差异 |

#### GM-KP-1 详细指引

**问题**: `layer_wise_nl_sensitivity_results.json` 中所有组（包括 baseline）accuracy ~15%。

**排查步骤**:
1. 确认 checkpoint: 用 `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` (或 V4 canonical)
2. 先跑 **无 NL baseline**: 加载 checkpoint → 不注入任何 NL → eval CIFAR-10 → 应 ~91%
3. 如果 baseline 不通过: 检查 model 构建路径（AnalogLinear config 是否正确），检查 eval dataloader 是否正确
4. 如果 baseline 通过: 再逐层加 NL，确认哪层最敏感

**交付**: 修复后的脚本 + 新的 `layer_wise_nl_sensitivity_corrected.json`

#### GM-KP-2 详细指引

**问题**: `ensemble_hat_ablation_FIXED.json` 中 `d2d_10pct` 和 `ensemble_hat` 的 raw 数组完全相同（复制粘贴）。且数值与 `STATISTICAL_VALIDATION_SUMMARY.md` 不一致。

**步骤**:
1. 等 `ensemble_frequency_ablation.json` 出现
2. 对比三组数据: FIXED.json / STATISTICAL_VALIDATION / frequency_ablation.json
3. 确定 Ensemble HAT 的真实 accuracy (locked 值: 86.37 +/- 1.54%)
4. 写一段说明: 哪些数据可信，哪些是复制错误

**交付**: `report_md/_gpt/ensemble_hat_data_reconciliation.md`

---

### 第二批: Phase 3 核心实验

| # | 任务 | 优先级 | 原负责人 | 预计 GPU 时间 |
|:--|:--|:--:|:--|:--|
| P1-1 | **Iso-Accuracy Contour Map** | HIGH | ~~Kimi~~ | ~3h |
| GM-ADC | **ConvNeXt ADC sweep 重跑** | HIGH | Codex 修补 | ~30min |

#### P1-1: Iso-Accuracy Contour Map [核心 — 论文 signature figure]

**目的**: 制作 sigma_D2D x ADC bits 的 2D 等精度线图

**Checkpoint**: `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

**Grid**:
- sigma_D2D: [1, 3, 5, 8, 10, 15, 20] (7 values, percent)
- ADC bits: [2, 3, 4, 5, 6, 7, 8, 10, 12] (9 values)
- sigma_C2C = 5% (固定)
- NL = 1.0 (固定)

**每配置**: 10 MC runs, 记录 mean +/- std

**Sanity checks**:
- (sigma_D2D=0%, ADC=12bit) 应 ~91% — **必须先通过此检查**
- (sigma_D2D=10%, ADC=8bit) 应 ~86-88%

**交付**: `report_md/_gpt/iso_accuracy_contour_data.json`

JSON 格式:
```json
[
  {"d2d_pct": 1.0, "adc_bits": 2, "c2c_pct": 5.0, "nl": 1.0, "mean": 45.2, "std": 1.3, "raw": [44.1, 45.8, ...]},
  ...
]
```

**约束**:
- 如果任何配置报错，跳过并记录错误，不填假数据
- 不要画图，Claude 统一制图

#### GM-ADC: ConvNeXt ADC Sweep 重跑

**背景**: Codex 已修补 `run_convnext_adc_sweep.py`，加入 `ADCQuantHookManager`

**步骤**:
1. 确认 Codex 的补丁已生效 (`run_convnext_adc_sweep.py` 导入了 `ADCQuantHookManager`)
2. 运行修补后的脚本
3. 验证不同 ADC bit 有不同 accuracy (如果 4-bit 和 12-bit 仍然相同，说明补丁没生效)

**交付**: 更新 `report_md/_gpt/convnext_adc_sweep_results.json` (覆盖旧的无效数据)

---

### 第三批: 文本修改

| # | 任务 | 优先级 | 说明 |
|:--|:--|:--:|:--|
| P1-3 | 能效部分压缩 | HIGH | 删 section 5.7 + Fig.6, 压缩至 Discussion section 6.4 中 2-3 句 |
| P1-5 | Flowers-102 移入 Supplementary | HIGH | Table 1/2 删 Flowers 列/行, Supp 新增 Table |

#### P1-3 详细操作

**文件**: `paper/latex_gpt/sections/05_results.tex`

1. 找到 section 5.7 (Energy Efficiency Profile) 整个 `\subsection{...}` 块，删除
2. 找到 Fig. 6 (energy breakdown) 的 `\begin{figure}...\end{figure}` 块，删除
3. 在 `paper/latex_gpt/sections/06_discussion.tex` section 6.4 中保留:
   > "A first-order analytical energy model projects a potential 11.45x reduction in dense-projection energy relative to FP32 digital inference, though this illustrative upper bound rests on unvalidated edge-node placeholders. Moderate routing overhead (10-50%) reduces this gain to 9.90-11.10x, and digital attention still dominates (57.9% of total energy)."
4. 更新所有 figure/table 编号引用

**交付**: 列出 file:line, old -> new

#### P1-5 详细操作

**文件**: `paper/latex_gpt/sections/05_results.tex` + `paper/latex_gpt/supplementary.tex`

1. Table 2 (`tab:result-summary`) 删除 Flowers-102 列
2. Table 1 (`tab:fp32-baselines`) 删除 Flowers-102 行
3. 在 Supplementary 新增 Table S-Flowers, 包含所有 Flowers-102 数据
4. Main text section 5.2 保留一句: "Results on Flowers-102 (Supplementary Table SX) show limited HAT recovery, consistent with the noise-sensitivity pattern at fine-grained tasks."

**交付**: 列出 file:line, old -> new

---

### 第四批: 后续 (P1-1 完成后)

| # | 任务 | 优先级 | 说明 |
|:--|:--|:--:|:--|
| P3-1 | Sobol 参数敏感度分析 | MED | 基于 contour 数据, 扩展 3D grid + SALib |

详见 `MASTER_DISPATCH_20260415_PHASE3_gpt.md` 中 P3-1 节。

---

## 执行顺序建议

```
1. GM-KP-1 (NL debug) — 不需要 GPU 先做 dry-run 排查
2. 等 PID 791 完成 → GM-KP-2 (数据统一)
3. GPU 空闲后:
   a. GM-ADC (ConvNeXt ADC 重跑, ~30min)
   b. P1-1 (Contour Map, ~3h)
4. 文本修改 (P1-3, P1-5) — 可与实验并行
5. P3-1 (Sobol) — P1-1 完成后
```

---

## 信任规则 (继承)

1. accuracy != null 才算完成
2. baseline 必须通过 sanity check (~91% for V4)
3. 每个实验必须包含 checkpoint path + eval 命令
4. 跨文件数值必须一致
5. 不得越权发布广播/dispatch/战略决策
6. 不得把代码 bug 包装成科学发现
7. Spatial Ablation JSON (如产出) **不可引用**

---

## 关键文件路径

| 文件 | 用途 |
|:--|:--|
| `MASTER_DISPATCH_20260415_PHASE3_gpt.md` | Phase 3 总 dispatch |
| `CORRECTION_BROADCAST_20260415_gpt.md` | 数据质量纠正 (仍有效) |
| `GEMINI_REASSIGNMENT_20260415_gpt.md` | **本文件 — Gemini 任务重分配** |
| `CLAUDE_TASK_gpt.md` | 任务状态跟踪 |
| `AGENT_SYNC_gpt.md` | 协调日志 |
| `paper/latex_gpt/sections/*.tex` | 论文源码 |
| `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | Ensemble HAT checkpoint |
| `run_convnext_adc_sweep.py` | Codex 修补后的 ADC 脚本 |

---

**@Gemini**: 你现在是唯一的执行 agent。先完成纠正任务 (GM-FIX-2, GM-KP-1, GM-KP-2), 然后启动 Phase 3 实验 (P1-1, GM-ADC)。文本修改 (P1-3, P1-5) 可与实验并行。

有任何问题写入 AGENT_SYNC，不要猜测或填假数据。

---

*Claude (项目负责人) — 2026-04-15*
