# CLAUDE ROUND-3 CLOSURE RULING + ROUND-4 PLAN
**Date:** 2026-04-25 00:50 CST
**From:** Claude (Chief Architect)
**Status:** Round-3 closed. Round-4 planning.

---

## 0. Round-3 acceptance

All 6 Round-3 items accepted with one conditional caveat (header discipline dependency — see §2). Kimi + Codex + Gemini cross-review chain converged on clean state after ~4 iterations of scrub-audit-fix cycles.

**Confirmed:**
- R3-1 Thesis chapters: 8 chapters drafted (EN Ch4/5; CN Ch1/5/6/7; existing EN Ch6/7 verified clean). `.kimi_draft_v3` sidecars created, zone 3B scrubbed.
- R3-2 Correlated D2D (AR1): verdict = zone 3A bug-immune. Checkpoint `V4_hybrid_standard_noise_hat_best.pt` at NL=1.0 uniform noise, AMP disabled, eval-only. JSON byte-identical to tracked release artifact. No rerun needed.
- R3-3 ADC per-instance recal: Stage 1 patch + unit test landed. Stage 2 re-eval remains gated.
- R3-4 AMP decorators: patched, 9/9 tests pass (added 1 new regression test). Future-proofing only.
- R3-5 Paper sync: root-only stubs deleted, CREDIT.md migrated, diff clean. Root `paper/thesis/` stubs flagged for decision.
- R3-6 Work 2 KV-cache preliminary: still gated on (R3-1 ch5 ✅ done) + (8×40GB remote return ⏳). One gate cleared, other pending.

**Residual items discovered during Round-3:**
- 3 EN thesis chapters (`chapter_1_hat_instance_overfitting.tex`, `chapter_7_deployment.tex`, `chapter_8_outlook.tex`) have no sidecars — relying on WARNING headers to block ingestion. Real fix is sidecar creation.
- Supplementary groupwise-NL table rows (c)-(f): retained as footnoted pre-fix diagnostic. Reviewer-sensitive but deliberate editorial choice.
- ADC wording discipline: diagnostic-only language now pervasive, which is safer but must stay consistent in Work 2 preview.

---

## 1. Critical observation from Round-3 cross-reviews

A pattern emerged over the Round-3 iterations that deserves explicit doctrine-level attention:

**ADC-on numbers are "hook-based diagnostic", NOT "deployment-fidelity".** Gemini's D4 finding (static calibration on ideal pre-noise array) is being treated as a reviewer-vulnerability. Codex + Kimi convergence is: never claim ADC-on as deployment-fidelity until per-instance calibration re-eval (Stage 2) lands.

Implication for paper narrative: the §5.7 table headline should read as **"bounded upper-limit reference under idealized hook protocol"**, not "realistic deployment." This changes the subtle framing of the severe-NL story.

**Ruling:** Kimi's current "hook diagnostic" wording discipline is correct. Carry it through all Round-4 work. Do not promote ADC-on back to "deployment-fidelity" until Stage-2 per-instance calibration rerun lands with stable numbers.

---

## 2. RULING on remaining items

### Item I1 — 3 EN thesis chapters without sidecars (WARNING-blocked)

**Decision:** Create sidecars. Dispatch Kimi.

Rationale:
- WARNING headers are fragile safety mechanism. A future integration pass could accidentally ingest.
- Proper fix is sidecar (`.kimi_draft_v3`) for each, zone-scrubbed per R3-1 methodology.
- Estimated work: ~2-3 days for all 3 chapters.

### Item I2 — Root `paper/thesis/` stubs

**Decision:** Replace with README pointing to `compute_vit/paper/thesis/`. Dispatch Kimi (5 min housekeeping).

Rationale:
- Deleting entirely has symmetry concern — future user / agent might look at root path by habit.
- README points them to correct location. Simple and safe.

### Item I3 — Stage-2 ADC per-instance calibration re-eval

**Decision:** Fire NOW. Do not wait for 8×40GB remote.

Rationale:
- Original gate was "avoid double compute." 8×40GB remote is working on cross-arch validation (ViT-Small / DeiT-Small on TinyImageNet), NOT on re-running current Tiny-ViT M-series. No compute redundancy risk.
- ADC per-instance recalibration re-eval takes ~3-4 GPU-h on local (6 checkpoints × 10 instances × 5 MC). Local GPU is free after AMP test runs.
- Expected +0.2 to +0.8 pp recovery. If it lands in that range, paper narrative stays intact. If > 2pp recovery, reopen D4 finding severity assessment.
- Having the Stage-2 number lets Kimi promote §5.7 wording from "hook diagnostic" to "post-module-output hook diagnostic with per-instance calibration" — a stronger, more defensible claim.

Gate change: **GATE OPEN** for Stage 2.

### Item I4 — Work 2 KV-cache preliminary (R3-6)

**Decision:** HOLD until 8×40GB remote returns with cross-arch results.

Rationale:
- R3-1 chapter 5 gate cleared.
- 8×40GB gate not yet cleared.
- If cross-arch validation on ViT-Small/DeiT-Small returns strong (Ensemble HAT pattern reproduces), Work 2 preview can use ViT-Small as base model (more impressive than Tiny-ViT-5M).
- If cross-arch returns weak, Work 2 preview falls back to Tiny-ViT-5M baseline.
- Either way, waiting for remote result informs Work 2 design decision. Cost of waiting: near-zero (months of buffer).

### Item I5 — Integration pass

**Decision:** HOLD until all of (I1 sidecars, I3 Stage-2 re-eval, I4 Work 2 preview, R3-2 cover letter v5 update) land. Then one batch integration by Claude.

Rationale:
- Integrating now = patching 3+ more times as these land. Wasteful.
- Batch integration = one clean pass, one review round, one commit sequence.
- Timeline: estimated 1-2 weeks until all land. No submission pressure.

### Item I6 — Supplementary groupwise-NL table (rows c-f)

**Decision:** Keep footnoted as pre-fix diagnostic.

Rationale:
- Reviewer might poke at it, but the footnote + caption discipline makes it defensible.
- Removing the table entirely loses the "MLP-path localization" argument, which is a useful narrative piece.
- Accept reviewer risk, keep the table. If reviewer escalates, we can drop it in revision.

---

## 3. Round-4 task matrix

| # | Item | Owner | Priority | Dispatch | Time |
|:--|:--|:--|:--:|:--|:--|
| R4-1 | EN Ch1, Ch7, Ch8 sidecar creation | Kimi | HIGH | `DISPATCH_KIMI_ROUND4_EN_SIDECARS_20260425.md` | ~2-3 days |
| R4-2 | Root `paper/thesis/` README cleanup | Kimi | LOW | In R4-1 dispatch | ~5 min |
| R4-3 | ADC Stage-2 per-instance re-eval | Codex | HIGH | `DISPATCH_CODEX_ROUND4_ADC_STAGE2_20260425.md` | ~3-4 GPU-h |
| R4-4 | Cover letter v5 update with post-Round-3 state | Kimi | MEDIUM | `DISPATCH_KIMI_COVER_LETTER_V5_20260425.md` | ~1 day |
| R4-5 | Kimi-side correlated D2D zone tag update (R3-2 follow-up) | Kimi | LOW | In R4-1 dispatch (bundled housekeeping) | ~30 min |
| R4-6 | Work 2 KV-cache preliminary | Kimi + Codex | MEDIUM | Existing dispatch unchanged | Gated on 8×40GB |

---

## 4. Sequencing

**Start NOW (parallel):**
- R4-1 Kimi EN sidecars (largest)
- R4-3 Codex ADC Stage 2 (fire once GPU confirmed idle)
- R4-4 Kimi cover letter v5

**In parallel as housekeeping:**
- R4-2 root thesis README
- R4-5 correlated D2D zone tag update

**Wait on signal:**
- R4-6 Work 2 preview (8×40GB remote return)

**Then Claude:**
- I5 integration pass after R4-1/3/4 land + R4-6 decision (Round-5)

---

## 5. What stays unchanged

- NARRATIVE_PIVOT as sole narrative source of truth
- Zone partition 3A/3B/3C + new "hook-diagnostic vs deployment-fidelity" distinction
- Nature Electronics venue target
- PhD-graduation as sole submission gate
- No retraining under any item
- 8×40GB remote runs independently

---

## 6. Escalation triggers

- R4-3 Stage-2 recovery > 2pp: D4 finding severity was underestimated, reopen §5.7 narrative
- R4-3 Stage-2 recovery < 0pp (regression): something wrong with per-instance calibration code, halt integration
- R4-1 EN sidecars surface new zone 3B contamination not caught in R3-1: extend scrub gate, rerun grep
- 8×40GB remote returns with Ensemble HAT failing to reproduce on ViT-Small: reopen NARRATIVE_PIVOT §2 scenarios, possibly downgrade venue target

---

## 7. One-line

Round-3 closed clean (6/6 accepted with header-discipline caveat); Round-4 = 6 finish-line items (3 start now, 1 gated), integration one batch at end, submission remains PhD-graduation-gated.
