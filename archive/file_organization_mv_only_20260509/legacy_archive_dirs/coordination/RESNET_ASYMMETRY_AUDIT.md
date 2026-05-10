# 🚨 ResNet-18 实验不对称性审计

> **日期**: 2026-04-13  
> **严重级别**: CRITICAL — 审稿人必然攻击  
> **状态**: 需要立即修复

---

## 问题识别

### 表格不对称证据

| 表格 | ResNet-18 数据 | Tiny-ViT 数据 | ConvNeXt 数据 |
|:-----|:---------------|:--------------|:--------------|
| **Table 1 (FP32 Baseline)** | 仅CIFAR-10 (94.98%) | CIFAR-10/100/Flowers | CIFAR-10/100/Flowers |
| **Table 2 (Result Summary)** | 仅FP32一行 | V3/V4/V6多行 | 隐含多行 |
| **正文讨论** | 仅提及R4 (Supp) | 大量实验 | 大量实验 |

### 审稿人攻击原话预测

> "作者声称在三种架构（ResNet-18, ConvNeXt-Tiny, Tiny-ViT-5M）上验证了框架，但Table 1和Table 2显示ResNet-18**仅完成了CIFAR-10基线**，缺乏CIFAR-100/Flowers-102数据，**更缺乏任何噪声/HAT实验**。这是不诚实的范围声明。"

> "摘要和封面信声称'validated on ResNet-18, ConvNeXt, and Tiny-ViT'，但证据明显不对称。ResNet只是'entry validation platform'而非完整验证。"

---

## 根本问题

### 1. 声称 vs 证据不匹配

**声称（封面信）**:
> "Hybrid analog/digital deployment decomposition validated on Tiny-ViT, ConvNeXt, **and ResNet backbones**"

**实际**:
- ResNet-18: 1个数据集，1个实验条件
- ConvNeXt: 3个数据集，多个实验条件
- Tiny-ViT: 3个数据集，多个实验条件

### 2. 范围降级未说明

正文（`04_experimental_setup.tex` L4）承认：
> "ResNet-18 on CIFAR-10 as an **entry validation platform**"

但摘要、封面信、贡献列表**未明确降级ResNet的角色**。

### 3. 表格设计误导

Table 1将ResNet与ConvNeXt/Tiny-ViT并列，使用"--"暗示数据缺失而非设计选择，读者会期待对称数据。

---

## 修复方案

### 方案A: 补充ResNet完整实验 (推荐，如果GPU时间允许)

**需要补充**:
| 实验 | GPU时间 | 紧迫性 |
|:-----|:--------|:-------|
| ResNet-18 CIFAR-100 FP32 | 0.5h | P1 |
| ResNet-18 CIFAR-100 V3/V4 | 2h | P1 |
| ResNet-18 Flowers-102 (可选) | 1h | P2 |

**优势**: 真正对称，无懈可击  
**风险**: 时间成本；可能显示ResNet也脆弱（但可解释）

### 方案B: 重新定位ResNet角色 (快速修复)

**修改范围**:

1. **摘要**: 改为
   > "Using **Tiny-ViT-5M and ConvNeXt-Tiny** as primary testbeds, with ResNet-18 as an initial validation platform..."

2. **封面信贡献列表**: 第三项改为
   > "Hybrid analog/digital deployment decomposition validated on **ConvNeXt and Tiny-ViT**, with initial baseline calibration on ResNet-18"

3. **Table 1**: 添加脚注
   > "ResNet-18 evaluated on CIFAR-10 only as an entry validation; full cross-dataset study focused on ConvNeXt and Tiny-ViT."

4. **04_experimental_setup**: 明确说明
   > "ResNet-18 on CIFAR-10 serves as an **initial calibration platform**; the primary experimental matrix covers ConvNeXt-Tiny (CNN from scratch) and Tiny-ViT-5M (transformer fine-tuned) across all three datasets."

**优势**: 快速，诚实  
**风险**: 审稿人可能仍质疑为何不完全移除ResNet

### 方案C: 移除ResNet主文提及 (最保守)

**修改**:
- 摘要、封面信、贡献列表**完全移除ResNet-18**
- 仅保留`04_experimental_setup`和Supplementary中的提及
- 解释为"Supplementary baseline calibration"

**优势**: 彻底避免攻击  
**风险**: 显得范围缩小；需要大量文本修改

---

## 推荐策略

**时间允许 → 方案A + 方案B表述调整**  
**时间紧迫 → 方案B立即执行**

### 立即行动清单

| 优先级 | 行动 | 负责人 | 时间 |
|:-------|:-----|:-------|:-----|
| P0 | 决策：补充实验 vs 重新定位 | 用户 | 今天 |
| P0 | 修改摘要/封面信/贡献列表 | Codex | 2小时 |
| P1 | 添加Table 1脚注 | Codex | 30分钟 |
| P1 (如选A) | 运行ResNet CIFAR-100实验 | Gemini | 2-3 GPU小时 |
| P2 | 全文检查"three architectures"表述 | Kimi | 1小时 |

---

## 防御性语言 (如果保持现状)

**不建议**，但如果必须：

> "ResNet-18 was intentionally scoped as an entry-level validation on CIFAR-10 to establish the simulation pipeline, while the full cross-dataset and cross-regime study focused on ConvNeXt and Tiny-ViT as representative of modern CNN and transformer deployment scenarios."

**弱点**: 审稿人会问"为何Table 1设计得看起来对称？"

---

## 结论

这是一个**必须修复**的问题。当前状态在审稿时几乎必然被攻击为"范围声明不诚实"或"实验设计不对称"。

**最诚实的做法**: 方案B — 明确降级ResNet角色，避免对称性误导。

**最完整做法**: 方案A — 补充实验，实现真正对称。

**决策权**: 用户，基于GPU时间和风险偏好。
