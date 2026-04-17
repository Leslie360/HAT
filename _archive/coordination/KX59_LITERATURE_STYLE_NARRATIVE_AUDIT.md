# KX59: Literature-Style Narrative Audit

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Goal**: 识别并修复"AI味/人机味/reviewer-defense味"段落

---

## 审计方法

对比真实Nature/Science子刊论文的叙事风格，识别当前手稿中以下特征：
- ❌ 过度防御性措辞 ("address this issue", "we show below")
- ❌ 机械性列表式写作
- ❌ 过度使用连接词 ("therefore", "however", "furthermore")
- ❌ 被动语态过度使用
- ❌ 解释性括号过多

---

## Section-by-Section Audit

### Section 02: Related Work

**现状评估**: ⭐⭐⭐⭐☆ (较好，已Codex修改)

**仍有改进空间**:

| 位置 | 当前 | 建议 |
|:-----|:-----|:-----|
| L6 | "As we show below" | 删除或改为具体指向 "Section 5.4 demonstrates" |
| L6 | "Ensemble HAT addresses this issue by" | "Ensemble HAT resamples" (直接陈述，不防御) |
| L13 | "The most relevant precursor... The present work follows" | 考虑合并为更流畅的对比，减少分段 |

---

### Section 03: Methodology

**现状评估**: ⭐⭐⭐☆☆ (需改进)

**识别问题**:

| 位置 | 问题类型 | 当前 | 建议 |
|:-----|:---------|:-----|:-----|
| L7-20 | 列表式机械 | 长段落列举operator mapping | 考虑表格或更自然的分类叙述 |
| "In this sense, we follow... while adapting" | 过度解释 | 双重从句解释动机 | 简化："We adopt this hybrid mapping" |
| L22 | "Relative to prior... our emphasis is" | 防御性比较 | 直接陈述独特之处："We extend... by" |

---

### Section 05: Results

**现状评估**: ⭐⭐⭐⭐☆ (较好)

**改进建议**:

| 位置 | 当前 | 建议 |
|:-----|:-----|:-----|
| L27 | "This scale-masking regime is specific to the present model and does not persist" | 过于限定性 | "This scale-masking protection disappears when..." |
| L45 | "A pure-digital control experiment shows" | 被动语态 | "Pure-digital controls confirm" |

---

### Section 06: Discussion

**现状评估**: ⭐⭐⭐☆☆ (需改进)

**主要问题**: 限制性和未来方向段落过于详细，像检查清单

**建议**: 将长列表式讨论改为主题式段落，每个段落一个核心观点。

---

## 具体修复建议 (可复制到LaTeX)

### 修复1: "As we show below"
**位置**: `02_related_work.tex` L6
**当前**: "As we show below, that choice can make the model fit..."
**建议**: "Section 5.4 shows that this choice can cause..."

### 修复2: "Ensemble HAT addresses this issue"
**位置**: `02_related_work.tex` L6
**当前**: "Ensemble HAT addresses this issue by resampling..."
**建议**: "Ensemble HAT resamples the static D2D mask each epoch, improving zero-shot transfer."

### 修复3: 过度解释从句
**位置**: `03_methodology.tex` L20
**当前**: "In this sense, we follow the general hybrid logic of prior CIM simulators while adapting the profile interface to organic-device regimes and to the operator mix of Tiny-ViT."
**建议**: "We adopt this hybrid logic, extending prior CIM simulators to organic optoelectronic profiles and Tiny-ViT operators."

### 修复4: 防御性比较
**位置**: `03_methodology.tex` L22
**当前**: "Relative to prior ViT-on-PIM studies, our emphasis is on device-aware specialization..."
**建议**: "Unlike prior ViT-on-PIM studies, we explicitly model photoresponse, profile substitution, and joint variability evaluation."

---

## 整体叙事改进建议

### 1. 减少"we show"类短语
**统计**: 当前手稿约15处"we show" / "we demonstrate"
**目标**: 减至5-8处，其余改为直接陈述

### 2. 简化双重从句
**识别**: 超过3行无句号的句子
**修复**: 拆分为2-3个短句

### 3. 删除冗余限定语
**识别**: "in the present regime", "in the current model"等重复出现
**修复**: 保留必要处，其余删除

### 4. 主动语态优先
**目标**: 主动:被动比例从当前约6:4改善至8:2

---

## 检查清单

- [ ] 删除或替换所有"As we show below"
- [ ] 删除"addresses this issue by"类防御短语
- [ ] 简化L20长从句
- [ ] Discussion段落主题化重组
- [ ] 全局检查"present regime/current model"冗余

---

**优先级**: P1 (文风改进，非阻塞但提升可读性)
