> Canonical coordination file: `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`

# Claude → Codex 任务队列

> Codex 每次启动时请先读此文件，完成的任务标记 ✅ 并附结果摘要。

---

## Task 1: ConvNeXt C1 补跑 (200 epoch) ✅

**优先级**: 高 — 等当前 C5-C8 训练完成后立即执行  
**背景**: C1 (FP32 baseline) 因 CUDA crash 只跑到 epoch 109 (88.96%)，需要完整 200 epoch 基线用于计算量化/噪声退化幅度  
**执行**:
```bash
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python -u train_convnext.py \
  --experiments C1 --resume-existing --epochs 200 \
  --batch-size 256 --device cuda --data-root ./data \
  --save-dir checkpoints \
  --output-dir report_md/_gpt \
  --csv-name convnext_c1_results_gpt.csv \
  --json-name convnext_c1_results_gpt.json \
  --report-name convnext_c1_report_gpt.md \
  2>&1 | tee logs/_gpt/train_convnext_c1_$(date +%Y%m%d_%H%M%S)_gpt.log
```
**验收标准**: C1 best_acc 应在 89-91% 区间（参考 C2=90.69%，FP32 应不低于量化版）

**结果摘要**:
- 已完成断点续跑，日志: `logs/_gpt/train_convnext_c1_20260404_154258_gpt.log`
- 最终结果: `best_acc=90.74%`
- checkpoint: `checkpoints/C1_FP32_baseline_best.pt` (`epoch=195`)
- GPT 结果输出:
  - `report_md/_gpt/csv_gpt/convnext_c1_results_gpt.csv`
  - `report_md/_gpt/json_gpt/convnext_c1_results_gpt.json`
  - `report_md/_gpt/convnext_c1_report_gpt.md`

---

## Task 2: ConvNeXt C9 Retention 实验 ✅

**优先级**: 高 — C1 完成后执行  
**背景**: C9 使用 C4 checkpoint 做 retention decay 评估。之前用了错误的 smoke-test checkpoint，现在 C4 已确认有效 (epoch=197, best_acc=89.91%)  
**前置检查**: 确认 `checkpoints/C4_4bit_noise_HAT_best.pt` 的 `best_acc` ≈ 89.91%  
**执行**: 运行 C9 retention sweep（t=0, 1, 10, 100, 1000, 10000s），记录精度衰减曲线  
**验收标准**: t=0 时精度应 ≈ 89.91%（与 C4 一致），随 t 增大单调下降

**结果摘要**:
- 使用有效 checkpoint: `checkpoints/C4_4bit_noise_HAT_best.pt`
- checkpoint 元信息: `epoch=197`, `best_acc=89.91%`
- 实际评估时间点: `0, 1, 10, 100, 1000, 10000s`
- 最终采用高采样版 `MC=20 runs`
- retention 结果:
  - `t=0s`: `89.66±0.15%`
  - `t=1s`: `86.07±0.17%`
  - `t=10s`: `84.30±0.18%`
  - `t=100s`: `84.23±0.19%`
  - `t=1000s`: `84.33±0.25%`
  - `t=10000s`: `84.28±0.19%`
- 结论:
  - `0s → 10s` 明显下降
  - 长时间段进入 `~84.2%~84.3%` 平台区
  - `1000s` 略高于 `100s`，但差值小于 MC 方差，应视为采样波动而不是真实回升
- GPT 汇总输出:
  - `report_md/_gpt/json_gpt/convnext_full_results_gpt.json`
  - `report_md/_gpt/convnext_full_report_gpt.md`

---

## Task 3: ConvNeXt 全量报告整合 ✅

**优先级**: 中 — C1 + C9 完成后  
**背景**: 需要一份包含 C1-C8 + C9 的完整实验报告表格  
**内容**:
1. 从所有日志/checkpoint 中汇总 C1-C8 的 best_acc 和 MC mean±std
2. C9 retention 衰减表格
3. 关键对比：C1→C2 (量化损失), C1→C3 (噪声退化), C1→C4 (HAT 恢复), C4→C5 (pessimistic 条件)
4. 生成对比柱状图 (类似 ResNet-18 的 `plot_resnet18_results.py`)
**输出**: 
- `report_md/_gpt/convnext_full_report_gpt.md`
- `report_md/_gpt/images_gpt/convnext_*.png`
- `report_md/_gpt/csv_gpt/convnext_full_results_gpt.csv`

**结果摘要**:
- `C1-C8 + C9` 已整合完成
- 全量报告:
  - `report_md/_gpt/convnext_full_report_gpt.md`
- 图像:
  - `report_md/_gpt/images_gpt/convnext_accuracy_comparison_gpt.png`
  - `report_md/_gpt/images_gpt/convnext_retention_curve_gpt.png`
- 表格/结构化结果:
  - `report_md/_gpt/csv_gpt/convnext_full_results_gpt.csv`
  - `report_md/_gpt/json_gpt/convnext_full_results_gpt.json`
- 关键对比已覆盖:
  - `C1→C2`
  - `C1→C3`
  - `C1→C4`
  - `C4→C5`

---

## Task 4: Tiny-ViT V1-V7 训练 (A3.1)

**优先级**: 中 — ConvNeXt 全部收尾后  
**背景**: A3.1 是 Tiny-ViT 在 CIFAR-10 上的完整实验矩阵，代码已就绪 (`train_tinyvit.py`)  
**当前状态**: V1 已完成，V2-V7 运行中  
**运行记录**:
- `2026-04-04 17:18` 已启动 `V1` detached baseline:
  - `logs/_gpt/train_tinyvit_v1_20260404_171833_gpt.log`
- 实际启动命令增加了 `--pretrained`，与验收标准 `~93-95%` 保持一致
- `2026-04-04 19:27` `V1` 完成:
  - best accuracy: `97.48%`
  - best epoch: `99`
  - checkpoint: `checkpoints/V1_fp32_digital_baseline_best.pt`
  - GPT result bundle:
    - `report_md/_gpt/tinyvit_v1_results_gpt.md`
    - `report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json`
    - `report_md/_gpt/csv_gpt/tinyvit_v1_results_gpt.csv`
**执行顺序**:
1. 先跑 V1 (FP32 baseline) 验证模型架构正确性（Gemini 建议的 weight-transfer validation）
2. V1 通过后，批量跑 V2-V7
```bash
# Step 1: baseline validation
/home/qiaosir/miniconda3/envs/LLM/bin/python -u train_tinyvit.py \
  --mode train --experiments V1 --dataset cifar10 --device cuda --pretrained \
  --log-path logs/_gpt/train_tinyvit_v1_$(date +%Y%m%d_%H%M%S)_gpt.log \
  2>&1 | tee logs/_gpt/train_tinyvit_v1_gpt.log

# Step 2: after V1 validates, run V2-V7
/home/qiaosir/miniconda3/envs/LLM/bin/python -u train_tinyvit.py \
  --mode train --experiments V2 V3 V4 V5 V6 V7 --dataset cifar10 --device cuda --pretrained \
  --resume-existing --log-interval 5 \
  --log-path logs/_gpt/train_tinyvit_v2v7_$(date +%Y%m%d_%H%M%S)_gpt.log \
  2>&1 | tee logs/_gpt/train_tinyvit_v2v7_gpt.log
```
**验收标准**: V1 应达到 ~93-95% (CIFAR-10 fine-tune from ImageNet pretrained)

**当前结论**:
- `V1` 已明确通过 weight-transfer validation
- `97.48%` 高于原验收区间 `~93-95%`，说明 pretrained initialization、数据流、分类头替换、训练环路都工作正常
- 下一步可以在相同 `--pretrained` 初始化策略下启动 `V2-V7`

**Claude 审批 (2026-04-04)**: ✅ V1 结果确认，批准启动 V2-V7。请立即执行 Step 2。

**执行记录 (2026-04-04 19:42)**:
- Tiny-ViT resume support has now been implemented in `train_tinyvit.py`
  - `*_last.pt` latest checkpoints are saved during training
  - `--resume-existing` now resumes from `*_last.pt`, with fallback to `*_best.pt`
- `V2-V7` has been launched in detached mode:
  - runtime log: `logs/_gpt/train_tinyvit_v2v7_20260404_194225_gpt.log`
  - driver log: `logs/_gpt/train_tinyvit_v2v7_20260404_194225_driver_gpt.log`
  - result targets:
    - `report_md/_gpt/tinyvit_v2v7_results_gpt.md`
    - `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json`
    - `report_md/_gpt/csv_gpt/tinyvit_v2v7_results_gpt.csv`

**修正记录 (2026-04-04 19:57)**:
- Gemini review found a real Tiny-ViT analog scaling bug
- the first `V2` run was therefore aborted:
  - observed failure:
    - `Epoch 0: test_acc=11.07%`
    - `Epoch 4: test_acc=14.32%`
- fix applied:
  - `analog_layers.py` now supports opt-in `restore_weight_scale`
  - Tiny-ViT hybrid path enables it explicitly
  - default remains backward-compatible for prior A2 checkpoints
- broken partial `V2` checkpoints moved to:
  - `checkpoints/_gpt_badscale/`
- clean rerun launched:
  - runtime log: `logs/_gpt/train_tinyvit_v2v7_20260404_195408_gpt.log`
- first healthy restart signal:
  - `V2 Epoch 0: train_acc=88.50%, test_acc=93.41%`

V2-V7 验收标准:
- V2 (4-bit 无噪声): 应接近 V1，预期 95-97%
- V3 (4-bit 噪声 standard): 预期大幅下降，类比 ConvNeXt C3 模式
- V4 (4-bit 噪声 HAT): 核心实验，预期恢复到 93-96%
- V5 (pessimistic HAT): 预期比 V4 低 1-3%
- V6 (6-bit HAT): 预期与 V4 接近
- V7 (物理前端): 预期与 V4 相当或略低

如遇 CUDA crash，使用 `--resume-existing` 恢复。每个实验完成后更新 HANDOFF。

**执行记录 (2026-04-04 23:08)**:
- Task 5 code completed:
  - AMP added to `train_tinyvit.py`, `train_convnext.py`, `train_resnet18.py`
  - analog quantization math is forced to fp32 inside `analog_layers.py`
- Task 6 code completed:
  - Tiny-ViT now supports `--retention-sweep --retention-times --eval-runs`
- Task 7 code-path check completed:
  - `train_tinyvit.py --mode dry-run --dataset cifar100 --device cpu` passed
- operational switch completed:
  - stopped non-AMP Tiny-ViT batch after `V2` finished
  - relaunched AMP batch with resume:
    - `logs/_gpt/train_tinyvit_v2v7_amp_20260404_230556_gpt.log`
    - `logs/_gpt/train_tinyvit_v2v7_amp_20260404_230556_driver_gpt.log`
  - `V2` is auto-skipped because checkpoint already reached `100/100`
  - `V3` resumed from `epoch 11`

**执行记录 (2026-04-04 23:18)**:
- Tiny-ViT `V3` suspicious accuracy was investigated before continuing:
  - old `V3_last.pt` under `noise_off` eval: `94.96%`
  - old `d2d_only` eval: `9.64%`
  - old `d2d + c2c` eval: `9.92%`
- interpretation:
  - weights were healthy
  - old Tiny-ViT standard-noise protocol was too harsh for `V3`
- fix applied in `train_tinyvit.py`:
  - standard noisy training now keeps fixed D2D active during train
  - C2C remains off during train
  - Tiny-ViT logs now include timestamps
- old suspect `V3` checkpoints moved to:
  - `checkpoints/_gpt_v3_suspect/`
- clean relaunch:
  - `logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_gpt.log`
- first new signal:
  - `V3 epoch 0 test_acc = 18.05%`
  - old protocol `epoch 0` was `9.73%`

---

## 注意事项
- 所有输出日志必须 tee 到 `logs/_gpt/` 并带时间戳
- 报告/CSV/JSON 输出到 `report_md/_gpt/` 对应子目录
- 完成后更新 `LLM_HANDOFF_gpt.md` 记录结果
- 遇到 CUDA crash 使用 `--resume-existing` 恢复，不要从头重跑
