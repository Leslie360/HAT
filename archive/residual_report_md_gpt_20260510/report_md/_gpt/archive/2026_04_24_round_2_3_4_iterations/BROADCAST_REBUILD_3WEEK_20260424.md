# BROADCAST — 3-Week Rebuild Plan (Post-Bug-Fix)
**Date:** 2026-04-24
**Issued by:** Claude (Architect)
**Window:** 2026-04-24 → 2026-05-15 (3 weeks, no calendar pressure)
**Supersedes:** §6 task table of `BROADCAST_HALT_AND_REPLICATE_20260424.md` (the HALT itself stands).
**Status:** Paper-1 NOT submit-ready. Rebuild it properly. No rush. User has explicitly removed deadline pressure.

---

## 0. Scope reframing

User directive: 不着急 (no rush). The 1-week minimal-replication shortcut I proposed earlier is **withdrawn**. We do this right.

Agent roles (per user directive):
- **Codex** — main force. GPU + code work.
- **Kimi** — main force. Text + literature + audit.
- **Gemini** — **error-finding only**. Independent code/text audit. No new theory, no design specs, no decision memos. Treat Gemini as a senior reviewer who reads everything and finds inconsistencies.

Two simultaneous workstreams:
- **Workstream A** (Codex-heavy): replicate post-fix experiments + regression-proof the codebase + audit which canonical figures may have been touched by the bug.
- **Workstream B** (Kimi-heavy): rewrite paper-1 around the new evidence + Erratum-tag all contaminated memos + update Chinese thesis Ch.5.

Gemini reads outputs from both and reports errors.

---

## 1. Bug scope re-clarification (read this before doing anything)

The bug is in `analog_layers.py:227-288` STE backward. It manifests **only when both**:
1. Backward pass passes through this code (i.e., training uses analog STE, not pure FP)
2. Effective NL exponent ≠ 1 (i.e., NL_LTP ≠ 1.0 OR NL_LTD ≠ -1.0)

At NL=1.0/-1.0 (canonical), `ratio^(NL-1) = ratio^0 = 1` for both LTP and LTD scales — branches are arithmetically identical regardless of the swap. **Canonical results are bug-immune.**

Bug-immune (KEEP without re-running):
- All R-series CIFAR-10/100/Flowers-102 baselines
- Ensemble HAT @ NL=1.0: 86.37 ± 1.54%
- Standard HAT @ NL=1.0 collapse to 10%
- 6-bit ADC cliff
- All D2D, C2C sweeps at NL=1.0
- Iso-accuracy contour map (NL=1.0)
- OPECT zero-shot 88.53 ± 0.08% (calibrated NL ≈ 1)
- CrossSim cross-framework comparison
- Retention V8 79% plateau

Bug-contaminated (DEPRECATE, do not cite as evidence):
- Everything in §5.x severe-NL stress test (CX-J1/1b/1c/1d, CX-K1/2/3/4/5)
- N=30 = 38.95%, Hartigan p=0.98 (test math correct, data wrong)
- "30% structural ceiling" claim
- "joint training pinned at 30.53%" claim
- All bimodal / multi-basin / structural-limit narrative

Codex must double-check this scope claim independently — see §3 CX-AUDIT-1.

---

## 2. Three-week timeline

| Week | Focus |
|:--|:--|
| **Week 1 (04-24 → 04-30)** | Replication + audit — agents work in parallel, no rewrites yet |
| **Week 2 (05-01 → 05-07)** | Paper rewrite + Chinese thesis Ch.5 update + cross-checks |
| **Week 3 (05-08 → 05-15)** | Polish + figures + final Gemini error sweep + new closure declaration |

**Hard checkpoints**:
- 04-30 Friday: M-series + audit landed; Claude reviews.
- 05-07 Friday: paper drafts + cover letter v4 ready; Claude reviews.
- 05-15 Friday: ready-to-submit; Claude declares closure.

No calendar deadline beyond 05-15. If we slip, we slip.

---

## 3. CODEX tasks (main force, Workstream A)

### 3.1 Replication runs (M-series, all from scratch on commit `33bed9c`)

| ID | Config | Seed | GPU-h | Status |
|:--|:--|:--|:--:|:--|
| CX-M1 | Standard HAT V3, uniform noise, NL=2.0 from scratch | 123 | 10 | 🟡 launched |
| CX-M2 | Ensemble HAT V4, uniform noise, NL=2.0 from scratch | 123 | 10 | ⏳ queued |
| CX-M3 | Proportional HAT V4, **proportional noise from scratch**, NL=2.0 | 123 | 10 | ⏳ queued |
| CX-M4 | Proportional HAT V4 replication | 456 | 10 | ⏳ conditional on M3 landing |
| CX-M5 | Standard HAT V3 third seed (only if M1 vs postfix_standard_hat differ > 2σ) | 456 | 10 | ⏳ conditional |

All runs use `--nl-ltp 2.0 --nl-ltd -2.0` explicit, AMP on, save to `checkpoints/_gpt/postfix_m_series/cx_m{N}_<config>_seed{S}/`. Each fresh-eval is 10×5 with explicit NL flags. JSON to `report_md/_gpt/json_gpt/cx_m{N}_fresh_eval.json`.

### 3.2 Bug-immunity audit (CX-AUDIT-1, NO GPU, ~3 h)

Independently verify the scope claim in §1: "canonical NL=1.0 results are bug-immune".

Method:
- Symbolic check: at NL_LTP=1.0, NL_LTD=-1.0, show `pow(ratio, 0) = 1` for any ratio in [0,1], thus LTP/LTD scales are identical and branch swap has no effect.
- Numerical check: load one canonical NL=1.0 checkpoint (e.g., postfix_standard_hat is at NL=2.0; pick a fresh canonical R-series checkpoint instead), reproduce its fresh-eval at NL=1.0 with current commit `33bed9c` code, confirm it matches the previously reported number within MC noise.
- For each canonical paper figure (Fig 4 / Fig 5 / iso-contour / case-study / retention), record which checkpoint it draws from and the training NL used. Confirm none used NL ≠ 1 OR second-order STE.

Output: `CODEX_BUG_IMMUNITY_AUDIT_20260424.md` with a table mapping every paper figure to its source checkpoint and bug-immunity status.

### 3.3 Regression test (CX-REGRESSION, ~2 h)

Add a permanent test that prevents the train/eval NL mismatch (the trap that produced the false 90.88% Proportional HAT headline):

- New test in `test_dual_bug_fix.py` (or a new `test_eval_provenance.py`):
  - Load any analog checkpoint
  - Assert `eval_NL == checkpoint.exp_cfg.NL` unless `--allow-eval-nl-override` is explicitly set
  - Default: warn-and-abort on mismatch
- Patch `eval_fresh_instances_postfix.py` to read NL from checkpoint metadata as default; CLI override only with explicit `--allow-eval-nl-override` flag.

Output: `CODEX_REGRESSION_TEST_20260424.md` documenting the new test + commit hash.

### 3.4 Optional: post-fix re-evaluation of canonical Ensemble HAT (CX-CANONICAL-RECHECK, ~2 GPU-h)

Even though canonical NL=1.0 should be bug-immune, run **one** sanity check:
- Re-eval the canonical V4 Ensemble HAT @ NL=1.0 checkpoint with commit `33bed9c` code, 10×5 fresh.
- Confirm it lands at 86.37 ± 1.54% (within 2 σ of original).

If it does → bug-immunity confirmed empirically, the §1 scope claim is verified.
If it doesn't → much bigger problem, escalate immediately to Claude.

Output: `CODEX_CANONICAL_RECHECK_20260424.md`.

### 3.5 Codex hygiene rules (continuous)

- All M-series runs: tee logs to `logs/_gpt/cx_m{N}_<ts>.log`.
- One CX_M{N}_SUMMARY.md per landing.
- No simultaneous GPU jobs.
- If any M-series result lands < 70% or > 90%, do not auto-launch the next; escalate to Claude.
- Provenance discipline: every saved artifact must carry checkpoint path + commit hash + NL train + NL eval in metadata.

---

## 4. KIMI tasks (main force, Workstream B)

### 4.1 Erratum / contamination tagging (K-ERR series, Week 1)

| ID | Task | Effort |
|:--|:--|:--|
| K-ERR-1 | ✅ already done — Erratum at top of `KIMI_FULL_REPORT_20260424.md` retracting Proportional 90.88% | done |
| K-ERR-2 | Sweep all `_gpt/` Kimi memos written 2026-04-21 → 04-23 that referenced "30% structural ceiling" or "bimodal basin" or "Hartigan p=0.98". Add an Erratum stub at top of each: "DEPRECATED 2026-04-24 — based on bug-contaminated data; see commit 33bed9c audit. Do not cite as evidence." | 2 h |
| K-ERR-3 | Same sweep for `paper/thesis_cn/chapter_5_failure_modes.tex` — add Chinese 勘误 paragraph at top, do NOT delete. Update Chinese thesis Ch.5 will happen in Week 2. | 1 h |

### 4.2 Paper-1 rewrite drafts (K-DRAFT series, Week 2)

| ID | Task | Effort |
|:--|:--|:--|
| K-DRAFT-1 | Rewrite §5.x severe-NL subsection: replace "structural limit / falsification" with "post-fix HAT recovery to 82% under NL=2.0". Use placeholder `[CX-M{1,2,3,4} pending]` for any number not yet locked by replication. Save to `paper/latex_gpt/sections/05_results.tex.kimi_draft_v2`. Do not overwrite the live `.tex` — Claude integrates at closure. | 2 d |
| K-DRAFT-2 | Rewrite cover letter to v4: include Erratum paragraph (commit 33bed9c, pre/post delta, replication count, prior preprint superseded). Save as `cover_letter_v4.tex.kimi_draft`. | 1 d |
| K-DRAFT-3 | Rewrite abstract: drop "30% structural ceiling" phrasing, add post-fix framing with placeholder. Save as `00_abstract.tex.kimi_draft_v2`. | 0.5 d |
| K-DRAFT-4 | Rewrite §6 Discussion limitation paragraph: drop bug-contaminated structural-limit claim, replace with "severe NL leaves residual 4 pp gap vs canonical". Save as `06_discussion.tex.kimi_draft_v2`. | 0.5 d |
| K-DRAFT-5 | Audit `paper/latex_gpt/supplementary.tex` for any reference to bug-contaminated numbers; produce a diff list (do not edit yet). | 1 d |
| K-DRAFT-6 | Update `paper/thesis_cn/chapter_5_failure_modes.tex` to the new framing in Chinese. This becomes the canonical thesis Ch.5. | 2 d |

### 4.3 Venue research (K-VENUE-1, Week 2-3)

Compare submission fit for: Nature Electronics, Nature Communications, Nature Comm Engineering, Sci Adv, Adv Sci, Adv Mater. For each:
- Aim/scope match
- Recent organic-CIM / analog-DNN / hardware-aware ML papers (2024-2026)
- Typical word/figure limits + supplementary policy
- Cover-letter expectations (especially regarding errata / preprint disclosure)

Output: `KIMI_VENUE_COMPARISON_20260505.md` with ranked recommendation. Default rank: Nature Electronics > Nature Communications > Nature Comm Engineering.

### 4.4 Final consistency audit (K-AUDIT-FINAL, Week 3)

After M-series numbers are filled in by Claude:
- Run `check_locked_numbers.py` (if exists) across all .tex files
- Cross-check every cited number appears in canonical JSON or M-series JSON
- Flag any orphan number for Claude

Output: `KIMI_FINAL_NUMBER_AUDIT_20260513.md`.

### 4.5 Kimi hygiene rules (continuous)

- All draft files saved with `.kimi_draft_v2` suffix; never overwrite live `.tex`. Claude does the integration at closure.
- All numbers in drafts are either (a) bug-immune from canonical, or (b) post-fix from M-series, or (c) `[TBD]` placeholder. Never invent.
- Chinese thesis lives in `paper/thesis_cn/`; English everywhere else.
- One AGENT_SYNC entry per task closure.

---

## 5. GEMINI tasks (error-finding only — limited scope per user directive)

Gemini is **not** doing theory, design, or strategy this round. Three specific error-hunting tasks only:

### 5.1 G-AUDIT-CODE (Week 1, ~1 d)

Independently audit `analog_layers.py` at commit `33bed9c` from a different angle than Codex. Specifically:
- Look for **third bugs** Codex's audit missed
- Verify the second-order STE branch mapping under edge cases (NL=1.0 limit, NL=0 limit, NL > 3 extrapolation)
- Check if AMP / GradScaler interacts safely with the custom STE
- Check if `convert_to_hybrid` correctly propagates noise mode + NL through nested layers

Output: `GEMINI_INDEPENDENT_CODE_AUDIT_20260427.md` — list of issues found OR explicit statement "no further bugs found beyond commit 33bed9c fixes".

### 5.2 G-AUDIT-TEXT (Week 2-3, ~2 d, in batches)

Read every Kimi draft (`*.kimi_draft_v2`) as soon as it lands and find:
- Internal inconsistencies (number A in one paragraph contradicts number B in another)
- Stale references to deprecated narrative
- Claims that exceed evidence
- Citation drift
- LaTeX label/ref mismatches

Output: `GEMINI_TEXT_AUDIT_<docname>_<date>.md` per draft. One short memo per draft, just an issue list. No rewrites.

### 5.3 G-HOSTILE (Week 3, ~1 d)

Run a hostile-reviewer simulation against the new framing. Specifically:
- 5 strongest reviewer attacks against "post-fix HAT recovers to 82%" headline
- 5 strongest reviewer attacks against the Erratum disclosure (e.g., "this paper had a critical bug — what else might be wrong?")
- Response paths for each

Output: `GEMINI_HOSTILE_REVIEW_POST_FIX_20260513.md`.

### 5.4 What Gemini does NOT do this round

- No theory memos
- No design specs
- No "decision tree" memos
- No paper-2 / Work 2 work
- No new memo unless explicitly requested above
- No ratification or audit beyond above three tasks

If Gemini is tempted to write something else: stop. Write nothing.

---

## 6. CLAUDE tasks (audit + integration, three checkpoints)

| ID | When | Task |
|:--|:--|:--|
| CLAUDE-FA | 2026-04-30 (Week 1 close) | Audit M-series landings + CX-AUDIT-1 + CX-REGRESSION + K-ERR-{1,2,3} + G-AUDIT-CODE. Decide whether bug-immunity claim holds; ratify M-series numbers as paper-claim-grade. |
| CLAUDE-FB | 2026-05-07 (Week 2 close) | Audit K-DRAFT-{1..6} + K-VENUE-1 + G-AUDIT-TEXT memos. Decide narrative pivot final wording; pick venue. |
| CLAUDE-FC | 2026-05-15 (Week 3 close) | Audit K-AUDIT-FINAL + G-HOSTILE. Integrate all Kimi drafts into live .tex files; commission new signature figure if needed; rebuild PDF; write `CLAUDE_LOOP_CLOSURE_DECLARATION_20260515.md`. |

Claude does NOT issue intermediate broadcasts unless something breaks.

---

## 7. Hard rules (enforced for the full window)

1. **No paper-1 frozen-file edits** until CLAUDE-FC. The 5 frozen files (abstract, results, discussion, cover letter, thesis Ch.5) are owned by Claude during integration. Kimi writes drafts as `.kimi_draft_v2`, never live.
2. **No GPU contention** — only one CX-M training at a time.
3. **No silent number swaps** — every number change must be traceable to a JSON in `json_gpt/` or `csv_gpt/`.
4. **No new agent invented** — Codex + Kimi + Gemini only. Remote remains in holding pattern.
5. **No Work 2 work** — KV-cache / Round R remains deferred until paper-1 submitted.
6. **Cover letter must disclose bug fix** — non-negotiable, baked into K-DRAFT-2.

---

## 8. Failure modes and fallbacks

| Failure | Response |
|:--|:--|
| M1 deviates from postfix_standard_hat (82.63%) by > 2 σ | Run M5 (third seed); flag to Claude. Don't rewrite paper around uncertain number. |
| M3 proportional under-performs uniform | Drop proportional from §5.x; keep uniform-only headline. |
| CX-AUDIT-1 finds canonical NL=1.0 results contaminated | **Major escalation** — paper-1 fundamental rewrite needed. Halt all Kimi drafts. Claude designs new round. |
| Gemini finds a third bug | Same — escalate, halt rewrites until fix lands and re-evaluate scope. |
| K-DRAFT timing slips beyond Week 2 | Acceptable. We're not racing. Claude waits. |
| Remote returns useful proportional NL=2.0 result before CX-M3 finishes | Use it as supporting evidence; do not let it overwrite local M3. |

---

## 9. User-visible summary

Three weeks, no rush. Codex re-runs four post-fix replications + verifies bug scope + adds a regression test against the train/eval-NL mismatch trap. Kimi tags all contaminated memos as deprecated, then drafts new §5 / abstract / cover-letter / Chinese thesis Ch.5 with placeholder numbers. Gemini does only three things: an independent code audit (looking for third bugs), text-consistency reviews of Kimi drafts, and a hostile-reviewer simulation. Claude reviews at three weekly checkpoints (04-30, 05-07, 05-15) and integrates everything at the end. Target venues re-ranked: Nature Electronics primary (best fit for organic CIM), NC secondary, Nature Comm Engineering tertiary. Cover letter explicitly discloses commit `33bed9c` bug fix.
