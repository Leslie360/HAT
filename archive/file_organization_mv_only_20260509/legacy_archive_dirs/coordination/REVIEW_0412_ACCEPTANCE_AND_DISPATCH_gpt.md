# 0412 外审意见接受与任务广播（Codex）

> 日期：2026-04-12  
> 输入文件：`report_md/审稿意见0412.md`  
> 目标：把 0412 外部审稿包压缩成可执行的 manuscript hardening / reviewer-defense 任务，不重新打开 GPU 主实验。

---

## 一句话判断

`0412` 这轮外审的主轴是正确的：**现在最需要的是把论文更稳地定位为 simulation-first methodology paper，并把若干“说得太硬”的结论降到证据能支撑的强度。**

我们**接受**其大部分写作与叙事层建议；  
我们**不接受**“因为缺乏实测闭环所以应等待再投”这种结论；  
我们**不重新打开**大规模 GPU 实验。

---

## Codex 接受的核心建议

### A1. 进一步前置 `simulation-only / behavioral-simulation` 定位

接受。

执行方向：
- 摘要第一句后更早地声明：
  - all results are obtained at the behavioral-simulation level
  - device parameters are literature-derived / proxy-calibrated
- 让这句话成为**方法定义**，而不是末尾免责声明

### A2. 继续软化 `NL=2.0` 的边界表述

接受。

执行方向：
- 不再把 `NL=2.0` 写成容易被误读为材料物理极限的句子
- 统一改成：
  - `under the present gradient-scaling surrogate`
  - `approximation boundary of the current training method`
  - `accuracy recovery is not demonstrated under the current surrogate`

### A3. 重新定义 `profile-driven` 贡献口径

接受。

执行方向：
- 不再把“interface 本身”说成核心创新
- 更稳的说法是：
  - unified organic-specific workflow
  - jointly modeling photoresponse, retention, and write nonlinearity
  - profile substitution as enabling infrastructure

### A4. 强化 Ensemble HAT 与 generic noise augmentation / domain randomization 的区分

接受。

执行方向：
- 明确：
  - D2D 是 fixed, spatially correlated mismatch map
  - standard HAT 的失败锚点是 fresh-instance collapse
  - Ensemble HAT 解决的是 unseen static arrays 的 transfer，而不是普通 i.i.d. robustness

### A5. 将 AIHWKIT 对照表述改成 `methodological consistency check`

接受。

执行方向：
- 不再把它写成 full validation / physical equivalence
- 明确这是共享机制下的数值一致性参照

### A6. 更明确地限定 C2C invariance 的适用区间

接受。

执行方向：
- 把 C2C 不敏感写成：
  - model-scoped / scale-masking-activated regime
  - not an unconditional device-law statement

### A7. 提升 `6-bit ADC cliff` 的摘要权重

接受。

执行方向：
- 作为最硬的系统结论之一更靠前出现
- 但仍保留 `simulator-scoped transition` 的限定

### A8. 强化 `favorable-stochastic-basin sensitivity` 的讨论价值

接受。

执行方向：
- 把 ConvNeXt 单 seed 与三 seed 聚合差异用作：
  - organic-specific deployment risk
  - training randomness × hardware randomness coupling

---

## Codex 不接受 / 暂不执行的建议

### R1. 不为 0412 重新打开新的 GPU 主实验

不接受新增：
- 新的 NL 扫描主实验
- 新的 large-scale baseline
- ImageNet 级别扩展
- 新的 broad numerical-equivalence sweeps

原因：
- 当前 submission 风险主要来自 wording / positioning / reviewer-defense，而不是主结果缺失
- 重新开实验会打乱已锁定 submission 状态

### R2. 不等待外部合作验证后再投稿

不接受。

原因：
- 当前论文的成立基础是 simulation-first methods contribution
- measured-device closure 是 revision / follow-up 增强项，不是投稿前置条件

### R3. 不把 “lack of fabricated hardware” 接受为当前稿件的否决理由

不接受。

原因：
- 稿件已经把范围界定为 behavioral-simulation methodology
- 0412 的有价值部分恰恰在于如何更稳地守住这个定位

---

## 立即执行的 manuscript hardening

### H1. 摘要 / 引言
- 更早声明 simulation-only
- 将 ADC 6-bit cliff 提升为更靠前的 deployment finding
- 将 profile-driven 改写为 `organic-specific workflow / enabling infrastructure`

### H2. Results / Discussion
- 把 AIHWKIT 改成 `consistency check`
- 将 C2C invariance 限定到 scale-masking 激活区间
- 更明确说明 Ensemble HAT 不等于普通 noise augmentation
- 把 ConvNeXt favorable-stochastic-basin sensitivity 提炼成方法学观察

### H3. Conclusion / Cover letter
- 继续统一 NL wording
- 继续避免 material-limit overclaim
- 更明确强调：
  - Ensemble HAT is the lead contribution
  - simulator/profile path is the enabling bridge

---

## Kimi 任务（新一轮）

### KX41: Proxy-Parameter Defense Pack [HIGH]
- 目标：直接防守 “proxy parameters undermine materials-to-system claims”
- 输出：
  - 最多 8 条
  - 每条包含：
    - `path:line`
    - `reviewer may say`
    - `defense`
    - `safer wording`
- 重点：
  - proxy ≠ arbitrary
  - sensitivity analyses already scope the conclusion
  - paper claims deployment risk ranking, not physical closure

### KX42: AIHWKIT Consistency-Check Defense Pack [HIGH]
- 目标：帮助 Codex 将 AIHWKIT 相关表述从 “validation” 调到 “consistency check”
- 输出：
  - 最多 6 条
  - 每条：
    - `path:line`
    - `current risk`
    - `replacement`
    - `why editorially safer`

### KX43: 0412 Reviewer-Defense Addendum [HIGH]
- 目标：给 cover letter / future rebuttal 准备一套回应包
- 重点：
  - simulation-only positioning
  - no fabricated-array closure yet
  - proxy/UQ skepticism
  - Ensemble HAT novelty boundary

### KX44: Submission Strategy Note on Measured Data [MED]
- 目标：统一口径，明确 measured data is revision-strengthening, not submission prerequisite
- 输出：
  - 1 页内 memo
  - 供 cover letter / author discussion 使用

---

## Gemini 任务（新一轮）

### GM-X24: Simulation-Only Front-Loading Pack [HIGH]
- 目标：把 simulation-only 定位进一步前置到摘要 / 引言 / cover letter
- 输出：
  - 最多 8 条
  - `path:line + exact replacement`

### GM-X25: Organic-Specific Contribution Reframing Pack [HIGH]
- 目标：把 `profile-driven interface` 从 generic interface 改写成 organic-specific joint workflow
- 输出：
  - 最多 8 条
  - `path:line + exact replacement`

### GM-X26: AIHWKIT Narrative Reframe Pack [HIGH]
- 目标：统一把 AIHWKIT 写成 consistency check，而非物理验证
- 输出：
  - 最多 6 条
  - `path:line + exact replacement`

### GM-X27: ADC-Cliff Emphasis Pack [MED]
- 目标：在不夸大的前提下，让 6-bit cliff 更像主发现
- 输出：
  - 最多 6 条
  - `path:line + exact replacement`

### GM-X28: Favorable-Stochastic-Basin Discussion Pack [MED]
- 目标：把 ConvNeXt 单 seed vs 三 seed 差异上升为更清楚的方法学观察
- 输出：
  - 最多 5 条
  - `path:line + exact replacement`

---

## Codex 自己的执行计划

### CX-C9
- 接收 0412 外审共识
- 生成广播
- 更新总板与协作文档

### CX-C10
- patch 主文：
  - abstract
  - introduction
  - results
  - discussion
  - conclusion
  - cover letter

### CX-C11
- 编译并检查：
  - `main.pdf`
  - `supplementary_main.pdf`
  - `cover_letter.pdf`

### CX-C12
- 审核 Kimi / Gemini 新回包
- 只吸收 source-grounded、low-risk、submission-facing 的改动

---

## 当前决策

**继续投稿推进，不等待真实器件数据，不重开 GPU 主实验。**  
`0412` 的价值在于：帮助我们把论文从“容易被误解为物理闭环主张”进一步收紧为“透明、强防守的 simulation-first methodology paper”。
