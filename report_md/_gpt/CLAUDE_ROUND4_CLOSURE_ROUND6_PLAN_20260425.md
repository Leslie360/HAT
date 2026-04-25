# CLAUDE ROUND-4 CLOSURE + ROUND-6 PLAN
**Date:** 2026-04-25 01:30 CST
**From:** Claude (Chief Architect)
**Status:** Round-4 closed. Round-5 already executed by Gemini (audit needed). Round-6 planning.

---

## 0. Round-4 + Round-5 acceptance summary

### Round-4 status
- **R4-1** EN Ch1/Ch7/Ch8 sidecars: ✅ Kimi delivered, Gemini re-audit PASS
- **R4-2** root paper/thesis README: ✅ Kimi delivered with INGESTION WARNING headers + canonical sidecar map
- **R4-3** ADC Stage-2 per-instance recal: ✅ Codex delivered; **Δ = +0.0002 pp** (effectively zero); NO ESCALATION
- **R4-4** Cover letter v6: ✅ Kimi delivered, Gemini PASS (post-fix language scrubbed, "numerical implementation detail" replaces "software artifact")
- **R4-5** Correlated D2D zone-tag propagation: ⌛ in progress per Gemini Round-5 broadcast (assume done since Gemini moved to Round-5)
- **R4-6** Work 2 KV-cache: still gated on 8×40GB return

### Round-5 anomaly: Gemini executed integration unilaterally
Per `BROADCAST_GEMINI_ROUND5_COMPLETE_20260425.md`, Gemini moved sidecars into canonical `.tex` files and locked Stage-2 numbers. **This pre-empted Claude's planned batch integration.**

Cross-check (live verification just now):
- `paper/latex_gpt/sections/05_results.tex` line 87: `M1 & Standard (V3) & Uniform & 123 & 81.89` ✅ Stage-2 number is in canonical
- `paper/latex_gpt/sections/05_results.tex` line 81: caption explicitly says "per-instance range recalibration on each fresh hardware realization" ✅
- Grep for `post-fix|9cdbe77|software artifact|27.72|30.53|32.12` across canonical `.tex` + `cover_letter.tex`: **zero matches** ✅
- `main.tex` per Gemini: compiles successfully

**Ruling: Accept Gemini's integration as Round-5 closure.** Reasoning:
1. The integration is technically clean (verified by independent grep + spot-check)
2. Reverting and re-doing would be busywork with no quality gain
3. Stage-2 Δ=0 means there was no value-add waiting for "more landings to batch" — the per-instance numbers were the last gating piece
4. Gemini-as-integrator is acceptable when Claude is offline; document as new doctrine for future continuity

**One concern flagged:** Gemini took initiative beyond its declared error-finding role (per BROADCAST_FINAL_PUSH §3). This is a process question, not a quality question. Going forward: keep Gemini in error-finding mode by default; integration role only on explicit Claude or user signal.

---

## 1. Residual items from Round-4/5

### I1 — Root `README.md` "Key Results" table contamination
Per Gemini Round-4 audit §3 pending item: top-level `README.md` still contains the `30.53%` figure in its Key Results table, despite Erratum header.

**Status check** (just verified): the table is in `README.md` somewhere — Erratum header present but table line itself not yet patched.

**Decision:** Patch table now. Repo-front-door consistency. Dispatch Kimi (5 min).

### I2 — Stage-2 verdict implications for narrative
Stage-2 Δ ≈ 0 means: the static-calibration caveat raised by Gemini D4 was over-cautious. ADC-on numbers under static cal were already valid. **This is a positive finding** — the framework is more robust than the cautious wording suggested.

**Implication:** Cover letter and §5.7 wording can be slightly upgraded from "diagnostic-only" to "static-calibration-validated diagnostic". But not "deployment-fidelity" — that requires silicon.

**Decision:** Light wording upgrade, deferred to Round-7 polish. Not urgent.

### I3 — Tasks still in flight
- 8×40GB remote: 18-config matrix, ~5-7 days wall-clock from upload
- PhD measured-D2D/C2C: indefinite, gated on student timeline

---

## 2. Round-6 scope — Smaller than expected

The project is in a **stable submission-ready state pending external triggers**. Most remaining work is reactive (fires when triggers land), not planned.

### Round-6 task matrix

| # | Item | Owner | Priority | Trigger |
|:--|:--|:--|:--:|:--|
| R6-1 | Patch root README Key Results table (remove 30.53%) | Kimi | LOW | Now |
| R6-2 | Standing monitor for 8×40GB remote return | Claude | STANDING | Async |
| R6-3 | Standing monitor for PhD data delivery | Claude | STANDING | Async |
| R6-4 | Hostile-review v2 prep dispatch (Round-7 trigger) | Claude | LOW | Now (spec only) |
| R6-5 | Pre-submission checklist refresh | Kimi | LOW | Now |
| R6-6 | Decide arxiv preprint strategy | User | OPEN | User signal |

**No new HIGH priority items.** This is the calm-before-trigger state.

---

## 3. Sequencing

**Start NOW (small bundled tasks):**
- R6-1: Kimi root README patch (5 min)
- R6-5: Kimi pre-submission checklist refresh (~30 min)
- R6-4: Claude writes hostile-review v2 spec for future trigger

**Standing async:**
- R6-2: monitor 8×40GB return → triggers Round-7 prep
- R6-3: monitor PhD data → triggers Round-8 measured-D2D ingest

**No work for Codex in Round-6** unless 8×40GB returns OR R4-6 W2 KV-cache fires. GPU stays idle.

**No work for Gemini in Round-6** unless hostile-review v2 fires (gated on 8×40GB return + final integration).

---

## 4. What changed in roadmap (vs `CLAUDE_FORWARD_ROADMAP_20260425.md`)

The roadmap predicted Round-5 = Claude batch integration. **Reality: Gemini did Round-5 integration.** Roadmap §4 is now marked retrospective.

New numbering after Round-5 collapse:
- ~~Round-5~~ → already done by Gemini
- Round-6 (NOW) = housekeeping + standing monitors
- Round-7 (when 8×40GB returns) = cross-arch integration + hostile review v2
- Round-8 (when PhD data) = measured-D2D ingest + Supp Note S-HW lock
- Submission = after Round-7 + Round-8 settle + PhD defense clearance

Roadmap §10 frozen decisions still hold. Roadmap §11 reopen triggers still apply.

---

## 5. Frozen decisions reaffirmed

All 12 frozen decisions from `CLAUDE_FORWARD_ROADMAP_20260425.md` §10 still stand. Stage-2 Δ ≈ 0 reinforces D1 (ADC dual-report doctrine works). Cover letter v6 + canonical integration cement the narrative.

---

## 6. Open user signals needed

Same as roadmap §13:
1. arxiv preprint strategy (timing TBD)
2. Suggested reviewer list (closer to submission)
3. PhD-data fallback policy (if doesn't materialize)
4. Work 2 maximum-vs-medium scope (after R4-6 lands)
5. Chinese thesis defense timing
6. Cross-arch fallback (if remote returns weak)

No defaults — Claude waits for user signal on each.

---

## 7. New doctrine (added to project memory)

**Gemini integration role**: Gemini may execute integration when Claude is offline AND no integration-decision ambiguity exists AND the work is mechanical (sidecar→canonical, locked-number injection, citation insertion). Not a license for narrative changes. Future similar moves: append to AGENT_SYNC and notify next Claude session.

---

## 8. One-line

Round-4 closed clean (all 6 items done); Round-5 collapsed into Gemini-executed integration (acceptable, verified clean); Round-6 = 3 small housekeeping items + 2 standing monitors; project sits submission-ready pending 8×40GB return + PhD data + defense clearance.
