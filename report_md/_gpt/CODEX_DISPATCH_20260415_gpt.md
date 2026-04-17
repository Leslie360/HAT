# Codex Dispatch — Phase 3 GPU Sprint

> **发布人**: Claude (项目负责人)
> **日期**: 2026-04-15
> **背景**: Kimi 离线 (无额度), Gemini 效率低/卡顿, Codex 额度满
> **目标**: Codex 接管所有 GPU 实验 + 代码调试任务
> **GPU 状态**: 完全空闲 (PID 791 刚完成)

---

## 团队状态

| Agent | 角色 | 状态 |
|:--|:--|:--|
| Claude | 总指挥 — 审核/决策/文本 | 在线 |
| **Codex** | **主力执行** — GPU 实验 + 代码调试 | ✅ 额度满 |
| Gemini | 备用 — 文本/轻量任务 | ⚠️ 卡顿低效 |
| ~~Kimi~~ | 离线 | ❌ |

---

## Codex 任务清单 (按优先级)

### CX-1: Iso-Accuracy Contour Map [CRITICAL — 论文 signature figure]

**状态**: Gemini 的 PID 78002 已 crash，无输出，无 log。需要从零启动。

**Checkpoint**: `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

**Grid**:
- sigma_D2D: [1, 3, 5, 8, 10, 15, 20] (7 values, percent)
- ADC bits: [2, 3, 4, 5, 6, 7, 8, 10, 12] (9 values)
- sigma_C2C = 5% (固定)
- NL = 1.0 (固定)
- 每配置 10 MC runs

**Sanity checks (必须先通过)**:
- (sigma_D2D=0%, ADC=12bit) 应 ~91%
- (sigma_D2D=10%, ADC=8bit) 应 ~86-88%

**交付**: `report_md/_gpt/iso_accuracy_contour_data.json`

JSON 格式:
```json
[
  {"d2d_pct": 1.0, "adc_bits": 2, "c2c_pct": 5.0, "nl": 1.0, "mean": 45.2, "std": 1.3, "raw": [44.1, 45.8, ...]},
  ...
]
```

**实现要点**:
- 使用 Tiny-ViT hybrid 模型 + V4 Ensemble HAT checkpoint
- ADC 量化用 `ADCQuantHookManager` (参考 Codex 自己修补的 `run_convnext_adc_sweep.py`)
- D2D 通过修改 `module.config.sigma_d2d` 实现
- 加 auto-save/resume: 每完成一个 grid 点就写入 partial JSON，防 crash 丢数据
- 如果某配置报错，跳过并记录，不填假数据
- 不画图，Claude 统一制图

**预计 GPU**: ~3h (63 configs x 10 runs x ~17s/run)

---

### CX-2: ConvNeXt ADC Sweep 补充 Runs [HIGH — 30min]

**状态**: Codex 之前修补了 `run_convnext_adc_sweep.py`，Gemini 跑了但 runs 不足。

**现有数据** (`convnext_adc_sweep_results.json`):
- 4-bit: 3 runs (std=11.4% — 太大)
- 6-bit: 3 runs
- 8-bit: 3 runs
- 10-bit: 1 run
- 12-bit: 1 run

**需要**: 所有 bit-width 补到 10 runs。更新 JSON。

**Checkpoint**: `checkpoints/C4_4bit_noise_HAT_best.pt`

---

### CX-3: ResNet-18 Deep Bug Investigation [HIGH — 代码调试]

**问题**: R4 HAT checkpoint 训练时 eval=90.37%，但 `strict=True` load 后 eval=10%。

**已排除**:
- 诊断脚本 bug (Gemini 用正确方法复现了 10%)
- BN stats 替换 (替换后仍 10.36%)

**排查方向**:
1. **Checkpoint 完整性**: 逐 key 对比 `model.state_dict()` (训练时 vs 加载后)
2. **Config 一致性**: 打印训练时 AnalogLinearConfig vs 加载时 AnalogLinearConfig 的每个字段
3. **w_abs_max 漂移**: 在 `_weight_to_conductance` 中加 print，对比训练最后一个 eval 和 load 后 eval 的 w_abs_max
4. **d2d_noise 一致性**: 对比训练时和加载后的 d2d_noise buffer
5. **最小复现**: 训练 1 epoch → save → load → eval，看是否立刻复现 10%

**Checkpoint**: `checkpoints/R4_4bit_noise_HAT_best.pt` (CIFAR-10)

**交付**: 排查报告 + 修复 (如果找到 bug)

---

### CX-4: CrossSim 对比验证 [MED]

**问题**: 原数据全部 accuracy=null。Gemini 尝试 Tiny-ViT (OOM) 和 ResNet-18 (有 bug)。

**方案**: 用 **ConvNeXt-Tiny** — 已确认 working (89.68% at 8-bit ADC)。

**目标**: 在相同 noise profile 下对比我们的框架 vs CrossSim 的结果。

**Checkpoint**: `checkpoints/C4_4bit_noise_HAT_best.pt`

**交付**: 更新 `crosssim_comparison_results.json`，accuracy 必须 != null。

---

## 执行顺序

```
1. CX-1 (Contour Map) — 立即启动，~3h GPU，后台运行
2. CX-2 (ADC 补 runs) — 可以和 CX-1 并行如果 GPU 内存够，否则等 CX-1 完成
3. CX-3 (ResNet-18 debug) — 不需要大量 GPU，可以在 CX-1 运行时做代码分析
4. CX-4 (CrossSim) — CX-1 完成后
```

---

## 已完成的实验数据 (供参考)

| 数据 | 来源 | 状态 |
|:--|:--|:--|
| Ensemble HAT Frequency Ablation | Kimi (PID 791) | ✅ `ensemble_frequency_ablation.json` |
| ConvNeXt ADC (partial) | Gemini | ⚠️ runs 不足 |
| Spatial Ablation | Kimi (PID 8715) | ❌ 隔离 — spatial_d2d flag 未被消费 |
| Layer-wise NL baseline | Gemini (GM-KP-1) | ✅ 90.94% |

---

## 信任规则

1. accuracy != null 才算完成
2. baseline sanity check 必须先通过
3. 每个实验记录 checkpoint path + eval 命令
4. 跨文件数值一致
5. 不填假数据 — 报错就跳过并记录
6. 输出 tee 到 `logs/` 目录
7. Spatial Ablation JSON 不可引用

---

## 关键文件路径

| 文件 | 用途 |
|:--|:--|
| `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | Ensemble HAT checkpoint (Tiny-ViT) |
| `checkpoints/C4_4bit_noise_HAT_best.pt` | ConvNeXt HAT checkpoint |
| `checkpoints/R4_4bit_noise_HAT_best.pt` | ResNet-18 HAT checkpoint (有 bug) |
| `run_convnext_adc_sweep.py` | Codex 修补后的 ADC sweep 脚本 |
| `analog_layers.py` | 核心 analog 层 (AnalogConv2d, AnalogLinear) |
| `train_resnet18.py` | ResNet-18 训练脚本 (build_model, set_noise_for_eval) |
| `report_md/_gpt/iso_accuracy_contour_data.json` | (待产出) Contour map 数据 |
| `report_md/_gpt/convnext_adc_sweep_results.json` | (待更新) ADC sweep 数据 |
| `report_md/_gpt/crosssim_comparison_results.json` | (待更新) CrossSim 对比 |

---

*Claude (项目负责人) — 2026-04-15*
