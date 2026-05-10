# 📡 Round P2 审稿意见广播 — 2026-04-20

**TO:** 内部循环 / 协作者
**FROM:** Claude (Opus 4.7)
**RE:** v20260420 外部评审意见完整汇编 + 决策建议

---

## 文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| **完整评审汇编** | `report_md/_gpt/EXTERNAL_REVIEW_COMPILATION_20260420_FULL.md` | 10 个独立评审视角，264 行 |
| **精简版** | `report_md/_gpt/EXTERNAL_REVIEW_COMPILATION_20260420.md` | 主要评审块，429 行 |
| **中文论文 Ch.1-4** | `paper/thesis_cn/` | Phase α 已完成，47,658 字符 |
| **理论备忘录** | `report_md/_gpt/theory_memos/` | Gemini 9 份备忘录，19,264 词 |

---

## 核心结论（一句话）

> **稿件已跨过"能不能投"的门槛，进入"投出去后会发生什么"的阶段。**
> 最可能路径：送审 → 混合评审（Minor + Major）→ 编辑给 Major Revision。
> 所有 objections 均可通过文字回应，无需新实验。

---

## 10 个评审视角的共识与分歧

### ✅ 共识（10/10 一致）
- 10%→86.37% 核心发现 **数据严谨、可追溯**
- 方法论诚实性 **exemplary**
- R1/R2/R3 三个高风险问题 **已全部关闭**
- MLP 32.12% fresh-instance 披露是 **关键加分项**

### ⚠️ 分歧（结构性争议）
- **Minor/Accept 阵营（5/10）**：方法学贡献足够强，simulation-only 可接受
- **Major 阵营（4/10）**：无 hardware validation 是原则性缺陷，idealized 模型外推边界存疑

**分歧本质**：NC 是否接受 simulation-only 的方法学论文——这不是写作问题，是社区标准问题。

---

## 立即行动项（Before Submit）

| 优先级 | 事项 | 耗时 | 负责人 |
|--------|------|------|--------|
| P0 | Figure 4(c) 统一为 **86.37±1.54%**（现 ±1.62% 不一致） | 30 秒 | Codex |
| P0 | SX.Y/SX.Z 替换为真实章节编号 | 5 分钟 | Kimi |
| P1 | Abstract 加 "(chance level for balanced 10-class task)" | 2 分钟 | Kimi |
| P1 | §4.5 加 training overhead footnote | 10 分钟 | Kimi |
| P2 | Cover letter 强化 "simulation baseline + risk ranking" framing | 30 分钟 | Gemini |

---

## 预准备 Rebuttal（无需现在改，提前备好不慌）

1. **"无硬件验证"** → OPECT 零样本 88.53% + profile interface 设计用于实测数据注入 + 合作时间线
2. **"理想化模型"** → risk ranking tool 定位 + AR(1) ρ=0.5 仍有效 + rank ordering 保留
3. **"Ensemble HAT = 正则化"** → 已有 control：per-batch degrades（86.16% vs 88.41% epoch）

---

## 本轮产出状态

| 组件 | 完成度 | 备注 |
|------|--------|------|
| 中文论文 Ch.1-4 | ✅ 100% | 47,658 字符，待审阅 |
| Gemini 理论备忘录 | ✅ 100% | 9 份，19,264 词 |
| CX-J1b GPU | 🔄 运行中 | Epoch 19/100，best=26.37% |
| 论文手稿 v20260420 | ✅ 待提交 | 2 个格式修复后即可 |

---

## 下一步需要用户决策

1. **是否现在提交 NC？**（修复 P0 后今晚可投）
2. **是否并行启动 CX-J1c（full-attention-linear）？**（J1b 完成后自动排队）
3. **Cover letter 核心段落由谁起草？**（建议 Gemini，30 分钟）

---

**完整细节见评审汇编文件。**
