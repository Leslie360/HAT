# 📢 Kimi 广播：基于多模型审稿意见的紧急建议

> **日期**: 2026-04-12  
> **来源**: 整合12+外部模型审稿意见 (`审稿意见model_0411.md`)  
> **紧迫性**: HIGH — 需在投稿前完成
> **更新**: 2026-04-13 — 修改1已完成，用户自有数据替代外部合作

---

## ✅ 已完成：修改1 — 摘要添加 "simulation-only" 声明

**执行者**: Gemini (GM-X20)  
**状态**: ✅ **已完成并编译通过**

**修改内容**: 在 `00_abstract.tex` 首段已添加：
> "All experiments are conducted at the behavioral simulation level using literature-derived proxy parameters; physical hardware validation remains future work."

**影响**: 消除60%的审稿人攻击点（Claude-Sonnet估计）

---

## 🔄 剩余4项修改（需继续执行）

### 2. 统一 NL=2.0 表述为 "approximation-limit boundary"
**状态**: ✅ **已完成 by Gemini (GM-X19)**
- `00_abstract.tex`: "hard failure mode" → "approximation-limit failure mode"
- `07_conclusion.tex`: "hard boundary" → "approximation-limit boundary"

---

### 3. Ensemble HAT 与 noise augmentation 明确区分
**问题**: 审稿人会问"这和标准噪声增强有什么区别？"  
**修改**: Related Work 新增3段对比  
- (a) noise injection QAT (Jacob et al. 2018)  
- (b) domain randomization (Tobin et al. 2017)  
- (c) multi-device analog training  

**关键区分点**: D2D的**结构化空间相关性** vs C2C的**i.i.d.噪声**  
> "The fixed spatial pattern of D2D mismatch (constant per device, correlated across array) is structurally different from i.i.d. noise augmentation — this distinction is the scientifically non-obvious part."

**影响**: defending Ensemble HAT 作为真正贡献  
**工作量**: 2小时（写作+引用）  
**负责人**: Gemini / Codex

---

### 4. C2C不变性添加机制解释
**状态**: ✅ **已完成 by Gemini (GM-X22)**
- 已在 `supplementary.tex` Table S3 下方添加机理解释
- 说明"scale-masking effect"导致C2C噪声被抑制在LSB阈值以下

---

### 5. 不对称性敏感度从Supp移到主文
**状态**: ✅ **已完成 by Gemini (GM-X23)**
- 2%悬崖、10%崩溃的定量结论已植入 `06_discussion.tex`

---

## 📊 投稿策略更新

### ✅ 已确认决策
| 项目 | 决策 |
|:-----|:-----|
| 联系Zhang/Vincze团队 | ❌ **暂不联系** — 用户将使用自有数据 |
| 外部数据合作 | ⏸️ **暂停** — 等待内部数据就绪 |
| 修改1-2 (摘要+NL表述) | ✅ **已完成** |
| 修改4-5 (C2C解释+不对称性) | ✅ **已完成** |
| 修改3 (Related Work对比) | 🔄 **待执行** |

### 推荐策略：选项A变体
**策略名称**: "现在就投，自有数据后续补充"

**理由**:
1. 用户自有数据即将就绪（无需等待外部合作）
2. 5项共识修改中4项已完成
3. 仅剩Related Work区分待完善

**时间线**:
- **本周**: 完成修改3 (Related Work对比)
- **下周**: 投NC，准备Major Revision
- **Revision阶段**: 如需要，补充自有实测数据验证

---

## 🎯 当前状态总结

| 修改项 | 状态 | 负责人 |
|:-------|:----:|:-------|
| 1. 摘要simulation-only声明 | ✅ 完成 | Gemini |
| 2. NL=2.0表述统一 | ✅ 完成 | Gemini |
| 3. Ensemble HAT区分 | 🔄 待执行 | Gemini/Codex |
| 4. C2C不变性解释 | ✅ 完成 | Gemini |
| 5. 不对称性敏感度移动 | ✅ 完成 | Gemini |

**剩余工作量**: ~2小时（修改3）

---

## 💡 关键更新

> **用户确认**: 不联系Zhang/Vincze团队，将使用自有数据替代。
> 
> **策略调整**: 从"等待外部验证"转为"自有数据后续补充"模式。

---

**广播更新完成。等待修改3执行。**
