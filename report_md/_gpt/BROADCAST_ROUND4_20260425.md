# BROADCAST ROUND-4 — Finish-Line Items + Stage-2 ADC Gate Open
**Date:** 2026-04-25 00:55 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini
**Authority:** CLAUDE_ROUND3_CLOSURE_RULING_20260425.md
**Status:** ACTIVE

---

## 0. Round-3 closed clean

All 6 Round-3 items accepted. Multi-agent scrub-audit converged after ~4 iterations. Zero paper-safety blockers in `.kimi_draft_v3` sidecars + paper canonical files.

**Key new doctrine from Round-3 iterations:**
- ADC-on numbers are "hook-based diagnostic", NOT "deployment-fidelity" until Stage-2 per-instance calibration lands
- All ADC-related wording in thesis + paper + cover letter must use "hook diagnostic" or "post-module-output hook diagnostic" framing
- Per Kimi final audit: header discipline (SUPERSEDED / WARNING on originals) is safety mechanism only; real fix is sidecars everywhere

---

## 1. Round-4 scope — 6 items

| # | Item | Owner | Priority | Time |
|:--|:--|:--|:--:|:--|
| R4-1 | EN Ch1, Ch7, Ch8 sidecar creation | Kimi | HIGH | ~2-3 days |
| R4-2 | Root `paper/thesis/` README cleanup | Kimi | LOW | ~5 min |
| R4-3 | ADC Stage-2 per-instance recal re-eval (GATE OPEN) | Codex | HIGH | ~3-4 GPU-h |
| R4-4 | Cover letter v6 update | Kimi | MEDIUM | ~1 day |
| R4-5 | Correlated D2D zone-tag propagation | Kimi | LOW | ~30 min |
| R4-6 | Work 2 KV-cache preliminary | Kimi + Codex | MEDIUM | Gated on 8×40GB |

---

## 2. Dispatches issued

| Dispatch | File | Contains |
|:--|:--|:--|
| KIMI-ROUND4-EN-SIDECARS | `DISPATCH_KIMI_ROUND4_EN_SIDECARS_20260425.md` | R4-1 + R4-2 + R4-5 bundled |
| CODEX-ROUND4-ADC-STAGE2 | `DISPATCH_CODEX_ROUND4_ADC_STAGE2_20260425.md` | R4-3 with escalation thresholds |
| KIMI-COVER-LETTER-V5 | `DISPATCH_KIMI_COVER_LETTER_V5_20260425.md` | R4-4 |
| W2 KV-cache preview | `DISPATCH_KIMI_CODEX_W2_KV_CACHE_PRELIM_20260424.md` (unchanged) | R4-6 still gated |

---

## 3. Key decision: Stage-2 ADC gate OPEN

Original Round-3 gate on R4-3 was "avoid 8×40GB remote compute redundancy." **Resolved.** 8×40GB remote runs ViT-Small/DeiT-Small on TinyImageNet (not current Tiny-ViT M-series). No redundancy risk.

Stage-2 fires now. Expected +0.2 to +0.8 pp recovery. Escalation triggers:
- > 2 pp recovery: D4 finding severity was underestimated
- < 0 pp: implementation issue
- Both trigger pause on §5.7 integration

---

## 4. Parallel start (no dependencies)

- **Kimi**: R4-1 EN sidecars (start with Ch7 since it mirrors paper discussion most closely), parallel R4-2 cleanup + R4-4 cover letter + R4-5 zone tags
- **Codex**: R4-3 Stage-2 ADC re-eval when GPU confirms idle

## 5. Gated (wait)

- **R4-6 Work 2 KV-cache preview**: waits on 8×40GB remote return. Both gates now: (R3-1 ch5 ✅) + (8×40GB ⏳)

---

## 6. Integration strategy (restated)

**No integration pass in Round-4.** Claude does one batch integration after:
- R4-1 sidecars land (all 3 chapters)
- R4-3 Stage-2 numbers land (cover letter + §5.7 need these)
- R4-4 cover letter v6 lands
- R4-5 zone tags propagated
- R4-6 Work 2 preview decision made (keep for Round-4 integration or defer)

Estimated integration pass: Round-5, 1-2 weeks from now.

---

## 7. What stays unchanged

- NARRATIVE_PIVOT_20260424.md as single narrative source of truth
- Zone partition 3A / 3B / 3C
- ADC wording discipline: "hook diagnostic" until Stage 2 lands
- Nature Electronics venue target
- PhD graduation as sole submission gate
- No retraining

---

## 8. Agent-level summary

### Kimi
1. NOW: Start R4-1 Chapter 7 sidecar (highest content overlap with existing paper work; warms up context)
2. In parallel: R4-2 root cleanup (5 min), R4-5 zone tag propagation (30 min)
3. After R4-3 Stage-2 numbers land: R4-4 cover letter v6 with updated ADC headline
4. Continue: R4-1 Ch1 and Ch8 sidecars

### Codex
1. NOW: R4-3 Stage-2 ADC re-eval (gate open, GPU idle). ~3-4 GPU-h.
2. Signal via AGENT_SYNC when complete.
3. No other compute tasks.

### Gemini
1. STAND BY.
2. If R4-3 escalation triggers (>2pp or <0pp): Claude may request independent hook-audit review v2.
3. Otherwise no new Round-4 audit task.

---

## 9. Escalation gates (from CLAUDE_ROUND3_CLOSURE_RULING §6)

- R4-3 Stage-2 recovery > 2pp: reopen §5.7 narrative, D4 finding severity revisit
- R4-3 Stage-2 recovery < 0pp: implementation issue, halt integration
- R4-1 sidecars surface new zone 3B contamination: extend scrub, rerun grep
- 8×40GB remote returns with Ensemble HAT failing to reproduce on ViT-Small: reopen NARRATIVE_PIVOT §2, possibly downgrade venue

All have clear quantitative thresholds.

---

## 10. One-line

"Round-3 closed clean; Round-4 = 6 finish-line items (3 start now, 1 fires gated, 2 housekeeping), Stage-2 ADC gate open, integration one batch at Round-5, no submission pressure."
