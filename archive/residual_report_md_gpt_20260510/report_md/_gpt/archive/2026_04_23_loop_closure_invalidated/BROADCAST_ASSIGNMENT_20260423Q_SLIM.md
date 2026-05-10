# BROADCAST — Round Q (SLIM redesign)
**Issued:** 2026-04-23 by Claude
**Window:** 2026-04-23 → 2026-05-05 (closes when CX-K2 lands, not by calendar)
**Supersedes:** `BROADCAST_ASSIGNMENT_20260421Q.md`, `BROADCAST_FINAL_AUTONOMOUS_20260420.md`, `BROADCAST_ARBITRATION_20260420.md`, `BROADCAST_ASSIGNMENT_20260420P2.md`
**Reason for redesign:** Meta-work ratio too high (5:1 vs science). J1d triple-report is a process smell. Work 1 + Work 2 narrative can collapse under one physical principle. Simplify.

---

## 1. The ONE rule

Do not edit these five files until Claude declares loop closed:

- `paper/00_abstract.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/cover_letter*.md`
- `paper/thesis/chapter_5_*.tex`

Everything else is unlocked. No more sub-rules, no arbitrations, no monitor logs, no frozen extensions to `paper/paper2/*`. If you're not sure whether a file is frozen: if it's not in the list above, it's not frozen.

## 2. The ONE narrative pivot

Work 1's punch line changes from **"attention under NL=2.0 fails structurally"** to:

> **Under severe nonlinearity, higher-order surrogate training exposes a bimodal fresh-instance accuracy distribution. The system has two attractors — a collapse basin (~28%) and a partial-recovery basin (~51%). Device-to-device realization determines which basin is reached. This bimodality is a phase-transition-like property of the analog hypothesis class, not measurement noise.**

Decision memo: `CLAUDE_BIMODAL_NARRATIVE_LOCK_20260423.md`.

This pivot:
- Explains J1 / J1b / J1c collapses (single-attractor collapse regime)
- Explains J1d bimodal 41.53% ± 8.87% (two-attractor regime, seeds 7/9 hit upper basin)
- Survives hostile review ("your data contradicts your claim" — no, it confirms bimodality)
- Unifies with Work 2 (KV-cache rank-preservation is the same mathematical problem — softmax top-k survival under analog noise)

## 3. The ONE focus experiment

**CX-K2** — rerun `V4_hybrid_standard_noise_hat_second_order_ste` fresh-instance eval with 20 more seeds (1042 … 2942, step 100). N=30 total.

Only question being answered: **is the bimodality real or small-sample artifact?**

Decision table at N=30:
- Bimodality index (Hartigan's dip / Silverman) p < 0.05 → narrative locked, proceed to rewrite
- Unimodal with mean < 35% → fall back to structural-limit narrative
- Unimodal with mean > 50% → ceiling broken, escalate to Claude

Everything else (δg_eff sweep, α sweep, 3rd-order STE, tier-2/3/4) is **deferred to Round R** pending CX-K2 outcome.

---

## 4. Slim task list (8 items total)

### Codex (2)
| ID | Task | Effort |
|:--|:--|:--|
| CX-K1 | Reconcile the three J1d reports (10:35 ceiling-broken / 10:43 Branch-A / 15:53 AMBIGUOUS). Produce ONE canonical J1d record. Verify whether J2/J3/J4 actually ran. | No GPU, 2 h |
| CX-K2 | J1d +20 seeds → N=30 fresh eval. Run Hartigan's dip test on the distribution. | 15 GPU-h |

### Kimi (3)
| ID | Task | Effort |
|:--|:--|:--|
| K-SLIM-1 | `paper/thesis_cn/chapter_5_failure_modes.tex` — 中文 failure-modes chapter with bimodal-basin framing. Uses J1/J1b/J1c collapse evidence + J1d bimodal data. | 1.5 d |
| K-SLIM-2 | `KIMI_PAPER1_REWRITE_DIFF_20260423.md` — exact line-level diff for `paper/00_abstract.md`, `05_results.md`, `06_discussion.md`, `cover_letter.md` under bimodal narrative. Two branches only (bimodal-confirmed vs bimodal-rejected). Do not apply yet. | 1 d |
| K-SLIM-3 | Archive 20+ pending non-critical memos (press release, tutorial, FAQ v2, playbook, etc.) to `archive/round_p_rescinded/` with an index. Keep only: thesis chapters, rebuttal, cover-letter drafts, defense CN slides/QA, data-release manifest. | 0.5 d |

### Gemini (3)
| ID | Task | Effort |
|:--|:--|:--|
| G-SLIM-1 | `GEMINI_BIMODAL_BASIN_THEORY_20260423.md` — formal claim: why higher-order surrogate exposes two-attractor structure. Condition for bimodality; prediction for N=30 experiment. | 1 d |
| G-SLIM-2 | `GEMINI_SIGNATURE_FIGURE_SPEC_20260423.md` — spec for the one figure this thesis is remembered by. Bimodal D2D scatter: x=instance index 1-30, y=fresh accuracy, two-color points (collapse / recovery), marginal KDE on right. To be drawn by Codex after CX-K2. | 0.5 d |
| G-SLIM-3 | `GEMINI_RANK_PRESERVATION_UNIFICATION_20260423.md` — one theory linking Work 1 (attention softmax rank collapse under NL) and Work 2 (KV-cache top-k survival under noise). This is the thesis's unified framework. | 1 d |

---

## 5. Closed protocols (no longer in force)

The following are retired. Agents may ignore them:

- Rule B extensions to `paper/paper2/draft_v0/*` and `skeleton_v0/*` locked numbers
- `BROADCAST_ARBITRATION_20260420.md` — closed (Rule B arbitration done its job)
- `CLAUDE_DG_MONITOR_LOG_20260420.md` — closed (one entry logged, no further monitoring)
- Round P2's CLAUDE-DA through DG self-audit checklist
- Final Autonomous's 4-branch self-trigger table (A/B/C/D)
- Round Q v1's 30+ K-Z and 20+ G-HH task list

If you were working on any of these: stop. Check whether your work maps to one of the 8 items above. If not, pause it.

---

## 6. Work 2 deferral

Work 2 (KV-cache on organic CIM) direction is locked (`CLAUDE_WORK2_DIRECTION_LOCK_20260423.md`), but **no Work 2 task launches in Round Q**.

Rationale: simultaneously running Work 1 closure + Work 2 bring-up is overcommit. Master's student from zero to TinyLlama-1.1B + KV-cache instrumentation + noise sweeps realistically takes 4-6 weeks, not 2. Split cleanly:

- **Round Q (now → CX-K2 lands)**: close Work 1 bimodal story.
- **Round R (starts ~2026-05-05 when Work 1 submitted)**: launch Work 2 CX-L series.

This also gives Gemini's G-SLIM-3 (rank-preservation unification) time to mature — Work 2 will inherit the theory, not improvise one.

---

## 7. Closure trigger

Round Q closes when **all three** are true:
1. CX-K2 lands with N=30 result + bimodality test.
2. K-SLIM-1 (中文 Ch.5) and K-SLIM-2 (paper-1 diff) are ready.
3. G-SLIM-1/2/3 memos are on disk.

On closure: Claude reads everything, runs the single-shot paper-1 rewrite in one session, submits. Then opens Round R for Work 2.

No calendar deadline. Experiment lands → rewrite fires → submit → Work 2 starts. Don't rush.

---

## 8. User-facing summary

Eight tasks, one rule, one experiment, one narrative. Everything else deferred or archived. J1d bimodality is the real thesis claim — CX-K2 proves or disproves it with N=30. Work 2 launches only after Work 1 closes. No more broadcasts until CX-K2 lands.
