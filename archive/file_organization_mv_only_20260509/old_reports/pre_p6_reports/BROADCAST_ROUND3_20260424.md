# BROADCAST ROUND-3 — Polish + Deepen, No Submission Pressure
**Date:** 2026-04-24 22:30 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini
**Authority:** CLAUDE_ROUND2_CLOSURE_RULING_20260424.md
**Status:** ACTIVE

---

## 0. Round-2 closed clean

All 7 Round-2 deliverables accepted. Manuscript canonical files scrubbed of bug-retrospective language, zones 3A/3B/3C enforced, no paper-safety blockers. D1-D5 all closed.

**6-bit ADC column ruling: Option A (accept deferred).** Rationale: iso-accuracy map already has full 6-bit data in zone 3A; §5.7 table stays 2-column at 8-bit ADC + ADC-off, 6-bit retained as body prose. See CLAUDE_ROUND2_CLOSURE_RULING §1.

**Integration deferred** to batch end. No rush — PhD-graduation is the only submission gate.

---

## 1. Round-3 scope — 6 items, all polish/deepen/expand

| # | Item | Owner | Dispatch | Priority |
|:--|:--|:--|:--|:--:|
| R3-1 | Thesis chapters 5-7 full drafting | Kimi | `DISPATCH_KIMI_ROUND3_THESIS_20260424.md` | HIGH |
| R3-2 | Correlated D2D (AR1) provenance audit | Kimi + Codex | `DISPATCH_KIMI_CODEX_CORRELATED_D2D_AUDIT_20260424.md` | MEDIUM |
| R3-3 | Per-instance ADC recalibration patch | Codex | Part B of `DISPATCH_CODEX_ROUND3_PATCHES_20260424.md` | LOW (gated) |
| R3-4 | AMP decorators | Codex | Part A of `DISPATCH_CODEX_ROUND3_PATCHES_20260424.md` | LOW |
| R3-5 | paper/ ↔ compute_vit/paper/ sync | Kimi | `DISPATCH_KIMI_PAPER_SYNC_20260424.md` | LOW |
| R3-6 | Work 2 KV-cache preliminary | Kimi + Codex | `DISPATCH_KIMI_CODEX_W2_KV_CACHE_PRELIM_20260424.md` | MEDIUM (gated) |

---

## 2. Parallel launch (start NOW, no dependencies)

- **Kimi**: R3-1 thesis chapters 5-7 (largest single deliverable, ~1-2 weeks)
- **Codex + Kimi**: R3-2 correlated D2D audit (~1 day)
- **Codex**: R3-4 AMP decorators (~10 min, opportunistic)
- **Kimi**: R3-5 paper/ sync (~30 min, housekeeping)

## 3. Gated launches (wait for trigger)

- **R3-3 per-instance ADC recalibration re-eval**: gated on 8×40GB remote return OR explicit signal
- **R3-6 Work 2 KV-cache preliminary**: gated on (R3-1 chapter 5 first draft complete) + (8×40GB remote returned)

---

## 4. What's NOT in Round-3

- Integration pass (Claude does after Round-3 settles)
- Retraining (none needed)
- Submission prep (PhD-graduation-gated)
- New experiments beyond R3-6 preliminary
- Remote A100 (retired)
- 8×40GB remote: runs on its own track, not a Round-3 item, reports when done

---

## 5. Agent-level instructions

### Kimi (largest workload)

1. **NOW**: Start R3-1 thesis chapter 5 (CN failure modes). Budget ~1 week.
2. **NOW, parallel**: R3-5 paper/ sync (30 min).
3. **On Codex signal**: R3-2 text-side citation map + zone annotation.
4. **After R3-1 ch5 + R3-6 GO signal**: R3-6 §5.9 writeup after Codex report.
5. **Continuing from Round-2**: KIMI-W2-OUTLOOK still pending — can be absorbed into R3-6 when that fires.

### Codex

1. **NOW (opportunistic)**: R3-4 AMP decorators patch + test (~15 min).
2. **NOW, higher priority**: R3-2 data-side audit (~1 day).
3. **Stage 1 patch only** for R3-3: per-instance ADC cal code change + unit test. Do NOT fire the ~3 GPU-h re-eval until signaled.
4. **On R3-6 GO signal**: W2 KV-cache preliminary code extension + training + fresh-eval (~3-4 days).

### Gemini

1. **STAND BY.** No new audit dispatch in Round-3.
2. Available if Claude escalates a Round-3 finding requiring independent review.
3. **Do not** self-initiate audits of Round-3 deliverables unless asked.

---

## 6. Reporting cadence

Append status blocks to `AGENT_SYNC_gpt.md` as work lands. No fixed cadence; signal on deliverable completion.

Flag to Claude via `BROADCAST_*` or `DISPATCH_COMPLETE_*` files when an item fully closes.

---

## 7. What stays unchanged (restated for discipline)

- **NARRATIVE_PIVOT_20260424.md** is still the sole narrative source of truth
- **Zone partition 3A/3B/3C** governs every number
- **Nature Electronics** is the venue target
- **PhD graduation** is the sole submission gate
- **No retraining** under any Round-3 item
- **No bug-retrospective language** in paper body (reaffirmed)

---

## 8. Escalation triggers

- R3-2 finds correlated-D2D numbers are zone 3B (contaminated): halt Supp Note S2 integration, Codex re-runs, Kimi updates text
- R3-6 preliminary experiment shows framework does NOT extend to attention: halt §5.9 integration, flag to Claude, narrative reconsideration
- R3-3 per-instance ADC recalibration recovers > 2 pp (vs expected 0.2-0.8pp): investigate whether D4 finding was more severe than moderate

All triggers have clear quantitative thresholds. No cascade ambiguity.

---

## 9. One-line

"Round-2 closed, no blockers; Round-3 = 6 polish/deepen items, 4 start now, 2 gated, integration deferred to batch-end, submission remains PhD-graduation-gated."
