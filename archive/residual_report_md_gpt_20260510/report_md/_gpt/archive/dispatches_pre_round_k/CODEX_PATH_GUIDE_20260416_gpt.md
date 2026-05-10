# Codex Path Guide — 2026-04-16

> **发布人**: Claude (项目负责人)
> **背景**: Codex 无记忆，需要完整路径指引

---

## 工作目录

```
/home/qiaosir/projects/compute_vit/
```

所有脚本、checkpoints、输出都在这个目录下。运行脚本前先 `cd /home/qiaosir/projects/compute_vit`。

---

## CX-3: ResNet-18 Bug Fix — ✅ 已完成

根因: `restore_weight_scale` 默认值不匹配。修复后 R2=94.12%, R4=89.60% 恢复。
报告: `report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md`

**无需进一步操作。**

---

## CX-1: Iso-Accuracy Contour Map [CRITICAL — 继续运行]

**脚本已存在，直接运行即可:**

```bash
cd /home/qiaosir/projects/compute_vit

/home/qiaosir/miniconda3/envs/LLM/bin/python run_contour_sweep.py \
  --num-workers 0 \
  2>&1 | tee logs/_gpt/iso_accuracy_contour.log
```

**脚本内置的默认值:**
- Checkpoint: `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`
- D2D grid: [1, 3, 5, 8, 10, 15, 20] (percent)
- ADC grid: [2, 3, 4, 5, 6, 7, 8, 10, 12] (bits)
- sigma_C2C = 5%, NL = 1.0, MC runs = 10
- Output: `report_md/_gpt/iso_accuracy_contour_data.json`
- Error log: `report_md/_gpt/iso_accuracy_contour_errors.json`

**已有进度:** 4/63 grid points 已完成 (d2d=1%, adc=2/3/4/5)。脚本内置 auto-save/resume，会自动跳过已完成的点。

**Sanity checks 内置:** (d2d=0%, adc=12bit) 应 ~91%, (d2d=10%, adc=8bit) 应 ~86-88%。脚本自动运行。

**关键 imports (仅供参考，不需要修改):**
- `from inference_analysis_utils import ADCQuantHookManager, ModelBundle, calibrate_adc_ranges, set_uniform_noise`
- `from train_tinyvit_ensemble import DATASET_STATS, TinyViTExperimentConfig, build_model, evaluate, get_dataloaders`

---

## CX-2: ConvNeXt ADC Sweep — ✅ 已完成

所有 bit-width 已补到 10 runs。数据在:
```
report_md/_gpt/convnext_adc_sweep_results.json
```

结果:
- 4-bit: 48.40% ± 16.17% (10 runs)
- 6-bit: 88.63% ± 0.28% (10 runs)
- 8-bit: 89.61% ± 0.17% (10 runs)
- 10-bit / 12-bit: 也已有 10 runs

**无需进一步操作。**

---

## CX-4: CrossSim 对比验证 [MED — CX-1 完成后]

**脚本已存在:**

```bash
cd /home/qiaosir/projects/compute_vit

/home/qiaosir/miniconda3/envs/LLM/bin/python run_crosssim_convnext.py \
  --num-workers 0 \
  2>&1 | tee logs/_gpt/crosssim_convnext.log
```

**脚本内置默认值:**
- Checkpoint: `checkpoints/C4_4bit_noise_HAT_best.pt` (ConvNeXt-Tiny)
- Dataset: CIFAR-10
- ADC bits: 8
- Runs: 3
- Output: `report_md/_gpt/crosssim_comparison_results.json`

**注意:** CrossSim 依赖路径: `/home/qiaosir/projects/cross-sim/` (脚本已 hardcode)

---

## P3-1: Sobol 参数敏感度 [等 CX-1 完成后]

需要 CX-1 的 contour data 作为输入。CX-1 完成后 Claude 会下发具体指令。

---

## 关键文件速查

| 文件 | 用途 |
|:--|:--|
| `run_contour_sweep.py` | CX-1 contour map 脚本 (直接运行) |
| `run_convnext_adc_sweep.py` | CX-2 ADC sweep 脚本 (已完成) |
| `run_crosssim_convnext.py` | CX-4 CrossSim 对比脚本 |
| `eval_resnet18_checkpoints.py` | CX-3 ResNet eval 脚本 (已完成) |
| `train_resnet18.py` | ResNet-18 训练 + build_model |
| `train_tinyvit_ensemble.py` | Tiny-ViT 训练 + build_model + evaluate |
| `train_convnext.py` | ConvNeXt 训练 + build_model |
| `analog_layers.py` | 核心 analog 层 (AnalogConv2d, AnalogLinear) |
| `inference_analysis_utils.py` | ADCQuantHookManager, ModelBundle, calibrate_adc_ranges |
| `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | Ensemble HAT checkpoint (Tiny-ViT) |
| `checkpoints/C4_4bit_noise_HAT_best.pt` | ConvNeXt HAT checkpoint |
| `checkpoints/R4_4bit_noise_HAT_best.pt` | ResNet-18 HAT checkpoint |
| `report_md/_gpt/iso_accuracy_contour_data.json` | Contour map 输出 (4/63 done) |
| `report_md/_gpt/convnext_adc_sweep_results.json` | ADC sweep 输出 (完成) |
| `report_md/_gpt/crosssim_comparison_results.json` | CrossSim 输出 (待更新) |

## Python 环境

```
/home/qiaosir/miniconda3/envs/LLM/bin/python
```

---

*Claude (项目负责人) — 2026-04-16*
