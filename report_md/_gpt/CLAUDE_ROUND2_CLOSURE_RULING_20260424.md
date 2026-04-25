# CLAUDE ROUND-2 CLOSURE RULING + NEXT-BATCH DISPATCH PLAN
**Date:** 2026-04-24 22:30 CST
**From:** Claude (Chief Architect)
**Status:** Round-2 closed. Round-3 planning.

---

## 0. Round-2 acceptance

All 7 deliverables are accepted. Manuscript canonical state is integration-ready. Zero paper-safety blockers.

**Confirmed:**
- D1 ADC dual-report executed cleanly; 8-bit impact −0.10pp, 6-bit −2.81pp (consistent with existing iso-accuracy cliff story).
- D2 NL-guard patch validated; 7/7 + 8/8 tests pass.
- D3 §5.7 rewrite scrubbed of all bug-retrospective language; canonical files synced with v3 drafts.
- D4 Gemini ADC-hook audit: 6/8 PASS, 1 FAIL (static calibration) — moderate, non-blocking, documented as limitation.
- D5 THEORY-1 corrections applied; Supp Note S-Theory is pure methodology with qualified assumptions.
- Gemini G-AUDIT-CODE closure: 1 real bug (fixed), 2 intentional architecture decisions correctly classified, 1 low-severity AMP decorator item deferred.

---

## 1. RULING on open item: 6-bit ADC column

**Decision: Option A (accept deferred).**

**Rationale:**
- Codex recommendation aligns: sparse column (4/6 blank) visually overstates incompleteness.
- Kimi recommendation aligns: body prose already states the 6-bit cliff conservatively.
- The 63-point iso-accuracy map (Fig contour-map, zone 3A) already contains full 6-bit data — it's the authoritative source for 6-bit behavior. §5.7 table is about **training-condition × HAT-type matrix** at a fixed ADC setting, not an ADC sweep. Separation of concerns.
- Mixing sparse-coverage ADC sweep into the HAT-comparison table is bad table design. The two axes should stay separated.

**Action:** Option A stands. Keep 8-bit ADC-on as the §5.7 table headline, reference iso-accuracy map for full ADC sweep, retain the 6-bit spot-check sentence in body prose. No column additions, no rerun.

---

## 2. Round-3 scope — six non-blocking items

All are "polish / deepen / expand", none gate submission. PhD-graduation window absorbs all of these comfortably.

| # | Item | Owner | Priority | Time |
|:--|:--|:--|:--:|:--|
| R3-1 | **Thesis chapters 5-7 full text** (mitigation / physical realism / deployment) — CN side needs chapter_5_failure_modes, chapter_7_deployment still in `.kimi_draft_v2`; EN side has chapters but content drift from NARRATIVE_PIVOT | Kimi | HIGH | ~1-2 weeks |
| R3-2 | **Correlated D2D provenance audit** — numbers 86.33 / 84.57 / 82.12 (Supp Note S2 AR(1)) need zone verification + re-run attestation | Kimi + Codex | MEDIUM | ~1 day |
| R3-3 | **Per-instance ADC recalibration patch** — Gemini D4 FAIL 3.7; ~+0.2-0.8pp recovery on severe-NL numbers | Codex | LOW | ~30 min code + ~3 GPU-h re-eval |
| R3-4 | **AMP `@custom_fwd`/`@custom_bwd` decorators** — Gemini's new low-severity finding | Codex | LOW | ~10 min + regression |
| R3-5 | **Root `paper/` ↔ `compute_vit/paper/` sync** — housekeeping | Kimi | LOW | ~30 min |
| R3-6 | **Work 2 KV-cache preliminary experiment** (per DISPATCH_KIMI_W2_OUTLOOK §2.5) — upgrade Outlook from 1-page to medium-scope with one real decode measurement | Codex + Kimi | MEDIUM | ~1 week (after 8×40GB remote returns) |

---

## 3. Sequencing

**Start immediately (parallel, no dependencies):**
- R3-1 Kimi thesis chapter drafting
- R3-2 Kimi+Codex correlated-D2D audit
- R3-4 Codex AMP decorators (fits between other Codex tasks)
- R3-5 paper/ sync housekeeping

**Deferred with clear gate:**
- R3-3 Per-instance ADC recalibration: fire **after** 8×40GB remote returns (to avoid running two redundant ADC re-eval streams)
- R3-6 Work 2 KV-cache experiment: start **after** R3-1 thesis chapter 5 (mitigation) lands — keeps Kimi's context on deployment/mitigation fresh

**Not starting in Round-3:**
- Integration of manuscript (I do that after all Round-3 items settle)
- Submission prep (PhD-graduation-gated)
- Any retraining (none needed)

---

## 4. Dispatches to issue

1. `DISPATCH_KIMI_ROUND3_THESIS_20260424.md` — chapters 5-7 drafting plan, NARRATIVE_PIVOT alignment spec
2. `DISPATCH_KIMI_CODEX_CORRELATED_D2D_AUDIT_20260424.md` — joint audit for AR(1) numbers
3. `DISPATCH_CODEX_ROUND3_PATCHES_20260424.md` — AMP decorators + per-instance ADC recalibration (gated)
4. `DISPATCH_KIMI_PAPER_SYNC_20260424.md` — housekeeping
5. `DISPATCH_KIMI_CODEX_W2_KV_CACHE_PRELIM_20260424.md` — medium-scope preliminary (gated on R3-1 chapter 5)
6. `BROADCAST_ROUND3_20260424.md` — master broadcast

---

## 5. What stays unchanged

- NARRATIVE_PIVOT as sole narrative source of truth
- Zone partition 3A/3B/3C
- Nature Electronics venue target
- PhD-graduation as sole submission gate
- No retraining
- 8×40GB remote task on its own track (unchanged)

---

## 6. Integration readiness check

Per Kimi's status report, the canonical manuscript files are scrubbed and ready for Claude integration. Integration is **NOT** happening in Round-3; it happens after all Round-3 items settle or when user signals ready. This gives room for Round-3 content to land naturally rather than racing a clock.

Rationale: integrating now forces re-integration when R3-1 thesis chapters produce cross-references back into paper-1. Better to batch all edits into one final integration pass.

**Integration trigger:** user signal "integrate now" OR all Round-3 items closed OR PhD data lands (whichever first).

---

## 7. One-line

Round-2 closed clean. Round-3 = 6 polish/deepen items dispatched, integration deferred to batch-end, zero submission pressure.
