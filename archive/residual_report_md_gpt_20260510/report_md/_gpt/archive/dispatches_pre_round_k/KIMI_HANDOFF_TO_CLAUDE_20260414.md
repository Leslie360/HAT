# Kimi → Codex 工作交接报告

> **日期**: 2026-04-14 23:30
> **汇报人**: Kimi
> **接收人**: Codex (Claude)
> **主题**: NC审稿意见Phase 1完成 + 关键问题发现

---

## 一、核心成果 (Executive Summary)

### ✅ 已完成 (NC审稿意见Phase 1)

| 任务 | 成果 | 文件 |
|:-----|:-----|:-----|
| 结构验证 | 确认符合NC规范 (Intro→Results→Discussion→Methods) | `main.tex` |
| 术语标准化 | 5处关键术语统一 | 多文件 |
| 摘要精简 | 280词→220词 | `00_abstract.tex` |
| 引言重构 | 5段递进式逻辑 | `01_introduction.tex` |
| 格式规范 | 数字/单位/乘号标准化 | 多文件 |

### 🔴 关键发现 (需立即决策)

**ResNet-18 CIFAR-100 数据完全无效**
- ADC扫描显示所有配置准确率均为 **1.00%**
- Root cause: train/eval分布不匹配 (已诊断确认)
- **决策**: 是否从论文中删除所有ResNet-18 CIFAR-100结果？

---

## 二、详细修改清单

### 2.1 术语标准化 (NC审稿要求)

| 原文 | 修改后 | 位置 |
|:-----|:-------|:-----|
| converter precision | **ADC resolution** | Abstract, Intro, Discussion, RW |
| D2D mismatch | **D2D variability** | Appendix |
| canonical regime | **canonical regime (defined on first use)** | Abstract, Results, Discussion |

### 2.2 引言重构 (NC审稿要求)

**原结构**: 4段，逻辑松散
**新结构**: 5段递进式

```
1. CIM架构背景与能效动机
2. 有机光电子器件的独特优势
3. 文献gap: 器件级→系统级的方法学缺失
4. 现有CIM模拟器的局限性
5. 本工作的核心贡献与3个主要发现
```

**关键改进**:
- 新增HAT挑战的铺垫，为Ensemble HAT铺垫
- 明确指出"标准HAT会过拟合特定硬件实例"
- 每段直接指向下一段要解决的科学问题

### 2.3 格式规范 (NC审稿要求)

| 类型 | 规范 | 示例 |
|:-----|:-----|:-----|
| 千位分隔符 | 10~000~ | 10,000 → 10~000~s |
| 乘号 | $\times$ | 11.45x → 11.45$\times$ |
| 百分比 | ~\% | 与数字间加空格 |
| 数组尺寸 | $128 \times 128$ | 标准 $n \times m$ 格式 |

### 2.4 摘要精简 (NC审稿要求)

**精简前** (约280词):
> "Organic optoelectronic synaptic devices combine multilevel conductance tuning with low static power, yet it remains unclear how reported device characteristics translate into task-level vision performance."

**精简后** (约220词):
> "Organic optoelectronic devices offer multilevel conductance tuning and low static power, yet whether these characteristics suffice for modern vision tasks remains unknown."

---

## 三、关键问题诊断 (需Codex决策)

### 3.1 ResNet-18 CIFAR-100 数据无效

**现象**:
- R1 (FP32): 78.64% (正常)
- R3 (Standard Noise): 1.00% (训练acc 99.43%, test acc 1.00%)
- R4 (HAT): ADC扫描显示所有配置均为1.00%

**Root Cause** (已确认):
```python
# train_resnet18.py build_model (line 141-147)
analog_cfg = AnalogLinearConfig(
    sigma_c2c=0.0 if not hat_training else 0.05,  # R3: 0.0
    noise_enabled=False if not hat_training else True,  # R3: False
    ...
)

# evaluate时 (line 164-168)
set_noise_for_eval()  # 强制启用noise_enabled=True, sigma_c2c=0.05
```

**结果**: 训练时无噪声，评估时突然注入噪声 → 严重分布偏移 → 模型崩溃

**Tiny-ViT/ConvNeXt无此问题的原因**: 它们的训练逻辑不同，HAT训练时噪声是启用的

### 3.2 对NC审稿意见的影响

**Reviewer Minor Comment #1**:
> "正文补充ResNet-18、ConvNeXt-Tiny的ADC位宽扫描结果"

**现状**:
- ConvNeXt-Tiny ADC扫描: 可用 (已有数据)
- ResNet-18 CIFAR-100 ADC扫描: ❌ 数据无效 (全部为1.00%)

**决策选项**:

| 选项 | 行动 | 影响 |
|:-----|:-----|:-----|
| A | 删除ResNet-18 CIFAR-100所有结果 | Table 2不对称，但诚实 |
| B | 仅保留CIFAR-10结果 | 满足跨架构验证要求 |
| C | 声明"不收敛"作为发现 | 需改写讨论 |
| D | 修复代码并重跑 | 需2-3天GPU时间 |

**建议**: 选A或B，优先保证 submission timeline

---

## 四、Phase 2 计划 (待Codex确认)

### 4.1 NC Major Comments 回应策略

| # | 问题 | 现有工作 | 缺口 | 建议行动 |
|---|:-----|:--------:|:-----|:---------|
| 1 | 基准对比 (AIHWKIT/DNN+NeuroSim/CrossSim) | ✅ AIHWKIT完成 (P13) | ❌ CrossSim | 安装CrossSim，跑对比实验 |
| 2 | NL=2.0写入非线性分析与方案 | ⚠️ 仅极限结果 | ❌ 模块消融+缓解方案 | 设计逐层NL注入实验 |
| 3 | Ensemble HAT创新性与消融 | ⚠️ 缺对比方法 | ❌ 多实例HAT/域随机化对比 | 文献调研+实现 |
| 4 | 能效模型硬件支撑 | ⚠️ 一阶模型 | ❌ 实测参数对标 | 可协商延后 |
| 5 | Profile普适性验证 | ⚠️ 2种profile | ❌ 更多器件类型 | 可协商延后 |

### 4.2 立即可做 (无需GPU)

1. **审稿回应信撰写**
   - 逐条回应5个Major Comments
   - 制定实验补充时间表

2. **CrossSim环境准备**
   - 安装CrossSim
   - 理解其API与配置

3. **文献调研**
   - 多实例HAT改进方法
   - 域随机化在CIM中的应用

### 4.3 需要GPU (需排队)

1. **CrossSim对比实验** (~8小时)
2. **NL=2.0模块消融** (~24小时)
3. **Ensemble HAT对比** (~16小时)

---

## 五、文件位置汇总

### 修改的文件
```
paper/latex_gpt/sections/
├── 00_abstract.tex          (摘要精简+术语)
├── 01_introduction.tex      (引言重构+术语)
├── 02_related_work.tex      (术语)
├── 05_results.tex           (术语+格式)
├── 06_discussion.tex        (术语+格式)
├── 07_conclusion.tex        (格式)
└── 08_appendix.tex          (术语)
```

### 诊断脚本
```
compute_vit/
├── debug_resnet_issue.py           (ResNet问题诊断)
├── debug_train_eval_mismatch.py    (分布不匹配验证)
├── run_resnet18_adc_sweep.py       (ADC扫描脚本)
└── RESNET_DEBUG_FINDINGS_20260414.md  (详细诊断报告)
```

### 结果文件
```
report_md/json/
└── resnet18_cifar100_adc_sweep.json    (1.00% across all configs)
```

---

## 六、需要Codex决策的事项

### 🔴 紧急 (影响论文内容)

1. **ResNet-18 CIFAR-100处理方式**
   - 选项A: 完全删除
   - 选项B: 仅保留CIFAR-10
   - 选项C: 声明为"不收敛发现"
   - 选项D: 修复重跑

2. **Phase 2优先级**
   - 优先处理哪些Major Comments?
   - #1 (CrossSim) 和 #3 (Ensemble HAT消融) 建议优先
   - #2 (NL模块消融) 工程量大，可协商

3. **审稿回应策略**
   - 承诺完成哪些修改?
   - 哪些可以协商延后?

### 🟡 重要 (影响质量)

4. **是否现在安装CrossSim?**
   - 需要Python 3.8+环境
   - 预计安装时间: 1-2小时

5. **Ensemble HAT对比方法选择**
   - 建议对比: 域随机化 (Domain Randomization)
   - 备选: 噪声对抗训练 (Adversarial Training)

---

## 七、下一步行动建议

### 建议1: 立即执行 (今天)
1. Codex决定ResNet-18 CIFAR-100处理方式
2. 更新Table 2 (移除ResNet-18 CIFAR-100列)
3. 重新编译PDF验证所有修改

### 建议2: 短期 (本周)
4. 撰写审稿回应信 (逐条回应Major Comments)
5. 安装CrossSim环境
6. 设计NL=2.0模块消融实验方案

### 建议3: 中期 (下周)
7. 执行CrossSim对比实验
8. 执行Ensemble HAT消融实验
9. 更新论文 with 新实验结果

---

## 八、关键链接

- NC审稿意见分析: `NC_REVIEWER_FEEDBACK_ANALYSIS_20260414.md`
- ResNet问题诊断: `RESNET_DEBUG_FINDINGS_20260414.md`
- 当前PDF: `paper/latex_gpt/main.pdf` (15 pages, clean compile)
- AGENT_SYNC: 已更新最新进度

---

**汇报完成。等待Codex决策。**
