# 2026-04-12 战略重置广播（Codex）

> 背景：用户最新决策已明确改变项目节奏与目标函数。
> 新策略优先级高于此前的“立刻冲 NC closeout”默认路线。

---

## 新的项目立场

### 1. 不锁死单一投稿目标

项目**不再默认只冲 Nature Communications**。
从现在开始，采用 **多元化 venue strategy**：

- 保留 NC 作为高目标选项
- 同时准备更务实的候选路线
- 所有文稿与实验决策以“最大化长期项目价值”而非“最短时间投稿”优先

### 2. GPU 空闲时，允许补做高 ROI 实验

此前的“不要重开 GPU-heavy experiments”是为了 closeout 节奏。
在当前新策略下，这条被放宽为：

- **允许**启动少量高价值、直接回应 reviewer 的补充实验
- 这些实验优先服务：
  - supplementary strengthening
  - reviewer defense
  - future revision / alternate venue robustness
- 但仍避免无边界扩实验

### 3. 不着急投稿，等待博士真实数据是合理策略的一部分

当前不再以“立刻投稿”为唯一目标。
自有 measured-device data 被视为：

- 论文增强包
- 方法学闭环强化点
- 长线项目资产

因此项目从“submission-closeout mode”切换为：

> **submission-and-evidence expansion mode**

### 4. Codex 角色切换

Codex 现在以 **审核 / 编排 / 定版** 为主，不再默认自己承担大块主写与新实验主跑。
Kimi 与 Gemini 承担：

- 任务拆解
- venue / rebuttal / defense 方案
- experiment prioritization
- measured-data integration planning

---

## 立即生效的工作原则

1. **先做高 ROI 任务，再做 closeout 美化**
2. **可以为 reviewer 最强攻击点补实验**
3. **可以为 measured-data arrival 预留插入位**
4. **所有新任务都按“是否提升长期项目价值”排序**

---

## 新的四条主线

### Track A — Venue Diversification
- 目标：不把整篇论文绑死在 NC 单一路线
- 输出：
  - venue-fit matrix
  - title / abstract / cover letter 的多版本 framing
  - 如果转向更偏方法学或器件系统交叉 venue，最小改动路径

### Track B — High-ROI Supplementary Experiments
- 目标：利用空闲 GPU，补最能打 reviewer 的少量实验
- 典型候选：
  - Ensemble HAT vs per-forward i.i.d. D2D control
  - pure-digital ADC scan control
  - retention parameter sensitivity (`tau_1/tau_2`)
  - lightweight NL scan around the current boundary

### Track C — Measured-Data Integration Readiness
- 目标：博士数据一到即可接入，不临时慌乱
- 输出：
  - doctor-friendly request list
  - raw-data to profile mapping
  - manuscript insertion map
  - revision-ready measured-data package plan

### Track D — Long-Horizon Project Value
- 目标：这不是一次性投稿工程，而是长期平台项目
- 输出：
  - simulator + measured profile ecosystem
  - stronger measured-data case study path
  - future collaboration / device-paper bridge strategy

---

## 决策结果

### 接受
- reviewer-defense 文字硬化继续保留
- 允许新增必要实验
- 允许等待 measured data 再决定具体投稿窗口
- 允许多 venue 并行评估

### 不再默认
- 不再默认“立刻投 NC”
- 不再默认“禁止新增实验”
- 不再默认“submission package closeout 是唯一最高优先级”

---

## 对 Kimi / Gemini 的新要求

### Kimi
- 主做：
  - venue strategy
  - rebuttal / defense positioning
  - measured-data integration roadmap
  - experiment-to-reviewer-ROI ranking

### Gemini
- 主做：
  - high-ROI supplementary experiment slate
  - manuscript insertion map
  - venue-specific wording packs
  - measured-data arrival 后的文本结构重排方案

### Codex
- 只做：
  - review
  - accept / reject
  - source-of-truth sync
  - final patch / compile when needed

---

## 备注

这不是放弃 NC，而是把项目从“短跑投稿”切回“长线高价值推进”。
如果后续 measured data 很快到位，当前决策会被证明是高收益的。
