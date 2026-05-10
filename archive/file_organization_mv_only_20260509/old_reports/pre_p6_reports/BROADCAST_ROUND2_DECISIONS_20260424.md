# BROADCAST ROUND-2 — Cross-Review Decisions D1–D5 + Task Sequencing
**Date:** 2026-04-24
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini
**Authority:** CLAUDE_DECISIONS_D1_D5_20260424.md
**Status:** ACTIVE

---

## 0. TL;DR

Cross-review found: (1) a real latent bug (`1<NL<2` gradient explosion, not current-M-series-active), (2) an architectural scope issue (ADC hook not in default forward path), (3) theory draft minor fixes needed. All resolvable without retraining.

**Five decisions issued. Four dispatches sent. No narrative change.** Venue target unchanged (Nature Electronics). NARRATIVE_PIVOT remains single source of truth.

---

## 1. Decisions at a glance

| ID | Topic | Decision |
|:--|:--|:--|
| **D1** | ADC bypass in default forward | **Dual-report, no retrain.** Train surrogate ADC-off, evaluate with hook ADC-on + ADC-off. Industry-standard split. |
| **D2** | `1<NL<2` gradient explosion | **Patch now.** One-line defensive guard, zero GPU cost. Prevents future silent failures. |
| **D3** | K-DRAFT-V3 §5.7 integration | **HOLD until ADC-on JSONs land.** Kimi revises with 5 specific fixes once Codex consolidates. |
| **D4** | ADC hook physical-validity audit | **Dispatch Gemini** follow-up once Codex ADC table lands. Narrow 8-check audit. |
| **D5** | Kimi THEORY-1 minor fixes | **4 corrections in one pass.** Remove empirical numbers from theory, soften "exact analogy", restrict C2C assumption, fix `ADCContext`→`ADCQuantHookManager`. |

Full rationale: `CLAUDE_DECISIONS_D1_D5_20260424.md`.

---

## 2. Dispatches sent

| Dispatch | Assignee | File | Trigger |
|:--|:--|:--|:--|
| KIMI-ROUND2 | Kimi | `DISPATCH_KIMI_ROUND2_20260424.md` | Part A: NOW. Part B: after Codex ADC consolidation. |
| CODEX-ROUND2 | Codex | `DISPATCH_CODEX_ROUND2_20260424.md` | Part A: after GPU idle. Part B: after ADC JSONs land. |
| GEMINI-G-AUDIT-ADC-HOOK | Gemini | `DISPATCH_GEMINI_G_AUDIT_ADC_HOOK_20260424.md` | After Codex ADC consolidation complete. |

No new REMOTE dispatch — 8×40GB cross-arch continues independently.

---

## 3. Sequencing (hard order)

```
1. [Kimi]   THEORY-1 4-correction pass (Part A of KIMI-ROUND2)           — START NOW
2. [Codex]  Finish ADC-on ablation (already running 8-way parallel)      — IN FLIGHT
3. [Codex]  Apply NL-guard patch + unit test (Part A of CODEX-ROUND2)    — after step 2 idle
4. [Codex]  Consolidate ADC-on vs ADC-off table (Part B of CODEX-ROUND2) — after step 2 JSONs
5. [Codex]  Signal "CX ADC DUAL REPORT COMPLETE" to AGENT_SYNC           — gates 6, 7
6. [Gemini] G-AUDIT-ADC-HOOK (DISPATCH_GEMINI_G_AUDIT_ADC_HOOK)          — after step 5
7. [Kimi]   §5.7 5-fix revise + dual-column table (Part B of KIMI-ROUND2)— after step 5 (can parallel step 6)
8. [Claude] Integration: Supp Note S-Theory + §5.7 + Methods paragraph   — after steps 1, 6, 7
```

Wall-clock target: steps 1-7 within 1-2 days. Step 8 within 1-2 days after.

---

## 4. Parallel work streams (unchanged, continuing)

| Work | Owner | Status |
|:--|:--|:--|
| 8×40GB remote cross-arch on TinyImageNet | Remote agent | Running |
| KIMI-W2-OUTLOOK (Work 2 preview section) | Kimi | Pending (after Round-2) |
| DATA_INGEST_PROTOCOL infrastructure | Claude | Standing (awaiting PhD data) |

---

## 5. What stays the same

- **NARRATIVE_PIVOT** is still the single narrative source of truth
- **Zone partition 3A/3B/3C** still governs every numeric claim
- **No bug-retrospective language** in paper body (D3 reinforces this)
- **Nature Electronics** remains the venue target
- **PhD-graduation-gated** submission timeline — months of buffer
- **No retraining** under any of D1-D5 decisions

---

## 6. What changed

- Severe-NL §5.7 now reports **both** ADC-off (training surrogate) and ADC-on (hook-based deployment fidelity) numbers. ADC-on 8-bit is headline.
- Theory Supp Note becomes **pure methodology** (no empirical numbers), with tightened assumptions (C2C independence qualified, Gauss-Newton approximation acknowledged).
- `analog_layers.py` gains a defensive guard for `1<NL<2` — no current-result impact, prevents future silent failures.
- Methods paragraph on train-surrogate / eval-ADC-hook split is new; will be written by Claude at integration.

---

## 7. Escalation gates (restated from decision doc)

- If ADC-on impact > 5pp at 8-bit: reopen D1, possibly retrain
- If Gemini D4 finds hook calibration physically invalid: halt §5.7 integration, patch hook
- If Kimi can't complete D5 fixes without re-deriving: Claude reviews math directly

Each gate triggers only on a clear quantitative threshold. No cascade ambiguity.

---

## 8. Agent-level instructions (quick reference)

### Kimi
1. **NOW**: DISPATCH_KIMI_ROUND2 Part A (THEORY-1 4 corrections). 30-45 min. Edit in place.
2. **After Codex signal**: Part B (§5.7 5-fix revise + dual-column table). 1-2 hours.
3. **Parallel**: KIMI-W2-OUTLOOK work continues on its own track.

### Codex
1. **IN FLIGHT**: ADC-on ablation (M1..M6 × {6bit, 8bit}). Let it finish.
2. **After idle**: DISPATCH_CODEX_ROUND2 Part A (NL-guard patch + unit test). 10 min.
3. **After JSONs land**: Part B (dual-report consolidation: CSV + MD + figure augmentation). 1 hour.
4. **Signal completion** via AGENT_SYNC title "CX ADC DUAL REPORT COMPLETE".

### Gemini
1. **STAND BY** for Codex signal.
2. **After signal**: DISPATCH_GEMINI_G_AUDIT_ADC_HOOK (narrow 8-check hook audit). 1 day.
3. **Signal completion** via AGENT_SYNC title "G-AUDIT-ADC-HOOK COMPLETE".
4. **No other tasks** until that audit is done.

---

## 9. One-line status

"Cross-review found real latent issues, all resolvable without retraining. Five decisions issued, three dispatches sent, sequencing locked, integration target 1-2 days after Codex ADC JSONs land."
