# 文本风格第二轮审计 — 残留问题

> **日期**: 2026-04-13  
> **发现**: 多处仍有实验报告/AI味

---

## 🔴 摘要 (Abstract) 残留问题

### L2: "Here we present..."
**问题**: "Here we present"是模板化开头，顶刊已少用
**建议**: 
```
// 当前
Here we present a behavioral simulation framework...

// 建议
We present a behavioral simulation framework...
// 或更直接
A behavioral simulation framework for organic optoelectronic CIM inference reveals...
```

### L2: "The framework is developed..."
**问题**: 被动语态 + 过程描述（像实验报告）
**建议**: 
```
// 当前
The framework is developed at the simulation level from literature-derived proxy parameters...

// 建议
Developed from literature-derived proxy parameters, the framework bridges...
```

### L4: "Using... we find that..."
**问题**: "Using X, we find that Y"是标准实验报告句式
**建议**:
```
// 当前
Using Tiny-ViT-5M, ConvNeXt-Tiny and ResNet-18 across three vision datasets, we find that...

// 建议
Across Tiny-ViT, ConvNeXt and ResNet on three vision datasets, converter precision—not nominal quantization—dominates accuracy.
```

### L6: "These results establish..."
**问题**: "These results establish"总结句式太平淡
**建议**:
```
// 当前
These results establish the framework as...

// 建议
The framework establishes a transparent bridge...
```

---

## 🔴 Introduction 残留问题

### L4: "are widely motivated by"
**问题**: 被动+抽象，像综述而非论文
**建议**: 
```
// 当前
Compute-in-memory (CIM) and processing-in-memory (PIM) architectures are widely motivated by...

// 建议
The energy cost of data movement between memory and arithmetic units motivates compute-in-memory (CIM) architectures...
```

### L6: 长列举问题
**问题**: "multilevel conductance states, retention, optical sensitivity, or low static power" — 列举过长像清单
**建议**: 删减为最核心的2-3个

### L8: "Here, we develop..."
**问题**: 又是"Here we"
**建议**: "We develop..."

### L10: 整段像实验报告总结
**问题**: 这段直接列出结果，应该移到Results
**建议**: Introduction不应预告具体数字，应留到Results

---

## 🔴 Methods 残留问题

### L31: "Under this mapping, 87.7\% of parameters..."
**问题**: 直接报数字像实验报告
**建议**: 
```
// 当前
Under this mapping, 87.7\% of parameters are assigned to analog execution, whereas 57.9\% of the estimated energy remains in the digital domain...

// 建议
This mapping assigns most parameters (87.7\%) to analog execution, yet most energy (57.9\%) remains digital because attention operations stay in the digital domain.
```

### L43: "The framework injects..."
**问题**: 平铺直叙技术细节，像API文档
**建议**: 合并句子，减少列举

### L45: "First-order modeling of... is supported"
**问题**: "is supported"被动语态
**建议**: "The framework models nonlinear write and retention with parameters anchored to..."

### L57: "The profile interface allows..."
**问题**: 功能描述像软件说明书
**建议**: 
```
// 当前
The profile interface allows technology-specific parameters to be substituted directly into the simulation pipeline.

// 建议
A replaceable profile interface enables technology-specific parameter substitution without code changes.
```

---

## 🔴 Results 残留问题

### L7: "We establish digital FP32 baselines..."
**问题**: "We establish"实验报告口吻
**建议**: "Digital FP32 baselines establish..."

### L27: "Evaluation of 4-bit hybrid models... shows that..."
**问题**: "Evaluation of X shows that Y"标准实验句式
**建议**: "Quantization alone introduces only a modest penalty in 4-bit hybrid models."

---

## 🔴 全局问题模式

### 1. 过度使用 "we"
**统计**: 平均每段2-3次"we"
**顶刊标准**: 只在必要处使用，多用被动或事物主语

### 2. 过程描述过多
**问题**: "is developed", "is implemented", "are assigned"
**建议**: 改为结果状态描述

### 3. 数字前置过多
**问题**: "87.7\% of parameters", "10,000 s"
**建议**: 数字后置或融入句子

---

## 💡 关键修复示例

### 摘要彻底重写建议

**当前版本 (仍有AI味)**:
```
Organic optoelectronic synaptic devices combine multilevel conductance tuning with low static power, yet the relationship between reported device characteristics and task-level vision performance remains unclear. Here we present a behavioral simulation framework...
```

**顶刊风格版本**:
```
Organic optoelectronic devices offer multilevel conductance tuning and low static power, yet whether these characteristics suffice for modern vision tasks remains unknown. We present a behavioral simulation framework that bridges device metrics to task-level performance through a replaceable profile interface.

Converter precision—not nominal quantization—dominates accuracy: below 6-bit ADC, accuracy collapses. Standard hardware-aware training overfits single device instances; resampling D2D masks during training recovers 86.37% fresh-instance accuracy. Severe write nonlinearity (NL=2.0) remains unrecoverable under gradient-scaling approximations.

This establishes a materials-to-system bridge for identifying device characteristics that constrain edge-vision deployment.
```

**变化**:
- 删除"Here we present"
- 删除"we find that"
- 更紧凑的因果陈述
- 直接数字结论

---

## 优先级

| 位置 | 问题 | 紧急度 |
|:-----|:-----|:-------|
| 摘要 L2-L4 | "Here we" + "we find" | 🔴 最高 |
| Introduction L10 | 结果预告段落 | 🔴 最高 |
| Methods L31, L43 | 过程描述 | 🟡 高 |
| Results L7, L27 | 实验句式 | 🟡 高 |

