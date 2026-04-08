# 有机光电存算一体仿真——全栈参考手册

> 整合自：课题立项报告、四轮方案审查、三组Perplexity文献调研
> 最终版 2026年4月
> 本文档为实验执行期间的唯一参数与决策参考源

---

## 第一章 架构决策定稿

### 1.1 Tiny-ViT-5M 层级映射规则

基于Perplexity任务一的文献调研结论，以下映射规则已确定：

**映射到有机光电交叉阵列（模拟域）的层：**
- Attention层的 WQ, WK, WV 投影矩阵（Dense Linear）
- FFN层的两个全连接矩阵（Dense Linear）
- Patch Embedding 卷积层（可展开为Dense矩阵）
- 分类头（参数量极小，可选映射）

**保留在数字CMOS协处理器的层：**
- 所有Depthwise Separable Convolution / MBConv层
- Q·Kᵀ 动态矩阵乘法
- Softmax计算
- LayerNorm
- 所有激活函数（GELU等）

**决策依据（文献锚点）：**
- EPIM (Wang et al., 2024, Tsinghua/Berkeley)：密集层在crossbar上可达93-98%利用率
- BWQ (Wu et al., 2023, Duke/Berkeley)：DwConv在OU级别（9×8有效并行）下利用率极低，不值得映射
- 所有2022-2026年PIM/CIM文献中，无一将DwConv映射到模拟阵列；一致做法是留在数字端

**重要修正：** 原方案声称的"85%算力映射到模拟阵列"需要下调。在DwConv排除后，实际可映射比例取决于Tiny-ViT-5M的具体参数统计，预计在**55-70%**之间。A1.1阶段的模型剖析脚本将给出精确数字。

### 1.2 交叉阵列物理约束

仿真中必须遵循的硬件约束参数：

| 参数 | 取值 | 来源 |
|:---|:---|:---|
| 物理阵列尺寸 | 128×128 | 文献常见中等规模 |
| 有效并行操作单元（OU） | **9行 × 8列** | BWQ (Wu et al., 2023) 实测约束 |
| 密集层利用率上界 | 93-98% | EPIM (Wang et al., 2024) |
| 权重表示方案 | **差分对**（G⁺ - G⁻），两组阵列 | 标准做法，支持正负权重 |
| ADC共享方式 | 列共享，每8列一个ADC | BWQ架构 |

### 1.3 权重映射方案

原方案未讨论此问题，现补充如下：

**浮点权重 → 电导值的映射流程：**
1. 训练后的浮点权重矩阵 W（可正可负）
2. 拆分为正负部分：W⁺ = max(W, 0)，W⁻ = max(-W, 0)
3. 分别线性映射到 [G_min, G_max] 区间：G = G_min + (W_norm) × (G_max - G_min)
4. 量化到 n_states 个离散电导值
5. 推理时：输出 = V_in · G⁺ - V_in · G⁻

**非线性权重更新建模（用于HAT训练）：**

LTP方向：ΔG_LTP = α_LTP × (G_max - G_current)^NL_LTP
LTD方向：ΔG_LTD = α_LTD × (G_current - G_min)^NL_LTD

其中NL > 0意味着远离边界时更新量更大（接近线性），NL < 0意味着靠近边界时更新量更大（饱和行为）。

---

## 第二章 仿真参数定稿

### 2.1 器件物理参数（三档场景）

所有参数均有文献锚点。主仿真使用"标准值"，敏感性分析扫描三档。

#### 多态存储与量化

| 参数 | 保守值 | 标准值 | 乐观值 | 文献来源 |
|:---|:---:|:---:|:---:|:---|
| 电导态数量 | 8态（3-bit） | **16态（4-bit）** | 64态（6-bit） | OEGST 14-bit; PEDOT:PSS 40态 (Jung 2024) |
| 动态范围 G_max/G_min | 5× | **10×** | 47× | OPECT 47.3×; TIPS-Pen >10⁵ |
| NL (LTP) | +2.0 | **+1.0** | +0.1 | LATP研究 -2.22~-6.59; NIR OPECT -0.015 |
| NL (LTD) | -2.0 | **-1.0** | -0.1 | 与LTP对称假设，多篇文献支持 |

#### 器件变异性

| 场景 | C2C (σ/μ) | D2D (σ/μ) | 来源 |
|:---:|:---:|:---:|:---|
| 乐观 | 1% | 3% | hBN光电突触 C2C<1% (npj 2D Mater. 2021) |
| **标准** | **5%** | **10%** | TIPS-Pen迁移率RSD ~14%，电导变异保守取低 |
| 悲观 | 10% | 20% | Alibart 2016: G_max σ=40-59%，工艺早期 |

**噪声注入实现：**
```
W_noisy = W + N(0, σ_D2D²)  ← 初始化时固定
W_inference = W_noisy + N(0, σ_C2C²)  ← 每次前向传播重采样
```

#### 保持时间与权重衰减

| 参数 | 值 | 来源 |
|:---|:---:|:---|
| τ₁（短时分量） | **140 ms** | Vincze et al. DNTT实测 |
| τ₂（长时分量） | **610 ms** | Vincze et al. DNTT实测 |
| A₀（持久分量比例） | **0.6** | 估计值：持久态占总增幅60% |
| 稳态保持时间 | **≥10,000 s** | Guo et al. TIPS-Pen ~12,600s |

**衰减模型：**
```
G(t) = G₀ × [A₁ × exp(-t/τ₁) + A₂ × exp(-t/τ₂) + A₀]
其中 A₁ + A₂ + A₀ = 1
```

#### 功耗参数

| 参数 | 值 | 来源 |
|:---|:---:|:---|
| 单次突触事件能耗（nominal） | **1.62 pJ** | Guo et al. TIPS-Pen 实测 |
| 暗电流 | **~100 pA** | TIPS-Pen 关态电流估算 |
| 静态待机功耗 | **~30 pW/器件** | I_dark × V_read ≈ 100pA × 0.3V |

### 2.2 ADC/DAC参数

来自Perplexity任务二的硅验证数据：

| 组件 | 4-bit | 6-bit | 8-bit | 来源 |
|:---|:---:|:---:|:---:|:---|
| ADC能耗/转换 | 3-6 fJ | 7-15 fJ | **20-30 fJ** | Yoon 2025: 24.8fJ; Zhang 2022: 10.2fJ |
| DAC能耗/转换 | — | — | **20-50 fJ** | Li 2022; 普遍高于ADC |

**仿真默认值：** 8-bit ADC取25 fJ/conversion，DAC取30 fJ/conversion

**ADC非线性建模（修正原方案的过于简化问题）：**
在量化步长Δ上叠加DNL扰动：
```
Δ_actual[i] = Δ_ideal × (1 + N(0, σ_DNL²))
其中 σ_DNL = 0.5 LSB（默认值）
```

---

## 第三章 能效评估方法论

### 3.1 能耗分解公式

总系统能耗 = 模拟MAC能耗 + ADC能耗 + DAC能耗 + 数字CMOS能耗 + 缓冲区读写能耗

```
E_total = E_analog + E_ADC + E_DAC + E_digital + E_buffer
```

各项计算方法：

```
E_analog = N_analog_MACs × E_per_MAC
E_ADC    = N_ADC_conversions × E_ADC_per_conv
E_DAC    = N_DAC_conversions × E_DAC_per_conv
E_digital = N_digital_MACs × E_digital_per_MAC + N_special_ops × E_special
E_buffer = N_SRAM_reads × E_SRAM_read + N_SRAM_writes × E_SRAM_write
```

### 3.2 能耗常数定稿表（28nm节点）

| 组件 | 能耗值 | 来源 |
|:---|:---:|:---|
| 模拟MAC（有机器件） | **100 fJ/MAC** | Gebregiorgis 2023, 三端有机器件 |
| 模拟MAC（保守估计） | **150 fJ/MAC** | RRAM文献中位数 |
| 8-bit ADC | **25 fJ/conv** | 多篇CIM论文中位数 |
| 8-bit DAC | **30 fJ/conv** | Li 2022估计 |
| INT8 数字MAC | **0.4 pJ/MAC** | Horowitz 2014 + 28nm缩放 |
| FP32 数字MAC | **2.5 pJ/MAC** | Horowitz 2014 + 28nm缩放 |
| Softmax exp运算 | **15 pJ/元素** | 估算值 |
| LayerNorm sqrt运算 | **8 pJ/元素** | 估算值 |
| SRAM读取（32-bit） | **5 pJ/次** | Horowitz 2014 |
| DRAM读取 | **1300 pJ/次** | Horowitz 2014（片外访存） |

### 3.3 参考能耗拆解案例

**Li et al. 2022（256×256 memristor阵列，时分复用）：**

| 组件 | 能耗 | 占比 |
|:---|:---:|:---:|
| Memristor MAC | 100 fJ | 73.5% |
| ADC（共享摊销） | 20 fJ | 14.7% |
| DAC | 10 fJ | 7.4% |
| 控制逻辑 | 6 fJ | 4.4% |
| **合计** | **136 fJ/MAC** | 100% |

**关键洞察：** ADC/DAC开销在不同架构中占总能耗的15-60%。时分复用可将ADC开销压到15%以下，朴素设计可达60%。

### 3.4 Python能效计算模板

```python
def estimate_layer_energy(layer_type, params, tech_node='28nm'):
    """
    计算单层的推理能耗
    
    layer_type: 'analog' | 'digital'
    params: dict containing:
        - N_MAC: MAC操作次数
        - N_outputs: 输出通道/元素数（用于ADC计算）
        - N_inputs: 输入元素数（用于DAC计算）
    """
    # 28nm能耗常数（单位：焦耳）
    constants = {
        '28nm': {
            'E_analog_MAC': 100e-15,    # 100 fJ (有机器件)
            'E_ADC_8bit': 25e-15,       # 25 fJ
            'E_DAC_8bit': 30e-15,       # 30 fJ
            'E_digital_INT8_MAC': 0.4e-12,  # 0.4 pJ
            'E_SRAM_read': 5e-12,       # 5 pJ
        }
    }
    c = constants[tech_node]
    
    if layer_type == 'analog':
        E_mac = params['N_MAC'] * c['E_analog_MAC']
        E_adc = params['N_outputs'] * c['E_ADC_8bit']
        E_dac = params['N_inputs'] * c['E_DAC_8bit']
        return {'MAC': E_mac, 'ADC': E_adc, 'DAC': E_dac,
                'total': E_mac + E_adc + E_dac}
    else:  # digital
        E_mac = params['N_MAC'] * c['E_digital_INT8_MAC']
        return {'MAC': E_mac, 'total': E_mac}


def estimate_model_energy(layer_configs):
    """
    计算整个模型的单次推理能耗
    
    layer_configs: list of (layer_type, params) tuples
    """
    total = {'analog_MAC': 0, 'ADC': 0, 'DAC': 0, 'digital_MAC': 0}
    for ltype, params in layer_configs:
        e = estimate_layer_energy(ltype, params)
        if ltype == 'analog':
            total['analog_MAC'] += e['MAC']
            total['ADC'] += e['ADC']
            total['DAC'] += e['DAC']
        else:
            total['digital_MAC'] += e['MAC']
    
    total['grand_total'] = sum(total.values())
    return total
```

### 3.5 工具选择

**主方案：自研Python分析模型**（上述代码）
- 原因：NeuroSim V2.0虽然支持自定义器件参数，但不原生支持OU级粒度（9×8），且三端有机器件的建模需要大量手动配置
- 优势：完全可控，参数透明，可直接嵌入PyTorch训练循环

**交叉验证：NeuroSim（可选）**
- 如果时间允许，可用NeuroSim在相同参数下跑一组对比，验证自研能效模型的合理性
- NeuroSim GitHub: https://github.com/neurosim/DNN_NeuroSim_V1.2

---

## 第四章 核心修正备忘

这些问题必须在论文和代码中体现，缺一不可。

### 4.1 反伽马噪声传播（致命级）

**原错误：** 声称反伽马补偿在全场景下具有鲁棒性。

**事实：** 散粒噪声方差 σ² = α × X^(1/γ)。当1/γ > 1（即γ < 1）时：
- 暗光区（X→0）：噪声方差被压缩 ✓
- 高光区（X→1）：噪声方差被放大 ✗

**论文中的正确表述：**
"反伽马补偿在低照度场景下提供物理级噪声抑制效果，但在高亮度区域引入噪声放大的权衡。"

**必须提供的图表：** Noise Variance vs. Pixel Intensity曲线族（不同γ值），标注暗光压缩区和高光放大区。

**可选进阶：** 分段补偿策略（暗光区用反伽马，高光区线性直通），但需要ablation实验支撑阈值选择，不要空口设定0.5。

### 4.2 CIFAR-10-C实验逻辑（致命级）

**原错误：** 用CIFAR-10-C的数字噪声验证前端光学补偿的鲁棒性。

**修正后的双轨实验设计：**

**轨道1：前端物理补偿效果** → 使用合成物理噪声注入流水线
- 输入图像 → 物理光电流模型 → 反伽马补偿 → 网络
- 对照组：无补偿直接过物理模型
- 扫描变量：γ_phys × I_dark

**轨道2：权重噪声鲁棒性** → 使用CIFAR-10-C
- HAT训练模型 vs 标准训练模型
- 测试CIFAR-10-C全15种干扰
- 这测试的是加噪训练的容忍度，与前端补偿无关

**两个轨道必须分开叙述，不可混为一谈。**

### 4.3 叙事定位（严重级）

**修正前：** "面向大模型推理瓶颈"
**修正后：** "面向边缘视觉推理的有机光电存算一体架构"

大模型访存墙作为1.1节的2-3句背景动机即可，核心叙事聚焦边缘端。

### 4.4 O(1)复杂度声明（重要级）

**修正前：** "在O(1)时间内被瞬间完成"
**修正后：** "单周期模拟MAC操作，端到端延迟受限于ADC转换时间和阵列IR drop"

在论文中注明假设的阵列尺寸和OU约束。

---

## 第五章 文献空白与创新定位

### 5.1 任务三的核心发现

**2022-2026年间，没有任何一篇纯有机器件论文做了包含C2C/D2D变异性建模的系统级神经网络仿真。**

现有论文的问题：

| 论文 | 年份 | 材料 | MNIST精度 | 变异性建模 |
|:---|:---:|:---|:---:|:---:|
| Alibart et al. (Nat. Commun.) | 2016 | Fe-TBP有机memristor | 86-88% | ✅ 完整Monte Carlo |
| Zeng et al. (Nanomaterials) | 2023 | EV/BTPA-F有机 | 97.3% | ❌ 理想器件 |
| Jung et al. (Adv. Sci.) | 2024 | PEDOT:PSS | 91.1% | ❌ 明确排除 |

**这意味着：**
1. 你的工作如果使用PyTorch框架、注入C2C/D2D噪声、在CIFAR-10上做HAT训练——在有机器件领域就是方法论层面近十年的空白填补
2. 唯一的前辈工作（Alibart 2016）用的是自定义Matlab代码 + 简单感知机 + MNIST + 500次Monte Carlo，你的工作在模型复杂度（Tiny-ViT vs 感知机）、框架规范性（PyTorch vs 自定义）、数据集（CIFAR-10 vs MNIST）上全面超越
3. 没有人用过AIHWKIT或PyTorch做有机器件仿真，这本身就是方法论创新

### 5.2 在论文Introduction中应强调的创新点

1. **首次**使用现代深度学习框架（PyTorch）对有机光突触器件进行系统级硬件感知训练仿真
2. **首次**在Vision Transformer架构上验证有机器件的噪声容忍度（此前最复杂的只有MLP）
3. **首次**同时建模C2C/D2D变异性、量化非线性、ADC失真、保持时间衰减的全栈有机器件仿真
4. 提出有机光电器件的"物理前端反伽马补偿"机制，并诚实分析其暗光/高光权衡

### 5.3 Alibart 2016方法论要点（作为方法论参考模板）

该论文的Monte Carlo方法可直接借鉴：
- 对V_t1、V_t2、G_max使用实验提取的σ值建立高斯分布
- 每次试验从分布中采样器件参数
- 运行500次独立训练+测试
- 统计成功率和平均精度

**你的方案对其的超越：**
- Alibart用500次Monte Carlo跑简单感知机；你可以在每次forward中注入噪声，等价于隐式Monte Carlo，但在Transformer上
- Alibart只做了MNIST逻辑门和单层感知机；你做ResNet、ConvNeXt、Tiny-ViT三级验证
- Alibart没有HAT（硬件感知训练）；你的核心贡献之一就是展示HAT对有机器件噪声的恢复效果

---

## 第六章 关键文献索引

按用途分类，方便写论文时快速定位。

### 架构映射相关
- EPIM (Wang et al., 2024, Tsinghua/Berkeley) — 密集层利用率93-98%
- BWQ (Wu et al., 2023, Duke/Berkeley) — OU约束9×8，6.08×加速
- Allspark (Ge et al., 2024, IEEE TC) — ViT-on-PIM工作负载编排
- Zero-Space FT (Li et al., 2024) — ReRAM容错，MSB复制策略

### 能效评估相关
- Horowitz (2014, ISSCC) — 数字CMOS能耗基准（45nm）
- Li et al. (2022, IEEE TCAS-I) — 时分复用CIM，136 fJ/MAC完整拆解
- Martins et al. (2025, Electronics) — RRAM推理，190 fJ/MAC
- Gebregiorgis et al. (2023, IEEE TETC) — 有机器件，100 fJ/MAC
- Yoon et al. (2025, IEEE TCAS-II) — 8-bit ADC 24.8 fJ
- Zhang et al. (2022, ISCAS) — 可重配置ADC 10.2 fJ

### 有机器件参数相关
- Vincze et al. (2026, Adv. Electron. Mater.) — DNTT体系，τ₁/τ₂实测
- Guo et al. (2024, ACS AMI) — TIPS-Pen，保持时间12600s，1.62 pJ
- 综述 Xu et al. (2025, ACS AMI) — 有机突触器件全景

### 系统级仿真方法论相关
- Alibart et al. (2016, Nat. Commun.) — 有机memristor Monte Carlo仿真（唯一参考）
- DNN+NeuroSim V2.0 (Peng et al., 2020, AICAS) — CIM仿真框架
- MemTorch — PyTorch memristor仿真框架

### 器件变异性与HAT相关
- Scientific Reports系统性仿真研究 — NL/变异性对精度的影响
- HfOx双层器件研究 — C2C/D2D分布压缩
- Fault-Aware Training综述 — 硬件感知训练容忍度提升约2×

---

## 附录：实验执行检查清单

### Phase 1 (第1-3周) 检查项
- [ ] Tiny-ViT-5M模型剖析完成，逐层参数量和矩阵维度已输出
- [ ] DwConv层已标记为"数字路径"，实际可映射比例已计算
- [ ] 阵列数量估算完成（128×128阵列，差分对方案）
- [ ] AnalogLinear层实现并通过单元测试（量化、噪声、衰减）
- [ ] ADCQuantizer层实现，含DNL扰动
- [ ] EnergyProfiler模块实现
- [ ] 物理噪声注入流水线搭建完成
- [ ] ResNet-18端到端前向传播可运行

### Phase 2 (第4-7周) 检查项
- [ ] ResNet-18 六组实验 (R1-R6) 完成
- [ ] ConvNeXt-Tiny 九组实验完成
- [ ] 前端物理补偿三组专项实验完成
- [ ] HAT vs 标准训练的CIFAR-10-C对比完成
- [ ] 噪声方差分析图（SNR vs 亮度）已生成
- [ ] 主线B实测数据状态确认

### Phase 3 (第8-11周) 检查项
- [ ] Tiny-ViT异构切分代码实现
- [ ] convert_to_hybrid()函数可将指定层替换为AnalogLinear
- [ ] V1-V7 七组实验完成
- [ ] CIFAR-100补充验证完成
- [ ] 能效评估数据完整
- [ ] Pareto图（精度 vs 能耗）已生成
- [ ] 若实测数据到位：参数替换重跑完成

### Phase 4 (第12-14周) 检查项
- [ ] 文献值 vs 实测值双版本对比完成
- [ ] 论文Fig.1-Fig.8全部图表就绪
- [ ] Tab.1-Tab.3数据表就绪
- [ ] 论文初稿完成

---

*本文档随实验进展更新。任何参数变更必须同步更新本文档并注明变更原因。*
