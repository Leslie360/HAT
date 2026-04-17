# KX60: Supplementary/Caption Tone Audit

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Goal**: 检查补充材料和图注的AI味/机械味

---

## 审计范围

- `paper/latex_gpt/supplementary.tex`
- 主文图注 (Fig 1-5 captions)
- 补充图注 (Fig S1-S5 captions)

---

## 补充材料审计

### 整体评估

**现状**: 详细、技术性强，但略显机械清单式

**主要观察**:

| 段落 | 评估 | 问题 |
|:-----|:-----|:-----|
| S1.1 Detailed Experiment Matrix | ⭐⭐⭐⭐☆ | 信息完整，但像数据库导出 |
| S1.2 Evaluation Protocol | ⭐⭐⭐⭐☆ | 技术准确，但被动语态多 |
| S1.3 Parameter Provenance | ⭐⭐⭐⭐⭐ | 已较好，证据导向 |
| S1.3.3 Sensitivity Analysis | ⭐⭐⭐⭐☆ | "Interpretation"段落防御性 |

---

## 具体修复建议

### 修复1: Experiment Matrix 开头
**位置**: `supplementary.tex` L9-14
**当前**: 
```
For Tiny-ViT, the canonical family consists of V1--V6. V3 denotes ``standard train with fixed D2D,'' not a direct one-to-one analog of the ConvNeXt C3 setting. The legacy V7 retention-aware checkpoint is excluded because...
```
**问题**: 过于详细的排除说明，像内部笔记
**建议**:
```
Tiny-ViT experiments follow the canonical V1--V6 protocol. V3 uses fixed D2D (analogous to ConvNeXt C3), while V7--V8 represent early retention-aware explorations excluded from the main analysis.
```

---

### 修复2: Sensitivity Analysis Interpretation
**位置**: `supplementary.tex`  sensitivity表格后
**当前**: 
> "The numerically identical rows... should therefore be read as a stability result rather than as a copy-paste artifact..."

**问题**: 过度防御，解释过多
**建议**:
> "Identical rows reflect scale-masking: C2C noise falls below the 4-bit LSB threshold."

---

### 修复3: 删除内部术语
**位置**: 多处
**识别**: "legacy V7", "corrected retention semantics", "rerun sanity check"
**建议**: 改为中性描述或删除

---

## 图注审计

### 主文图注评估

| 图 | 评估 | 建议 |
|:---|:-----|:-----|
| Fig 1 | ⭐⭐⭐⭐⭐ | 简洁清晰 |
| Fig 2 | ⭐⭐⭐⭐⭐ | 良好 |
| Fig 3 | ⭐⭐⭐⭐☆ | 略长，可精简 |
| Fig 4 | ⭐⭐⭐⭐⭐ | "Error bars show..." 标准格式 |
| Fig 5 | ⭐⭐⭐⭐☆ | "and HAT recovery" 稍模糊 |

### 补充图注评估

| 图 | 评估 | 建议 |
|:---|:-----|:-----|
| Fig S1 | ⭐⭐⭐⭐☆ | 技术详细，但被动语态多 |
| Fig S2-S5 | ⭐⭐⭐⭐☆ | 类似模式 |

---

## 语气改进模板

### ❌ 避免
- "It should be noted that..."
- "We emphasize that..."
- "This is not a X but rather a Y"
- "careful readers will observe"

### ✅ 推荐
- 直接陈述事实
- 删除强调性前缀
- 让数据自己说话

---

## 具体修复列表

| # | 位置 | 修复内容 |
|:-:|:-----|:---------|
| 1 | Supp L9-14 | 简化V7排除说明 |
| 2 | Supp sensitivity | 删除防御性解释段落 |
| 3 | Supp 多处 | 删除"legacy", "corrected"等内部术语 |
| 4 | Fig 3 caption | 精简长度 |
| 5 | Fig S1-S5 | 减少被动语态 |

---

## 优先级

- **P1**: Supp L9-14 简化 (最显眼)
- **P2**: Sensitivity解释段落 (防御性最强)
- **P3**: 图注被动语态 (细节改进)

---

**非阻塞任务，但提升整体专业感。**
