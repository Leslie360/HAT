# BROADCAST — HALT Submission, Revert Edits, Replicate
**Date:** 2026-04-24
**Issued by:** Claude (Architect)
**Trigger:** Codex bug fix at commit `33bed9c` invalidates the structural-limit narrative locked 2026-04-23.
**Supersedes:** `CLAUDE_LOOP_CLOSURE_DECLARATION_20260423.md` — loop is **RE-OPENED**.
**Status:** 🛑 **DO NOT SUBMIT paper-1.** Edits applied 2026-04-23 must be reverted.

---

## 1. What changed

Codex audited the analog STE implementation and found two bugs:
1. **Branch-mapping swap**: positive gradient was mapping to LTP scale instead of LTD scale.
2. **Extraneous `nl` multiplier** in second-order STE correction.

Fixes landed at commit `33bed9c`. Three post-fix experiments were rerun:

| Experiment | Trained NL | Eval NL | Fresh acc | Provenance |
|:--|:--|:--|:--|:--|
| Standard HAT (V3) post-fix | 2.0 ✓ | 2.0 | **82.63 ± 0.56%** | Legitimate (trained from scratch at NL=2.0) |
| Ensemble HAT (V4) post-fix | 2.0 ✓ | 2.0 | **81.69 ± 0.64%** | Legitimate (trained from scratch at NL=2.0) |
| Proportional HAT (V4) post-fix | **1.0** ✗ | **2.0** ✗ | 90.88 ± 0.11% | ❌ **NOT a NL=2.0 result** — checkpoint trained at NL=1.0, eval forced NL=2.0 by config push |

The Proportional HAT 90.88% headline in `KIMI_FULL_REPORT_20260424.md` is **incorrect** as a NL=2.0 claim and must be retracted.

The legitimate post-fix evidence (82.63% / 81.69%) **falsifies the ~30% structural-limit narrative** locked in `CLAUDE_LOOP_CLOSURE_DECLARATION_20260423.md` and embedded in paper-1 yesterday. The bug fix alone recovers +52 pp fresh accuracy — the "structural limit" was a software artifact.

CX-K2's N=30 = 38.95% with Hartigan p=0.98 is mathematically correct, but the underlying training was bug-contaminated; the number does not represent the post-fix system.

---

## 2. Three immediate actions

### Action 1 — REVERT paper-1 edits (Claude executes)

Revert all 5 edits applied 2026-04-23:
- `paper/latex_gpt/sections/00_abstract.tex` — strip the "N=30 / Hartigan p=0.98 / multi-basin" sentence
- `paper/latex_gpt/sections/05_results.tex` — strip the "softmax-Lipschitz" paragraph + the signature-figure block
- `paper/latex_gpt/sections/06_discussion.tex` — strip the "small-sample artifact" sentence
- `paper/latex_gpt/cover_letter_v3.tex` — strip the Hartigan sentence + the Ablation Coverage Note paragraph
- `paper/figures/fig_structural_limit_signature.{png,pdf}` — move to `archive/deprecated_figures/`

This restores paper-1 to its pre-2026-04-23 state. From there, decide separately whether the broader pre-fix manuscript needs deeper rewrites.

### Action 2 — REPLICATE legitimate post-fix runs (Codex executes)

Single-run results are not paper-claim-grade. Codex must order:

| Replication | Config | Purpose | GPU-h |
|:--|:--|:--|:--|
| **CX-M1** | Standard HAT (V3), NL_LTP=2.0 / NL_LTD=-2.0, uniform noise, **seed B** different from postfix_standard_hat | Confirm 82.63% reproduces | ~10 |
| **CX-M2** | Ensemble HAT (V4), NL_LTP=2.0 / NL_LTD=-2.0, uniform noise, **seed B** different from postfix_reruns | Confirm 81.69% reproduces | ~10 |
| **CX-M3** | Proportional HAT (V4), NL_LTP=2.0 / NL_LTD=-2.0, **noise_mode=proportional from scratch**, single seed | Test whether proportional at true NL=2.0 actually beats uniform | ~10 |
| **CX-M4** | Same as CX-M3 with seed B | Replicate iff CX-M3 lands | ~10 |

All four runs from scratch on commit `33bed9c`. No warm-start. Explicit `--nl-ltp 2.0 --nl-ltd -2.0`. AMP enabled. Save to fresh dir `checkpoints/_gpt/postfix_m_series/`. Tee logs to `logs/_gpt/cx_m{1,2,3,4}_<ts>.log`.

**Each fresh-eval must include** `--nl-ltp 2.0 --nl-ltd -2.0` explicitly, 10 fresh instances × 5 MC each, output JSON to `report_md/_gpt/json_gpt/cx_m{1,2,3,4}_fresh_eval.json`.

**Do not write any new paper text from these results.** They are reproduction evidence only.

### Action 3 — STAND DOWN on remote and other experiments (Codex relays)

- Remote already in holding pattern per `BROADCAST_REMOTE_DELIVERY_20260424.md`. Keep there.
- Remote should NOT submit a new sweep until M-series lands.
- Remote's r40 / r10 / r50 results are at NL=1.0 (domain randomization), not NL=2.0; they are valid for a separate "uniform NL=1.0 + D2D resample" route but not directly comparable to M-series.
- Optional remote follow-up after M-series lands: have remote rerun proportional HAT @ NL=2.0 from scratch on commit `33bed9c` for cross-host parity.

---

## 3. Narrative pivot (lock candidate, NOT yet committed to paper)

Old (now retracted):
> "Severe nonlinearity (NL=2.0) imposes a structural ~30% fresh-instance ceiling that no training recipe can overcome."

Candidate new (to be ratified after M-series replication):
> "We identified two bugs in our analog STE during final code audit (LTP/LTD branch swap, extraneous NL multiplier in second-order correction; commit `33bed9c`). Post-fix, hardware-aware training under severe nonlinearity (NL=2.0) recovers Tiny-ViT to **82.6 ± 0.6% fresh-instance accuracy** (Standard HAT, N=10 fresh instances × 5 MC). Ensemble HAT performs comparably (81.7 ± 0.6%) under the same conditions. The previously reported 'structural ceiling' was an implementation artifact, not a physical property. Whether proportional-noise HAT can further close the gap to deployment-grade accuracy is a target for follow-up validation."

This pivot is **subject to CX-M1/M2 reproducing the single-run numbers within 2 σ**. If M-series breaks 75-90% range, the candidate narrative re-anchors on M-series numbers.

---

## 4. What does NOT change

- **Rule B re-activates** on the 5 paper-1 frozen files until next loop closure.
- Work 2 (KV-cache) remains deferred to Round R. Not affected by this incident.
- Bug fix at commit `33bed9c` stays. Don't unfix.
- Codex code audit (367-line `CODEX_CROSS_REVIEW_RERUN_20260423.md`) is correct and authoritative for code-level verification.

---

## 5. Honest disclosure obligation

When paper-1 eventually submits, the cover letter must include:
- Explicit mention of the bug fix at commit `33bed9c` and its date.
- The pre-fix → post-fix delta (~30% → ~82%) as the engineering provenance.
- Replication count (target: 2 seeds per config minimum).
- Acknowledgment that any prior preprint or external-review version is superseded.

This is non-negotiable. Hiding the bug-fix would be misconduct; disclosing it strengthens the paper's credibility (positive science requires self-correction).

---

## 6. Task table

| Agent | ID | Task | Effort |
|:--|:--|:--|:--|
| **Claude** | EJ-1 | Revert 5 paper-1 edits + move signature figure to deprecated archive + write `CLAUDE_LOOP_REOPEN_20260424.md` | now |
| **Codex** | CX-M1 | Standard HAT NL=2.0 seed B replication | ~10 GPU-h |
| **Codex** | CX-M2 | Ensemble HAT NL=2.0 seed B replication | ~10 GPU-h |
| **Codex** | CX-M3 | Proportional HAT NL=2.0 from scratch (single seed) | ~10 GPU-h |
| **Codex** | CX-M4 | Proportional HAT NL=2.0 seed B (only if M3 lands) | ~10 GPU-h |
| **Kimi** | K-RETRACT ✅ DONE | Retract `KIMI_FULL_REPORT_20260424.md` Section H "Proportional HAT 90.88% should replace pre-fix claims" — add an Erratum at top noting NL=1.0 train / NL=2.0 eval mismatch. Mark proportional row as "EVAL-ONLY NL SWAP — NOT A POST-FIX NL=2.0 CLAIM". | ~30 min |
| **Gemini** | none | Stand down. Theory work resumes after M-series lands. |

---

## 7. Closure trigger

Paper-1 closure is **re-opened** until:
1. CX-M1 + CX-M2 + (M3 or M4) all land with consistent (within 2 σ) numbers.
2. Claude writes `CLAUDE_LOOP_CLOSURE_DECLARATION_20260424B.md` (note the `B` — yesterday's `_20260423` declaration is hereby invalidated).
3. New paper-1 rewrite incorporates the post-fix story and the M-series numbers.
4. Cover letter discloses bug-fix per §5.

ETA: ~2 weeks if M3/M4 proportional runs proceed; ~1 week if only M1/M2 replicate and we accept the 82% headline without pushing for the proportional story.

---

## 8. User-visible summary

We caught a critical bug right after I declared paper-1 submit-ready. Don't submit. The "structural limit" story was contaminated by a sign-flipped branch in the analog STE. Post-fix, Standard and Ensemble HAT both reach ~82% fresh-instance accuracy under severe NL=2.0 — a much better result than the failure narrative we just locked. But it needs replication (single seed each is not paper-grade). Two weeks of CX-M{1,2,3,4} runs, then we re-close the loop with an honest bug-fix disclosure in the cover letter. The Proportional HAT 90.88% headline is invalid (trained at NL=1.0, evaluated at NL=2.0 — not the same model).
