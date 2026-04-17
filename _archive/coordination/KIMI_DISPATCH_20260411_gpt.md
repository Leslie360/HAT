# Kimi 任务单 — 2026-04-11 09:30 (Claude 休眠前最终版)

> **欢迎 Kimi！你的主要角色是质量门：校对、数字核查、一致性检查。**
> **完成每个任务后在 `AGENT_SYNC_gpt.md` 末尾追加 `[Kimi]` block。**

---

## 背景

- 你是新加入的团队成员，这是第二轮试用任务
- 第一轮 K1-K5 被 Codex 抢先完成了（不是你的问题）
- 这一轮侧重校对和检查，不需要改代码
- 项目：有机光电 CIM 边缘视觉推理的硬件感知仿真框架，目标期刊 Nature Communications

---

## 参考数据（Locked Numbers）

| 实验 | 数值 |
|:--|:--|
| V1 (3-seed) | 98.06 ± 0.17% |
| V4 (3-seed) | 87.95 ± 0.27% |
| C1 (3-seed) | 82.43 ± 0.17% |
| C4 (3-seed) | 84.75 ± 0.72% |
| Ensemble HAT (fresh instance) | 86.37 ± 1.54% |
| V8 (retention) | 89.67 ± 0.08% |
| Energy | 273.94 μJ, 11.45x reduction |

---

## KM1: 全文 Proofreading — Abstract + Intro + Conclusion [MED]

**检查文件：**
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

**检查项：**

| 类别 | 具体内容 |
|:--|:--|
| LaTeX 问题 | `??` 未解析引用、多余 `$` 符号、缺失 `\%`、`\ref` 错误 |
| 拼写/语法 | 英语语法错误、拼写错误、主谓不一致 |
| 术语一致 | HAT/hardware-aware training 写法统一？σ_C2C 写法统一？ |
| 过长句 | 超过 40 词的句子标出来 |
| 数字格式 | ±前后有空格？百分号一致？小数点不是冒号？ |

**交付格式：**
```
文件: 00_abstract.tex
- Line X: "86.371.54%" → 应为 "86.37±1.54%" [如果还未修复]
- Line Y: "..." 语法问题 → 建议改为 "..."
```

---

## KM2: Abstract 数字核查 [MED]

**操作：**
1. 读 `paper/latex_gpt/sections/00_abstract.tex`
2. 列出 abstract 中出现的**每一个数字**
3. 逐一与上面的 Locked Numbers 表对比
4. 检查：
   - 数字是否匹配？
   - ± 符号是否正确？
   - 11.45x claim 是否有 qualifier（"first-order" / "upper-bound"）？
   - 如果 abstract 提到 C4，是否用了 84.75±0.72%（而非旧的 91.98%）？

**交付：** 数字一致性报告

---

## KM3: Conclusion 与 Results 一致性 [MED]

**操作：**
1. 读 `paper/latex_gpt/sections/07_conclusion.tex`
2. 读 `paper/latex_gpt/sections/05_results.tex`
3. 列出 conclusion 中的每一个 claim：

| Conclusion Claim | Results 中的支撑 | 一致？ |
|:--|:--|:--:|
| "V4 达到 xx%" | §5.x line Y | ✅/❌ |
| ... | ... | ... |

4. 额外检查：
   - Conclusion 是否有 overclaim（Results 里没有数据支撑的断言）？
   - Results 中的重要发现是否在 Conclusion 中被遗漏？
   - 11.45x claim 是否与 Results 一致并有 qualifier？

**交付：** Claim vs Evidence 对照表

---

## KM4: Reference 完整性审计 [LOW]

**操作：**
1. 读 `paper/latex_gpt/refs_gpt.bib`
2. 检查以下问题：

| 检查项 | 说明 |
|:--|:--|
| `and others` 占位 | 以前有 10 条，应该已全部补全。确认一下 |
| `TODO` 标记 | 搜索任何 TODO/TBD/FIXME |
| 缺 year | 每条 entry 必须有 year 字段 |
| 缺 journal/booktitle | 每条 entry 必须有发表场所 |
| 重复 entry | 不同 key 但指向同一篇论文 |
| URL/DOI | 不强制，但标注缺失的 |

**交付：** 问题清单

---

## 输出模板

每个任务完成后在 `AGENT_SYNC_gpt.md` 末尾追加：

```markdown
## [Kimi] 2026-04-XX HH:MM — Task KMN: 任务名称
### Status
- 完成
### Findings
- 问题 1: ...
- 问题 2: ...
### Recommended Fixes
- Fix 1: 文件 line X, "old text" → "new text"
- Fix 2: ...
### Evidence
- `paper/latex_gpt/sections/00_abstract.tex` line X-Y
```

---

## 规则

1. **不要直接改 .tex 文件。** 只提出修改建议，Claude 醒来后审批执行。
2. **不要编造任何内容。** 你的角色是检查，不是创作。
3. **不要碰代码文件。** 代码是 Codex 的领域。
4. 如果发现重大问题（如论文中引用了不存在的数据），在 AGENT_SYNC 中标为 `⚠️ CRITICAL`。
5. 有疑问写在 AGENT_SYNC 中，Claude 醒来后会回复。
