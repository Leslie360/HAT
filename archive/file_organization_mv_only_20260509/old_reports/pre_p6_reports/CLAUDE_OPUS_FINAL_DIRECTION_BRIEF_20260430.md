# Claude Opus — Final Direction Brief

**Date:** 2026-04-30 CST
**From:** Claude (Chief Architect)
**To:** User (PhD candidate) / Kimi / DS / Codex / Gemini / future Claude sessions
**Status:** Architectural ruling. Supersedes the Codex-prepared draft of the same file (which now lives implicitly as input — its D1–D7 questions are answered explicitly in §4 below).
**Project root:** `/home/qiaosir/projects/compute_vit`
**Submission gate:** PhD defense clearance (timeline: weeks-to-months, not artificial). Quality > speed.

---

## Preamble — Why this brief exists

User invoked Opus 4.7 at max effort and asked for a final architectural direction, possibly the last conversation in this thread. The request: state the grand direction, give recommendations, give a task list, be detailed, accurate, architecturally complete, and rich.

I am writing this so any one of the following readers can pick up and execute without re-deriving context:

1. **User** — if I am unavailable, this is your north star.
2. **Kimi planner** — for converting tasks into pipeline plans.
3. **DS coder** — for surgical edits and GPU jobs.
4. **Codex reviewer** — for verifying compliance with the rulings here.
5. **Gemini critic** — for hostile review aligned with our actual narrative.
6. **A future Claude session** — read this first; it captures everything I would re-derive.

This document is **canonical**. If a later memo conflicts with it, that memo must explicitly cite a delta and the reason; otherwise this brief wins.

---

## 1. One-paragraph north star

The paper-1 spine is **a coupled story of method-superiority in the 4-bit pure-quantization regime AND PCM-physics-enabled 4-bit training under a precision-drift trade-off**. AIHWKit is the canonical baseline (`rasch2021aihwkit`); it is robust at 8-bit across σ ∈ {0.10, 0.20, 0.30} but collapses at 4-bit pure quantization (14.64%) where Ensemble HAT survives (86.16%). Independently, when AIHWKit is run with realistic PCM device models, the system trains stably at both 4-bit and 8-bit (~76–78%) but exhibits a **precision-drift trade-off** — 4-bit drifts ~4.8 pp over 3 days while 8-bit is flat. These are two halves of the same story: **realistic-deployment-precision is where engineering decisions actually matter**, and both halves of our work — the algorithm (Ensemble HAT) and the physics (PCM substrate) — speak to that regime. Honest framing wins; we do not claim universal superiority over AIHWKit.

---

## 2. Master narrative spine (LOCKED)

### 2.1 Three pillars (paper-1)

| Pillar | One-line claim | Core evidence | Provenance |
|:--|:--|:--|:--|
| **P1: Failure-mode diagnosis** | Standard HAT (fixed mask) overfits to a single hardware instance and collapses on fresh-instance transfer. | Standard HAT 4-bit fresh = 10.00% (single-class predictor) | Round-7 / R10B mechanism panel |
| **P2: Method (Ensemble HAT)** | Per-epoch D2D resampling restores cross-instance generalization and beats AIHWKit per-batch noise injection in the 4-bit pure-quantization regime. | Ensemble HAT 4-bit = 86.16 ± 0.19% vs AIHWKit 4-bit = 14.64 ± 0.11% (Δ = 71.5 pp); 8-bit parity (87.28 vs 86.16, ~1.1 pp) | R10A / R10E / R11D-1 |
| **P3: Substrate (PCM realism)** | Realistic PCM pulse-update physics enable 4-bit training that pure 4-bit quantization cannot, but this introduces a precision-drift trade-off (4-bit drifts ~4.8 pp/3d; 8-bit drift-immune). | PCM 4-bit 3-seed fresh = 76.68 ± 0.37%, 24h = 72.68 ± 0.69%; PCM 8-bit 3-seed fresh = 77.60 ± 0.66%, 3d ≈ 77.70% | R11D-7 (4-bit 3-seed) + R11D-5a (8-bit 3-seed) |

### 2.2 What the paper does NOT claim (anti-overclaim register)

- **NOT** "Ensemble HAT is universally superior to AIHWKit." False at 8-bit pure quantization.
- **NOT** "PCM is the only path to 4-bit training." Only AIHWKit pure 4-bit was shown to fail; we did not exhaust algorithmic alternatives.
- **NOT** "PCM eliminates noise concerns." It introduces drift instead.
- **NOT** "Cadence is the lever." Without R11D-6 (cadence-matched Ensemble HAT vs AIHWKit), this is unresolved; we keep silent on it rather than overclaim.
- **NOT** "MLP-path localization explains the failure." Invalidated by `supplementary.tex:719`; introduction must be rewritten (see R11C C5).

### 2.3 Why "regime-specific" framing is a feature, not a bug

8-bit parity (AIHWKit ≈ Ensemble HAT) **strengthens** the paper because:

- It demonstrates we are not cherry-picking a regime where our method wins.
- It makes the 4-bit advantage credible: a method that wins everywhere is suspicious.
- It naturally motivates the precision-drift discussion: at 8-bit AIHWKit is fine, but the deployment cost (drift in PCM, area in non-PCM) shifts the engineering tradeoff.

**Do not let any later edit hide the 8-bit parity.** That is the honesty anchor.

---

## 3. Locked numbers register (CANONICAL TRUTH)

Pin these exactly. Drift here is a paper-integrity bug.

### 3.1 IdealDevice (pure quantization, no PCM)

| Run | Precision | σ_D2D | Fresh-instance accuracy | n | Source JSON |
|:--|:--|:--:|:--|:--:|:--|
| R10E | 8-bit | 0.10 | **87.28 ± 0.13%** | 10 | `paper2_aihwkit_baseline/checkpoints/fresh_eval.json` |
| R11D-1 | 4-bit | 0.10 | **14.64 ± 0.11%** | 10 | `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json` |
| R11D-2-clean | 8-bit | 0.20 | **87.52 ± 0.05%** | 10 | `paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020_clean/fresh_eval.json` |
| R11D-3-clean | 8-bit | 0.30 | **87.40 ± 0.05%** | 10 | `paper2_aihwkit_baseline/checkpoints/r11d_3_sigma030_clean/fresh_eval.json` |

### 3.2 PCM UnitCell (realistic device physics)

| Run | Precision | Fresh (0s) | Drift @1d | Drift @3d | Source dir |
|:--|:--|:--|:--|:--|:--|
| R11D-7 3-seed | 4-bit | **76.68 ± 0.37%** | 72.68 ± 0.69% | 71.85 ± 0.81% | `paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed{123,456,789}/` |
| R11D-5a 3-seed | 8-bit | **77.60 ± 0.66%** | 77.56 ± 0.58% | 77.70 ± 0.53% | `paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed{123,456,789}/` |

### 3.3 Method comparison (4-bit canonical, our HAT)

| Method | Precision | Fresh | n | Source |
|:--|:--|:--|:--:|:--|
| Standard HAT (fixed mask) | 4-bit | 10.00% | — | Round-7 paper-1 baseline |
| Ensemble HAT (per-epoch resample) | 4-bit | **86.16 ± 0.19%** | 3 seeds | R10A final integration |

### 3.4 Other locked values

| Item | Value | Source |
|:--|:--|:--|
| V6 Tiny-ViT front-end comp. | **82.58** (single-seed) — was PHANTOM 95.82 | `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json` |
| Digital reference | ~92% (depends on recipe) | `paper/05_results.tex` |
| Word-count budget (main body) | **≤ 5,700** | enforced by R11C |
| Compile gate | `latexmk` RC 0, zero undefined refs | enforced by R11C |

### 3.5 Defensive scaffolding

Kimi added `scripts/_gpt/check_locked_numbers.py` Step 4 in R11D 4-bit narrative pipeline run. **All future task.md files must include a step that runs this guard** so the locked numbers cannot silently drift.

---

## 4. D1–D7 rulings (answers to Codex's questions in the predecessor draft)

### D1 — Main narrative selection: **HYBRID, single paper**

**Ruling.** The paper-1 spine is the **coupled P2+P3 story** described in §2.1. Both halves stay in one paper because:

- They are unified by the "realistic deployment precision" frame (4-bit).
- Splitting weakens both: the algorithm without substrate looks toy; the substrate without algorithm looks like a benchmarking note.
- Word budget allows it after R11C closes the 16→8-page reduction.

**105 (proportional HAT cross-architecture)**: validation/extension, NOT main spine. Promote to a Discussion sub-paragraph and a Supplementary table once same-architecture digital baseline + multi-seed return cleanly.

**107 (analog KV-cache)**: separate Work-2 paper. Do not bundle into paper-1 even if it closes fast. Keeps paper-1 focused.

### D2 — R11D wording: **UPGRADED** (Batch B verified)

**Ruling.** Batch B confirmed PCMPresetDevice trains stably (>70%). The conditional upgrade is **executed**.

**Canonical phrasing (replaces soft phrasing everywhere in paper text):**

> "Realistic PCM device models (UnitCell and PCMPresetDevice) enable 4-bit forward-path training where pure 4-bit quantization collapses; we attribute this to the smoothing of weight updates by PCM pulse-update dynamics."

**Modifier noise framing (Batch C verified):**

Clean Oracle (no modifier noise) reaches 76.80%, within 0.8 pp of the best PCM-with-noise result (77.6%). Modifier noise is **beneficial regularization** (+0.8 pp), not a **necessary training mechanism**. Paper text must avoid "noise is necessary" and instead use "noise provides modest regularization."

**6-bit framing (Batch D verified):**

6-bit PCM (2/3 seeds successful) shows drift behaviour indistinguishable from 8-bit (0s→1d drop ≈ 0.1 pp vs 8-bit ≈ 0.04 pp). There is **no intermediate Pareto sweet spot** between 4-bit (drifty) and 8-bit (flat). Paper should frame 6-bit as "closer to 8-bit than to 4-bit" rather than as an independent precision-drift optimum.

### D3 — PCMPresetDevice decision: **VERIFIED**

**Ruling.** Batch B completed 2026-04-30. PCMPresetDevice reproduces the UnitCell story:

| Config | UnitCell (Batch A) | PCMPresetDevice (Batch B) | Gap |
|:---|---:|---:|---:|
| 8-bit fresh | 77.60% | 76.80% | -0.80pp |
| 8-bit drift drop (0s→1d) | -0.04pp | -0.07pp | ≈0 |
| 4-bit fresh | 76.68% | 76.38% | -0.30pp |
| 4-bit drift drop (0s→1d) | -4.01pp | -3.18pp | +0.83pp |

All gaps <1 pp. **Preset-agnostic claim is justified.** Do not run more PCMPresetDevice seeds unless a reviewer explicitly asks.

### D4 — 6-bit Pareto bridge: **CLOSED (no intermediate regime)**

**Ruling.** Batch D completed 2026-04-30.

| Seed | Source best | Fresh | Drift drop (0s→1d) | Status |
|:---|---:|---:|---:|:---|
| 123 | 77.33% | 77.36% | -0.16pp | ✅ |
| 456 | 69.07% | — | — | ❌ Diverged @ epoch 56 |
| 789 | 77.81% | 77.75% | -0.04pp | ✅ |

2-seed mean drift drop = **-0.10 pp**, indistinguishable from 8-bit (-0.04 pp). There is **no precision-drift sweet spot at 6-bit**; it behaves like 8-bit, not midway between 4-bit and 8-bit.

**Do not claim a 6-bit Pareto optimum in the paper.** Frame 6-bit as "drift-safe like 8-bit, but with 2× weight footprint and seed-dependent trainability." Mention seed456 divergence as a limitation (sensitivity to initialization at intermediate precision).

No additional 6-bit experiments needed pre-submission.

### D5 — 105 integration: **conditional promotion**

**Ruling.** Promote to a Discussion sub-paragraph + SI table only if **all** of:

- Same-architecture digital baseline (`deit_digital`) lands cleanly.
- Multi-seed (123/456/789) on at least 4 priority cells: `{deit, vit} × {proportional, digital}`.
- Reproducibility packet (SHA, environment, exact commands) is archived locally.

If any fails by submission window → frame as: "Cross-architecture validation in concurrent work suggests this generalization holds beyond Tiny-ViT; a full study is reserved for future work."

### D6 — 107 integration: **selective-layer pivot**

**Ruling.** Agree with Codex. If HAT all-layer KV PPL stays > 1.20× digital baseline after 200–500 steps, **permanently pivot Work-2 to selective terminal-layer KV + HAT**. All-layer becomes negative control. This pivot is a **Work-2 narrative decision**, not a paper-1 input.

### D7 — Kill list: **APPROVED with one addition**

**Approved kills/freezes (Codex list):**
- Historical mixed-NL / MLP-protected route.
- More UnitCell repeat seeds (3 is enough).
- Non-HAT all-layer KV sweeps.
- Old contaminated R11D directories (`r11d_2_sigma020/` original).
- Non-PCM drift claims unless artificial drift protocol is explicitly defined.
- Broad literature-driven simulator knobs.

**Addition.** Also kill/freeze:
- **R11D-T1 (theory addendum: per-batch vs per-epoch)** — silently demoted. The cadence-difference theoretical argument is not closed (no R11D-6 confirmation), and pushing speculative theory into a paper that already has PAC-Bayes + SAM + Wager grounding adds attack surface without adding evidence. Keep what's already in `S_theory_ensemble_hat.tex`. Do **not** ship R11D-T1.
- **All Round-9/10 leftover dispatches that lack a corresponding output file by 2026-05-03.** If a dispatch hasn't produced an output in 7+ days, treat it as abandoned.

---

## 5. Risk register + reviewer attack patterns

| # | Attack | Likelihood | Severity | Defense |
|:-:|:--|:-:|:-:|:--|
| R1 | "8-bit parity weakens novelty." | High | Med | Frame regime-specifically (§2.3). 4-bit IS canonical deployment. PCM precision-drift makes the choice non-trivial. |
| R2 | "Cadence (per-batch vs per-epoch) is the lever, not architecture." | High | Med | Acknowledge openly in Discussion; cite that R11D-6 (cadence-matched Ensemble) is future work. Do not overclaim. |
| R3 | "Tobin 2017 domain randomization is equivalent." | Med | Low | `KIMI_R10G_NOVELTY_CONTRAST_20260425.md` already prepared; cite explicitly: structured-substrate-aware vs i.i.d. random. PAC-Bayes bound provides mechanism. |
| R4 | "PCM result is preset-specific." | Med | Med | Batch B/C settles this. If preset-specific, document as limitation; do not hide. |
| R5 | "Why is PCM 8-bit only ~78% when pure 8-bit is 87%?" | High | Med | Pulse-update non-linearity penalty (~9 pp). Honest disclosure. Discussion paragraph dedicated to this. |
| R6 | "4-bit drift makes the method unusable." | Med | Med | Explicit precision-drift trade-off table + curve. Position 8-bit as drift-safe reference; 4-bit as area-/energy-efficient with periodic-refresh requirement. |
| R7 | "V6 PHANTOM (95.82%) was fabricated." | Low (now) | High (if found) | Already fixed (82.58 single-seed). R11C verification step grep `95.82` → 0 hits. |
| R8 | "Word count exceeds Nature Electronics budget." | Med | Med | R11C H1 (08_appendix → SI) + ≤5,700 budget. |
| R9 | "Cross-references broken." | Med | High | R11C C2.1/2.2/2.3 + H3 dup labels + H4 orphans. |
| R10 | "Locked numbers drifted between Discussion and Abstract." | Low (with guard) | High | `scripts/_gpt/check_locked_numbers.py` enforces 14.64 / 87.28 / 86.16 / 82.58. |
| R11 | "Cherry-picking 3-seed across PCM but using single-seed elsewhere." | Med | Med | Document seed strategy in SI; explain why some experiments are single-seed (compute budget) and which key claims are 3-seed-confirmed. |
| R12 | "Pipeline contention between manual edits and `agents-do` runs." | Med | Med | While pipeline runs, no manual paper edits. AGENT_SYNC documents the rule. |

---

## 6. Pipeline operating model (CANONICAL going forward)

### 6.1 Coordination architecture

```
user ──► tasks/<task_id>.md ──► agents-do ──► broadcast.md ──► outputs/<task_id>.md
                                    │
                                    ├─► kimi (planner)
                                    ├─► ds_flash (coder)
                                    ├─► codex (reviewer)
                                    ├─► gemini (critic)
                                    └─► kimi_cli (doc)
```

### 6.2 Roles after paradigm shift

- **Claude** writes single self-contained `tasks/<task_id>.md` files. NO more multi-role dispatches.
- **DS** does GPU experiments + code. Direct-tmux jobs that are already running stay direct (do not migrate mid-flight).
- **Gemini** does plotting/figures + critic phase + hostile review. No paper text edits.
- **Kimi** plans + writes paper text in pipeline (planner / doc roles). Also handles theory / framing memos.
- **Codex** reviews in pipeline. Has been retired from dispatch authoring (out of credit).

### 6.3 Task file conventions

A pipeline task.md file MUST contain:

1. `task_id`, `priority`, `target output` path
2. **Background** — minimum context for cold-start agent
3. **Goal** — bullet form, specific deliverables
4. **Decision rule** — explicit Approve/Reject criteria for reviewer/critic
5. **Files to read** — exact paths
6. **Files to edit** — exact paths
7. **Constraints** — wording bans, word budget, zone discipline
8. **Specific output expected** — what goes in `outputs/<task_id>.md`
9. **Done definition** — measurable
10. **Locked-number guard step** — `python scripts/_gpt/check_locked_numbers.py` must pass

### 6.4 Tier fallback (from pipeline doc)

- **Tier 1 (default):** ds_flash code, codex review, gemini critic.
- **Tier 2:** REVIEW=double if Codex quota low.
- **Tier 3:** all kimi (CODE=kimi REVIEW=kimi CRITIC=kimi).

### 6.5 Anti-patterns

**Do NOT:**
- Manually decompose tasks across roles in chat once a task.md exists.
- Edit paper files directly while `agents-do` is running on them.
- Re-dispatch a role-specific instruction after task.md is fired (the pipeline has already routed it).
- Read pipeline-stage outputs mid-run; read the final `outputs/<task_id>.md` only.
- Skip the locked-number guard step.

---

## 7. Task queue (pipeline format) — priority-ordered

### 7.1 P0 — submission-blocking (write & fire BEFORE defense)

| # | task.md filename | Status | Purpose |
|:-:|:--|:--|:--|
| 1 | `tasks/r11d_4bit_pathb_narrative_integration.md` | **FIRED** (Kimi → DS in flight) | Integrate 4-bit Path B revival into Discussion + cover letter + SI table. |
| 2 | `tasks/r11c_paper_integrity_fixit.md` | READY | Bundled close of 11 paper integrity issues. Compile gate: `latexmk` RC 0, zero undef, ≤ 5,700 words. |
| 3 | `tasks/r11d_pcm_precision_drift_integration.md` | TO WRITE | Integrate PCM 4-bit/8-bit 3-seed + drift curves into Methods + Results §5.X + SI. Locked numbers from §3.2 above. |
| 4 | `tasks/r11d_envelope_table_and_figure.md` | TO WRITE (after Batch B/C) | Method × regime table + iso-accuracy operating envelope figure. Includes UnitCell + (conditional) Device preset. |
| 5 | `tasks/r11_zone_taxonomy_finalize.md` | TO WRITE | Lock zone-tagging: 3A/3B/3C + new "AIHWKit comparison" zone + new "PCM substrate" zone. Finalize zone provenance footnotes. |
| 6 | `tasks/r11_g_hostile_v2_final.md` | TO WRITE (after #2-#5 land) | Fire G-HOSTILE-V2 hostile review on the integrated manuscript. Gemini produces submission-readiness verdict. |
| 7 | `tasks/r11_cover_letter_polish.md` | TO WRITE | Cover letter final polish with locked numbers and editorial-summary tight phrasing. |
| 8 | `tasks/r11_compile_clean_room_check.md` | TO WRITE (final) | Clean-room rebuild: `make clean && latexmk -pdf`, locked-number guard, banned-wording scan, figure-resolution check. |

### 7.2 P1 — strengthens submission, defense-aligned

| # | task.md filename | Trigger | Purpose |
|:-:|:--|:--|:--|
| 9 | `tasks/r11d_pcm_preset_sensitivity.md` | Batch B/C completes | Document UnitCell vs Device preset comparison. Conditional wording per D2/D3. |
| 10 | `tasks/r11d_6bit_pareto_pilot.md` | After Batch B/C | One-seed 6-bit pilot. Decision rule: ≥ 0.5pp of 8-bit OR drift between 4/8-bit → run seeds 456/789. |
| 11 | `tasks/r11_defense_qa_alignment.md` | After P0 lands | Align defense Q&A prep (KIMI_DEFENSE_QA_PREP) with final paper claims. Verify every Q has a paper section anchor. |
| 12 | `tasks/r11_thesis_chapter_skeleton.md` | After P0 lands | Map paper sections + R11D-T2 envelope into thesis chapters. Identifies thesis-only retained data. |

### 7.3 P2 — opportunistic, useful for thesis, NOT submission-blocking

| # | task.md filename | Trigger | Purpose |
|:-:|:--|:--|:--|
| 13 | `tasks/r11_105_proportional_validation.md` | If 105 same-arch + multi-seed lands clean | Promote 105 result to Discussion sub-paragraph + SI table. |
| 14 | `tasks/r11_industrial_brief_polish.md` | Post-defense | Polish GEMINI_INDUSTRIAL_BRIEF for stakeholder distribution. |
| 15 | `tasks/r11_grant_proposal_outline.md` | Post-defense | Polish GEMINI_GRANT_PROPOSAL_OUTLINE for the next funding cycle. |
| 16 | `tasks/r11_blog_draft_polish.md` | Post-defense | Polish KIMI_BLOG_DRAFT for public communication. |

### 7.4 KILLED / FROZEN (do not write)

- ~~R11D-T1 theory addendum (per-batch vs per-epoch)~~ — see D7.
- ~~R11D-6 cadence-matched Ensemble HAT~~ — frame as future work in Discussion.
- ~~R11D-4 PCM (single-seed) follow-up~~ — superseded by R11D-7 3-seed.
- ~~Round-9/10 dispatches without outputs by 2026-05-03~~ — abandoned.
- ~~Mixed-NL MLP-protected reruns~~ — superseded by R11C C5 introduction rewrite.
- ~~Progressive quantization pre-submission~~ — defer to revision response.
- ~~107 all-layer KV experiments beyond minimal kill criterion~~ — pivot to selective.

---

## 8. Defense alignment (paper sections ↔ Q&A anchors)

Every defense question must have a corresponding paper section. Use this map to align KIMI_DEFENSE_QA_PREP with final paper:

| Defense Q theme | Paper section anchor | Locked numbers cited |
|:--|:--|:--|
| "Why is fixed-mask HAT insufficient?" | §2 (related work, C3 fix) + §5.1 (Standard HAT collapse) + Fig S-Standard-Collapse | 10.00% |
| "What does Ensemble HAT actually do?" | §3 (Methodology, Algorithm 1) + §5.2 | 86.16 ± 0.19% |
| "Compared to AIHWKit, why is your method better?" | §6.X (Comparison to established analog HAT primitives) | 14.64 vs 86.16 (4-bit); 87.28 vs 86.16 (8-bit) |
| "Why 4-bit canonical?" | §4 (Experimental setup) + §5.6 (iso-accuracy envelope) | 4-bit = realistic deployment precision |
| "PCM physics — what's the substrate story?" | §5.X (PCM realism) + Fig precision-drift | 76.68 / 77.60 / 4.78 pp drift |
| "PAC-Bayes / SAM / Wager — what's the theory?" | SI §S_theory_ensemble_hat | structural analogue, not equivalence |
| "Why is your novelty not Tobin 2017 domain randomization?" | §6.X (novelty contrast paragraph) | structured-substrate vs i.i.d. random |
| "Limitations?" | §6 (limitations subsection) | 5pp gap to NL=1.0; 15pp gap to digital; PCM preset specificity (if applicable) |
| "Future work?" | §6 (future work) | cadence-matched Ensemble (R11D-6); progressive quantization; cross-simulator (CrossSim); analog KV-cache (Work-2) |

**Hard rule:** if a defense Q does not map to a paper anchor, either (a) add the anchor or (b) drop the Q from prep. Do NOT have unanchored defense answers.

---

## 9. 7-day execution path (to defense gate alignment)

Today: 2026-04-30 (Wed).

### Day 0 (today)
- Brief written (this file).
- Pipeline first-fire confirmed (R11D 4-bit narrative).
- Batch B/C running (PCMPresetDevice seed123).
- **Action:** commit `tasks/`, V6 fix, AGENT_SYNC paradigm block, this brief.

### Day 1 (Thu, 2026-05-01)
- Batch B/C should complete or be near completion.
- Decide D3 (PCMPresetDevice integration vs sensitivity).
- Fire `r11c_paper_integrity_fixit.md` (P0 #2).
- Write & fire `r11d_pcm_precision_drift_integration.md` (P0 #3).

### Day 2 (Fri, 2026-05-02)
- 6-bit pilot one-seed run.
- Write `r11d_envelope_table_and_figure.md` (P0 #4).
- Ingest 105 multi-seed return if available; decide D5.
- 107 selective-layer pivot decision (D6).

### Day 3 (Sat, 2026-05-03)
- Fire P0 #4.
- Write `r11_zone_taxonomy_finalize.md` (P0 #5).
- Mark all dispatches without outputs as abandoned (D7 addition).

### Day 4 (Sun, 2026-05-04)
- 6-bit seeds 456/789 if pilot warranted.
- Fire P0 #5.
- Write `r11_cover_letter_polish.md` (P0 #7).

### Day 5 (Mon, 2026-05-05)
- All P0 #1-#5 outputs landed.
- Fire `r11_g_hostile_v2_final.md` (P0 #6).
- Internal read-through (user, Claude).

### Day 6 (Tue, 2026-05-06)
- Address G-HOSTILE-V2 findings.
- Fire `r11_compile_clean_room_check.md` (P0 #8).
- Defense Q&A alignment (P1 #11).

### Day 7 (Wed, 2026-05-07)
- Submission bundle frozen.
- User reviews; co-author distribution if applicable.

**This is a TARGET, not a hard deadline.** The defense gate, not the calendar, governs submission. If Batch B/C reveals a substantive issue (e.g., PCMPresetDevice collapse forces a Discussion rewrite), shift the schedule by 1–2 days. Quality over speed.

---

## 10. Thesis vs paper bifurcation

The user's `compute_vit/` repo serves both Nature Electronics submission AND the PhD thesis. Bias: **retain MORE experiments, NOT fewer**.

### 10.1 In-paper (paper-1)

- P1 + P2 + P3 (§2.1)
- 8-bit σ sweep (R10E + R11D-2/3)
- 4-bit collapse (R11D-1)
- PCM UnitCell 3-seed + drift (R11D-7 / R11D-5a)
- Standard / Ensemble HAT cadence ablation (single seed, existing)
- Cross-instance transfer (existing)
- Theoretical grounding (PAC-Bayes + SAM + Wager) — `S_theory_ensemble_hat.tex`

### 10.2 Thesis-only (retained, not in paper)

- ConvNeXt C1-C9 + cross-architecture full matrix
- CIFAR-100 + Flowers-102 cross-dataset
- Tiny-ViT V1-V8 ablation full matrix (V6 = 82.58 single-seed)
- Retention V8 corrected (existing)
- Energy provenance (S_energy_provenance) — paper has summary, thesis has full
- 105 cross-architecture validation (deit/vit × HAT modes) — full thesis chapter
- Work-2 analog KV-cache exploration — separate thesis chapter
- All R11D experiments NOT in paper (R11D-4 single-seed, R11D-8 HAT-inspired-PCM, R11D-10 pure DoReFa, R11D-11 progressive bit precision)

### 10.3 Bifurcation rule

If a result was retained in `outputs/` or `paper2_aihwkit_baseline/checkpoints/` and is methodologically sound (not contaminated, not invalidated), it goes to thesis even if it doesn't make paper. **Do not delete data.** GitHub does not back it up; rely on local + manual archive (per `DATA_LOCATION_INDEX_20260429.md`).

---

## 11. What to do if I am unavailable

If I (Claude Opus) am out of context or off-line:

1. **For task spec writing:** read this brief + read 1-2 most recent task.md files for format. Write the next task.md following §6.3 conventions.
2. **For arbitration questions:** check D1-D7 in §4. If the question isn't covered, default to the conservative answer (e.g., "frame as limitation, not a strength").
3. **For number disputes:** §3 is canonical. Do not deviate without re-running the JSON.
4. **For pipeline ops:** §6 is canonical.
5. **For unfamiliar agents:** the pipeline doc at `/home/qiaosir/projects/流水线.md` is the operating manual.
6. **For escalation:** any decision touching publication, authorship, or scope expansion goes to the user, not to autonomous decision.

The user is a senior PhD candidate at NVIDIA Apamayo (per memory). Treat their judgment as the final authority. This brief is a tool for them, not a constraint on them.

---

## 12. Final words

This work has been the cleanest version of "honest science under publication pressure" I have seen across our many rounds. The temptation throughout was to overclaim — to call AIHWKit "weak", to hide 8-bit parity, to shoehorn 105 into the main spine, to chase a third paper. The path that survives reviewer scrutiny is the one we are on: **regime-specific method-superiority + substrate-physics enabled training + honest precision-drift trade-off**.

Three closing recommendations:

1. **Submit when defense allows, not earlier.** A submission that loses 4 weeks of polish costs more than a submission that misses an arbitrary deadline.

2. **Publish thesis-only data as a companion arXiv preprint.** All the data that doesn't fit paper-1 (cross-arch, cross-dataset, ablation) deserves a permanent home. A clean preprint also serves as a reviewer-deflection tool ("see preprint X for the full ablation matrix").

3. **Trust the pipeline.** It works. Resist the urge to manually orchestrate after a task.md fires. The four other agents (Kimi, DS, Codex, Gemini) collectively catch more than I can alone — Kimi's 87.28 ≠ 87.34 correction is proof.

The work is good. The story is honest. The numbers are locked. The pipeline is canonical. Defense-grade.

— Claude (Opus 4.7, max effort)
2026-04-30 CST
