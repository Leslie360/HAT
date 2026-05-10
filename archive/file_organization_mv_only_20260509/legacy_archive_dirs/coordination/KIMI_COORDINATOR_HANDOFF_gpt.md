# Kimi 协调员交接文档 (Claude → Kimi)

> **Claude 额度用完，Codex/Gemini 下线。Kimi 是唯一活跃 agent，兼任协调员。**
> **本文档是你运作项目的唯一参考。**

---

## 一、项目状态

| 指标 | 值 |
|:--|:--|
| **目标期刊** | Nature Communications |
| **License** | Apache 2.0 |
| **主文** | 13 页 (main.pdf)，~10-11 页内容 |
| **补充材料** | 10 页 (supplementary_main.pdf) |
| **编译状态** | 干净，无 `??` 引用 |
| **Reviewer issues** | 104 条，✅~48 (46%), 🔶~40, ❌~9 |
| **P13 AIHWKIT** | PID 214264 运行中，自动队列接 P14 |

---

## 二、正在自动运行的任务（不要干预）

### P13 已完成 ✅

结果：digital 95.46%, AIHWKIT **90.08 ± 0.21%** (10K×10, CPU analog)
- 详见 `report_md/_gpt/P13_aihwkit_shared_regime_result.md`
- 与 subset 对比：Full 90.08±0.21% vs Subset 91.80±1.02% — 准确率略低但方差小 5 倍
- Claude 已写入 AGENT_SYNC 和 CLAUDE_TASK Locked Numbers

### P14 失败 ❌

P14-A (Flowers V2) 和 P14-B (数据消融) 都崩了：
- 原因：`checkpoints/_gpt/p14_flowers_v2/V2_hybrid_no_noise_best.pt` 不存在
- V2（无噪声、无 retention 的 hybrid）从未训练过
- **需要用户决定**：(a) 训练 V2 checkpoint（需 GPU）或 (b) 用 V1 做 baseline 重设计

**你要做的：**
1. 将 P13 AIHWKIT full 数字写入论文 (`06_discussion.tex` 或 Supplementary)
2. 更新 Coverage #1 (AIHWKIT comparison) → ✅
3. 向用户汇报 P14 失败，请求决策

---

## 三、Locked Numbers（论文中的数字，不可更改）

| 实验 | 值 | 在论文中位置 |
|:--|:--|:--|
| V1 (3-seed) | 98.06 ± 0.17% | Results 表格 |
| V4 (3-seed) | 87.95 ± 0.27% | Results 表格 |
| C1 (3-seed) | 82.43 ± 0.17% | Results 表格 |
| C4 (3-seed) | 84.75 ± 0.72% | §5 NL/HAT 段落 |
| V8 (retention) | 89.67 ± 0.08% | Appendix |
| Ensemble HAT (fresh) | 86.37 ± 1.54% | §5 + §6 |
| Energy | 273.94 µJ, 11.45x | §5 Energy |
| AIHWKIT subset | 91.80 ± 1.02% (256) | Supp 对比 |
| AIHWKIT full (10K×10) | **90.08 ± 0.21%** (digital 95.46%) | **待写入论文** |

---

## 四、你的待办任务

### 立即可做

1. **写入 P13 AIHWKIT full 到论文** — 90.08±0.21% 写入 `06_discussion.tex` RRAM comparison 或 Supplementary
2. **更新 Coverage #1 (AIHWKIT comparison)** → ✅
3. **Title 决策** — 你已评估了 5 个候选，等用户决定后改 `main.tex` 的 `\title{}`
4. **Coverage matrix #44 升级** — 论文已 13 页，可将 manuscript length 升级为 ✅
5. **向用户汇报 P14 失败** — V2 checkpoint 不存在，需要决定是否训练 V2 或重设计 ablation

### P14 阻塞中（等用户决定）

6. **Flowers V2 ablation 分析** — 需要先训练 V2 或用 V1 做 baseline
7. **数据消融表** — 被 P14-A 失败阻塞
8. **更新 Coverage #12 (data ablation), #33 (Flowers)** — 等 P14 解决后

### 长期（如果有余力）

9. **剩余 ❌ issues 评估** — 剩 9 个，大部分 scope 外。写一份简短说明为什么不做。
10. **最终 pre-submission checklist** — 确认所有 reviewer 回复到位

---

## 五、关键规则

1. **不编造数字或文献** — 数字只用 Locked Numbers 或实验 log
2. **不改 main.tex 结构** — 只改 sections/*.tex 和 supplementary.tex 的内容
3. **不碰 scripts 或 checkpoints**
4. **AGENT_SYNC 只写一次** — 不要重复追加相同内容（上轮教训）
5. **Gemini 信任规则** — 如果 Gemini 回来，它的 completion claim 必须在源码中验证
6. **不替用户做决策** — Title 选择、是否再压缩等，写方案等用户拍板

---

## 六、文件地图

| 文件 | 用途 |
|:--|:--|
| `AGENT_SYNC_gpt.md` | 所有 agent 的工作记录，**你的日志也写这里** |
| `CLAUDE_TASK_gpt.md` | 总任务清单 + Locked Numbers |
| `REVIEWER_COVERAGE_MATRIX_gpt.md` | 104 issue 覆盖状态 |
| `paper/latex_gpt/sections/*.tex` | 论文各章节 |
| `paper/latex_gpt/supplementary.tex` | 补充材料 |
| `paper/latex_gpt/refs_gpt.bib` | 参考文献 |
| `logs/_gpt/` | 所有实验日志 |

---

## 七、与用户沟通

用户（Leslie）是项目负责人。你向他汇报时：
- 用中文
- 简明扼要
- 如果需要决策（如 title 选择），列出选项 + 你的建议
- 如果发现问题，直接说问题 + 建议方案
- 不要问"要不要写入"，直接写（用户之前明确要求过）

---

*Claude 签字交接。祝顺利。*
