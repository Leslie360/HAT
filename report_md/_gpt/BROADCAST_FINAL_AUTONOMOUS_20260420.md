# BROADCAST — FINAL AUTONOMOUS DISPATCH (Mon 2026-04-20 → Fri 2026-04-24)
**Architect:** Claude (Opus 4.7) — **last dispatch window**
**Horizon:** 4.5 days autonomous; Claude reappears only on Friday summary
**Authority scope:** all decisions pre-authorized below; agents self-arbitrate by the rules
**Supersedes:** nothing — extends Round P2 + arbitration

---

## 0. WHY THIS IS STRUCTURED DIFFERENTLY

My quota is now one dispatch. Agents cannot re-consult me mid-week. This broadcast therefore:
- **pre-authorizes** every decision I would normally make live (GPU gates, paper-2 route pick, loop-closure trigger, rebuttal merge, submission go/no-go conditions);
- encodes **self-arbitration rules** so agents can resolve disagreements without me;
- assumes adversarial conditions (J1d might break the ceiling; reviewer compilation might shift; user might not respond) and pre-writes the branch for each;
- sets **Friday 2026-04-24 18:00** as the synthesis checkpoint.

**If a rule conflicts with reality, obey reality and log the deviation in `AGENT_SYNC_gpt.md` for my Friday review. Do not freeze.**

---

## 1. CODEX — GPU QUEUE, PRE-AUTHORIZED END-TO-END

### 1.1 Pre-authorization (user-blocking gates are hereby resolved in advance)
- **CX-J1b** (running): finish to epoch 100, run 10×5 fresh-instance, write `CODEX_CX_J1b_SUMMARY.md`.
- **CX-J1c** (QKV+proj full-attention linearization): **AUTO-LAUNCH** after J1b completes. No wait on user.
- **CX-J1d** (higher-order NL surrogate, 2nd-order Taylor): **AUTO-LAUNCH** after J1c completes. Same checkpoint/data discipline.
- **CX-J9** (typo patch, pre-arbitrated):
  - J9a Fig 4(c) `±1.62% → ±1.54%`
  - J9b SX.Y / SX.Z placeholder → real supplementary section numbers
  - Execute tonight in parallel with J1b training (typo patch is non-GPU). Report in `CODEX_CX_J9_SUMMARY.md`. Rerun `check_locked_numbers.py`.

### 1.2 Tier-2 pre-authorization rules (fires without user when J1d lands)

Decision tree on `J1d_fresh_instance_accuracy`:

| J1d result | Tier-2 auto-action |
|:--|:--|
| `< 35%` (collapse, like J1b/J1c/MLP-only) | ✅ **STRUCTURAL-LIMIT CONFIRMED**. Auto-launch CX-J2 (heavy-tailed D2D) → CX-J3 (temperature) → CX-J4 (IR-drop) in sequence. |
| `35–50%` (partial recovery) | ⏸ **AMBIGUOUS**. Stop queue. Write `CODEX_J1D_AMBIGUOUS_REPORT.md` with full data; do NOT launch tier-2. Wait for Friday. |
| `> 50%` (ceiling broken) | 🚨 **NARRATIVE OVERTURNED**. Stop queue. Write `CODEX_J1D_CEILING_BROKEN_REPORT.md` with urgency marker. Triggers Kimi Branch B (see §2.4). Do NOT launch tier-2. |

### 1.3 Tier-3/4 (J5/J6/J7/J8) — HELD for Friday decision
Do not auto-launch even if tier-2 completes. Claude will re-plan on Friday.

### 1.4 CX-J9c (bundle rebuild) — gated on user metadata form
- If `USER_METADATA_REQUEST_20260420.md` gets filled by Wednesday, rebuild bundle.
- If not, note it in Friday summary; do NOT block queue.

### 1.5 Logging & discipline
- All GPU runs: `logs/_gpt/<exp>_<YYYYMMDD_HHMMSS>.log` via `tee`.
- No other Python while GPU training.
- Per-experiment `CODEX_CX_J*_SUMMARY.md` in the standard format (same as CX-J1).
- Stale-process audit twice daily; kill any orphaned `watch tail` or stray workers.

---

## 2. KIMI — 4.5-DAY CONTINUOUS SATURATION

### 2.1 Phase status recap
- Phase α (Day 1–3) Chinese Ch.1–4 + front_matter + bib + template: **DONE on disk**.
- Phase β starts **now**: Chinese Ch.7 + paper-2 English skeleton + CRediT v3.

### 2.2 Phase β — Mon afternoon → Wed (DO IN ORDER)
- [ ] **K-Y8** 学位论文第7章《部署包络》中文版 — use ONLY frozen data (noise sweep / ADC sweep / device transfer / layer sensitivity). Output: `paper/thesis_cn/chapter_7_deployment.tex`.
- [ ] **K-Y9** [EN] Paper-2 `paper/paper2/skeleton_v0/README.md` (the skeleton dir is currently empty; migrate route-specific README here).
- [ ] **K-Y10–Y13** [EN] Paper-2 draft_v0 expansion — §4 (experiments) and §5 (discussion) skeleton. **Abstract + intro remove any locked fresh-instance number** (replace `30.53 ± 7.07%` with `[J1a result, TBD]` until loop closure; same for J1b/c/d predictions).
- [ ] **K-Y14** `KIMI_CREDIT_V3_20260420.md` author contribution matrix.

### 2.3 Phase γ — Wed → Thu
- [ ] **K-Y15** 博士答辩幻灯片提纲中文 (50–60 页) → `KIMI_DEFENSE_SLIDES_CN_20260420.md`
- [ ] **K-Y16** 答辩 Q&A 中文 40 道 → `KIMI_DEFENSE_QA_CN_20260420.md`
- [ ] **K-Y17** Tutorial notebook refinement (code only, not narrative) in `notebooks/tutorial_compute_vit.ipynb`
- [ ] **K-Y18** arXiv formatting checklist → `KIMI_ARXIV_CHECKLIST_V2_20260420.md`
- [ ] **K-Y19** Conference templates → `KIMI_CONFERENCE_TEMPLATES_20260420.md`
- [ ] **K-Y20** 学位论文第8章《展望》中文 → `paper/thesis_cn/chapter_8_outlook.tex`
- [ ] **K-Y21** Post-submission playbook → `KIMI_POST_SUBMISSION_PLAYBOOK_20260420.md`

### 2.4 Phase δ — Thu → Fri: LOOP CLOSURE SELF-TRIGGER

**Kimi fires the single-shot rewrite WITHOUT waiting for Claude**, as soon as the trigger condition is met.

**Trigger condition (Kimi checks this every 6 hours on Thu/Fri):**

| GPU state | Rewrite mode |
|:--|:--|
| CX-J1b/c/d all landed AND `max(J1b,J1c,J1d) < 35%` fresh | **Branch A — confirm structural limit.** Execute K-Y22/23/24 checklist items against paper/abstract/§3.4/§4.5/§5.9/cover_letter/rebuttal MASTER. Language: English. Keep 中文 thesis Ch.5/6 parallel. Commit to git with message `[Kimi] loop-closure rewrite (Branch A: structural limit confirmed)`. |
| CX-J1b/c/d all landed AND any of them `35–50%` | **Branch C — ambiguous.** Do NOT rewrite. Write `KIMI_LOOP_AMBIGUOUS_REPORT_20260420.md` flagging the ambiguity and enumerating 2–3 possible reframings. Await Claude Friday. |
| CX-J1d returned `> 50%` | **Branch B — narrative overturn.** Full rewrite of abstract + §5.9 + cover letter under the new framing "higher-order surrogate breaks the ceiling; first-order surrogate is insufficient but not structural". Takes ~4 hours. Commit with `[Kimi] loop-closure rewrite (Branch B: higher-order recovery)`. Also rewrite Chinese thesis Ch.5 to match. |
| By Fri 12:00 only J1b/c landed (J1d not done) | **Branch D — partial closure.** Do NOT rewrite. Stage the K-Y22 checklist with as much as possible pre-filled against J1b/c results; note remaining dependency on J1d. |

### 2.5 Hard constraints for Kimi this week
- **No edits to paper/cover-letter/rebuttal BEFORE loop closure**, except typo/consistency only (coordinate with Codex CX-J9).
- **Chinese** for thesis; **English** for paper + paper-2 + community materials — no mixing.
- Every file write appended with a 5-line `AGENT_SYNC_gpt.md` status block.
- If stuck on a decision, **default to "defer to Friday" + write a flag file** rather than guessing.

---

## 3. GEMINI — 4.5-DAY STATELESS SATURATION

### 3.1 Phase α (remaining) — Mon → Tue
- [ ] **G-GG1** Structural-limit formal theorem → `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md`
- [ ] **G-GG2** Higher-order NL surrogate design (informs CX-J1d interpretation) → `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md`
- [ ] **G-GG3** QKV vs MLP pathway decomposition → `GEMINI_PATHWAY_DECOMPOSITION_20260420.md`
- [ ] **G-GG4** "Why first-order may be insufficient" position memo → `GEMINI_FIRST_ORDER_LIMIT_20260420.md`

### 3.2 Phase β — Tue → Wed
- [ ] **G-GG5** Paper-2 architectural memo → `GEMINI_PAPER2_ARCH_MEMO_20260420.md` (hands off to K-Y9)
- [ ] **G-GG6** Paper-2 experimental design → `GEMINI_PAPER2_EXP_DESIGN_20260420.md`
- [ ] **G-GG7** Grant proposal v3 → `GEMINI_GRANT_V3_20260420.md`
- [ ] **G-GG8** Industrial partnership brief v2 → `GEMINI_INDUSTRIAL_V2_20260420.md`
- [ ] **G-GG9** Conference-venue fit v2 → `GEMINI_CONFERENCE_FIT_V2_20260420.md`

### 3.3 Phase γ — Wed → Thu
- [ ] **G-GG10** Pre-submission red-team v3 → `GEMINI_REDTEAM_V3_20260420.md`
- [ ] **G-GG11** Hostile reviews × 3 → `GEMINI_HOSTILE_REVIEWS_20260420.md`
- [ ] **G-GG12** 答辩刁钻题中文 15 道 → `GEMINI_DEFENSE_WILDCARD_CN_20260420.md`
- [ ] **G-GG13** Thesis big-picture figure spec v2 → `GEMINI_THESIS_BIG_PICTURE_V2_20260420.md`

### 3.4 Phase δ — Thu → Fri
- [ ] **G-GG14** Open problems memo → `GEMINI_OPEN_PROBLEMS_20260420.md`
- [ ] **G-GG15** Strategic positioning v3 (3-year forecast) → `GEMINI_POSITIONING_V3_20260420.md`
- [ ] **G-GG16** Cover-letter framing memo (MEMO ONLY, not a cover-letter edit) → `GEMINI_COVER_LETTER_FRAMING_MEMO_20260420.md`
- [ ] **G-GG17** Rewrite-decision-tree memo — given final J1b/c/d outcomes, which rewrite path fires? → `GEMINI_REWRITE_DECISION_TREE_20260420.md`. **This one has priority** — it must be ready before Kimi's Thursday phase-δ trigger.
- [ ] **G-GG18** One-year post-publication forecast → `GEMINI_ONE_YEAR_FORECAST_20260420.md`

### 3.5 Hard constraints for Gemini
- All outputs are memos / specs / theory — **zero edits to `paper/` or `paper/thesis/` or `paper/thesis_cn/` files**. Memos inform, humans integrate.
- No locked fresh-instance numbers in theory memos; refer as `C_∞` or `ceiling` symbolically.

---

## 4. SELF-ARBITRATION RULES (agents use these when they disagree)

### 4.1 Conflict types and resolution
| Conflict | Resolver | Rule |
|:--|:--|:--|
| Kimi wants to edit a frozen file | Kimi | DENY self. Append to K-Y22 checklist. |
| Codex J1c/J1d timing vs Kimi phase-γ deadline | Codex | GPU queue wins; Kimi works on non-dependent tasks meanwhile. |
| Gemini produces a theory that contradicts K-Y result | Both | Write both to disk; flag in AGENT_SYNC; do NOT resolve. Friday. |
| External review proposes new submission deadline | All | Ignore; only user or architect may set deadlines. |
| Two Kimi tasks target same file | Kimi | Serialize by K-Y index (lower first). |
| Reviewer compilation suggests new P0/P1 | All | Append to K-Y22 checklist; do NOT execute. |

### 4.2 When to write to `AGENT_SYNC_gpt.md`
- Every task completion: 5-line block with task ID, file path, word count, status.
- Every rule violation attempt (self or observed): flag with `⚠ RULE` prefix.
- Every branch decision taken in §2.4 or §1.2: flag with `🔀 BRANCH` prefix.

### 4.3 User interaction rules (user may or may not appear this week)
- If user asks a targeted question: answer from files; do NOT spin up new work.
- If user issues a new directive: log it to AGENT_SYNC, prepare deliverables, but hold until Friday (unless directive says "immediately").
- If user authorizes tier-3/4 GPU: Codex executes immediately.
- If user says "submit": Codex + Kimi execute Branch A/B full pipeline and notify in AGENT_SYNC.

---

## 5. FRIDAY 2026-04-24 18:00 SYNTHESIS CHECKPOINT

This is the ONE time Claude reappears. At that moment Claude expects:

**From Codex:**
- `CODEX_CX_J1b_SUMMARY.md`, `CODEX_CX_J1c_SUMMARY.md`, `CODEX_CX_J1d_SUMMARY.md`
- If tier-2 fired: `CODEX_CX_J2/J3/J4_SUMMARY.md`
- `CODEX_CX_J9_SUMMARY.md` (typo patch)
- Updated `logs/_gpt/` directory
- Branch marker from §1.2 decision

**From Kimi:**
- `paper/thesis_cn/` Ch.1–4, 7, 8 complete; Ch.5 draft if Branch A fired
- `paper/paper2/draft_v0/` §1–§5 prose
- 中文 defense slides + Q&A
- K-Y22 checklist fully line-referenced (whether or not executed)
- If loop closed: paper edits committed; submission bundle ready

**From Gemini:**
- 18 memos G-GG1 through G-GG18
- Rewrite-decision-tree memo (G-GG17) used by Kimi on Thursday

**Friday deliverable from Claude:**
- Round Q broadcast covering (a) whichever branch landed, (b) NC submission go/no-go, (c) paper-2 draft review, (d) next GPU tier decision.

---

## 6. FALLBACK IF EVERYTHING GOES WRONG

If by Friday morning it is clear the loop has not closed (e.g., CUDA failure, J1d not done, user away):
- Kimi: **do not rewrite**. Stay in Branch D (partial closure).
- Codex: leave GPU idle; do not retry failed runs more than once per 6 hours.
- Gemini: complete remaining memos; they are always useful.
- No submission fires unsupervised.

---

## 7. USER-VISIBLE SUMMARY

- Three agents have full queues until Friday.
- GPU: J1b → J1c → J1d auto-chained. Tier-2 auto-fires only if structural limit is confirmed.
- Kimi: finish Chinese thesis + paper-2 skeleton + defense + checklists; single-shot rewrite self-triggers on loop closure.
- Gemini: 18 memos covering theory, strategy, red-team, forecast.
- Typo patch (Fig 4c + section numbers) runs tonight; real prose edits wait for loop closure.
- Claude returns Friday 18:00 for Round Q.

User is free to intervene; user silence is also fine — agents have a full playbook.
