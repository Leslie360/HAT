# BROADCAST — Round Q 14-Day Assignment
**Issued:** 2026-04-21 16:00 by Claude (Architect)
**Window:** 2026-04-21 → 2026-05-05 (14 days)
**Supersedes:** `BROADCAST_FINAL_AUTONOMOUS_20260420.md` (checkpoint fired early due to J1d ambiguity)
**Rule A still active:** Chinese thesis → `paper/thesis_cn/`. Paper-1 + paper-2 stay English.
**Rule B still active:** No paper-text edits until loop closure declared. Forbidden files listed in §0.

---

## 0. Rule B frozen-file list (unchanged)

Do **NOT** touch during this window:
- `paper/00_abstract.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/cover_letter*.md`
- `KIMI_REBUTTAL_MASTER_20260420.md`
- `paper/thesis/chapter_5_*.tex`
- **NEW:** `paper/paper2/draft_v0/*` (until paper-2 route ratified; see K-Z11)
- **NEW:** `paper/paper2/skeleton_v0/*` locked-number lines (G-HH6 scrub prerequisite)

Allowed: all `_gpt/` memos, `paper/thesis_cn/*`, new `paper/paper2/skeleton_v1/*`, checklists, defense, community.

---

## 1. Why Round Q exists (context)

CX-J1d produced **three mutually inconsistent reports** inside four hours (10:35 ceiling-broken, 10:43 Branch-A-confirmed, 15:53 AMBIGUOUS 41.53±8.87%). Branch A report even claims J2/J3/J4 auto-launched. We cannot write a thesis chapter or submission cover letter on top of contradictory logs.

**Round Q's job**:
1. **Disambiguate J1d.** Establish ONE canonical fresh-instance number with version-stamped JSON.
2. **Probe the bimodality.** The 41.53% mean hides a range 27.51→51.62%. This is either (a) stochastic basin instability (new physical claim) or (b) measurement artifact (seed count too small). We need to know which.
3. **Stabilize narrative.** Three possible stories: structural-limit confirmed / first-order-surrogate-artifact / partial-recovery-with-D2D-basins. Each needs a different paper framing — we commit to one only after disambiguation.
4. **Finish all Rule-B-safe deliverables** (Chinese thesis, paper-2 theory-first skeleton, defense, community) so that when loop closes the single-shot rewrite is genuinely one-shot.

---

## 2. CODEX — GPU queue (14 days, ~180-250 GPU-h)

### 2.1 Immediate (Day 1-2): J1d disambiguation

**CX-K1 — J1d reconciliation audit (NO GPU, 2 h)**
- [ ] Read all three J1d reports (`CEILING_BROKEN_REPORT`, `BRANCH_A_CONFIRMED`, `AMBIGUOUS_REPORT`).
- [ ] Inspect `logs/_gpt/cx_j1d_*.log` + `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json` + `second_order_ste.json`.
- [ ] Write `CODEX_J1D_RECONCILIATION_20260421.md` with:
  - Timeline of every J1d run (which seed, which δg_eff, which config).
  - Which report corresponds to which actual run.
  - Whether J2/J3/J4 actually launched (check checkpoint dirs + GPU logs), or if that was a stale plan statement.
  - Canonical J1d result → **41.53 ± 8.87%** from 2026-04-21 15:53 is treated as authoritative unless JSON audit contradicts it.
- [ ] If J2/J3/J4 actually ran: report their fresh-instance results and mark them as **not authorized** (Branch A trigger was wrong). Preserve data; do not delete.
- [ ] If J2/J3/J4 did NOT run: confirm so and await explicit re-authorization below.

**CX-K2 — J1d-stability extension (10-15 GPU-h, Day 2-3)**
- [ ] Rerun `V4_hybrid_standard_noise_hat_second_order_ste` fresh-instance eval with **20 more seeds** (seeds 1042…2942, step 100).
- [ ] Combined N=30 should sharpen the mean; σ should stabilize.
- [ ] Output: `cx_k2_fresh_eval.json` with per-seed accuracy and summary stats.
- [ ] Trigger interpretation:
  - N=30 mean in [25, 35) → collapse confirmed, J1d-2 was an unlucky high-tail fluke.
  - N=30 mean in [35, 50] → bimodality is real; proceed to CX-K3.
  - N=30 mean > 50 → ceiling genuinely broken; write `CODEX_K2_CEILING_CONFIRMED.md` and alert Claude (pause queue).

### 2.2 Basin / surrogate probe (Day 3-7, ~80 GPU-h)

**Run only if CX-K2 confirms bimodality (35-50%).** Otherwise skip to §2.3.

**CX-K3 — δg_eff sweep on J1d-2 config (40 GPU-h)**
- [ ] Warm-start from `second_order_ste_best.pt`.
- [ ] Sweep δg_eff ∈ {0.0, 0.05, 0.10, 0.15, 0.20, 0.25}. 6 training runs × 100 epochs each (AMP, no other changes).
- [ ] For each: 10×5 fresh-instance eval.
- [ ] Output: `cx_k3_dgeff_sweep.json` + `CODEX_CX_K3_SUMMARY.md`.
- [ ] Question answered: does non-zero δg_eff shift the mean / reduce variance / change bimodal → unimodal?

**CX-K4 — Second-order strength sweep (30 GPU-h)**
- [ ] Modify `StraightThroughQuantize.backward` to accept a scalar α ∈ [0, 1] scaling the second-order term.
- [ ] Sweep α ∈ {0.0, 0.25, 0.5, 0.75, 1.0}. α=0 = original first-order; α=1 = current J1d-2.
- [ ] 5 training runs × 60 epochs each (shorter, we just need the transfer landing).
- [ ] Fresh-instance 10×5 per run.
- [ ] Output: `cx_k4_alpha_sweep.json`.
- [ ] Question: is the partial recovery smooth in α, or threshold-like at α≈1?

**CX-K5 — Third-order STE sanity (10 GPU-h)**
- [ ] Add cubic term to STE. One run, 100 epochs, 10×5 fresh eval.
- [ ] Output: `cx_k5_third_order.json`.
- [ ] Question: does adding one more Taylor order improve or degrade? If degrades → J1d-2 was already saturated and basin instability is intrinsic. If improves → surrogate fidelity hypothesis strengthens.

### 2.3 Tier-2 (conditional, Day 7-10, ~60 GPU-h)

**Rules:**
- Launch J2/J3/J4 **only if K2 mean < 35%** (structural limit confirmed — tier-2 is now a rebuttal asset).
- Launch **only J2** if K2 mean in [35, 50) (keep δg_eff/α sweeps priority; tier-2 as ablation).
- Launch **nothing** if K2 mean > 50% (narrative pivot — wait for Claude).

CX-J2 (heavy-tailed D2D), CX-J3 (temperature drift), CX-J4 (IR drop) specs unchanged from Round P2.

### 2.4 Tier-3/4 (Day 11-14)

- CX-J7 (ADC floor) — 10 GPU-h, cheap, run unconditionally on Day 11.
- CX-J5, CX-J6, CX-J8 — **user-gated only**. Do not auto-launch.

### 2.5 Codex housekeeping (continuous)

- [ ] Every experiment: JSON + log + `CODEX_CX_*_SUMMARY.md` + AGENT_SYNC entry (single compact block).
- [ ] Every experiment: tee to `logs/_gpt/<name>_<timestamp>.log`.
- [ ] No Python / GPU processes while another CX-K* is training.
- [ ] **Rule of three**: if any experiment produces a result that contradicts a prior experiment's summary, write a reconciliation memo within 24 h before launching the next one.

---

## 3. KIMI — 14-day queue (4 phases, K-Z1…Z30)

### 3.1 Phase α (Day 1-3) — finish Wave-1 backlog

Wave-1 dispatch (2026-04-21 10:39) is overdue. Close it first.

- [ ] **K-Z1** `KIMI_CREDIT_V3_20260420.md` — author contribution matrix, language-neutral.
- [ ] **K-Z2** `KIMI_ARXIV_CHECKLIST_V2_20260420.md` — source-data, code snapshot, PDF sanity, ancillary files.
- [ ] **K-Z3** `KIMI_CONFERENCE_TEMPLATES_20260420.md` — NeurIPS-W vs MLSys vs ICML-W vs DATE packaging.
- [ ] **K-Z4** `KIMI_POST_SUBMISSION_PLAYBOOK_20260420.md` — time-ordered actions post-submit.
- [ ] **K-Z5** `paper/thesis_cn/chapter_8_outlook.tex` — 中文展望章, J1d-number-agnostic.
- [ ] **K-Z6** `KIMI_DEFENSE_SLIDES_CN_20260420.md` — 50-60 slide outline, 中文, falsification framing.
- [ ] **K-Z7** `KIMI_DEFENSE_QA_CN_20260420.md` — 40-question defense bank, 中文, emphasize hostile angles.
- [ ] **K-Z8** `KIMI_PAPER2_GAP_ANALYSIS_20260420.md` — skeleton_v0 vs what's missing, number-agnostic.
- [ ] **K-Z9** `KIMI_ROUND_Q_ADVANCE_BRIEF_20260420.md` — Friday synthesis one-pager (now folded into Day 3 handover).

### 3.2 Phase β (Day 4-7) — Chinese thesis consolidation + paper-2 EN draft v1

- [ ] **K-Z10** `paper/thesis_cn/chapter_5_failure_modes.tex` ⚠ 注意: **不是** `paper/thesis/chapter_5_*` (frozen); 中文 thesis 的 Ch.5 是新文件。Write 中文版 failure-modes chapter using J1b/J1c collapse evidence + J1d ambiguity framed as "stochastic-basin sensitivity".
- [ ] **K-Z11** `paper/thesis_cn/chapter_6_physical_realism.tex` — 中文版, covers Tier-2/3/4 experiment scope (conditional text; write with `\if` blocks for J1d < 35% vs 35-50% vs > 50%).
- [ ] **K-Z12** `paper/paper2/skeleton_v1/SKELETON.md` — theory-first paper-2 outline, **zero locked numbers** in abstract/intro (Rule B extension: skeleton_v1 is editable; draft_v0 is frozen pending route ratification).
- [ ] **K-Z13–Z17** `paper/paper2/skeleton_v1/01_intro.md`, `02_related.md`, `03_theory.md`, `04_experiment_plan.md`, `05_discussion.md` — EN, number-agnostic, placeholders `[J1a result]` `[K2 result]` etc.
- [ ] **K-Z18** `paper/thesis_cn/abstract_cn.tex` — 中文摘要, placeholder-safe for any J1d branch outcome.

### 3.3 Phase γ (Day 8-10) — defense + community rollups

- [ ] **K-Z19** `KIMI_TUTORIAL_ARXIV_DRAFT_20260420.md` — arXiv tutorial note, 3-5 pages, EN.
- [ ] **K-Z20** `KIMI_COMMUNITY_FAQ_V2_20260420.md` — update `KIMI_PUBLIC_FAQ_20260420.md` with J1d findings (non-locked).
- [ ] **K-Z21** `paper/thesis_cn/chapter_8_outlook.tex` revision — integrate CX-K3/K4/K5 findings.
- [ ] **K-Z22** `KIMI_THESIS_CN_CONSISTENCY_CHECK_20260421.md` — cross-chapter number / terminology / notation consistency sweep for 中文 thesis.

### 3.4 Phase δ (Day 11-14) — loop-closure prep + Round R brief

- [ ] **K-Z23** `KIMI_PAPER_REWRITE_CHECKLIST_V2_20260421.md` — expand K-Y22 with exact line-level edits for all four J1d branches (A/B/C/D). Pre-staged edits only, no prose yet.
- [ ] **K-Z24** `KIMI_COVER_LETTER_BRANCH_DRAFTS_20260505.md` — four cover-letter drafts, one per branch. To be selected and injected at loop closure.
- [ ] **K-Z25** `KIMI_ABSTRACT_BRANCH_DRAFTS_20260505.md` — four abstract drafts, one per branch.
- [ ] **K-Z26** `KIMI_REBUTTAL_V2_DELTA_20260505.md` — delta-only rebuttal update (do NOT edit MASTER yet).
- [ ] **K-Z27** `KIMI_ROUND_R_ADVANCE_BRIEF_20260505.md` — Round R seed for Claude after 2026-05-05.
- [ ] **K-Z28** `KIMI_THESIS_CN_FINAL_AUDIT_20260505.md` — full consistency + citation audit of 中文 thesis.
- [ ] **K-Z29** `KIMI_DATA_RELEASE_MANIFEST_V2_20260505.md` — Zenodo-ready manifest including CX-K runs.
- [ ] **K-Z30** `KIMI_RULE_B_CLOSURE_PROTOCOL_20260505.md` — step-by-step loop-closure execution order (which file edited in what order; rollback procedure).

### 3.5 Kimi rules

- Rule B still applies: zero edits to frozen files (§0 list).
- All thesis work in Simplified Chinese.
- Paper-2 EN draft lives in `paper/paper2/skeleton_v1/` (new dir — old `draft_v0/` and `skeleton_v0/` are frozen references).
- If a task requires a number that depends on CX-K outcomes, use placeholder `[CX-Kn result, TBD]`.
- Append one compact AGENT_SYNC block per phase closure (not per task).

---

## 4. GEMINI — 14-day queue (stateless memos, G-HH1…HH20)

### 4.1 Phase α (Day 1-3) — overdue synthesis

Close Wave-1 synthesis dispatch first.

- [x] **G-HH1** `GEMINI_J1D_BRANCH_SYNTHESIS_20260421.md` — branch memo: <35% / 35-50% / >50%, what can/cannot be claimed per branch, which paper-2 route remains viable.
- [x] **G-HH2** `GEMINI_PAPER2_CROSSWALK_20260421.md` — map `skeleton_v0/` sections to existing Kimi/Gemini memos; flag theoretically supported vs need-experiments.
- [x] **G-HH3** `GEMINI_THESIS_CN_DEPENDENCY_MAP_20260421.md` — crosswalk memos → 中文 thesis chapters; safe-now vs wait-for-closure.
- [x] **G-HH4** `GEMINI_DEFENSE_ATTACK_SURFACE_20260421.md` — 15 strongest hostile defense-committee angles + response paths.

### 4.2 Phase β (Day 4-7) — bimodality theory

- [x] **G-HH5** `GEMINI_BIMODAL_BASIN_THEORY_20260421.md` — formal claim: under fresh-instance D2D sampling, higher-order surrogate exposes a bimodal basin structure. Derive condition under which mean fresh accuracy is bimodal vs Gaussian.
- [x] **G-HH6** `GEMINI_PAPER2_LOCKED_NUMBER_SCRUB_20260421.md` — specific grep of `skeleton_v0/00_abstract.md` and all draft_v0 files; enumerate every locked number; recommend placeholder replacement wording.
- [x] **G-HH7** `GEMINI_SURROGATE_FIDELITY_LADDER_20260421.md` — theoretical ordering of STE orders (1st / 2nd / 3rd / exact) against fresh-instance variance.
- [x] **G-HH8** `GEMINI_DGEFF_MEAN_FIELD_20260421.md` — mean-field prediction for δg_eff effect on fresh-instance mean (informs CX-K3 interpretation).
- [x] **G-HH9** `GEMINI_REWRITE_DECISION_TREE_V2_20260421.md` — update G-GG17 with the ambiguous branch and its sub-cases (bimodal-real vs seed-too-few).

### 4.3 Phase γ (Day 8-10) — paper-2 viability + grant pivot

- [x] **G-HH10** `GEMINI_PAPER2_ROUTE_FINAL_20260425.md` — after CX-K2/K3/K4 data lands, pick paper-2 route (structural-limit / surrogate-artifact / bimodal-basin). This memo replaces `CLAUDE_DC_PAPER_2_ROUTE_20260420.md` authority.
- [x] **G-HH11** `GEMINI_GRANT_PIVOT_V2_20260425.md` — grant framing update: bimodal-basin narrative vs clean structural-limit.
- [x] **G-HH12** `GEMINI_INDUSTRIAL_OUTREACH_V3_20260425.md` — industrial positioning given the uncertainty.
- [x] **G-HH13** `GEMINI_HOSTILE_REVIEW_V4_20260425.md` — simulate 3 hostile NC reviewers against whichever branch G-HH10 picks.

### 4.4 Phase δ (Day 11-14) — forward-look + Round R

- [x] **G-HH14** `GEMINI_POST_LOOP_EXPERIMENT_QUEUE_20260501.md` — next-quarter GPU queue if paper-2 gets accepted → what new experiments to fund.
- [x] **G-HH15** `GEMINI_ONE_YEAR_FORECAST_V2_20260501.md` — update G-GG15 with bimodal basin implications.
- [x] **G-HH16** `GEMINI_OPEN_PROBLEMS_V2_20260501.md` — update open problems list.
- [x] **G-HH17** `GEMINI_DEFENSE_WILDCARD_V2_CN_20260501.md` — 10 wildcard defense questions, 中文.
- [x] **G-HH18** `GEMINI_CONFERENCE_FIT_V3_20260501.md` — where paper-2 best fits given final narrative.
- [x] **G-HH19** `GEMINI_ROUND_R_ADVANCE_BRIEF_20260505.md` — Round R seed for Claude.
- [x] **G-HH20** `GEMINI_RULE_B_RELEASE_MEMO_20260505.md` — loop-closure green-light checklist from a theory-integrity angle.

### 4.5 Gemini rules

- Stateless: every memo is independently readable.
- Number-agnostic until CX-K2 lands (2026-04-23). After K2, numbers are allowed **only** for CX-K-series metrics.
- Do not touch `paper/` or `paper/thesis/` or `paper/thesis_cn/`.
- One AGENT_SYNC block per phase closure.

---

## 5. CLAUDE — self-tasks (audit + arbitration only)

- [ ] **CLAUDE-EA** (Day 1) — read CX-K1 reconciliation memo; ratify J1d canonical number; update `CLAUDE_DG_MONITOR_LOG_20260420.md` Entry 002 with the triple-report resolution.
- [ ] **CLAUDE-EB** (Day 3) — Phase α audit: verify K-Z1…Z9 landed + G-HH1…HH4 landed + CX-K1/K2 landed.
- [ ] **CLAUDE-EC** (Day 7) — Phase β audit: ratify paper-2 route decision (G-HH10 + K-Z12).
- [ ] **CLAUDE-ED** (Day 10) — Phase γ audit: check CX-K3/K4/K5 status; decide tier-2 launch.
- [ ] **CLAUDE-EE** (Day 14 / 2026-05-05) — Round R broadcast. Loop-closure decision: fire K-Z30 single-shot rewrite OR extend into Round R with updated triggers.
- [ ] **CLAUDE-EF** (continuous) — Rule B enforcement log. Every attempted violation → CLAUDE_DG new entry.

---

## 6. Pre-authorized branch triggers (agents apply without Claude)

| Trigger | Actor | Action |
|:--|:--|:--|
| CX-K2 mean < 35% | Codex | Launch J2 immediately; launch J3/J4 48 h later if no contradiction found. Notify Kimi (Branch A path). |
| CX-K2 mean ∈ [35, 50) | Codex | Launch K3 (δg_eff sweep). Do NOT launch J3/J4. Notify Kimi (Branch C path — bimodal). |
| CX-K2 mean > 50% | Codex | **Stop queue.** Write `CODEX_K2_CEILING_CONFIRMED.md`. Notify Kimi + Gemini (Branch B path — narrative overturn). Wait for Claude. |
| K-Z16 paper-2 route needs number | Kimi | Use placeholder `[CX-Kn TBD]`; do not block on missing data. |
| Gemini memo conflicts with Kimi text | Both | Write `CONFLICT_NOTE_<topic>.md`; do not silently override. |
| Any agent tempted to edit §0 forbidden file | All | Abort edit. Write a `RULE_B_VIOLATION_ATTEMPT_<timestamp>.md` explaining what they were about to do and stop. |

---

## 7. Fallback rules (failure modes)

| Failure | Response |
|:--|:--|
| GPU stall > 12 h on any CX-K* | Codex writes `CX_STALL_<exp>.md`, holds queue, does not skip |
| Kimi Wave-1 task still empty on Day 4 | Kimi escalates to `KIMI_BLOCKED_<task>.md`; Claude re-triages on CLAUDE-EB |
| Gemini memo requires data not yet produced | Write memo with explicit `<DATA-PENDING-CX-Kn>` tags; do not fabricate |
| Two agents produce contradictory claims | Open `CONFLICT_NOTE_<topic>.md`; flag for Claude; continue Rule-B-safe work |
| User issues new directive mid-window | Parse as override of matching §, keep rest in motion |

---

## 8. Friday 2026-04-25 mini-checkpoint (Day 4)

Agents write a one-line status each in AGENT_SYNC under header `## Round Q Day-4 pulse`. Content:
- Codex: CX-K1 + K2 status, J1d canonical number, tier-2 decision.
- Kimi: Phase α closed? Y/N, blockers.
- Gemini: G-HH1-4 delivered? Y/N, G-HH10 route preview.

**Claude does not need to respond** unless a conflict is flagged. Claude returns on 2026-05-05 for Round R.

---

## 9. Hard-dated milestones

| Date | Milestone | Owner |
|:--|:--|:--|
| 2026-04-22 | CX-K1 reconciliation complete | Codex |
| 2026-04-23 | CX-K2 landed (N=30 fresh eval) | Codex |
| 2026-04-24 | Phase α (Wave-1 backlog) closed | Kimi + Gemini |
| 2026-04-25 | Day-4 pulse in AGENT_SYNC | All |
| 2026-04-28 | Paper-2 route picked (G-HH10) | Gemini (ratified by Claude-EC) |
| 2026-05-01 | CX-K3/K4/K5 all landed | Codex |
| 2026-05-03 | K-Z23-Z26 branch drafts complete | Kimi |
| 2026-05-05 | Round R broadcast / loop-closure | Claude |

---

## 10. User-visible summary

Round Q is a 14-day disambiguation-and-stabilization cycle. The J1d triple-report confusion (10:35 ceiling-broken, 10:43 Branch-A, 15:53 AMBIGUOUS) must be resolved before any paper is written. Codex re-runs J1d with 30 seeds, then sweeps δg_eff and second-order strength to decide whether the bimodality is real. Kimi finishes the overdue Wave-1 backlog (CRediT, arXiv, conference, defense CN, thesis Ch.8), writes 中文 thesis Ch.5/6/8/abstract, and drafts four branch-conditioned cover letters. Gemini synthesizes existing memos into branch-aware guidance and picks the paper-2 route after K2/K3/K4 lands. Rule B holds: no paper text changes until loop closes. Claude returns 2026-05-05 for Round R.
