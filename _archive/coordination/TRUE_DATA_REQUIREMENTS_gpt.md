# 数据需求澄清与提取指南 (True Data Requirements)

这份文档旨在彻底理清“我们需要向材料博士要什么”以及“我们需要向 Nature Communications 提交什么”，并纠正之前 Kimi 任务单中的错误和幻觉。

---

## 第一部分：发给材料博士的【器件物理参数索要清单】
**用途：** 获取真实的实验测量数据，以便将其转换为 JSON 格式的 Device Profile（如 `zhang_2025_opect.json`），驱动我们的系统级 CIM 仿真。
**接收人：** 材料学/器件方向的合作博士生。

> **有机光电器件 CIM 仿真 —— 物理参数提取清单**
> 
> 博士你好，为了在系统层面评估我们的器件在跑视觉大模型 (Tiny-ViT) 时的真实表现，我们需要基于你的实测数据建立一个器件画像 (Device Profile)。请协助提取或提供以下参数：
> 
> **核心参数 (Core Metrics - 必须)：**
> 1. **电导范围 (Conductance Window):** $G_{min}$ 和 $G_{max}$ 分别是多少（或提供动态范围 Dynamic Range）？
> 2. **稳定状态数 (Number of States):** 在此工作范围内，能够稳定区分出多少个多值电导状态 ($n_{states}$)？
> 3. **器件间波动 (D2D Variability):** 阵列中不同器件在相同写入条件下的固有电导散布，相对标准差 $\sigma_{D2D}$ 大约是多少？（例如 3% 或 5%）。
> 4. **读写波动 (C2C Variability):** 同一个器件反复写同一个状态时的波动，相对标准差 $\sigma_{C2C}$ 大约是多少？
> 
> **进阶物理参数 (Advanced Physics - 如果有测量数据)：**
> 5. **保持力/漂移 (Retention Drift):** 随着时间推移，电导衰减的时间常数。如果我们用双指数衰减拟合，需要拟合参数 $A_0, \tau_1, \tau_2$。
> 6. **写入非线性 (Non-linear Write):** 连续施加脉冲时的电导更新曲线非线性因子。长时增强 ($NL_{LTP}$) 和长时抑制 ($NL_{LTD}$) 大约是多少？
> 7. **光电响应特征 (若适用):** 如果是光控器件，是否有暗电流 ($I_{dark}$) 的相对比例，以及光强-电导响应的非线性曲线特征 (Gamma 因子 $\gamma_{phys}$)？

---

## 第二部分：发给我们自己（一作）的【NC 投稿 Source Data 真实提取指南】
**用途：** 指导作者如何准备 Nature Communications 强制要求的 `Source Data.xlsx` 文件。纠正了 Kimi 伪造的 `json_gpt` 路径和遗漏的 Supplementary 图表。
**接收人：** 负责打包最终 Submission 文件的作者（你 / Codex）。

**核心原则：** 不要去找 Kimi 编造的 `json_gpt/...`，必须从真实运行的日志 (`logs/_gpt/`)、实际生成的 JSON (`asymmetry_sweep_results_gemini.json` 等) 或绘图脚本 (`plot_paper_figures.py`) 的底层数组中提取作图坐标。

### 主文图表 (Main Text)
| 图表编号 | 内容描述 | 真实数据来源 (提取路径) |
| :--- | :--- | :--- |
| **Table 1** | FP32 数字基线准确率 | 论文正文 `05_results.tex` 表 1 (直接复制表格) |
| **Fig 4** | 跨数据集精度对比 (Accuracy Comparison) | `train_tinyvit.py` / `train_convnext.py` 的测试日志输出 (FP32, V3/C3, V4/C4 的均值与标准差) |
| **Fig 5** | HAT 精度恢复轨迹 (HAT Recovery) | 同上，绘制降幅与恢复的绝对值 |
| **Table 2** | 各架构物理机制下的精度汇总 | 论文正文 `05_results.tex` 表 2 (包含误差棒，直接复制) |
| **Fig 11** | 能量分解 (Energy Breakdown) | 分析能量模型或运行日志输出的 Attention、MAC、ADC 等耗能占比 ($\mu$J) |

### 附件图表 (Supplementary Information)
| 图表编号 | 内容描述 | 真实数据来源 (提取路径) |
| :--- | :--- | :--- |
| **Table S1/S2** | 参数矩阵 (Experiment Matrix) | `supplementary.tex` 中 V1-V8, C1-C4 的配置参数表 |
| **Fig S4** | 分析信噪比曲线 (SNR Curves) | 前端补偿模型/绘图脚本中的理论计算数组 |
| **Fig S5** | 连续噪声与 ADC 扫描 (Noise/ADC Sweep) | 对应的二维扫参脚本输出日志 / 提取精度的网格数据 |
| **Fig S6** | 保持力与时间漂移 (Retention Curve) | `eval_fresh_instances.py` 或保留测试脚本 10,000s 范围内的精度衰减数据 |
| **Fig S7** | Zero-Shot 实例迁移 (Zero-Shot Transfer) | 10个 fresh D2D mask 下的精度评测日志提取的散点集 |
| **Fig S8** | 光电非线性补偿 (Frontend Comp) | V6 实验 (有/无逆 Gamma 补偿) 的精度对比日志 |
| **Fig S9** | 能量-精度 Pareto 前沿 | V2-V7 实验结果汇总（X 轴能耗，Y 轴精度） |
| **Table S3** | (EXP-A) 差分不对称性敏感度 | `asymmetry_sweep_results_gemini.json` (0, 1, 2, 5, 10% 对应精度) |
| **Table S4** | (EXP-B) 物理非理想性扫参 | `nonideality_sweep_results_gemini.json` (IR Drop + Sneak Path 的 12 个组合) |

*(注：Fig 1, 2, 3, S1, S2 等概念示意图、架构图及注意力热力图 Fig S10 无需提取数值型 Source Data)*
