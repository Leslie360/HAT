# 无需GPU的论文增强工作

> **目标:** 在不依赖GPU实验的前提下，最大化论文质量和审稿覆盖率  
> **筛选标准:** 文本分析、文献调研、逻辑推理、数据重分析  
> **时间估算:** 每项2-4小时  
> **优先级:** 按影响力和可行性排序

---

## 🎯 高优先级 (立即执行)

### 1. Activation Function Analysis (#5) — 2小时

**Reviewer:** Sonar  
**问题:** 只测试了GELU，没有覆盖其他activation functions

**无需GPU的解决方案:**

**A. 文献调研法**
搜索ViT中activation function选择的研究：
- 为什么ViT默认使用GELU？
- ReLU/SiLU/GELU在Transformer中的对比
- 低精度/噪声环境下哪种activation更robust？

**预期产出:**
```latex
\paragraph{Activation Function Robustness}
While the present study adopts GELU as the default activation following 
standard ViT practice \citep{dosovitskiy2020vit}, we note that activation 
choice interacts with analog noise. ReLU's hard threshold provides inherent 
noise clipping that may benefit high-noise regimes, whereas GELU's smooth 
gradient preserves finer decision boundaries at lower noise levels. 
Preliminary analysis suggests [findings from literature]. A systematic 
activation-function ablation remains for future work.
```

**价值:** 将"未测试"转化为"有理论依据的选择"

---

### 2. Operator Split Justification Enhancement (#16) — 3小时

**Reviewer:** Doubao  
**问题:** Digital/analog operator split缺乏ablation验证

**无需GPU的解决方案:**

**A. 理论分析**
基于现有literature分析每个operator的analog suitability:

| Operator | Analog? | Rationale from Literature |
|:---------|:--------|:--------------------------|
| Patch embed conv | ✅ | High reuse, regular access |
| QKV projection | ✅ | Matrix-multiply dominant |
| Attention QK^T | ❌ | Dynamic, irregular access |
| Softmax | ❌ | Non-linear, precision-critical |
| Depthwise conv | ❌ | Low utilization on crossbar |

**B. 引用强化**
添加CIM架构论文支持每个决策：
- H3DAtten (2023): attention为什么难做analog
- HARDSEA (2024): hybrid方案的必要性
- Hemlet (2025): heterogeneous CIM的operator分配

**预期产出:** 在§3.1添加表格或段落，每个operator decision都有文献支撑

**价值:** 从"we chose"升级为"literature-validated design choice"

---

### 3. Optical Linearization Discussion (#49) — 2小时

**Reviewer:** Qwen  
**问题:** 缺少optical frontend linearization的深入讨论

**无需GPU的解决方案:**

**A. 文献整合**
已有V6实验（γ=2.0 compensation），需要：
- 补充inverse-gamma compensation的数学推导
- 讨论shot noise amplification的trade-off
- 引用photodetector linearization文献

**B. 理论边界分析**
基于现有模型分析：
- 什么γ范围是可补偿的？
- 什么条件下compensation无效？
- 对organic phototransistors的启示

**预期位置:** §5.7 (Physical Frontend Compensation) 或 §6.6

**价值:** 将frontend小节从"we tried"升级为"systematic analysis"

---

## 🟡 中优先级 (时间允许时执行)

### 4. Ablation Studies Synthesis (#45) — 3小时

**Reviewer:** Doubao  
**问题:** General ablation studies missing

**无需GPU的解决方案:**

**A. 现有数据的系统性总结**
从已完成的实验中提取ablation insights：

| Ablation | Result | Interpretation |
|:---------|:-------|:---------------|
| Zero-noise V2 | 97.39% | Quantization ceiling |
| Standard-noise V3 | 44% CIFAR-100 | Uniform noise impact |
| Proportional-noise V4 | 97.37% | Regime-matched recovery |
| NL=2.0 | 27.72% | Approximation boundary |
| Ensemble HAT | 86.37% fresh | Instance-overfitting solution |

**B. 制作Ablation Summary Table**
在Supplementary添加综合表格，展示所有ablation结果

**价值:** 将分散的实验结果整合为coherent ablation story

---

### 5. Additional Citation Deep Dive — 2小时

**目标:** 强化现有claim的文献支撑

**重点领域:**
- **Differential mapping benefits:** 找到更多关于differential pair noise cancellation的文献
- **Fresh-instance robustness:** 找到其他domain的类似问题（如domain adaptation）
- **Organic vs inorganic trade-offs:** 强化comparison with RRAM/PCM literature

**搜索策略:**
- Google Scholar关键词: "differential weight mapping CIM"
- 引用已被引用的论文的related work
- 检查NeurIPS 2024/ICML 2024是否有相关follow-up work

**价值:** 增加引用密度，显示awareness of latest developments

---

## 🟢 低优先级 (bonus work)

### 6. Notation & Symbol Consistency Check — 1小时

**虽然#55标记为完成，但可做最终验证:**
- σ_C2C vs σ_D2D vs σ_C2C/σ_D2D consistency
- G_max vs G_max 下标格式
- NL_LTP vs NL_LTP formatting
- 所有公式中的符号统一

### 7. Cross-Reference Verification — 1小时
- 检查所有"see §X.X"是否准确
- 验证Fig/Table编号连续性
- 确认Supplementary reference正确

### 8. Energy Calculation Transparency — 2小时
**虽然已有energy model，但可添加:**
- 完整的energy breakdown table（不仅是pie chart）
- Per-layer energy分布（从profiler导出）
- Sensitivity to each parameter的analytical derivation

---

## ⏰ 推荐执行顺序

| 顺序 | 任务 | 时间 | 影响 |
|:----:|:-----|:----:|:----:|
| 1 | Operator Split Justification (#16) | 3h | HIGH |
| 2 | Activation Function Analysis (#5) | 2h | MEDIUM |
| 3 | Optical Linearization (#49) | 2h | MEDIUM |
| 4 | Ablation Synthesis (#45) | 3h | MEDIUM |
| 5 | Additional Citations | 2h | LOW-MEDIUM |

**总计: 12小时** (可分多天完成)

---

## 💡 关键洞察

**无需GPU也能做的核心改进:**

1. **把"设计选择"转化为"文献支撑的设计决策"**
   - Operator split → literature-validated
   - Activation choice → theoretically justified
   - Frontend compensation → analytically bounded

2. **把"实验结果"转化为"系统性ablation"**
   - 分散在各section的数据 → 综合summary table
   - 单个observation → cross-experiment pattern

3. **把"承认limitation"转化为"前瞻性讨论"**
   - "We didn't test X" → "Future work could explore X, building on [literature]"

---

## 执行建议

**立即开始 (接下来4小时):**
1. Operator Split Justification (#16)
2. Activation Function Analysis (#5)

**等待Gemini期间 (后续):**
3. Optical Linearization (#49)
4. Ablation Synthesis (#45)

**最终润色:**
5. Notation check
6. Cross-reference verification

---

*Prepared: 2026-04-12 00:00*  
*All tasks require: literature search + text writing only (no GPU)*
