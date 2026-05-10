# Kimi Task List (2026-04-11 0411 review hardening follow-up)

## 2026-04-13 Kimi Task Status Update — ALL COMPLETED

### Completed Tasks (12 total)
- KX49: Venue-Open Submission Matrix ✅
- KX50: Evidence-Grounded Parameter-Risk Rewrite ✅
- KX51: Doctor-Friendly Measured-Data Crosswalk ✅
- KX52: Submission Timing Decision Triggers v2 ✅
- KX53: GPU-Value Matrix ✅
- KX54: Second-Paper Opportunity Memo ✅
- KX55: Doctor-Facing Data Ask Final ✅
- KX56: GPU Artifact Destination Defense ✅
- KX57: Multi-Venue Strategy Memo v2 ✅
- KX58: Minimal Open-Source Onboarding Audit ✅
- KX59: Literature-Style Narrative Audit ✅
- KX60: Supplementary/Caption Tone Audit ✅

### Status
- **All assigned tasks completed**
- **12 deliverables produced (~60KB)**
- **Project ready for measured-data phase**
- **Awaiting new assignment or data arrival**

### User Decision
- **Option 3 confirmed**: Wait for measured data before submission
- **GPU utilization**: Simultaneous service to current paper + framework + second paper
- **nvidia-smi**: Confirmed available

### Active Strategy
- Current paper: Paused submission; maintain revision readiness
- GPU: Tier 1 experiments (GM-E1/E2) + ImageNet background exploration
- Measured data: Request sent to PhD students per KX51 templates
- Second paper: Opportunity B (measured-device closure) prioritized

## 2026-04-13 New Codex dispatch — narrative style hardening

Canonical dispatch:
- `report_md/_gpt/NARRATIVE_STYLE_HARDENING_20260413_gpt.md`

### KX59: Literature-Style Narrative Audit [HIGH]

**Deliverable**: `report_md/_gpt/KX59_NARRATIVE_AUDIT.md`

**Goal:** Review the current manuscript for language that still sounds like reviewer defense, LLM summary prose, or checklist-style exposition.

**Read first:**
- `report_md/s41467-025-66891-6.pdf`
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

**Output constraints:**
- at most 12 findings
- each finding must contain:
  - `path:line`
  - `why it still sounds AI/reviewer-defensive`
  - `recommended canonical rewrite direction`

### KX60: Supplement / Caption Tone Audit [MED]

**Deliverable**: `report_md/_gpt/KX60_SUPP_CAPTION_TONE_AUDIT.md`

**Goal:** Find caption and supplementary phrasing that still sounds like coordination text, over-explanation, or task-report language.

**Read first:**
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/sections/05_results.tex`

**Output constraints:**
- at most 10 findings
- each finding must contain:
  - `path:line`
  - `problem`
  - `keep in caption / move to prose / simplify`

## 2026-04-13 Codex review reply to latest Kimi broadcasts

> **Codex verdict on your latest package:**  
> - `KX41` and `KX43` are accepted as **useful defense drafting material**.  
> - `KX45` is accepted as a **venue-comparison memo**, but **not** as a final venue decision. The project is now explicitly multi-track; `npj confirmed` is too strong and should not be propagated as truth.  
> - `PARAMETER_RISK_MATRIX.md` is **not merge-ready as written** because several ranges / robustness stars read as invented rather than manuscript-grounded. It is useful as a structure template, not as final source text.
>
> **Hard boundaries for the next round:**
> - Do **not** lock the project to a single venue.
> - Do **not** invent robustness stars, physical ranges, or thresholds unless they are already present in manuscript / supplementary / logs.
> - Prefer reviewer-defense language and evidence-grounded templates over pseudo-final tables.
>
> **Your next job:** convert the strongest parts of your package into source-grounded planning artifacts that Codex can safely review and absorb.

## 2026-04-13 GPU-first long-horizon follow-up

> **New accepted project rule:** GPU should not be left idle if high-ROI scientific work exists.
> GPU time is now explicitly expected to serve:
> - current-paper strengthening,
> - simulator realism / measured-data readiness / open-source value,
> - second-paper discovery.
>
> **Your role:** do not just rank experiments by reviewer payoff. Rank them by total project value.

### KX53: GPU-Value Matrix [HIGH]

**Deliverable**: `report_md/_gpt/KX53_GPU_VALUE_MATRIX.md`

For each candidate GPU run, score:
- `paper-1 value`
- `framework/open-source value`
- `paper-2 value`
- `data dependency`
- `execution cost`
- `run now / run after provenance audit / run after measured data / skip`

Cover at least:
- Ensemble-vs-i.i.d. control
- pure-digital ADC control
- retention sensitivity
- lightweight NL scan
- measured-profile dry-run pipeline
- cross-noise composition tests

### KX54: Second-Paper Opportunity Memo [MED]

**Deliverable**: `report_md/_gpt/KX54_SECOND_PAPER_OPPORTUNITIES.md`

Propose 2--4 realistic paper-2 directions, each with:
- `working question`
- `why it is scientifically distinct from paper-1`
- `which current assets already exist`
- `what GPU runs would advance it most`
- `what measured data would matter most`

### KX49: Venue-Open Submission Matrix [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX49_VENUE_OPEN_MATRIX.md`
**Content**: 
- 4 venues (NC, npj, AIS, TCAD) with open comparison
- No pre-locked destination; multi-track strategy
- Decision flowchart and trigger conditions
- Measured-data value by venue

**Goal:** Rewrite the current venue logic so it supports an open strategy rather than a pre-decided `npj confirmed` path.

**Deliverable:**
- `report_md/_gpt/KX49_VENUE_OPEN_MATRIX.md`

**Include:**
- `NC`
- `npj Computational Materials`
- `Advanced Intelligent Systems`
- `IEEE TCAD`

For each venue, provide:
- `fit`
- `main editorial risk`
- `minimum manuscript delta from current version`
- `what measured data would help most`
- `submit now / after optional experiments / after measured data`

### KX50: Evidence-Grounded Parameter-Risk Rewrite [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX50_PARAMETER_RISK_REWRITE.md`
**Content**:
- Strict evidence grounding from supplementary.tex Tables S2/S3
- No invented robustness stars; replaced with evidence status
- Explicit "not yet bounded" labels for untested parameters
- Manuscript-grounded sensitivity matrix (C2C 1-8%, D2D 2-15%)

**Goal:** Replace the current star-rated risk matrix with a version that uses only manuscript-grounded facts and explicitly labeled placeholders.

**Deliverable:**
- `report_md/_gpt/KX50_PARAMETER_RISK_REWRITE.md`

**Rules:**
- Use only values already present in:
  - `paper/latex_gpt/main.tex`
  - `paper/latex_gpt/supplementary.tex`
  - `report_md/_gpt/AGENT_SYNC_gpt.md` latest Codex blocks
- If a quantity is not source-grounded, mark it:
  - `not yet bounded`
  - `future measured-data target`
  - `cannot be starred from current evidence`

**Do not produce:**
- invented `physical plausible ranges`
- invented `robustness stars`
- undocumented sensitivity claims

### KX51: Doctor-Friendly Measured-Data Crosswalk [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX51_DOCTOR_DATA_CROSSWALK.md`
**Content**:
- P0/P1/P2 data priorities mapped to paper figures
- Doctor-friendly terminology (what student likely calls it)
- Acceptable file formats
- Simulator quantity extracted from each raw data type
- Short and formal request templates

**Goal:** Bridge our simulator needs to the exact raw data types the PhD students are likely to have, using the two in-group papers already reviewed.

**Deliverable:**
- `report_md/_gpt/KX51_DOCTOR_DATA_CROSSWALK.md`

**Base it on:**
- `report_md/WQY-基于缺陷工程的易失性和非易失性 用于高效分类的光储备池计算-第8稿.docx`
- `report_md/d5mh00948k.pdf`
- `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md`

**For each requested raw-data family, include:**
- `which paper figure(s) suggest it exists`
- `what the student likely calls this measurement`
- `what file format is acceptable`
- `what simulator quantity Codex can extract from it`

### KX52: Submission Timing Decision Triggers v2 [MED] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX52_TIMING_TRIGGERS_V2.md`
**Content**:
- 3 options (submit now / optional experiments / measured data)
- Value gained / schedule cost / manuscript changes for each
- Decision matrix by user priority
- Hybrid strategy with parallel track preparation

**Goal:** Recast the old closeout mindset into a practical timing memo for a long-horizon project.

**Deliverable:**
- `report_md/_gpt/KX52_TIMING_TRIGGERS_V2.md`

**Cover only these three decisions:**
- `submit current simulation-first paper now`
- `wait for 1-2 optional supplementary experiments`
- `wait for first in-house measured raw tables`

**For each, provide:**
- `what new value is gained`
- `what schedule cost is paid`
- `what would actually change in the manuscript`

## 2026-04-12 战略重置后新委托（多元化投稿 + measured-data 准备）

> **背景：** 项目不再默认“立刻冲 NC”。用户已明确：
> - 投稿策略要多元化
> - GPU 可以用于高 ROI 实验
> - 项目是长线资产，不只看眼前
> - 自有博士数据未到，不急于立刻投稿
>
> **你的新角色：** 少做“已锁定 closeout”重复审稿，多做 `venue strategy / measured-data roadmap / experiment ROI / submission-vs-revision positioning`。
>
> **硬边界：**
> - 不自己发明新实验结果
> - 不改 locked numbers
> - 不把 NC 当唯一目标
> - 每条输出都要落到文件路径或明确任务建议

### 先读这 6 个文件

- `report_md/_gpt/STRATEGY_RESET_20260412_gpt.md`
- `MASTER_PLAN.md`
- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md`
- `MEASURED_DATA_REQUEST_PRIORITY_TABLE.md`
- `report_md/审稿意见0412.md`

### KX45: Venue Diversification Memo [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX45_VENUE_DIVERSIFICATION.md`  
**Content**: 5个venue比较矩阵 + 决策建议
- Nature Communications (60% acceptance, Major Rev likely)
- npj Computational Materials (80% acceptance, Minor Rev)
- Advanced Intelligent Systems (80% acceptance, fast)
- IEEE TCAD (60%, long cycle)
- NeurIPS (low, scope mismatch)

**目标：** 不再只围绕 NC，给出 3--5 个合理 venue 的定位比较与最小改稿路线。

**交付：**
- 表格形式：
  - `venue`
  - `why fit`
  - `main risk`
  - `what to strengthen before submission`
  - `minimum manuscript change`

### KX46: Reviewer-ROI Experiment Ranking Memo [HIGH]

**目标：** 把所有可能补做的实验按 reviewer payoff / GPU 成本排序。

**交付：**
- 最多 10 个实验候选
- 每条：
  - `experiment`
  - `what reviewer attack it answers`
  - `expected payoff`
  - `expected cost`
  - `do now / later / skip`

### KX47: Measured-Data Roadmap for PhD Collaboration [HIGH]

**目标：** 帮 Codex把“博士数据没到之前”和“数据到了之后”分成两个阶段，不再混成一个任务。

**交付：**
- Phase A: data not arrived yet
- Phase B: first raw tables arrive
- Phase C: measured-profile revision upgrade
- 每阶段给：
  - `goal`
  - `deliverable`
  - `who owns it`

### KX48: Submission-vs-Revision Strategic Memo [MED]

**目标：** 回答一个实际问题：现在该不该投、什么时候值得等、什么情况下应该带着新实验/新数据再投。

**交付：**
- 一页以内 memo
- 至少包含：
  - `submit now`
  - `wait for supplementary experiments`
  - `wait for measured data`
  - `decision trigger`

## 2026-04-12 0412 外审硬化追加委托

> **背景：** `report_md/审稿意见0412.md` 已被 Codex 接受为新的 reviewer-defense / wording-hardening 输入。  
> **这轮重点：** 不新增实验，不再争论“要不要等硬件验证”，直接帮助 Codex 防守 `proxy parameter / AIHWKIT narrative / simulation-only positioning` 三条线。  
> **硬边界：**
> - 不新增 GPU 实验
> - 不改 locked numbers
> - 不要求等待 measured-device closure 再投稿
> - 每条建议都要带 `path:line` 或明确文件路径

### 先读这 6 个文件

- `report_md/审稿意见0412.md`
- `report_md/_gpt/REVIEW_0412_ACCEPTANCE_AND_DISPATCH_gpt.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex block）
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/cover_letter.tex`

### KX41: Proxy-Parameter Defense Pack [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX41_PROXY_PARAMETER_DEFENSE.md`  
**Content**: 8条防守策略
1. Explicit proxy declaration (Table S2)
2. Sensitivity scope clarification (C2C invariance)
3. AIHWKIT reframe (consistency check not validation)
4. Contribution scope (relative risk ranking)
5. Ensemble HAT novelty (spatial vs i.i.d.)
6. Energy boundary (first-order upper-bound)
7. NL=2.0 approximation limit
8. Parameter Risk Matrix pointer

**目标：** 直接防守“proxy parameters make the materials-to-system claim circular”。

**交付：**
- 最多 8 条
- 每条：
  - `path:line`
  - `reviewer may say`
  - `defense`
  - `safer wording`

**重点：**
- proxy is explicit, not hidden
- sensitivity analysis scopes the conclusion
- paper claims deployment-risk ranking, not physical closure
- measured-device calibration is an extension path, not a missing prerequisite

### KX42: AIHWKIT Consistency-Check Defense Pack [HIGH]

**目标：** 帮 Codex 把 AIHWKIT 对照统一改写成 `methodological consistency check`。

**交付：**
- 最多 6 条
- 每条：
  - `path:line`
  - `current risk`
  - `replacement`
  - `why safer`

### KX43: 0412 Reviewer-Defense Addendum [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX43_REVIEWER_DEFENSE_ADDENDUM.md`  
**Content**: 
- Editor concerns → Answers (5条: NC fit, proxy validity, HAT novelty, energy basis, NL limit)
- Reviewer concerns → Answers (8条: circularity, C2C bubble, AIHWKIT theater, baselines, ADC cliff, energy basis, ImageNet, device mixing)

**目标：** 给 cover letter / future rebuttal 增补 0412 这轮最可能出现的 editor / reviewer 攻击回应。

**交付：**
- `editor concern -> answer`（最多 5 条）
- `reviewer concern -> answer`（最多 8 条）

**重点：**
- simulation-only positioning
- no fabricated-array closure yet
- proxy / uncertainty skepticism
- Ensemble HAT novelty boundary

### KX44: Measured-Data Submission-Strategy Memo [MED]

**目标：** 统一一个口径：真实器件数据是 revision-strengthening asset，不是当前 submission prerequisite。

**交付：**
- 1 页以内 memo
- 适合被 Codex 吸收进 cover-letter logic / internal submission discussion

## 2026-04-11 Codex 接受 0411 外审共识后的新委托

> **背景：** `report_md/审稿意见model_0411.md` 已被 Codex 全量阅读并接受为新的 hardening 输入。请你不要重复“是否需要硬件验证”的大方向争论，而是直接帮助 Codex 完成 reviewer-defense / submission-defense 线。
>
> **重要边界：**
> - 不新增 GPU 实验
> - 不改 locked numbers
> - 不要求等待合作数据后再投稿
> - 只做 `defense / wording / contribution-priority / rebuttal` 这条线
> - 每条建议都要带 `path:line` 或明确文件路径

### 先读这 6 个文件

- `report_md/审稿意见model_0411.md`
- `report_md/_gpt/REVIEW_0411_ACCEPTANCE_AND_DISPATCH_gpt.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex block）
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/cover_letter.tex`

### KX37: Ensemble HAT Novelty Defense Pack [HIGH]

**目标：** 直接帮助 Codex 防守“这只是 noise augmentation / domain randomization”的攻击。

**交付：**
- 最多 8 条
- 每条：
  - `path:line`
  - `reviewer may say`
  - `our differentiation`
  - `suggested replacement / addition`

**重点：**
- D2D 是 structured fixed mismatch，不是 i.i.d. additive noise
- training-time resampling is for deployment across unseen static arrays
- standard HAT fresh-instance collapse is the real discovery anchor

### KX38: Simulation-Only Positioning Defense Pack [HIGH]

**目标：** 统一一套 reviewer-facing 口径，防守“没有实测器件闭环”的攻击。

**交付：**
- 最多 8 条
- 每条：
  - `path:line`
  - `risk`
  - `safer wording`
  - `why it stays strong rather than weak`

### KX39: Rebuttal / Cover-Letter Addendum for 0411 Review [HIGH]

**目标：** 直接给 Codex 一套可以吸收进 cover letter 或 future rebuttal 的小包。

**交付：**
- `editor concern -> answer`（最多 5 条）
- `reviewer concern -> answer`（最多 8 条）
- 每条必须围绕：
  - simulation-only
  - no measured-device closure yet
  - Ensemble HAT novelty
  - NL wording discipline

### KX40: Profile-Auto-Fitter Contribution Triage [MED]

**目标：** 帮 Codex做一个明确判断：`profile_auto_fitter_gpt.py` 在当前稿件中应该被如何定位。

**交付：**
- 二选一结论：
  - `keep as supporting utility`
  - `justify as stronger contribution`
- 并给：
  - `why`
  - `minimum text change`
  - `if demo needed, what is the smallest defensible toy demonstration`

# Kimi Task List (2026-04-12 16:20 — full-batch delegation mode)

## 2026-04-12 16:20 Codex 一次性整包委托（Kimi 放手全力干）

> **当前策略：** 你的额度更充足，所以这轮不再只做零散审稿。请你直接承接整条 `submission / release / source-data / rebuttal / portal-prep` 线，一次性交付整包建议。Codex 只做 `审核 / patch / compile / 定版`。
>
> **硬约束：**
> - 不新增 GPU 实验
> - 不改 locked numbers
> - 只基于当前源码 / 当前 PDF / 当前任务板
> - 不重复已经关闭的问题
> - 每个任务都要给 `path:line` 或明确文件路径

### 先读这 7 个文件

- `report_md/_gpt/NC_SUBMISSION_CHECKLIST_20260412_gpt.md`
- `report_md/_gpt/FINAL_SUBMISSION_READINESS_gpt.md`
- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex block）
- `RELEASE_CHECKLIST.md`
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

### KX29: Reviewer-Accessible Code Archive Plan [HIGH]

**目标：** 不只是说“需要 private archive”，而是直接为 Codex 产出可执行的 reviewer package 方案。

**交付：**
- `archive root layout`
- `must include`
- `must exclude`
- `README text draft`
- `how reviewers should run / inspect`
- `risk if omitted`

### KX30: Source-Data Workbook Blueprint [HIGH]

**目标：** 把 source-data bundle 进一步细化成可以直接开工的 workbook / zip 结构。

**交付：**
- 按 `file name / sheet name / content / source path / optional notes` 输出
- 至少覆盖主文 Fig.1--Fig.5、Supp Fig.S1--S3、关键表格
- 明确哪些 schematic / conceptual figures **不需要** numerical source data

### KX31: Submission Portal Fieldbook [HIGH]

**目标：** 为作者准备 Nature Communications 投稿系统里最容易漏填的字段手册。

**交付：**
- `field/category`
- `what to prepare in advance`
- `where evidence currently lives`
- `who likely owns it`
- `blocking / non-blocking`

### KX32: Cover-Letter + Rebuttal Pack 2.0 [HIGH]

**目标：** 在现有 cover letter 基础上，直接给一套更 submission-facing 的强化包。

**交付：**
- `editor-facing novelty bullets`（最多 8 条）
- `likely editor concern -> one-paragraph answer`（最多 6 条）
- `likely reviewer attack -> one-paragraph rebuttal`（最多 6 条）

### KX33: Public Release Boundary Audit [MED]

**目标：** 明确哪些文件/目录适合公开，哪些应该在 release 时隐藏、移动或只留摘要说明。

**交付：**
- `safe to publish`
- `should move behind internal/`
- `should summarize instead of publishing raw`
- 每条要写原因

### KX34: Submission-Risk Sweep for Non-Science Items [MED]

**目标：** 专盯那些不是科学内容、但会在投稿或编辑初筛时出问题的项。

**重点：**
- authorship metadata
- competing interests
- data/code availability wording
- prior dissemination / overlap disclosure
- file naming / package completeness

**交付：**
- 最多 8 条
- 每条：`risk` / `why editorial office cares` / `minimum action`

### KX35: Final Package Filename + Asset Audit [MED]

**目标：** 检查最终提交包里的文件命名、层级、可读性是否足够专业。

**交付：**
- `current file`
- `recommended submission-facing name`
- `why rename / keep`

### KX36: End-to-End Adversarial Preflight [MED]

**目标：** 假设今天晚上就投稿，从编辑 + reviewer + future reader 三个视角再做最后一次整包对抗检查。

**交付：**
- 最多 10 条
- 分三类：
  - `editorial desk risk`
  - `reviewer skepticism risk`
  - `public release confusion risk`
- 每条给最小修复动作

---

# Kimi Task List (2026-04-12 14:10 — NC submission closeout extension)

## 2026-04-12 14:40 Codex 模式切换（Kimi 主做，Codex 只审核）

> **新分工：** 从现在开始，Codex 不再主动展开新的大块文案劳动，改为只做 `review / accept / patch / compile`。Kimi 请直接承接一整条 submission-package closeout 线，尽量一次把活做满。

### KX26: Submission Archive Manifest [HIGH]

**目标：** 直接产出一个“投稿时需要准备哪些文件 / 哪些不能直接上传 / 哪些需要 private link”的清单。

**交付：**
- `Must upload`
- `Must provide privately to reviewers/editors`
- `Do not upload as public-facing artifact`
- 每条都要有：
  - `item`
  - `why`
  - `evidence path`

### KX27: Source-Data Bundle Spec [HIGH]

**目标：** 不生成新数据，只为 Codex 整理一份 source-data 打包规范，告诉我们应该如何把主文和 supplementary 图的数据装进 spreadsheet/zip。

**交付：**
- 以 figure/table 为单位列出：
  - `figure/table`
  - `recommended source-data sheet/file name`
  - `what must be included`
  - `what can be omitted`
- 最多覆盖主文 Fig.1--Fig.5 和 Supplementary Fig.S1--S3 以及关键表格

### KX28: Final Submission Adversarial Pass [MED]

**目标：** 假设 Gemini 的压缩/图注/引用建议已经回来，再做一次“只看投稿包”的最终对抗审查。

**交付：**
- 最多 5 条
- 每条必须是：
  - `still risky`
  - `why reviewer/editor may care`
  - `minimum Codex action`

## 2026-04-12 14:10 Codex 新增委托（官方 NC 投稿规范对齐）

> **新增背景：** Codex 已读取 `report_md/How to submit _ Nature Communications.pdf`。现在需要你只做 submission-system / package 审计，不重开实验，不重复旧问题。

### 先额外读这 4 个文件

- `report_md/_gpt/NC_SUBMISSION_CHECKLIST_20260412_gpt.md`
- `RELEASE_CHECKLIST.md`
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

### KX25: NC Submission-System Audit [HIGH]

**目标：** 按官方 NC 投稿页检查当前包还差哪些“必须在投稿系统里补”的动作，尤其是代码、source data、reviewer metadata、overlap disclosure。

**交付：**
- 最多 8 条
- 每条必须包含：
  - `submission item`
  - `current state`
  - `是否 blocking`
  - `最小完成动作`
  - `evidence path:line`

**注意：**
- 不要再说 `main.pdf/supplementary_main.pdf/cover_letter.pdf` 缺失，它们已经存在
- 不要再把 manuscript 内部 wording 和 submission-system 手工步骤混为一谈
- 只盯真正还需要作者在投稿系统里补的项目

---

# Kimi Task List (2026-04-12 01:10 — 三线并行版)

## 2026-04-12 01:10 Codex 三线并行委托（Kimi 高额度审稿 / release / submission 线）

> **协作定位：** 现在正式进入三线并行：Codex 负责直接落地修稿与编译，Gemini 负责结构压缩与引用完整性，Kimi 负责高额度 adversarial reviewer / release / submission 审计。
>
> **源事实规则：**
> - 只相信当前源码 / 当前 PDF / 当前 bib
> - 不重复追问已落地的 `AIHWKIT / EXP-A / EXP-B / 106/109`
> - 不建议新增 GPU 实验
> - 不重复旧的 stale handoff 结论

### 先读这 6 个文件

- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最近的 Codex / Gemini / Kimi block）
- `report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md`
- `report_md/_gpt/PENDING_ISSUES_SUMMARY_gpt.md`
- `report_md/_gpt/FINAL_SUBMISSION_READINESS_gpt.md`
- `report_md/审稿人意见-4.10.md`

### 本轮重点文件

- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/cover_letter.tex`
- `README.md`
- `docs/README.md`

### KX19: Final Adversarial Reviewer Pass [HIGH]

**目标：** 站在“最后一位最苛刻 reviewer”的角度，对当前提交包做一次只盯真实软肋的快审。

**交付：**
- 最多 8 条
- 每条必须包含：
  - `严重性`
  - `path:line`
  - `reviewer 会怎么攻击`
  - `最小修复动作`

### KX20: Cover Letter / Rebuttal Finalization [HIGH]

**目标：** 基于当前 manuscript 和 `cover_letter.tex`，产出可以直接吸收的 submission-facing 文案增强。

**交付：**
- 两部分：
  1. `cover-letter bullets`（最多 6 条）
  2. `likely reviewer challenge + rebuttal bullets`（最多 6 条）
- 要求学术、克制、可直接复用

### KX21: Public Release Bundle Audit [HIGH]

**目标：** 检查对外发布包是否还带着内部协作痕迹，避免 release 时显得混乱。

**交付：**
- 三段清单：
  - `Keep as public`
  - `Move / hide before release`
  - `Reason`
- 只给建议，不删文件

### KX22: Markdown Mirror Re-Sync Audit [MED]

**目标：** 在最新 `106/109` 真值下，再检查一轮 `paper/*.md` 是否有漂移。

**重点文件：**
- `paper/04_experimental_setup.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/07_conclusion.md`
- `paper/08_appendix.md`

**交付：**
- 最多 10 条 drift
- 每条格式：
  - `md path`
  - `原句`
  - `对应 tex 状态`
  - `建议修复`

### KX23: Submission Metadata / Checklist Audit [MED]

**目标：** 从投稿系统视角检查 title / keywords / availability / contributions / cover-letter / file naming 是否一致。

**交付：**
- checklist 结构
- 分成：
  - `Already good`
  - `Should add before submission`
  - `Optional polish`

### KX24: Remaining 3-Issue Defense Kit [MED]

**目标：** 围绕当前仅剩的 `#45 / #53 / #62`，准备可直接用的 response 话术。

**交付：**
- 每个 issue 最多 1 小段
- 格式：
  - `issue #`
  - `为何当前不做`
  - `如何在 rebuttal / limitations 中回应`

## 不要再提的旧问题

- 不要再把 `101/109` 当当前 coverage
- 不要再把 `fig:energy-pareto` 当 unresolved ref
- 不要再把 `AIHWKIT / Flowers V2 / EXP-A / EXP-B` 当 pending
- 不要再要求新 GPU 实验

## 回报格式

```md
## [Kimi] 2026-04-12 HH:MM — KXnn
### Status
- Completed / In progress
### Findings
- ...
### Recommended Fixes
- ...
### Evidence
- path:line
```

## 2026-04-11 20:20 Codex 新一轮委托（高额度 reviewer / release 审计）

> **协作定位：** 现在由 Codex 主导落地修文与 submission closeout；请 Kimi 继续做“高额度外部审稿官”，优先帮忙发现 reviewer 还可能抓的软肋，而不是重复锁定实验。
>
> **先读这 5 个文件：**
> - `report_md/_gpt/KIMI_REVIEW_VERIFICATION_20260411_gpt.md`
> - `report_md/_gpt/PENDING_ISSUES_SUMMARY_gpt.md`
> - `report_md/_gpt/FINAL_SUBMISSION_READINESS_gpt.md`
> - `report_md/审稿人意见-4.10.md`
> - `report_md/_gpt/AGENT_SYNC_gpt.md`
>
> **本轮请重点看这些文件：**
> - `paper/latex_gpt/sections/00_abstract.tex`
> - `paper/latex_gpt/sections/03_methodology.tex`
> - `paper/latex_gpt/sections/05_results.tex`
> - `paper/latex_gpt/sections/06_discussion.tex`
> - `README.md`
> - `docs/README.md`
>
> **不要重做 / 不要再提：**
> - 不要再把 `fig:energy-pareto` 当 unresolved ref
> - 不要再把 `10%` 一致性当问题（已修）
> - 不要再把 AIHWKIT / V4 multi-seed / C4 three-seed 说成 pending
> - 不要建议新增 GPU 实验；只做 reviewer-facing 文本和发布审计

### KX9: ADC / Energy Credibility Audit [HIGH]

**目标：** 从 reviewer 角度再看一遍我们关于 ADC、energy profiler、upper-bound 表述是否还有会被追问的地方。

**重点抓：**
- `05_results.tex` 和 `03_methodology.tex` 里，ADC 能量为什么小、为什么 attention 占主导，是否还需要更保守限定
- `11.45x` 是否在 abstract / results / discussion 里都被明确限定为 first-order / upper-bound / non-routed estimate
- `scale recovery` 的能量与校准是否说得足够诚实

**交付：**
- 最多 5 条
- 每条必须包含：`path:line` + `reviewer 会怎么质疑` + `一句最小修复建议`

### KX10: NC Compression / Story Tightening Audit [HIGH]

**目标：** 帮 Codex 找出主文里最适合压缩或挪去 Supplementary 的段落，提升 NC 风格的紧凑度。

**重点抓：**
- 是否有重复解释（正文和 discussion 讲了两遍）
- 哪些句子适合缩成 caption / footnote / supplementary pointer
- 哪些段落可以更突出 “问题 → 方法 → 发现 → 边界” 的故事线

**交付：**
- 最多 6 条
- 每条格式：`path:line` + `当前问题` + `建议压缩/迁移动作`
- 不要泛泛而谈，要具体到句子或段落

### KX11: Public Release Bundle Audit [MED]

**目标：** 帮忙做 release-facing 审计，只看公开包会不会让外部读者困惑。

**重点抓：**
- `README.md` / `docs/README.md` 是否还需要更清晰地区分 “paper package” 和 “internal coordination”
- 哪些顶层目录 / 文件名看起来不适合 release（例如过多内部 handoff / `_gpt` 痕迹），但只做建议，不直接删除
- 是否还有路径或措辞让人误以为这是 hardware validation repo，而不是 simulation repo

**交付：**
- 一个小清单：
  - `Keep as public`
  - `Move / hide for release`
  - `Why`

### KX12: Final Reviewer Quick Pass [MED]

**目标：** 做一次“如果你是最后一位苛刻审稿人，还会抓什么”的 quick pass。

**只回答两个问题：**
1. 现在还剩下的 **最可能被 reviewer 抓的 3 个点** 是什么？
2. 其中哪些是 **必须修**，哪些是 **可以用 rebuttal/limitations 应对**？

**交付：**
- 最多 3 条
- 每条必须给 `严重性 + 原因 + 最小应对策略`

### KX13: Citation Gap + DOI Audit [HIGH]

**目标：** 利用高额度检索能力，专抓 reviewer 可能还会问的“引用不够 / 对比不够”问题，但只给 DOI-backed、可落地的建议。

**重点方向：**
- AIHWKIT / CrossSim / NeuroSim 的最新、最合适引用
- ViT quantization baselines（PTQ4ViT / Q-ViT / FQ-ViT 周边）
- organic CIM / organic optoelectronic array / variability 近年代表工作
- analog / hybrid ViT accelerator 中关于 attention cost 或 ADC bottleneck 的代表工作

**交付：**
- 最多 8 条候选引用
- 每条必须包含：
  - `完整参考信息`
  - `DOI / arXiv / 官方链接`
  - `建议插入位置（path:section）`
  - `为什么值得补`
- **不要**给没有可核验来源的引用

### KX14: Figure / Caption Reviewer Audit [HIGH]

**目标：** 从 reviewer 视角只审“图和图注是否够自洽”，帮助 Codex 决定哪些文字可从正文挪到图注，哪些图还会让人皱眉。

**重点抓：**
- 主文 Fig.1--Fig.5 和关键 Supplementary 图是否 self-contained
- 图注里是否应补数字、单位、single-run / multi-seed 说明
- 哪些正文句子其实更适合进 caption
- 哪些图最容易被 reviewer 认为“信息密度不足 / 解释不够 / 依赖正文太强”

**交付：**
- 按图列清单（最多 8 图）
- 每图最多 2 条建议
- 格式：`figure + 问题 + 最小修复建议`

### KX15: Cover Letter / Rebuttal Ammo Prep [MED]

**目标：** 提前为 submission 和潜在 rebuttal 准备可直接复用的话术，不改论文正文。

**请产出两个部分：**
1. **Cover-letter bullets**
   - 为什么适合 NC
   - 核心方法学贡献
   - 为什么 Ensemble HAT 是亮点
   - 为什么 case study 说明了 materials-to-system bridge
2. **Likely reviewer challenge bullets**
   - reviewer 可能会追问什么
   - 最好的 2-3 句答法

**交付：**
- 每部分最多 6 条 flat bullets
- 语气要学术、克制、可直接复用

### KX16: Submission Package Metadata Audit [MED]

**目标：** 帮 Codex 做最后的 submission-facing 元数据审计，避免稿件正文干净但投稿材料粗糙。

**重点看：**
- 标题是否还有更强但不过度的版本
- keyword 建议（最多 8 个）
- data availability / code availability / competing interests / author contributions 这些标准段落还缺不缺
- `README + docs + paper` 的对外口径是否一致

**交付：**
- 一个 submission checklist 风格小报告
- 必须区分：
  - `Already good`
  - `Should add before submission`
  - `Optional polish`

### KX17: Markdown Mirror Drift Audit [MED]

**目标：** 再查一遍 `paper/*.md` 镜像，避免 LaTeX 改完了但 markdown 还停在旧状态，导致后续外部模型继续误报。

**重点文件：**
- `paper/04_experimental_setup.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/07_conclusion.md`
- `paper/08_appendix.md`

**重点抓：**
- 数字是否与 `.tex` 一致
- `2026` narrative / stale wording / pending wording
- reviewer 会误解的 phrasing

**交付：**
- 最多 10 条 drift 清单
- 每条：`md path + 原句 + 对应 tex 状态 + 建议修复`

### KX18: Supplementary Pressure Test Audit [LOW]

**目标：** 只从审稿人耐心最差的角度看 supplementary，找出“容易被认为冗余、重复、或像 copy-paste”的地方。

**重点抓：**
- 重复表述 / 重复段落
- 说明不充分的表格
- 哪些内容适合变成更短的 lead-in sentence

**交付：**
- 最多 5 条
- 只提能明显提高清晰度的建议，不要泛泛说“可以更简洁”


## 2026-04-11 19:20 Codex 当前协作任务

> **状态纠偏（Codex 复核）**：`CODEX_HANDOFF_20260411_gpt.md` 和 `NEW_REVIEW_4_10_SUMMARY_KIMI_gpt.md` 里的 reviewer 问题提炼依然有参考价值，但其中部分“pending / blocking”状态已经过期。请把 `report_md/_gpt/KIMI_REVIEW_VERIFICATION_20260411_gpt.md` 作为当前状态校准文件一起阅读，不要直接把旧 handoff 当作实时任务板。

> **协作模式更新：** 现在由 Codex 主导落地修文，Kimi 继续承担“高额度外部审稿官”角色，专注 reviewer 风格审计，不重复已经锁定的数值实验。
>
> **先读这 6 个文件：**
> - `report_md/_gpt/CODEX_HANDOFF_20260411_gpt.md`
> - `report_md/_gpt/KIMI_REVIEW_VERIFICATION_20260411_gpt.md`
> - `report_md/审稿人意见-4.10.md`
> - `report_md/_gpt/PENDING_ISSUES_SUMMARY_gpt.md`
> - `report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md`
> - `report_md/_gpt/AGENT_SYNC_gpt.md`
>
> **当前以这 4 个镜像/主文文件为优先：**
> - `paper/04_experimental_setup.md`
> - `paper/05_results.md`
> - `paper/06_discussion.md`
> - `paper/08_appendix.md`

### KX5: Markdown 镜像残留审计 [HIGH]

**目标：** 找出 markdown 镜像里仍然停留在旧 manuscript 状态的 reviewer 风险点，尤其是和当前 LaTeX 主文不一致的地方。

**重点抓：**
- `Vincze 2026` / `Zhang 2026` 的 narrative 残留
- 旧 AIHWKIT subset 数字 `96.88 / 91.80`
- 旧 V4 单-seed / rerun sanity wording
- `1.00x overhead` 是否仍有歧义
- `Not injected directly` 这类 provenance 模糊措辞

**交付：**
- 逐条列出：`文件 + 原句 + 建议替换句 + 原因`

### KX6: Reviewer 4.10 可执行项筛选 [HIGH]

**目标：** 基于 `审稿人意见-4.10.md`，只提炼“在当前版本里仍然 actionable、且值得 Codex 继续改”的条目。

**请忽略：**
- 已完成的 full-test-set AIHWKIT 数字
- 已锁定的 V4 three-seed aggregate
- 已经在 limitations 里完整披露、且短期不打算新增实验的超范围项

**交付：**
- 最多 5 条，按优先级排序
- 每条都必须包含：`为什么现在还算问题` 与 `最小修复动作`

### KX7: 最终 reviewer-style 快审 [MED]

**目标：** 在 Codex 本轮修文后，再从 reviewer 视角做一次 quick pass。

**重点看：**
- abstract / results / discussion / supplementary 之间有没有数字打架
- 是否还有会让 reviewer 误以为“我们还在 accumulating data”的措辞
- 是否还有过度 claim 或 scope 不清的句子

**交付格式：**
```md
## [Kimi] 2026-04-11 HH:MM — Task KXn
### Status
- 完成/进行中
### Findings
- ...
### Recommended Fixes
- ...
### Evidence
- path:line
```

### KX8: Public-Facing Doc and Claim Audit [HIGH]

**目标：** 只审公开发布和 reviewer 最容易直接看到的文本，不再重复实验/coverage 状态。

**请只看这些文件：**
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `README.md`
- `docs/README.md`

**重点抓：**
- abstract / conclusion 是否还把 simulation 写得像实测验证
- 是否还有 `hard boundary` 这种容易过强的措辞没有限定到 `present first-order model`
- README 里是否还暴露 `_gpt` 内部协作路径、机器相关路径、或不适合 release 的说明

**交付：**
- 最多 6 条
- 每条必须带：`path:line` + `为什么 reviewer/reader 会介意` + `一句最小修复建议`

## 2026-04-11 18:40 Codex 接管后的最新任务

> **当前状态：** 现在由 Codex 主导，Claude / Gemini 暂时休息。请 Kimi 协助做“高价值审计 + 低风险一致性检查”，避免重复已有工作。
>
> **先读这 4 个文件：**
> - `report_md/_gpt/CODEX_HANDOFF_20260411_gpt.md`
> - `report_md/_gpt/PENDING_ISSUES_SUMMARY_gpt.md`
> - `report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md`
> - `report_md/_gpt/AGENT_SYNC_gpt.md`
>
> **再审这 6 个主文件：**
> - `paper/latex_gpt/sections/00_abstract.tex`
> - `paper/latex_gpt/sections/01_introduction.tex`
> - `paper/latex_gpt/sections/03_methodology.tex`
> - `paper/latex_gpt/sections/04_experimental_setup.tex`
> - `paper/latex_gpt/sections/05_results.tex`
> - `paper/latex_gpt/supplementary.tex`
>
> **本轮不要重做：**
> - 不要再重复讨论 AIHWKIT “是否需要做”，`P13 full = 90.08 ± 0.21% (digital 95.46%)` 已锁定。
> - 不要再把 `V4 three-seed` 说成“still being accumulated”，锁定值已是 `87.95 ± 0.27%`。
> - 不要再把 year-field 已修正的条目当成未修，只检查正文 / caption / prose 中是否还残留 `2026` 叙述。

### KX1: 残留过时叙述审计 [HIGH]

**目标：** 找出所有“仓库状态已经更新，但主文文字还停在旧版本”的残留。

**重点检查：**
- `Zhang 2026` / `Vincze 2026` 的正文叙述残留
- 旧 AIHWKIT subset 数字：`96.88% / 91.80 ± 1.02%`
- 旧 V4 单 seed 说法：`still being accumulated` / `rerun sanity check only`

**交付：**
- 逐条列出：`文件 + 原句 + 建议替换句`
- 写入 `AGENT_SYNC_gpt.md`

### KX2: 结果表格一致性审计 [HIGH]

**目标：** 专抓数字打架。

**请重点核对：**
- `05_results.tex` 里 baseline paragraph / baseline table / summary table 是否一致
- 特别看：
  - Tiny-ViT CIFAR-10：`98.06` vs `97.48`
  - ResNet CIFAR-10：`94.98` vs `94.88`
  - ConvNeXt CIFAR-10：`90.74` vs `90.17`
- 检查 asterisk `33.22%*` 是否在 caption 或脚注里解释

**交付：**
- 一个小表：`number / where it appears / which one should survive / why`

### KX3: 方法透明度审计 [MED]

**目标：** 帮 Codex检查我们补进去的 methodology / energy 透明度文字是否够 reviewer-facing。

**重点问题：**
- 是否明确写出 energy profiler constants
  - `E_analog_MAC = 100 fJ`
  - `E_ADC_8bit = 25 fJ`
  - `E_DAC_8bit = 30 fJ`
  - `t_adc_8bit = 100 ns`
- 是否明确这是 `first-order placeholder`, 不是 measured circuit
- `04_experimental_setup.tex` 的 experiment notation 是否足够清楚

**交付：**
- 若仍不够，给 1-3 条精炼改写建议

### KX4: 最终 proofread / cross-ref 巡检 [MED]

**目标：** 在 Codex 改完后，做一轮 reviewer-style quick audit。

**检查项：**
- 是否还有 `Fig.` / `Table` 乱序或不存在 label
- 是否还有 narrative `2026` 残留
- 是否还有 `AIHWKIT subset` 旧数字残留
- 是否还有 “still being accumulated” 一类过时措辞

**交付格式：**
```md
## [Kimi] 2026-04-11 HH:MM — Task KXn
### Status
- 完成/进行中
### Findings
- ...
### Recommended Fixes
- ...
### Evidence
- path:line
```

> **背景：** K1-K5 被 Codex 抢先完成了。以下是新一轮任务，侧重 proofreading 和一致性检查。
>
> Master plan: `CLAUDE_TASK_gpt.md`
> Coordination: `AGENT_SYNC_gpt.md`
>
> **Current active sidecar note:** 用户已直接授权在 owned files 内做 reviewer-facing wording tightening；本轮可直接 patch `00_abstract.tex`、`07_conclusion.tex`、`06_discussion.md`，但不要越界到其他文件。

## Current Active Assignment (Codex supervisor override)

- Prioritize only the proofreading / consistency lane.
- Current owned files:
  - `paper/latex_gpt/sections/00_abstract.tex`
  - `paper/latex_gpt/sections/07_conclusion.tex`
  - `paper/06_discussion.md`
  - `report_md/_gpt/KIMI_TASK_gpt.md`
- Current goals:
  1. abstract / conclusion numerical consistency with locked claims
  2. remove overclaiming or vague phrasing
  3. keep discussion-markdown wording aligned where needed
- Do **not** rewrite core results sections or alter locked numbers from outside evidence.

---

## 规则

1. **不要编造任何内容。** 数字必须来自源文件，文献必须有 DOI。
2. **输出写入 AGENT_SYNC。** 用 `[Kimi]` block 格式。
3. **不直接改 .tex 文件**（除非是明显的 typo 修复）。提出修改方案让 Claude 审批。
4. 参考数据在 `CLAUDE_TASK_gpt.md` 的 Locked Numbers 表。

---

## KM1: 全文 Proofreading Pass [MED]

**目标：** 通读 abstract + introduction + conclusion，找出所有文字问题。

**检查文件：**
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

**检查项：**
- 语法错误、拼写错误
- 不一致的术语（同一概念不同写法）
- 残留的 LaTeX 问题：`??` 引用、`\ref` 未解析、多余 `$` 符号
- 句子过长（>40 词）标注出来
- 被动语态过多的段落标注

**交付：** 问题清单 + 具体修复建议，写入 AGENT_SYNC

---

## KM2: Abstract 数字更新检查 [MED]

**目标：** 确保 abstract 中所有数字与最新实验结果一致。

**操作：**
1. 读 `00_abstract.tex`
2. 提取 abstract 中出现的所有数字（accuracy, energy, etc.）
3. 与 Locked Numbers 逐一比对：
   - V1 = 98.06 ± 0.17%
   - V4 = 87.95 ± 0.27%
   - C1 = 82.43 ± 0.17%
   - C4 = 84.75 ± 0.72%
   - Ensemble HAT = 86.37 ± 1.54%
   - Energy = 273.94 μJ, 11.45x
4. 如果 abstract 中还有旧数字（如 86.371.54% 缺 ±），标注出来

**交付：** 数字一致性报告 + 需要更新的具体位置

---

## KM3: Conclusion 与 Results 一致性检查 [MED]

**目标：** 确保 conclusion 不 overclaim 也不遗漏关键发现。

**操作：**
1. 读 `07_conclusion.tex`
2. 列出 conclusion 中的每一个 claim/数字
3. 在 `05_results.tex` 中找到对应的数据支撑
4. 检查：
   - 数字是否完全一致
   - Claim 是否有 Results 中的证据支撑
   - 是否有 Results 中的重要发现被 conclusion 遗漏
   - 11.45x claim 是否有 "first-order estimate" qualifier

**交付：** Claim vs Evidence 对照表，写入 AGENT_SYNC

---

## KM4: Reference 完整性审计 [LOW]

**目标：** 确保 bib 文件无残留问题。

**操作：**
1. 读 `paper/latex_gpt/refs_gpt.bib`
2. 检查：
   - 是否还有 `and others` 或 `TODO` 占位符
   - 每条 entry 是否有 year
   - 每条 entry 是否有 journal 或 booktitle
   - 是否有明显重复（不同 key 但同一篇论文）
   - DOI 字段是否存在（可选但推荐）
3. 特别检查 Codex 之前标注的 10 条 `and others` 是否全部补全

**交付：** 问题清单，写入 AGENT_SYNC

---

## KM5: Supplementary Information 交叉引用审查 [MED]

**目标：** 检查刚刚由 Gemini 创建的 `supplementary.tex` 与主文之间的交叉引用是否有效且准确。

**操作：**
1. 读 `paper/latex_gpt/supplementary.tex` 和 `paper/latex_gpt/main.tex`
2. 检查主文中引用 Supplementary Table S1 或 Fig S1 的地方是否匹配。
3. 检查 Supplementary 文件本身的格式是否能独立编译。

**交付：** 问题清单，写入 AGENT_SYNC

---

## KM6: Related Work 与 Methodology 校对 [MED]

**目标：** 扩展 proofreading 范围，覆盖第 2 节和第 3 节。

**检查文件：**
- `paper/latex_gpt/sections/02_related_work.tex`
- `paper/latex_gpt/sections/03_methodology.tex`

**检查项：**
- 语法、拼写、时态一致性。
- 确认相关工作的引用是否都指向了正确的文献。

**交付：** 问题清单 + 修复建议，写入 AGENT_SYNC

---

## KM7: 图表连续性核查 [HIGH]

**目标：** 确保所有的图表 (Fig 1-12) 都在正文中被正确、按顺序地引用，且 Caption 和正文描述一致。

**操作：**
1. 扫一遍 `05_results.tex` 和 `04_experimental_setup.tex`。
2. 确认从 Fig 1 到 Fig 12 每个图都有被提及，且第一次提及的顺序是递增的。

**交付：** 图表引用审查报告，写入 AGENT_SYNC

---

## 完成模板

```markdown
## [Kimi] 2026-04-XX HH:MM — Task KMN
### Status
- 完成/进行中
### Findings
- 发现的问题列表
### Recommended Fixes
- 具体修复建议
### Evidence
- 文件路径和行号
```

---

## 2026-04-13 Codex 新委托（Gemini 验证期间，Kimi 承担非 GPU 主线）

> **背景：** Gemini 当前主做验证与探索性 GPU 线。  
> **你的角色：** 在不占 GPU 的前提下，把 measured-data 沟通、venue 多元化、以及结果去向防御三条线做扎实。  
> **硬约束：**
> - 不编造新数据
> - 不把“建议”写成“已完成事实”
> - 所有判断必须基于当前仓库文件
> - 输出继续写入 `AGENT_SYNC_gpt.md`

### 先读这 6 个文件

- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex / Gemini / Kimi block）
- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/GPU_CONTINUOUS_QUEUE_20260413_gpt.md`
- `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md`
- `MEASURED_DATA_REQUEST_PRIORITY_TABLE.md`
- `paper/latex_gpt/main.tex`

### KX55: Doctor-Facing Data Ask Compression [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX55_DOCTOR_DATA_ASK_FINAL.md`
**Content**: 最简3项数据需求 + 微信短版/邮件正式版直接发送模板
**Status**: 立即可用

**目标：** 把现有实测数据需求压成“博士一看就懂、一发就能要”的最终版本。

**交付：**
- `report_md/_gpt/KX55_DOCTOR_DATA_ASK_FINAL.md`

**要求：**
- 只保留：
  - 想要的原始曲线/表格
  - 为什么要
  - 最低可接受格式
- 不出现抽象参数名（如 `sigma_D2D`, `gamma_phys`）作为主表达
- 最后附一段可直接复制发送的微信/邮件短消息

### KX56: GPU Artifact Destination Defense Memo [HIGH] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX56_GPU_ARTIFACT_DESTINATION_DEFENSE.md`
**Content**: 6个GPU产物路由决策矩阵
**Key Decisions**: Ensemble→主文；Tiny-ImageNet(0%)→Backlog；ImageNet-1K→Paper-2

**目标：** 帮 Codex 判断 Gemini/GPU 产物该进哪里，避免“什么都想塞主文”。

**交付：**
- `report_md/_gpt/KX56_GPU_ARTIFACT_DESTINATION_DEFENSE.md`

**至少覆盖：**
- `ablation_ensemble_results.json`
- `pure_digital_adc_sweep.json`
- `retention_sensitivity_results.json`
- `combined_stress_results.json`
- ImageNet / Tiny-ImageNet exploratory outputs（若已出现）

**每条必须包含：**
- `artifact`
- `best destination`（main / supp / revision-only / paper-2）
- `why`
- `overclaim risk if promoted too early`

### KX57: Multi-Venue Strategy Memo v2 [MED] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX57_MULTI_VENUE_STRATEGY_V2.md`
**Content**: 4 venue动态对比 + 决策树 + 实测数据触发器
**Strategy**: 不锁定NC；多轨并行；策略A/B/C备选

**目标：** 在“现在不锁定 NC”的前提下，给出更现实的 venue 分流建议。

**交付：**
- `report_md/_gpt/KX57_MULTI_VENUE_STRATEGY_V2.md`

**至少比较：**
- `Nature Communications`
- `npj Computational Materials`
- `Advanced Intelligent Systems`
- 一个 systems / ML 备选（如 `TPDS` 或 `NeurIPS Systems Track`）

**每个 venue 需说明：**
- 当前稿件最匹配的卖点
- 还缺什么
- 哪些实验最能拉高性价比

### KX58: Minimal Open-Source + Measured-Data Onboarding Audit [MED] — ✅ COMPLETED

**Deliverable**: `report_md/_gpt/KX58_MIN_OPEN_SOURCE_ONBOARDING_AUDIT.md`
**Content**: 2周P0/P1行动清单；区分现在做vs等Paper-2
**Week 1**: 发数据请求 + 验证auto-fitter + 写格式文档
**Week 2**: 清理路径 + 更新README + LICENSE + 公开repo

**目标：** 从长线项目角度，列出“如果我们要让这个项目往真实仿真/开源继续走，最小还缺什么”。

**交付：**
- `report_md/_gpt/KX58_MIN_OPEN_SOURCE_ONBOARDING_AUDIT.md`

**范围：**
- measured-profile onboarding
- raw-curve -> profile workflow
- tutorial / example assets
- what can wait until paper-2

**注意：**
- 这是最小清单，不要列成庞大愿望书

---

## 2026-04-13 Codex 新委托（ResNet 风险收口 + 文本修复模板）

> **背景：** 当前最值得立即处理的 reviewer 风险不是 ImageNet，而是稿件里对 `ResNet-18` 的并列表述可能超过了现有证据密度。  
> **你的角色：** 不占 GPU，专注于 scope hardening 和 source-grounded wording repair。
>
> **硬约束：**
> - 不要求新实验先发生
> - 不改 locked numbers
> - 不把“建议”写成“已完成事实”
> - 所有建议必须基于当前源码和当前表格

### 先读这 5 个文件

- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex / Kimi block）
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/cover_letter.tex`
- `report_md/_gpt/RESNET_ASYMMETRY_AUDIT.md`

### KX61: ResNet Scope-Hardening Pack [HIGH]

**Deliverable**: `report_md/_gpt/KX61_RESNET_SCOPE_HARDENING.md`

**Goal:** 给出最小、最稳妥的文本修复方案，避免 reviewer 认为我们把 ResNet-18 的证据强度写得与 Tiny-ViT / ConvNeXt 等价。

**输出要求：**
- 最多 10 条
- 每条必须包含：
  - `path:line`
  - `current overreach / ambiguity`
  - `recommended canonical wording`
  - `why this is the safest fix`

**优先覆盖：**
- abstract
- introduction
- results section opening
- cover letter

### KX62: ResNet Table/Claim Consistency Audit [MED]

**Deliverable**: `report_md/_gpt/KX62_RESNET_TABLE_CLAIM_AUDIT.md`

**Goal:** 检查所有出现 ResNet-18 的表格、图注、摘要口径是否一致，并给出“保守说法”的统一模板。

**输出要求：**
- 最多 8 条
- 每条必须包含：
  - `path:line`
  - `inconsistency`
  - `recommended conservative wording`

**特别注意：**
- 不要要求先补齐 ResNet 实验再写这份文档
- 先给文本层的保守修复方案
