# 全面审稿审计报告

> **日期**: 2026-04-13  
> **范围**: 全论文局限 + AI味 + 学术风格  
> **状态**: 关键问题发现

---

## 第一部分：类似ResNet的局限（不对称/不完整）

### 🔴 1.1 实验覆盖不对称（除ResNet外）

| 问题 | 位置 | 严重程度 | 说明 |
|:-----|:-----|:---------|:-----|
| **Flowers-102 HAT缺失** | Table 2 | 🔴 高 | ConvNeXt Flowers-102 HAT结果缺失；Table 2显示33.22%* (single-run)后无HAT恢复数据 |
| **CIFAR-100 V6缺失** | Results | 🟡 中 | Tiny-ViT V6 (Frontend Opto) 仅报告CIFAR-10，CIFAR-100/Flowers缺失 |
| **Energy分析仅Tiny-ViT** | Fig 11 | 🟡 中 | 能耗分解仅Tiny-ViT，无ConvNeXt/ResNet对比 |

**审稿人攻击预测**:
> "Table 2显示ConvNeXt在Flowers-102上 baseline 33.22%，但HAT恢复数据在哪？如果无法恢复，应明确说明。"

---

### 🔴 1.2 声称vs证据不匹配

| 声称 | 证据 | 问题 |
|:-----|:-----|:-----|
| "three vision datasets" (摘要) | ResNet仅CIFAR-10 | 已识别，需修复 |
| "hybrid analog/digital decomposition validated on ResNet, ConvNeXt, and Tiny-ViT" (封面信) | ResNet无混合实验 | 严重夸大 |
| "cross-dataset accuracy" (Fig 4) | 实际仅Tiny-ViT完整 | 图题可能误导 |

---

### 🟡 1.3 统计严谨性问题

| 位置 | 问题 | 建议 |
|:-----|:-----|:-----|
| Table 2 asterisks | 多处single-run标记(*)，但无解释为何某些实验无MC | 添加统一脚注说明 |
| Flowers-102 ConvNeXt | 33.22%*标记为single-run，但正文说"does not recover" | 需明确是否尝试HAT及结果 |
| V4 ConvNeXt "91.98% best seed" vs "84.75 ± 0.72%" | 7pp差距巨大，仅归因于"seed sensitivity" | 需更深入分析或限制声称 |

---

## 第二部分：AI味太浓的表达

### 🔴 2.1 机械连接词过度使用

**高频问题词**:
- "Furthermore" / "Moreover" / "In addition" — 学术写作中过度使用显得机械
- "Therefore" / "Thus" — 因果强制化
- "It is important to note that..." / "We emphasize that..." — 防御性强调

**具体位置**:
| 位置 | 当前表达 | 建议修改 |
|:-----|:---------|:---------|
| Introduction L6 | "As a result, there is still no clear route..." | 删除"As a result"，直接陈述 |
| Introduction L10 | "Within this scope, several results emerge clearly" | 删除"clearly" |
| Results L27 | "This scale-masking regime is specific to the present model and does not persist" | "This protection disappears when..." |
| Discussion L6 | "Three constraints instead emerge more clearly" | "Three constraints dominate" |

---

### 🔴 2.2 完美结构化段落（AI生成痕迹）

**问题模式**: 每个段落严格遵循"总-分-总"，连接词完美，缺乏真实学术写作的迂回。

**典型例子**:
```latex
% 当前 (太完美，像模板)
The first is converter precision. The transition around 6-bit ADC resolution marks a clear change in model behavior: below this point Transformer inference degrades sharply, indicating that improvements in conductance control remain gated by readout precision in the present mixed-signal stack.

% 建议 (更自然)
Converter precision proves to be the dominant constraint. Reducing ADC resolution below 6 bits causes an abrupt accuracy collapse, suggesting that conductance control improvements cannot translate to system gains without matched readout precision.
```

---

### 🔴 2.3 过度防御性语言

| 位置 | 当前 (防御性) | 建议 (自信直接) |
|:-----|:--------------|:----------------|
| Abstract L4 | "We further find that standard HAT overfits..." | "Standard HAT overfits..." |
| Discussion L10 | "This improved transferability is accompanied by a residual gap..." | "A residual gap remains..." |
| Discussion L20 | "suggests that Transformer inference depends strongly on" | "indicates that Transformer inference depends on" |
| Limitations | 整段过多"should be kept in view", "not modeled" | 直接列出限制，无需过度 soften |

---

### 🟡 2.4 解释性括号过多

**问题**: 过多括号解释，打断阅读流。

| 位置 | 问题表达 |
|:-----|:---------|
| Introduction L6 | "variability, converter precision, retention-induced drift, and transfer across fabricated instances" | 列举过长 |
| Methods L43 | "quantization, cycle-to-cycle (C2C) and device-to-device (D2D) variability, ADC distortion, retention drift, and nonlinear-write surrogates" | 括号缩写后文不一定都用 |

---

## 第三部分：实验报告口吻 vs 顶刊风格

### 🔴 3.1 实验列表式写作（Methods/Supp）

**问题**: Supplementary Section 1.1 像实验笔记本，不像学术补充材料。

**当前**:
```
For Tiny-ViT, the canonical family consists of V1--V6. V3 denotes ``standard train with fixed D2D,'' not a direct one-to-one analog of the ConvNeXt C3 setting. The legacy V7 retention-aware checkpoint is excluded because...
```

**顶刊风格**:
```
The Tiny-ViT experiments follow a canonical protocol (V1--V6). V3 uses fixed D2D masking, analogous to ConvNeXt C3, while V7--V8 represent early retention-aware explorations excluded from the main analysis.
```

---

### 🔴 3.2 内部术语外泄

**不应出现在主文的术语**:
- "legacy V7" — 内部版本控制术语
- "corrected retention semantics" — 开发过程术语  
- "rerun sanity check" — 开发流程术语
- "V1/V2/V3..." — 应在Supp详细说明，主文用描述性名称

---

### 🔴 3.3 过度详细的排除说明

**当前** (Supp L12):
> "The legacy V7 retention-aware checkpoint is excluded because it predates the corrected retention semantics..."

**问题**: 读者不关心V7为什么被排除，只想知道用了什么。

**建议**: 直接陈述使用的版本，排除理由移至footnote或删除。

---

### 🟡 3.4 图注像技术文档而非学术叙述

**当前 Fig 4 caption**:
> "Cross-dataset accuracy under the canonical deployment regime. Error bars show standard deviation over 10 Monte Carlo inference runs."

**顶刊风格**:
> "Accuracy across datasets under canonical deployment (mean ± s.d., 10 Monte Carlo runs)."

---

## 第四部分：具体修复建议

### 4.1 立即修复（阻塞性问题）

1. **ResNet-18补充实验** (已规划)
2. **ConvNeXt Flowers-102 HAT数据**: 明确说明是否尝试及结果
3. **摘要/封面信**: 降级ResNet角色或补充实验后重新定位

### 4.2 高优先级修复（AI味）

1. **删除以下连接词** (全局搜索-替换):
   - "Furthermore" → 删除或改为"Also"
   - "Moreover" → 删除
   - "It is important to note that" → 直接陈述
   - "We emphasize that" → 删除

2. **简化句子**:
   - 超过3行的句子拆分为2句
   - 删除嵌套从句中的"which"从句

### 4.3 中优先级修复（风格）

1. **Supplementary重写**:
   - 删除所有"legacy", "corrected", "sanity check"
   - 实验矩阵改为表格而非列表式描述

2. **图注精简**:
   - 删除"Error bars show..."等标准说明，改为"mean ± s.d."

---

## 第五部分：顶刊风格示例对比

### 不好的 (AI/实验报告味)

> "We study a hybrid analog/digital inference stack in which dense linear operators are executed on differential-pair crossbar arrays, while control-heavy or utilization-poor operators remain digital. Table 1 summarizes the mapping adopted here, following established practice in heterogeneous CIM accelerators."

### 好的 (Nature/Science风格)

> "We adopt a hybrid mapping: dense linear operators execute on analog crossbars, while dynamic attention and normalization remain digital (Table 1). This partition follows recent heterogeneous CIM accelerators."

**差异**:
- 删除"we study" (显而易见)
- 删除"in which"从句
- "control-heavy or utilization-poor" → "dynamic attention" (具体直接)
- "summarizes the mapping adopted here" → "(Table 1)" (简洁)

---

## 总结

| 类别 | 问题数 | 紧急度 |
|:-----|:-------|:-------|
| 数据不对称 | 3个 | 🔴 高 (ResNet已规划) |
| AI连接词 | 15+处 | 🔴 高 |
| 防御性语言 | 10+处 | 🟡 中 |
| 实验报告口吻 | 多处 | 🟡 中 |
| 内部术语 | 5+处 | 🟡 中 |

**建议行动**:
1. 立即执行ResNet补充实验
2. 全局删除机械连接词 (30分钟任务)
3. 重写Supplementary开头段落
4. 全文 passive voice audit
