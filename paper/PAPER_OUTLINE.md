# Paper Outline: Hardware-Aware Simulation of Organic Optoelectronic Synaptic Transistors for Edge Vision Inference

> 本文件为论文总框架。Codex 按此结构在 `paper/` 下生成各节初稿。
> 数据引用均指向 `report_md/` 和 `report_md/_gpt/` 下的实验结果。
>
> **状态说明（2026-04-06, closeout）**：本文件现作为历史设计与收口参考。当前锁定的投稿叙事、结果口径与完成状态以 `paper/*.md` 正文、`MASTER_PLAN.md` 和 `paper/FIGURE_PLAN.md` 为准；本文件不再作为逐项执行清单。
>
> **当前真正剩余的收稿工作**：
> 1. 统一正文与图注口径
> 2. 锁定引用键并收进 `latex_gpt`
> 3. 手工补 `Fig.1 / Fig.2`
> 4. 将 `latex_gpt` 迁入最终投稿模板

---

## Meta

- **Target venue**: ACS Applied Materials & Interfaces / Advanced Electronic Materials (二选一，待定)
- **Scope**: 仿真论文，非器件制备论文
- **Core claim**: 首次使用现代 DL 框架对有机光电突触器件进行含 C2C/D2D 变异性的系统级硬件感知训练仿真，在 Vision Transformer 上验证

---

## 1. Introduction (paper/01_introduction.md)

**结构** (约 1500 词):

1. **动机** (2-3 句): 边缘视觉推理的能效瓶颈 → 存算一体是潜在方案
   - 引用 Horowitz 2014 (数据搬运能耗 >> 计算能耗)
   - 不要过度强调大模型，聚焦边缘端 (参考手册 §4.3 修正)

2. **有机光电器件的机遇**: 光电一体、低功耗、柔性、溶液加工
   - 引用 Xu et al. 2025 综述, Guo et al. 2024 TIPS-Pen

3. **现有仿真的空白**: 2016-2026 十年间无人做过含变异性的系统级仿真
   - Alibart 2016: Matlab + 感知机 + MNIST, 唯一前辈
   - Zeng 2023, Jung 2024: 理想器件, 无变异性建模
   - 表格对比 (→ Tab.1)

4. **本文贡献** (4 点):
   - 首次 PyTorch 系统级有机器件仿真
   - 首次在 ViT 架构上验证有机器件噪声容忍度
   - 首次同时建模 C2C/D2D/量化/ADC/retention 的全栈仿真
   - 物理前端反伽马补偿机制 + 诚实的 SNR 权衡分析

5. **文章结构概述** (1 段)

**数据依赖**: 无 (纯文献)

---

## 2. Related Work (paper/02_related_work.md)

**结构** (约 1000 词):

1. **CIM/PIM 仿真框架**: NeuroSim, MemTorch, AIHWKIT → 均针对 RRAM/PCM, 无有机器件支持
2. **有机突触器件进展**: OPECT, PEDOT:PSS, TIPS-Pen → 单器件表征为主, 系统级仿真缺失
3. **硬件感知训练 (HAT)**: Fault-Aware Training 综述 → 容忍度提升约 2×, 但未在有机器件上验证
4. **ViT on CIM**: Allspark (Ge 2024), EPIM (Wang 2024) → 密集层适合 crossbar, DwConv 留数字端

**数据依赖**: 无 (纯文献, 引用参考手册 §5-§6)

---

## 3. Methodology (paper/03_methodology.md)

**结构** (约 2500 词, 论文最核心章节):

### 3.1 System Architecture Overview
- Fig.1: 系统架构总览图 (analog/digital split, crossbar arrays, physical frontend, digital coprocessor)
- Tiny-ViT-5M 层级映射规则 + 映射决策依据
- 数据来源: `array_mapping_report.md`, `model_profiling.py` 输出

### 3.2 Analog Crossbar Simulation
- 权重→电导映射: W → W+/W- → normalize → [G_min, G_max] → STE quantize
- 差分对方案
- Scale recovery (A3 引入, 与 A2 的区别需注明)
- Fig.2: 权重映射流程图 (float → conductance → quantize → differential)
- 数据来源: `analog_layers.py` 代码

### 3.3 Device Variability Modeling
- D2D: 初始化时固定, N(0, σ_d2d² × G_range²)
- C2C: 每次前向传播重采样, N(0, σ_c2c² × G_range²)
- 三档参数 (乐观/标准/悲观) + 文献锚点
- 数据来源: 参考手册 §2.1

### 3.4 Hardware-Aware Training (HAT)
- STE 量化 + 噪声注入 → 梯度直通
- 训练时: D2D 固定 + C2C 每步重采样
- 推理时: Monte Carlo 评估 (多次前向取均值和方差)
- 数据来源: `analog_layers.py` StraightThroughQuantize

### 3.5 Physical Frontend Compensation
- 光电流模型: I = α·P^γ + I_dark + shot noise
- 反伽马预处理: P_in = X^(1/γ)
- SNR 权衡分析 (§4.1 修正)
- Fig.3: SNR vs pixel intensity 曲线族 (不同 γ)
- 数据来源: `a23_physical_compensation_report.md`

### 3.6 Retention Decay Model
- 双指数衰减: G(t) = G_min + (G-G_min) × [A₁·exp(-t/τ₁) + A₂·exp(-t/τ₂) + A₀]
- 参数来自 Vincze et al. 2026
- 数据来源: 参考手册 §2.1

### 3.X Measurement-to-Simulator Calibration
- 给出“材料测量 → 仿真参数”的映射表
- 明确当前是 literature priors，后续可直接替换为自有 measured profiles
- 强调这是方法贡献的一部分，不只是实现细节

### 3.7 Energy Estimation Model
- 公式: E_total = E_analog + E_ADC + E_DAC + E_digital
- 各项能耗常数 (28nm 节点) + 文献来源
- Tab.2: 能耗常数表
- 数据来源: 参考手册 §3.1-§3.2, `EnergyProfiler`

**数据依赖**: 代码 + 参考手册 (均已就绪)

---

## 4. Experimental Setup (paper/04_experimental_setup.md)

**结构** (约 800 词):

### 4.1 Models and Datasets
- ResNet-18 (A2.1 验证), ConvNeXt-Tiny (A2.2 主实验), Tiny-ViT-5M (A3.1 目标模型)
- CIFAR-10 (主数据集), CIFAR-100 (泛化验证)
- 训练超参: lr, optimizer, scheduler, epochs, batch_size

### 4.2 Experiment Matrix
- Tab.3: 完整实验矩阵 (R1-R6, C1-C9, V1-V6 canonical; V7 仅作 legacy 注记)
- 每组实验的变量和目的

### 4.3 Evaluation Protocol
- Best test accuracy
- Monte Carlo evaluation (10-20 runs, mean ± std)
- Retention sweep 时间点

**数据依赖**: 实验配置 (已确定)

---

## 5. Results and Discussion (paper/05_results.md)

**当前锁定主线**:

1. **Canonical regime**  
   - CIFAR-10 / CIFAR-100 / Flowers-102 的跨数据集结果已经锁定  
   - 主结论是：噪声脆弱性与 HAT 价值随任务复杂度上升而显著放大

2. **Temporal / frontend regime**  
   - corrected retention 已锁定  
   - inverse-gamma frontend compensation 与 SNR trade-off 已锁定

3. **Physics-extension regime**  
   - proportional-noise 与 nonlinear-write stress tests 已锁定  
   - proportional-HAT 可在匹配分布下恢复性能，但不具备跨噪声语义通用性  
   - NL=2.0 仍是主要 failure mode

**本章当前不再依赖额外训练。**

---

## 6. Discussion (paper/06_discussion.md)

**当前锁定主线**:
1. 真正的瓶颈是 ADC、instance transfer、以及 richer-physics mismatch，而不是名义均匀噪声本身
2. Transformer 比 CNN 更依赖训练-部署物理语义匹配
3. Flowers-102 给出 HAT 的数据量下界，而不是“方法无效”
4. 全文应坚持 `first-order behavioral simulation framework` 的降级口径
5. 未来工作聚焦 measured-profile fitting、multi-instance HAT、mixed-precision peripherals

---

## 7. Conclusion (paper/07_conclusion.md)

**当前锁定主线**:
1. 本工作完成了从器件参数到系统级视觉推理结果的 first-order behavioral bridge
2. 关键结论不只是“有机 CIM 可行”，而是“其有效性高度依赖任务复杂度与物理建模语义”
3. future work 不是继续堆 benchmark，而是 measured-profile calibration、instance generalization 与更高保真物理写入模型

---

## Figure Plan (historical summary; canonical status in `paper/FIGURE_PLAN.md`)

| Fig # | 内容 | 数据来源 | 状态 |
|:---:|:---|:---|:---:|
| 1 | 系统架构总览 (analog/digital split + crossbar + frontend) | 手绘/TikZ | 仍需手工制作 |
| 2 | 权重→电导映射流程图 | `analog_layers.py` | 仍需手工制作 |
| 3 | SNR vs pixel intensity 曲线族 | `a23_physical_compensation_report.md` | 已锁定 |
| 4 | 三模型精度对比柱状图 | R/C/V canonical + multidataset | 已锁定 |
| 5 | HAT recovery 对比图 | 同上 | 已锁定 |
| 6 | 物理前端补偿效果 | A2.3 Group 1+3 | 已锁定 |
| 7 | Retention 衰减曲线 | C9 + Tiny-ViT V4 retention | 已锁定 |
| 8 | Pareto: 精度 vs 能耗 | EnergyProfiler + 全部精度数据 | draft 可用 |
| 9 | **噪声敏感度 heatmap** (σ_c2c × σ_d2d → accuracy) | Task 11 noise sweep | 已锁定 |
| 10 | **跨器件类型精度对比** (Organic/RRAM/PCM/Ideal) | Task 12 device comparison | 已锁定 |
| 11 | **能耗分项饼图/堆叠柱状图** (Analog MAC/ADC/DAC/Digital) | EnergyProfiler dry-run | 已锁定 draft |

## Table Plan

| Tab # | 内容 | 状态 |
|:---:|:---|:---:|
| 1 | 文献对比: 有机器件仿真空白 | 可写 |
| 2 | 能耗常数表 (28nm) | 已可直接收口 |
| 3 | 完整实验矩阵 (canonical + physical extensions) | 已锁定 |
| 4 | Tiny-ViT 层级映射汇总 | 已可直接收口 |
| 5 | Retention 衰减数据表 (canonical corrected curves) | 已锁定 |
| 6 | **跨器件参数表** (Organic/RRAM/PCM 物理参数 + 文献来源) | 已可直接收口 |
| 7 | **噪声敏感度数据表** (σ sweep 关键数据点) | 已锁定 |

## Final Closeout Reminder

- `paper_zh/` 由 Gemini 维护；本提纲只服务英文主稿与统一结果口径。
- 若本文件与 `paper/*.md` 正文冲突，以正文为准。
- 若本文件与 `paper/FIGURE_PLAN.md` 冲突，以 `FIGURE_PLAN.md` 为准。
