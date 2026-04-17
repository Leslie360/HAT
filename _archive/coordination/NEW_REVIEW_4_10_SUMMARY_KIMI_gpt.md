# New Reviewer Comments (4.10) - Kimi's Analysis

> Codex verification note (2026-04-11): this file is still useful as a reviewer-issue summary, but parts of its task/status wording are now stale. Several items listed here as pending were completed later. For the verified current-state audit, see `KIMI_REVIEW_VERIFICATION_20260411_gpt.md`.

**Date:** 2026-04-11  
**Source:** `compute_vit/report_md/审稿人意见-4.10.md`  
**Status:** Ready for Codex Handoff

---

## Reviewers Included

1. **kimi** (comprehensive technical review)
2. **deepseek** (detailed technical and presentation issues)
3. **doubao** (结构清晰, Major Revision)
4. **ds-txun** (detailed parameter validation concerns)
5. **mimo** (中文评审, Minor Revision)
6. **Qwen** (technical soundness focus)

---

## Critical Issues Requiring Action (优先级排序)

### 🔴 P0: 统计严谨性 (多模型Reviewer共同关注)

**问题描述:**
- 核心Tiny-ViT结果（V4, Ensemble HAT）基于**单种子训练**
- ConvNeXt有3种子结果（84.75±0.72%），但Tiny-ViT缺乏
- Supplement提到"multi-seed campaign still being accumulated"不合适

**具体要求:**
- 为核心实验（V4 canonical HAT, V4 Ensemble HAT, NL=2.0 stress test）提供**多种子（≥3）统计**
- Table 2需要为所有关键结果添加误差条

**Reviewer引用:**
- deepseek (Sec 3.3): "headline Tiny-ViT results rely on single-seed training"
- doubao (Q5): "complete multi-seed results for all core experiments"
- ds-txun (Specific Issue): "The phrase 'still being accumulated' is inappropriate"

---

### 🔴 P1: 能量模型透明度

**问题描述:**
- ADC能量占比<0.1%与传统CIM文献矛盾
- E_cell（差分对单元能量）值未声明
- 2.5 pJ/FP32 MAC引用Horowitz 2014，但缺乏现代加速器对比

**具体要求:**
1. 在Fig 5 caption或Methods中说明ADC架构（SAR? Flash? Pipeline?）
2. 明确声明E_cell值及其文献来源
3. 补充INT8数字加速器对比（如Edge TPU, NPU）

**Reviewer引用:**
- kimi (Q1): "ADC Model Validation - What specific ADC architecture?"
- deepseek (Sec 3.4): "E_cell value... must be justified"
- ds-txun: "How does your hybrid system compare to commercial INT8 edge NPUs?"

---

### 🔴 P2: 系统性验证不足

**问题描述:**
- 与AIHWKIT比较仅1个ResNet-18点（Supplement 1.7）
- 缺乏与CrossSim/NeuroSim的对比
- "profile-driven"声称仅用2个文献profile验证

**具体要求:**
- 扩展AIHWKIT对比到ViT（至少Tiny-ViT V4 regime）
- 或明确声明为future work并降低声称

**Reviewer引用:**
- deepseek (Sec 5.2): "The paper's AIHWKIT comparison is minimal"
- doubao (Missing References): " cite and benchmark against recent AIHWKIT ViT studies"

---

### 🟡 P3: 参数验证

**问题描述:**
- Canonical参数（G_max/G_min=10, σ_C2C=5%, σ_D2D=10%）缺乏定量文献支持
- Zhang 2026 profile使用"proxy estimates"而非直接提取

**具体要求:**
- 为canonical profile的每个参数提供文献提取方法
- 说明从Vincze 2025提取的具体过程

**Reviewer引用:**
- ds-txun (Q1): "quantitative justification for each of these values"
- deepseek (Sec 3.1): "G_max/G_min = 10... does not explain why 10 is chosen"

---

### 🟡 P4: 叙述清晰度

**问题描述:**
1. **V1-V8符号**: 主文未定义，强迫读者查Supplement
2. **Scale masking**: 缺乏定量支持，呈现为假设而非机制
3. **Figure S2**: Tiny-ViT面板6个绿条都标"10.0"，无法区分

**具体要求:**
- 在主文添加V1-V8定义表
- 为scale masking提供定量分析（σ_noise vs quantization step）
- 修复Fig S2标签

**Reviewer引用:**
- kimi (Specific Issues): "V1-V8 notation... forcing the reader to flip to the supplement"
- deepseek (Sec 4.1 Q1): "scale recovery rescales... This is a hypothesis, not a proven mechanism"

---

### 🟡 P5: 技术细节

**问题描述:**
1. **Ensemble HAT开销**: "∼1.00×"表述模糊（是1×还是2×？）
2. **Retention验证**: 仅在Ensemble HAT上验证，未在standard HAT/non-HAT上测试
3. **Uniform vs proportional**: 缺乏物理依据说明

**Reviewer引用:**
- kimi (Q4): "Does this mean zero overhead, or 100% overhead?"
- deepseek (Sec 3.5): "only performed on the Ensemble HAT checkpoint"

---

## 快速修复（格式/文字）

| 问题 | 位置 | 修复 |
|:-----|:-----|:-----|
| 年份不一致 | Table 2, Refs | Vincze 2025 vs 2026；Zhang 2026 vs Liu 2025 |
| 数字不一致 | Table 1 vs 正文 | "98.06%" vs "97.48%" for Tiny-ViT CIFAR-10 |
| 星号未定义 | Table 1 | 33.22%* 未解释 |
| 连字符断词 | 多处 | "mathe-matical", "ampli-tude", "localibra-tion" |
| Fig S2标签 | Supplement | 所有Tiny-ViT条都显示"10.0" |

---

## Reviewer共识

### 共同认可
- ✓ 填补有机CIM模拟 gap 有意义
- ✓ Ensemble HAT 10%→86%是重要贡献
- ✓ 论文结构清晰，限制透明

### 共同担忧
- ✗ 统计严谨性不足（单种子）
- ✗ 能量模型假设需要更透明
- ✗ 验证范围有限（仅用文献proxy）

### 分歧
- **Minor Revision**: mimo
- **Major Revision**: kimi, deepseek, doubao, ds-txun, Qwen
- **Major (leaning Reject)**: ds-txun (如果无法加强实验验证)

---

## Kimi建议的行动方案

### Phase 1: 数据收集（高优先级）
1. **P0 多种子实验**: 运行Tiny-ViT V4和Ensemble HAT的3种子变体
2. **P1 能量参数**: 明确E_cell值和ADC架构假设

### Phase 2: 文档更新（中优先级）
3. **P3 参数provenance**: 添加canonical profile参数提取附录
4. **P4 清晰度**: V1-V8表，scale masking定量分析

### Phase 3: 对比实验（可选但推荐）
5. **P2 AIHWKIT ViT对比**: 至少1个额外数据点

### Phase 4: 格式修复（快速）
6. 修复所有数字/年份/标签不一致

---

## 交接给Codex

**@Codex**: 
1. 请基于以上分析制定详细任务分解
2. 优先处理P0统计严谨性和P1能量模型透明度
3. 需要新实验的任务标记为"需计算资源"
4. 完成后更新REVIEWER_COVERAGE_MATRIX_gpt.md

**关联文件:**
- `REVIEWER_COVERAGE_MATRIX_gpt.md` - 现有issue跟踪
- `审稿人意见-4.10.md` - 完整原始意见
- `FINAL_SUBMISSION_READINESS_gpt.md` - 当前状态（需更新）
