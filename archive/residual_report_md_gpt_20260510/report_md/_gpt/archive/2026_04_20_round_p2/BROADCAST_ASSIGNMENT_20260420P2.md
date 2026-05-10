# BROADCAST ASSIGNMENT — Round P2 (REDESIGN, 14-day)
**Date:** 2026-04-20
**Architect:** Claude (Opus 4.7)
**Supersedes:** BROADCAST_ASSIGNMENT_20260421P.md (rescinded)
**Duration:** 14 days

---

## TWO RULE CHANGES (effective immediately)

### Rule A — Thesis language
- The PhD thesis (学位论文) is **中文**.
- All thesis deliverables are `.tex` or `.md` in **简体中文**, not English.
- Paper-2 (forward journal paper) stays in English.
- NC submission (paper-1) stays in English.
- This affects ~40% of outstanding Kimi text tasks — they must be re-scoped.

### Rule B — No paper-text edits while GPU queue is live
- Per-experiment rewrites are **wasteful**: every new CX-J* result can invalidate the previous rewrite. CX-J1 already proved this (joint-training narrative died on contact).
- NEW rule: **complete the GPU loop first**, THEN do one coherent rewrite.
- During the GPU loop, Kimi/Gemini work on:
  - design-phase / theory-phase artifacts that are agnostic to the number
  - thesis **Chinese** prose for already-frozen results (Ch.1–4 + retention + noise sweep)
  - paper-2 architectural skeleton (which is theory-first, not number-first)
  - community / defense materials that don't depend on the final punchline
- **Forbidden during GPU loop**: edits to `paper/00_abstract.md`, `paper/05_results.md`, `paper/06_discussion.md`, `paper/cover_letter*.md`, rebuttal MASTER, any `paper/thesis/chapter_5_*.tex` (since Ch.5 is the disputed mitigation chapter).
- **Allowed**: thesis Ch.1–4 + Ch.7 (deployment envelope frozen) + Ch.8 (outlook) in Chinese, paper-2 theory/methods, defense slides skeleton, grant proposals, press kit variants.
- **Single-shot rewrite fires once**: after the last CX-J* lands OR user declares "GPU loop closed".

---

## ARCHITECTURAL INTENT

1. **Close the GPU loop first**. The negative CX-J1 result mandates diagnostic follow-ups (CX-J1b/c/d). Until those finish, we do not know if:
   - the failure is structural (J1b+J1c collapse too) → falsification-style thesis
   - the failure is surrogate-fidelity (J1d breaks the ceiling) → reframe as "first-order limit" thesis
   - some intermediate outcome
2. **Decouple text work from GPU outcomes**. Everything Kimi/Gemini writes for 14 days must be NUMBER-AGNOSTIC or backed by already-frozen results.
3. **One atomic rewrite at loop closure**. When all CX-J* are done, Kimi gets a single consolidated rewrite task (paper + thesis) with the final numbers locked. No churn.
4. **Thesis is Chinese**. Re-language every outstanding thesis task.

---

## CODEX — GPU queue (unchanged from Round P)

- [ ] CX-J1b ⛔ QKV-only protected linearization at NL=2.0 (15–20 GPU-h)
- [ ] CX-J1c ⛔ Full-attention-linear at NL=2.0 (15–20 GPU-h)
- [ ] CX-J1d ⛔ Higher-order NL surrogate (20–30 GPU-h)
- [ ] CX-J2 ⛔ Heavy-tailed D2D full sweep (8–12 GPU-h)
- [ ] CX-J3 ⛔ Temperature drift Arrhenius (10–14 GPU-h)
- [ ] CX-J4 ⛔ IR-drop 16×16 + 32×32 (8–12 GPU-h)
- [ ] CX-J5 ⛔ Per-batch HAT cadence sweep (20–30 GPU-h)
- [ ] CX-J6 ⛔ Retention-extended (15–25 GPU-h)
- [ ] CX-J7 ⛔ ADC floor scan (3–5 GPU-h)
- [ ] CX-J8 ⛔ ImageNet-100 pilot (100–150 GPU-h)

**Recommended order**: J1b → J1c → J1d → J2 → J3 → J4 → J7 (cheap) → J5 → J6 → J8 (largest last).
**Total**: ~215–317 GPU-h. Across 14 days: feasible at 15–22 GPU-h/day sustained.

**Codex rule**: do not touch `paper/`, `paper/thesis/`, rebuttal files. Codex is pure executor. Land results to `report_md/_gpt/json_gpt/` + `csv_gpt/` + per-run `.md` summary only.

---

## KIMI — 14-day number-agnostic + Chinese thesis saturation (28 tasks, 4 phases)

### Phase α — Days 1–3: Chinese thesis Ch.1–3 (frozen results only)

**⚠ Language: all output is 简体中文 unless marked [EN].**

- [ ] **K-Y1** 学位论文第1章《引言》中文版 → `paper/thesis_cn/chapter_1_introduction.tex`
- [ ] **K-Y2** 学位论文第2章《相关工作》中文版 → `paper/thesis_cn/chapter_2_related_work.tex`
- [ ] **K-Y3** 学位论文第3章《方法论》中文版 → `paper/thesis_cn/chapter_3_methodology.tex`
- [ ] **K-Y4** 学位论文第4章《基准实验》中文版 — 仅使用已冻结的 baseline 数据（ResNet/ConvNeXt/Tiny-ViT V1–V6 + 跨数据集）→ `paper/thesis_cn/chapter_4_benchmarks.tex`
- [ ] **K-Y5** 学位论文摘要 + 致谢 + 中英文关键词 → `paper/thesis_cn/front_matter.tex`
- [ ] **K-Y6** 学位论文参考文献整理（BibTeX 中文规范）→ `paper/thesis_cn/references.bib`
- [ ] **K-Y7** 学位论文 LaTeX 模板选型 + 格式要求文档（看学校规范）→ `KIMI_THESIS_CN_TEMPLATE_20260420.md`

### Phase β — Days 4–7: Chinese thesis Ch.7 + paper-2 theory-first

- [ ] **K-Y8** 学位论文第7章《部署包络》中文版（使用已冻结的 noise sweep / ADC sweep / device transfer / layer sensitivity）→ `paper/thesis_cn/chapter_7_deployment.tex`
- [ ] **K-Y9** [EN] Paper-2 architectural skeleton — theory-first, NOT number-first (routes R-A/R-B/R-C still viable) → `paper/paper2/skeleton_v0/README.md`
- [ ] **K-Y10** [EN] Paper-2 §1 Introduction (generic problem framing, no numbers) → `paper/paper2/skeleton_v0/01_intro.md`
- [ ] **K-Y11** [EN] Paper-2 §2 Related work (30+ refs, depth pass) → `paper/paper2/skeleton_v0/02_related.md`
- [ ] **K-Y12** [EN] Paper-2 §3 Methods (theoretical framework, equations only, no experimental numbers) → `paper/paper2/skeleton_v0/03_methods.md`
- [ ] **K-Y13** [EN] Paper-2 §4 Experimental design (what would be measured; no measurements yet) → `paper/paper2/skeleton_v0/04_experiments.md`
- [ ] **K-Y14** Fresh CRediT v3 draft + author contribution matrix — language-neutral → `KIMI_CREDIT_V3_20260420.md`

### Phase γ — Days 8–10: defense + community (both languages)

- [ ] **K-Y15** 博士答辩幻灯片提纲（中文，50–60 页）→ `KIMI_DEFENSE_SLIDES_CN_20260420.md`
- [ ] **K-Y16** 博士答辩 Q&A 题库（中文，40 道）→ `KIMI_DEFENSE_QA_CN_20260420.md`
- [ ] **K-Y17** [EN] Tutorial notebook refinement (code-focused, no result narratives yet) → `notebooks/tutorial_compute_vit.ipynb` (in-place)
- [ ] **K-Y18** [EN] ArXiv-ready formatting checklist (process doc, not text edit) → `KIMI_ARXIV_CHECKLIST_V2_20260420.md`
- [ ] **K-Y19** [EN] Conference venue package (NeurIPS-W / MLSys / ICML-W submission templates) → `KIMI_CONFERENCE_TEMPLATES_20260420.md`
- [ ] **K-Y20** 学位论文第8章《展望》中文版（纯展望，不依赖 CX-J* 结果）→ `paper/thesis_cn/chapter_8_outlook.tex`
- [ ] **K-Y21** [EN] Post-submission playbook (process, not numbers) → `KIMI_POST_SUBMISSION_PLAYBOOK_20260420.md`

### Phase δ — Days 11–14: atomic rewrite ready-queue

**These 7 tasks are DRAFT-PREPARED during phase δ but EXECUTED only after user declares "GPU loop closed". They are placeholders that gather data specs, NOT narrative text.**

- [ ] **K-Y22** Single-shot rewrite checklist (paper §5.9 + abstract + cover letter) — checklist only, no prose → `KIMI_PAPER_REWRITE_CHECKLIST_20260420.md`
- [ ] **K-Y23** 单次重写清单（学位论文第5章 + 第6章，中文）→ `KIMI_THESIS_CN_REWRITE_CHECKLIST_20260420.md`
- [ ] **K-Y24** [EN] Rebuttal MASTER v3 checklist (which OBJ-ids need new data) — checklist only → `KIMI_REBUTTAL_MASTER_V3_CHECKLIST_20260420.md`
- [ ] **K-Y25** 学位论文交叉章节一致性检查清单（中文）→ `KIMI_THESIS_CN_CONSISTENCY_CHECKLIST_20260420.md`
- [ ] **K-Y26** [EN] NC final packaging checklist (files, sizes, formats) → `KIMI_NC_PACKAGING_V3_CHECKLIST_20260420.md`
- [ ] **K-Y27** [EN] Paper-2 skeleton-to-draft gap analysis → `KIMI_PAPER2_GAP_ANALYSIS_20260420.md`
- [ ] **K-Y28** Round Q advance brief (what 2-week plan fires post-loop-closure) → `KIMI_ROUND_Q_ADVANCE_BRIEF_20260420.md`

---

## GEMINI — 14-day stateless theory + design (18 tasks, 4 phases)

### Phase α — Days 1–3: theory foundations (number-agnostic)
- [ ] **G-GG1** Structural-limit hypothesis formal statement (math, not numbers) → `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md`
- [ ] **G-GG2** Higher-order NL surrogate design (informs CX-J1d) → `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md`
- [ ] **G-GG3** QKV vs MLP pathway decomposition theory (informs CX-J1b/c interpretation) → `GEMINI_PATHWAY_DECOMPOSITION_20260420.md`
- [ ] **G-GG4** "Why first-order surrogate may be insufficient" position memo (pure analysis) → `GEMINI_FIRST_ORDER_LIMIT_20260420.md`

### Phase β — Days 4–7: paper-2 design + field positioning
- [ ] **G-GG5** [EN] Paper-2 architectural memo (hands off to K-Y9) → `GEMINI_PAPER2_ARCH_MEMO_20260420.md`
- [ ] **G-GG6** [EN] Paper-2 experimental design — which 4–6 experiments anchor it → `GEMINI_PAPER2_EXP_DESIGN_20260420.md`
- [ ] **G-GG7** Grant proposal outline v3 (language-pivot-tolerant) → `GEMINI_GRANT_V3_20260420.md`
- [ ] **G-GG8** Industrial partnership brief v2 → `GEMINI_INDUSTRIAL_V2_20260420.md`
- [ ] **G-GG9** Conference-venue fit v2 (NeurIPS / MLSys / DATE / ISSCC strategy) → `GEMINI_CONFERENCE_FIT_V2_20260420.md`

### Phase γ — Days 8–10: red-team + hostile simulation
- [ ] **G-GG10** Pre-submission red-team v3 (structural critique, no text edits) → `GEMINI_REDTEAM_V3_20260420.md`
- [ ] **G-GG11** Simulated hostile reviews × 3 (adversarial) → `GEMINI_HOSTILE_REVIEWS_20260420.md`
- [ ] **G-GG12** 博士答辩刁钻问题池（中文，15 道）→ `GEMINI_DEFENSE_WILDCARD_CN_20260420.md`
- [ ] **G-GG13** Thesis big-picture figure spec v2 (language-neutral) → `GEMINI_THESIS_BIG_PICTURE_V2_20260420.md`

### Phase δ — Days 11–14: forward-look + rewrite-support
- [ ] **G-GG14** "Open problems after this paper" memo → `GEMINI_OPEN_PROBLEMS_20260420.md`
- [ ] **G-GG15** Strategic positioning v3 (3-year field forecast) → `GEMINI_POSITIONING_V3_20260420.md`
- [ ] **G-GG16** Pedagogical review of K-Y17 tutorial → `GEMINI_TUTORIAL_CRITIQUE_20260420.md`
- [ ] **G-GG17** Decision tree: given final CX-J* outcomes, which rewrite path fires? → `GEMINI_REWRITE_DECISION_TREE_20260420.md`
- [ ] **G-GG18** "One year post-publication" success-metrics forecast → `GEMINI_ONE_YEAR_FORECAST_20260420.md`

---

## CLAUDE SELF — audit + loop-closure trigger

- [ ] **CLAUDE-DA** Day 1: ratify language-pivot (Chinese thesis) + no-rewrite-during-loop rule
- [ ] **CLAUDE-DB** Day 3: phase-α audit (K-Y1–Y7 Chinese Ch.1–3 + G-GG1–GG4)
- [ ] **CLAUDE-DC** Day 4: paper-2 route final selection (⚠ frozen, will not re-litigate)
- [ ] **CLAUDE-DD** Day 7: phase-β audit + tier-2 GPU gate decision
- [ ] **CLAUDE-DE** Day 10: phase-γ audit
- [ ] **CLAUDE-DF** Day 14 OR loop-closure: trigger single-shot rewrite → Round Q broadcast
- [ ] **CLAUDE-DG** Continuous: monitor CX-J* landings; veto any Kimi/Gemini attempt to edit paper-text during loop

---

## EXECUTION RULES (Round P2)

1. **Language rule**: all thesis content (学位论文) in simplified Chinese; paper + paper-2 stay English.
2. **No-rewrite-during-loop**: forbidden files listed above. Checklists OK, prose edits NO.
3. **Single-shot rewrite**: fires once, at loop closure. Round Q broadcast delivers the unified rewrite task.
4. **GPU queue**: Codex executor only; no text side-effects.
5. **Parallelism**: all independent tasks fire in parallel.
6. **AGENT_SYNC append rule**: 5-line status block per task completion.
7. **Logging**: all Codex runs tee to `logs/_gpt/<exp>_<timestamp>.log`.
8. **No Python while GPU training**.

---

## TIMELINE GANTT

```
Day  1  2  3  4  5  6  7  8  9 10 11 12 13 14  15+
Kimi α  α  α  β  β  β  β  γ  γ  γ  δ  δ  δ  δ  (rewrite, post-Round-Q)
Gem  α  α  α  β  β  β  β  γ  γ  γ  δ  δ  δ  δ
GPU  J1b─  J1c──  J1d────  J2──  J3──  J4─  J7  J5───  J6───  (J8 optional)
Cla  DA──DB────DC─DD───────DE─────────DF→Round Q
```

---

## EXPECTED BY DAY 14 (loop closure, if tier-1+/2 done)

- 学位论文 Ch.1/2/3/4/7/8 完整中文版（Ch.5/6 等 loop 闭合）
- Paper-2 skeleton v0 (EN, theory + methods + exp design, 0 experimental numbers)
- Defense materials drafted in Chinese
- Grant / industrial / conference strategy memos
- CX-J1b/c/d + J2/J3/J4 landed (decides thesis punchline)
- Checklists for the single-shot rewrite ready to fire

---

## GATES

1. **Day 0 (now)**: user authorizes language pivot + no-rewrite-during-loop rule (default = approve)
2. **Day 1**: CX-J1b GPU authorization
3. **Day 4**: paper-2 route final pick (R-A/R-B/R-C)
4. **Day 7**: tier-2 GPU (J2/J3/J4) authorization
5. **Day 14 or loop-closure**: single-shot rewrite triggers + Round Q broadcast

If user is silent at any gate: text agents continue; only Codex GPU queue blocks.
