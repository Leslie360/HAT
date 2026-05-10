# Gemini 任务单 — 2026-04-14 Phase 2 NC Reviewer Response

> **协调员**: Claude (总指挥)
> **你的角色**: GPU 实验 + 代码修改
> **优先级**: P0 → P1 → P2，按顺序执行
> **硬约束**: 不改 locked numbers，不编造数据，所有实验结果用 JSON 导出

---

## 先读这些文件

1. `report_md/_gpt/PROJECT_MASTER_SUMMARY_FOR_AGENTS_gpt.md` — 项目真值
2. `report_md/_gpt/NC_REVIEWER_FEEDBACK_ANALYSIS_20260414.md` — NC 审稿意见
3. `report_md/_gpt/RESNET_DEBUG_FINDINGS_20260414.md` — ResNet 问题诊断
4. `report_md/_gpt/GM_X47_NEW_EXPERIMENT_PROPOSALS.md` — 你之前设计的实验方案
5. `report_md/_gpt/GEMINI_PROJECT_TRUTH_PACK_20260413_gpt.md` — 避坑指南

---

## GM-P0: CrossSim 对比实验 [CRITICAL — Major #1]

**审稿意见**: 基准对比不足，仅有 AIHWKIT，要求补 CrossSim

**步骤**:
1. 安装 CrossSim（`pip install crosssim` 或从源码）
2. 配置与我们的 canonical regime 匹配的参数：
   - 4-bit 量化, 5% C2C, 10% D2D
   - ResNet-18 on CIFAR-10 (已有 R1 baseline 94.98%)
3. 跑 CrossSim 仿真，记录准确率
4. 与我们的框架 (90.08±0.21% AIHWKIT) 做对比表

**交付**:
- `logs/_gpt/crosssim_comparison.log`
- `report_md/_gpt/json_gpt/crosssim_results.json`
- 对比表（我们 vs AIHWKIT vs CrossSim），包含：配置、准确率、运行时间

**预计**: ~8h GPU

---

## GM-P1: Ensemble HAT 消融实验 [HIGH — Major #3]

**审稿意见**: Ensemble HAT 创新性不充分，缺对比方法和消融

**步骤**:

### GM-P1a: i.i.d. 噪声对比
- 用 V4 checkpoint，对比两种训练策略：
  1. Ensemble HAT (epoch-level D2D resampling) — 已有结果 86.37±1.54%
  2. i.i.d. 噪声增强 (每 batch 随机噪声，不保持空间结构)
- 在 10 个 fresh arrays 上评估
- 证明：空间结构化的 D2D resampling 优于简单的 i.i.d. 噪声

### GM-P1b: 重采样频率扫描
- 扫描 D2D mask 重采样频率: 每 1 epoch / 每 5 epoch / 每 10 epoch / 每 50 epoch / 不重采样
- 在 10 个 fresh arrays 上评估
- 画：重采样频率 vs fresh-instance accuracy 曲线

### GM-P1c: D2D 方差边界
- 参考 `GM_X47_NEW_EXPERIMENT_PROPOSALS.md` 中的 GM-E6 设计
- 扫描 σ_D2D ∈ [0.03, 0.05, 0.10, 0.15]
- 对比 Standard HAT vs Ensemble HAT 在不同 D2D 方差下的表现

**交付**:
- `logs/_gpt/ensemble_hat_ablation_*.log`
- `report_md/_gpt/json_gpt/ensemble_hat_ablation.json`
- 准确率对比表 + 曲线数据

**预计**: ~16h GPU

---

## GM-P2: NL=2.0 层级消融 [HIGH — Major #2]

**审稿意见**: NL=2.0 只给了极限结果 (27.72±0.82%)，缺乏机理解释

**步骤**:
- 参考 `GM_X47_NEW_EXPERIMENT_PROPOSALS.md` 中的 GM-E8 设计
- 逐层注入 NL=2.0，其余层保持线性：
  - Group A: Attention QKV Projections only
  - Group B: Attention Output Projections only
  - Group C: MLP (fc1 + fc2) only
  - Group D: Patch Embedding only
  - Group E: All layers (已有结果 27.72±0.82%)
- 每组 10 MC runs

**代码修改**:
- 需要在 `analog_layers.py` 或推理脚本中添加 per-layer NL 控制
- 不要改动已有的训练逻辑，只改推理时的 NL 注入

**交付**:
- 修改后的推理脚本
- `report_md/_gpt/json_gpt/nl_layer_ablation.json`
- 每组准确率 + 降幅表

**预计**: ~24h GPU

---

## GM-P3: ResNet-18 CIFAR-10 ADC 扫描 [MED — Minor #1]

**背景**: ResNet-18 CIFAR-100 数据无效（已确认），但 CIFAR-10 可能有效

**步骤**:
1. 验证 ResNet-18 CIFAR-10 的 R3/R4 是否存在同样的 train/eval 不匹配
2. 如果 CIFAR-10 数据有效，做 ADC 扫描 (2-8 bit)
3. 如果 CIFAR-10 也无效，报告给 Claude，不要硬跑

**交付**:
- 验证结论 + ADC 扫描结果（如有效）
- `report_md/_gpt/json_gpt/resnet18_cifar10_adc_sweep.json`

---

## 输出规则

1. 每个实验完成后在 AGENT_SYNC 追加一个 `[Gemini]` block
2. 不要声称已 merge 到论文 — 只报告实验结果
3. 实验数据用 JSON 导出，论文文本更新由 Claude 统一安排
4. 遇到技术问题直接报告，不要跳过
5. **按 P0→P1→P2→P3 顺序执行，不要跳跃**
