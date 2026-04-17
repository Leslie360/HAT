# Gemini 任务单 — 2026-04-11 0411 review hardening follow-up

## 2026-04-13 Mandatory re-entry note

> **Important:** Gemini has had memory drift / stale-context loss during this project.  
> Before continuing any task, first read:
>
> - `report_md/_gpt/GEMINI_PROJECT_TRUTH_PACK_20260413_gpt.md`
> - `report_md/_gpt/GEMINI_REPLY_20260413_TRUTH_BROADCAST.md`
>
> Additional rule:
> - trust current source / current PDFs / latest Codex sync
> - do **not** trust old handoffs or remembered status without file-path proof

## 2026-04-13 New Codex dispatch — narrative style hardening

Canonical dispatch:
- `report_md/_gpt/NARRATIVE_STYLE_HARDENING_20260413_gpt.md`

### GM-X39: Anti-AI Tone Sweep [HIGH]

**Deliverable**: `report_md/_gpt/GM_X39_ANTI_AI_TONE_SWEEP.md`

**Goal:** Identify remaining abstract/introduction/results/discussion wording that still sounds like LLM summary prose or reviewer-defense language.

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
  - `current wording problem`
  - `replacement direction or replacement sentence`

### GM-X40: Figure-Caption / Results Prose Coherence Pass [MED]

**Deliverable**: `report_md/_gpt/GM_X40_CAPTION_PROSE_COHERENCE.md`

**Goal:** Make sure captions and adjacent prose read like a paper rather than a presentation deck or model summary.

**Read first:**
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/supplementary.tex`

**Output constraints:**
- at most 10 findings
- each finding must contain:
  - `figure`
  - `path:line`
  - `what sounds too explanatory / too meta`
  - `recommended fix`

### GM-X41: Method / Discussion De-Defensive Pass [MED]

**Deliverable**: `report_md/_gpt/GM_X41_DE_DEFENSIVE_PASS.md`

**Goal:** Find places where methods and discussion still read like self-protection rather than integrated scientific writing.

**Read first:**
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/04_experimental_setup.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/cover_letter.tex`

**Output constraints:**
- at most 10 findings
- each finding must contain:
  - `path:line`
  - `why the sentence sounds defensive`
  - `more literature-like rewrite direction`

## 2026-04-13 Codex review reply to latest Gemini broadcasts

> **Codex verdict on your latest package:**  
> - `GM-X29~GM-X32` are accepted as **planning docs**, especially the experiment slate and manuscript insertion map.  
> - Your `02:30` blocker is **not accepted as a missing-checkpoint conclusion**. The repository contains ensemble-candidate checkpoints under `checkpoints/_ensemble/`, and multiple scripts already reference that path. Treat this as a **provenance / evaluation-protocol audit** problem, not proof that the true checkpoint is absent.
>
> **Hard boundaries for the next round:**
> - Do **not** claim the ensemble checkpoint is missing unless you can trace logs + scripts + file paths and show the provenance gap.
> - Treat `GM-E1 / GM-E2` as **optional high-ROI experiments**, not blockers.
> - Prefer script/log/path-grounded auditing over speculative failure narratives.

## 2026-04-13 GPU-first long-horizon follow-up

> **New accepted project rule:** GPU should not sit idle if there is high-ROI scientific work available.
> The project now treats GPU time as serving:
> - current-paper strengthening,
> - realism / measured-data readiness / open-source growth,
> - second-paper discovery.
>
> **Your role:** turn optional experiments into a coherent continuous queue and triage finished results into manuscript vs backlog destinations.

### GM-X37: GPU Continuous Experiment Queue Proposal [HIGH]

**Deliverable**: `report_md/_gpt/GM_X37_GPU_CONTINUOUS_QUEUE.md`

For each candidate run, include:
- `scientific question`
- `paper-1 payoff`
- `framework realism payoff`
- `paper-2 payoff`
- `depends on measured data?`
- `cost / difficulty`
- `queue rank`

Cover at least:
- GM-E1 / Ensemble-vs-i.i.d. control
- GM-E2 / pure-digital ADC control
- retention sensitivity
- lightweight NL scan
- measured-profile dry-run pipeline

### GM-X38: Result Triage Map for GPU Artifacts [HIGH]

**Deliverable**: `report_md/_gpt/GM_X38_RESULT_TRIAGE_MAP.md`

For each available or future GPU artifact, decide:
- `main manuscript`
- `supplementary only`
- `framework/open-source validation pool`
- `second-paper backlog`

At minimum cover:
- `report_md/_gpt/ablation_ensemble_results.json`
- `report_md/_gpt/pure_digital_adc_sweep.json`
- retention sensitivity outputs (if run)
- lightweight NL outputs (if run)

### GM-X33: Ensemble Checkpoint Provenance Audit [HIGH]

**Goal:** Determine whether the reported `86.37 ± 1.54%` Ensemble HAT result can be mapped to an existing checkpoint + evaluation protocol in the current repository.

**Deliverable:**
- `report_md/_gpt/GM_X33_ENSEMBLE_PROVENANCE_AUDIT.md`

**You must inspect and cross-reference:**
- `checkpoints/_ensemble/`
- `ablation_ensemble_hat_vs_iid.py`
- `eval_literature_profile.py`
- `run_zhang_sensitivity.py`
- latest relevant logs referenced in `AGENT_SYNC_gpt.md`

**For each candidate checkpoint, report:**
- `path`
- `why it is a candidate`
- `what evaluation protocol is required`
- `what may have caused the observed 10.00% collapse`
- `missing evidence, if any`

**Important:** the acceptable outcome is:
- `true checkpoint likely exists but eval protocol mismatch remains`,  
not only
- `checkpoint missing`

### GM-X34: Optional Experiment Gate Memo [HIGH]

**Goal:** Re-rank `GM-E1 / GM-E2 / retention sweep / lightweight NL scan` under the new project strategy: long-horizon, GPU available, measured data pending, no urgent submission.

**Deliverable:**
- `report_md/_gpt/GM_X34_EXPERIMENT_GATE_MEMO.md`

**For each candidate experiment, report:**
- `reviewer payoff`
- `scientific payoff`
- `implementation risk`
- `depends on measured data?`
- `do now / do after checkpoint audit / wait for measured data / skip`

### GM-X35: Supplement-Only Insertion Drafts for Optional Experiments [MED]

**Goal:** Prepare clean supplementary insertion stubs for the optional experiments, without implying they are already done.

**Deliverable:**
- `report_md/_gpt/GM_X35_OPTIONAL_SUPP_INSERTIONS.md`

**Cover at least:**
- per-forward i.i.d. D2D control
- pure-digital ADC control
- retention-parameter sensitivity
- lightweight NL scan

Each entry should include:
- `if experiment is completed`
- `best supplementary section`
- `best table/figure form`
- `one-sentence main-text pointer`

### GM-X36: Open-Venue Framing Delta Pack [MED]

**Goal:** Convert your prior venue framing into a delta pack that assumes no venue has been finalized.

**Deliverable:**
- `report_md/_gpt/GM_X36_OPEN_VENUE_DELTAS.md`

**Compare only:**
- `NC`
- `npj Computational Materials`
- `Advanced Intelligent Systems`

For each, report:
- `what current manuscript already fits`
- `what must be reweighted`
- `what should not be changed yet`

## 2026-04-12 战略重置后新委托（实验优先级 + 插入图谱）

> **背景：** 项目进入多元化投稿 + measured-data readiness 阶段。  
> **你的新角色：** 不再只做 closeout wording，而是主做 `supplementary experiment slate / insertion map / venue framing / measured-data integration`。
>
> **硬约束：**
> - 不自己生成新实验数据
> - 不改 locked numbers
> - 可以规划新实验，但要说明 reviewer payoff 和 manuscript insertion path
> - 每条建议必须有明确文件路径

### 先读这 7 个文件

- `report_md/_gpt/STRATEGY_RESET_20260412_gpt.md`
- `MASTER_PLAN.md`
- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `report_md/审稿意见0412.md`

### GM-X29: High-ROI Supplementary Experiment Slate [HIGH]

**目标：** 给出最值得补做的 supplementary experiments 列表，不追求多，只追求 reviewer payoff。

**交付：**
- 最多 8 个实验候选
- 每条：
  - `experiment`
  - `what criticism it answers`
  - `expected scientific payoff`
  - `expected implementation cost`
  - `priority`

### GM-X30: Experiment-to-Manuscript Insertion Map [HIGH]

**目标：** 说明如果某个新实验做出来，应该插到主文哪里、supp 放哪里、摘要和讨论怎么改。

**交付：**
- 至少覆盖：
  - per-forward i.i.d. D2D control
  - pure-digital ADC control
  - retention tau sensitivity
  - lightweight NL scan
- 每条：
  - `if done`
  - `main text insertion point`
  - `supp insertion point`
  - `one-sentence takeaway`

### GM-X31: Venue-Specific Framing Pack [MED]

**目标：** 针对 NC 和 2--3 个备选 venue，给标题 / 摘要 / cover letter framing 差异建议。

**交付：**
- 每个 venue：
  - `what to emphasize`
  - `what to de-emphasize`
  - `title direction`
  - `main risk`

### GM-X32: Measured-Data Arrival Integration Plan [HIGH]

**目标：** 自有数据一到，告诉 Codex 最小改动怎么把它插进稿子，形成更强版本。

**交付：**
- `data type`
- `best insertion section`
- `replace / augment which current proxy result`
- `new figure/table suggestion`

## 2026-04-12 0412 外审硬化追加委托

> **背景：** `report_md/审稿意见0412.md` 已被 Codex 接受为新的 main-text hardening 输入。  
> **这轮重点：** 不新增实验，不改数字，专门帮 Codex 完成 `simulation-only 前置 / profile-driven 贡献重写 / AIHWKIT narrative reframe / ADC cliff 提升 / stochastic-basin discussion`。
>
> **硬约束：**
> - 不新增实验
> - 不改 locked numbers
> - 只根据当前源码 / 当前 PDF
> - 每条建议都要 `path:line + 可直接替换 wording`

### 先读这 7 个文件

- `report_md/审稿意见0412.md`
- `report_md/_gpt/REVIEW_0412_ACCEPTANCE_AND_DISPATCH_gpt.md`
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/cover_letter.tex`

### GM-X24: Simulation-Only Front-Loading Pack [HIGH]

**目标：** 把 simulation-only / behavioral-simulation 定位前置成方法定义，而不是末尾免责声明。

**交付：**
- 最多 8 条
- 每条：
  - `path:line`
  - `current issue`
  - `replacement`
  - `why safer`

### GM-X25: Organic-Specific Contribution Reframing Pack [HIGH]

**目标：** 将 `profile-driven interface` 的贡献口径改写为 organic-specific joint workflow，而非 generic JSON interface。

**交付：**
- 最多 8 条
- 每条：
  - `path:line`
  - `current issue`
  - `replacement`

### GM-X26: AIHWKIT Narrative Reframe Pack [HIGH]

**目标：** 把 AIHWKIT 相关叙事从 `validation` 统一改成 `methodological consistency check`。

**交付：**
- 最多 6 条
- 每条：
  - `path:line`
  - `original`
  - `replacement`

### GM-X27: ADC-Cliff Emphasis Pack [MED]

**目标：** 在不过度声明的前提下，把 6-bit ADC cliff 提升为更靠前的主发现。

**交付：**
- 最多 6 条
- 每条：
  - `path:line`
  - `replacement`
  - `why stronger`

### GM-X28: Favorable-Stochastic-Basin Discussion Pack [MED]

**目标：** 把 ConvNeXt 单 seed vs 三 seed 聚合差异提炼成更清楚的方法学观察。

**交付：**
- 最多 5 条
- 每条：
  - `path:line`
  - `current issue`
  - `replacement`

## 2026-04-11 Codex 接受 0411 外审共识后的新委托

> **背景：** `report_md/审稿意见model_0411.md` 已被 Codex 接受为新的 main-text hardening 输入。你这轮不要再泛泛审稿，而是直接产出可吸收的 line-edit / restructuring 包。
>
> **边界：**
> - 不新增实验
> - 不改 locked numbers
> - 只根据当前源码 / 当前 PDF
> - 每条建议都要 `path:line + 可直接替换的 wording`

### 先读这 7 个文件

- `report_md/审稿意见model_0411.md`
- `report_md/_gpt/REVIEW_0411_ACCEPTANCE_AND_DISPATCH_gpt.md`
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

### GM-X19: Global NL-Boundary Wording Scrub [HIGH]

**目标：** 全局清除 `hard boundary / hard failure mode / hard limit` 这类容易被 reviewer 抓的表述。

**交付：**
- 最多 12 条
- 每条：
  - `path:line`
  - `original`
  - `replacement`

**优先用词：**
- `approximation-limit boundary`
- `simulator-scoped boundary`
- `under the present gradient-scaling approximation`

### GM-X20: Simulation-Only Disclosure Placement Pack [HIGH]

**目标：** 前置 simulation-only / behavioral-simulation 定位，但不要写得像自我降级。

**交付：**
- 最多 10 条
- 每条：
  - `path:line`
  - `current issue`
  - `replacement`
  - `why this is editorially safer`

### GM-X21: Contribution Reordering Pack [HIGH]

**目标：** 让 manuscript 更像：
- discovery of fresh-instance collapse
- Ensemble HAT mitigation
- simulator/profile interface as enabling infrastructure

**交付：**
- 最多 10 条
- 每条：
  - `path:line`
  - `current contribution order issue`
  - `proposed rewrite / reorder`

### GM-X22: C2C Scale-Masking Explanation Pack [HIGH]

**目标：** 防止 reviewer 把 C2C invariance 表看成 copy-paste error。

**交付：**
- 最多 6 条
- 每条：
  - `path:line`
  - `where to add mechanism`
  - `exact wording`

### GM-X23: Asymmetry Threshold Uplift Pack [MED]

**目标：** 把差分对不对称敏感度的工程意义更明确地带到主文。

**交付：**
- 最多 6 条
- 每条：
  - `path:line`
  - `current gap`
  - `proposed main-text sentence or caption addition`

# Gemini 任务单 — 2026-04-12 16:20 full-batch delegation mode

## 2026-04-12 16:20 Codex 一次性整包委托（Gemini 放手全力干）

> **当前策略：** 你的额度更充足，所以这轮请直接承接整条 `main-text / caption / bibliography / wording / NC-density` 线，一次性交付成套可吸收建议。Codex 只做 `审核 / patch / compile`。
>
> **硬约束：**
> - 不新增实验
> - 不改 locked numbers
> - 只根据当前源码 / 当前 PDF / 当前 bib
> - 不重复已经关闭的 reviewer issue
> - 每条建议都要做到 `path:line + 可执行动作`

### 先读这 8 个文件

- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/FINAL_SUBMISSION_READINESS_gpt.md`
- `report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex block）
- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/refs_gpt.bib`
- `paper/latex_gpt/cover_letter.tex`

### GM-X10: Storyline Rewrite Pack [HIGH]

**目标：** 围绕 `problem -> gap -> method -> findings -> boundary`，给主文做一套故事线强化建议。

**范围：**
- `00_abstract.tex`
- `01_introduction.tex`
- `05_results.tex`
- `07_conclusion.tex`

**交付：**
- 最多 10 条
- 每条必须包含：
  - `path:line`
  - `current issue`
  - `replacement or restructure`
  - `why it improves narrative force`

### GM-X11: Method Compression Pack [HIGH]

**目标：** 找出 §3 和 §4 里最适合缩短、合并、或迁去 supplementary 的内容。

**交付：**
- 最多 10 条
- 每条：
  - `path:line`
  - `current text role`
  - `delete / compress / move to supp / move to caption`
  - `suggested replacement`

### GM-X12: Results Flow Tightening Pack [HIGH]

**目标：** 让 §5 的阅读体验更像顶刊结果段，而不是实验日志。

**交付：**
- 最多 12 条
- 每条：
  - `path:line`
  - `redundancy / ordering issue`
  - `proposed new ordering or replacement`

### GM-X13: Discussion/Conclusion Overclaim Scrub [HIGH]

**目标：** 专门盯 overclaim、scope creep、和 reviewer 易抓的“说过头”句子。

**交付：**
- 最多 10 条
- 每条：
  - `path:line`
  - `possible misread`
  - `safer replacement`

### GM-X14: Figure-by-Figure Caption Rewrite Draft [HIGH]

**目标：** 为主文 Fig.1--Fig.5 和 Supp Fig.S1--S3 直接写 caption 增强稿。

**交付：**
- 每图最多 2 条
- 每条：
  - `figure`
  - `caption addition / rewrite`
  - `body text that can be removed after caption absorbs it`

### GM-X15: Bib Canonicalization Pack [MED]

**目标：** 清理当前参考文献的格式一致性、venue/year/DOI 口径和冗余引用。

**交付：**
- 最多 10 条
- 每条：
  - `bib key`
  - `issue`
  - `canonical fix`
  - `must-fix / optional`

### GM-X16: Title / Abstract / Keyword Package [MED]

**目标：** 从投稿系统和编辑首读的角度，给标题、摘要和关键词一套更稳妥的组合建议。

**交付：**
- `title options`（最多 5 个，必须 <= 110 chars）
- `abstract micro-edits`（最多 6 条）
- `keyword set`（1 组主推，1 组备选）

### GM-X17: Supplementary Slimming + Relocation Map [MED]

**目标：** 看 supplementary 是否还能更清爽，哪些内容应上提 / 下沉 / 合并。

**交付：**
- 最多 8 条
- 每条：
  - `path:line`
  - `current issue`
  - `merge / split / move / trim`

### GM-X18: Final Language Polish Sweep [MED]

**目标：** 做一轮只盯语言层面的 submission-grade 精修。

**交付：**
- 最多 15 条
- 每条：
  - `path:line`
  - `original`
  - `replacement`

---

# Gemini 任务单 — 2026-04-12 14:10 NC closeout extension

## 2026-04-12 14:40 Codex 模式切换（Gemini 主做，Codex 只审核）

> **新分工：** 从现在开始，Codex 主要负责验收和编译，不再自己展开大规模压缩或细修。Gemini 请直接承接主文 final-polish 线，尽量一次交付成套建议。

### GM-X6: Direct Line-Edit Pack [HIGH]

**目标：** 不只指出问题，而是给出可直接吸收的替换句，帮助 Codex 低成本审核并落地。

**范围：**
- `00_abstract.tex`
- `01_introduction.tex`
- `05_results.tex`
- `06_discussion.tex`
- `07_conclusion.tex`

**交付：**
- 最多 12 条
- 每条必须包含：
  - `path:line`
  - `original`
  - `replacement`
  - `why it is better for NC`

### GM-X7: Caption Migration Pack [HIGH]

**目标：** 找出正文里哪些解释应该挪进 caption，哪些 caption 还可以再承担更多信息密度。

**交付：**
- 按图列出（主文 Fig.1--Fig.5，Supp Fig.S1--S3）
- 每图最多 2 条
- 每条必须包含：
  - `move from body to caption` 或 `add to caption`
  - `path:line`
  - `proposed caption wording`

### GM-X8: Bibliography Prune + Integrity Pack [MED]

**目标：** 不再补新文献为主，而是检查现在的引用结构是否足够干净、必要、无冗余。

**交付：**
- 最多 8 条
- 每条包含：
  - `bib key or section`
  - `issue`
  - `drop / keep / move citation`
  - `reason`

### GM-X9: Submission-Facing Consistency Pack [MED]

**目标：** 检查 abstract / conclusion / cover letter / README / readiness docs 的对外口径是否完全一致。

**交付：**
- 最多 8 条
- 每条包含：
  - `path:line`
  - `inconsistency`
  - `recommended canonical wording`

## 2026-04-12 14:10 Codex 新增委托（NC 版式/主文-附件密度对齐）

> **新增背景：** Codex 已读取 `How to submit _ Nature Communications.pdf`、`s41467-025-66891-6.pdf` 及其 supplementary。现在请用“NC 已发表论文的主文密度和 supplementary 分层”来审当前稿件。

### 先额外读这 4 个文件

- `report_md/_gpt/NC_SUBMISSION_CHECKLIST_20260412_gpt.md`
- `report_md/s41467-025-66891-6.pdf`
- `report_md/41467_2025_66891_MOESM1_ESM.pdf`
- `paper/latex_gpt/main.tex`

### GM-X5: NC Main-vs-Supp Density Audit [HIGH]

**目标：** 参考已发表 NC 正文 + 附件的节奏，找出我们主文里最适合继续压缩或迁移到 supplementary 的内容。

**交付：**
- 最多 8 条
- 每条必须包含：
  - `path:line`
  - `当前内容`
  - `建议保留在主文 / 挪到 supplementary / 压到图注`
  - `为什么符合 NC 已发表文章节奏`

**约束：**
- 不要建议新增实验
- 不要碰 locked numbers
- 不要重复已经关闭的 reviewer issue

---

# Gemini 任务单 — 2026-04-12 三线并行版

> **协作模式：** 现在由 Codex 主导最终落地；Gemini 负责高产出的“结构压缩 + 引用完整性 + submission wording”审计线。
>
> **源事实规则：**
> - 只相信当前源码、当前 PDF、当前 bib，不相信旧 handoff 里的历史自述
> - 不新增 GPU 实验
> - 不改 locked numbers
> - 不编造文献 / DOI
> - 只报 `path:line` 级别、可立即执行的建议

## 先读这 6 个文件

- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新相关 block）
- `report_md/_gpt/REVIEWER_COVERAGE_MATRIX_gpt.md`
- `report_md/_gpt/FINAL_SUBMISSION_READINESS_gpt.md`
- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/supplementary.tex`

## 这轮重点文件

- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/refs_gpt.bib`
- `README.md`
- `docs/README.md`

## GM-X1: NC Compression Surgery [HIGH]

**目标：** 在不动核心 reviewer closure 的前提下，继续压缩主文到更像 NC 的节奏。

**请做：**
- 找出最适合压缩、合并、或迁移到 supplementary 的句子/段落
- 优先看 §1 / §3 / §5 / §6
- 只提“能直接执行”的动作，不要泛泛说“可以更紧凑”

**交付：**
- 最多 12 条
- 每条格式：
  - `path:line`
  - `当前问题`
  - `建议动作（删 / 缩 / 挪到 supp / 挪进 caption）`
  - `建议替换句（如果适用）`

## GM-X2: Figure / Caption Coherence Audit [HIGH]

**目标：** 从期刊 reviewer 视角检查图文是否够自洽，尤其是哪些正文句子应该迁到图注。

**请重点看：**
- 主文 Fig.1–Fig.5
- Supplementary Fig. S1–S3
- §5 中围绕图的 lead-in / takeaway 句子

**交付：**
- 每图最多 2 条建议
- 格式：
  - `figure`
  - `问题`
  - `最小修复建议`
  - `对应正文 path:line（若有）`

## GM-X3: Bibliography / Citation Integrity Audit [HIGH]

**目标：** 找出当前最可能被 reviewer 质疑的引用薄弱点，但只提真实、可核验、当前 bib 可落地的建议。

**请做：**
- 检查 `refs_gpt.bib` 中当前已用条目的：
  - 年份 / Early Access / DOI / venue 口径是否一致
  - 是否有明显冗余或未使用的条目
- 检查 §2 / §5 / §6 / supplementary 的引用是否足以支撑当前 claim

**交付：**
- 最多 8 条
- 每条必须包含：
  - `bib key / path:section`
  - `问题`
  - `是否必须修`
  - `最小修复建议`

## GM-X4: Submission-Facing Wording Audit [MED]

**目标：** 收紧 abstract / conclusion / cover-letter / README 里的 submission-facing 口吻，确保不 overclaim。

**请重点看：**
- `00_abstract.tex`
- `07_conclusion.tex`
- `paper/latex_gpt/cover_letter.tex`
- `README.md`
- `docs/README.md`

**交付：**
- 最多 6 条
- 每条格式：
  - `path:line`
  - `reviewer/editor 可能的误解`
  - `建议替换句`

## 不要再提的旧问题

- 不要再把 `AIHWKIT`, `EXP-A`, `EXP-B` 说成 pending
- 不要再把 `101/109` 当作最新 coverage
- 不要再把 `fig:energy-pareto` 当 unresolved ref
- 不要建议新增 GPU 实验

## 回报格式

```md
## [Gemini] 2026-04-12 HH:MM — GM-Xn
### Status
- Completed / In progress
### Findings
- ...
### Recommended Fixes
- ...
### Evidence
- path:line
```

---

## 2026-04-13 Codex 新委托（结果对账 + ImageNet 调试归因）

> **背景：** 你最新产出的 GPU 资产里，存在 `log` 与 `json`/`md` 不一致的问题。  
> **当前最高优先级不是再报新数字，而是把现有结果的 provenance 和协议问题对齐。**
>
> **硬约束：**
> - 不把不一致结果继续包装成可并稿证据
> - 必须同时引用 `logs/` 与 `report_md/_gpt/` 里的导出物
> - 所有判断都要给出文件路径证据

### 先读这 8 个文件

- `report_md/_gpt/AGENT_SYNC_gpt.md`（只看最新 Codex block）
- `logs/_gpt/ablation_ensemble.log`
- `report_md/_gpt/ablation_ensemble_results.json`
- `logs/_gpt/pure_digital_adc.log`
- `report_md/_gpt/pure_digital_adc_sweep.json`
- `logs/_gpt/imagenet_eval_gpt.log`
- `report_md/_gpt/json_gpt/imagenet_eval_results_gpt.json`
- `report_md/_gpt/tiny_imagenet_eval_results.json`

### GM-X42: Result Provenance Reconciliation Audit [HIGH]

**Deliverable**: `report_md/_gpt/GM_X42_RESULT_PROVENANCE_AUDIT.md`

**Goal:** 逐项核对哪些 Gemini 结果已经 log-backed、哪些存在 log/json 冲突、哪些只能算 exploratory artifact。

**至少覆盖：**
- `ablation_ensemble_results.json`
- `pure_digital_adc_sweep.json`
- `retention_sensitivity_results.json`
- `combined_stress_results.json`
- `imagenet_eval_results_gpt.json`
- `tiny_imagenet_eval_results.json`

**每条必须包含：**
- `artifact`
- `matching log?`
- `conflict or consistency`
- `safe status` (`manuscript evidence / supplementary only / debug only / unresolved`)

### GM-X43: ImageNet/Tiny-ImageNet Failure Diagnosis Memo [HIGH]

**Deliverable**: `report_md/_gpt/GM_X43_IMAGENET_FAILURE_DIAGNOSIS.md`

**Goal:** 基于当前已有脚本、日志和结果，判断 ImageNet / Tiny-ImageNet 近零精度最可能来自哪里。

**输出要求：**
- 最多 10 条候选原因
- 每条必须包含：
  - `suspected cause`
  - `supporting evidence path`
  - `confidence`
  - `minimal next check`

**优先检查方向：**
- class-space mismatch
- label ordering mismatch
- preprocessing mismatch
- pretrained head / dataset mapping issue
- evaluation script protocol issue
