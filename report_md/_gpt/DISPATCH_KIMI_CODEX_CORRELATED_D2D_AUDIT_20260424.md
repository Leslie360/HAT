# DISPATCH KIMI+CODEX — Correlated D2D (AR1) Provenance Audit
**Date:** 2026-04-24 22:30 CST
**Issued by:** Claude
**Assignees:** Kimi (text side) + Codex (data side)
**Depends on:** CLAUDE_ROUND2_CLOSURE_RULING §2 R3-2
**Priority:** MEDIUM (blocks Supp Note S2 final lock)
**Time budget:** ~1 day

---

## 1. Objective

Audit the provenance of the correlated-D2D (AR(1)) numbers cited in Supp Note S2 and paper Discussion §6.4 (Limitations):

- `86.33 ± 1.61%` — matched i.i.d. baseline
- `84.57 ± 2.39%` — ρ=0.3 AR(1) D2D perturbation
- `82.12 ± 3.95%` — ρ=0.5 AR(1)
- Minimum `73.7%` across all tested instances

Confirm: (a) which commit these numbers were generated at, (b) whether the generating code is in the bug-immune zone (NL=1.0 canonical) or needs re-verification, (c) JSON source file paths, (d) eval protocol matches current canonical methodology.

These numbers are load-bearing for the "spatial correlation degrades Ensemble HAT gracefully but proportionally" sub-claim. If the provenance is clean, they stay in zone 3A. If contaminated, they need rerun or removal.

---

## 2. Codex side (data audit)

### 2.1 Locate JSON source

Target file: `fresh_instance_eval_v4_ensemble_correlated_d2d.json` (referenced in current `06_discussion.tex` Limitations paragraph).

Check:
- File exists? Path? Size? Last modified?
- Git blame on the script that produced it
- Commit hash at generation time (is it pre or post commit 33bed9c dual-bug fix?)
- Eval protocol: NL_LTP, NL_LTD, noise_mode, sigma_d2d, sigma_c2c, num_instances, mc_runs

### 2.2 Zone classification

Based on §2.1 findings, classify as zone 3A / 3B / 3C:
- If NL=1.0 canonical: zone 3A bug-immune, keep
- If NL≠1.0 pre-fix: zone 3B invalidated, rerun or remove
- If NL=1.0 but generated pre-fix with any AMP/worldview difference: verify via a quick reproduction

### 2.3 Reproduction (if needed)

If §2.2 classification is zone 3B or "verify needed":
- Rerun `fresh_instance_eval_v4_ensemble_correlated_d2d.json` at current commit 33bed9c + NL=1.0 canonical + AR(1) at ρ=0, 0.3, 0.5
- ~1-2 GPU-h total
- Confirm numbers reproduce within 2σ of existing
- If major drift, flag to Claude

### 2.4 Deliverable

`CODEX_CORRELATED_D2D_AUDIT_REPORT_20260424.md` with:
- Source JSON provenance table
- Zone classification verdict
- Reproduction verdict (if applicable)
- Paper-safe statement for Kimi to cite in Supp Note S2

---

## 3. Kimi side (text audit)

### 3.1 Locate all cites

Grep paper and supplementary for these numbers:
- `86.33`, `84.57`, `82.12`, `73.7`
- "AR(1)", "correlated", "spatial correlation"
- "Supp Note S2"

Produce a citation map: where each number is cited across paper/latex_gpt/ and paper/thesis*/.

### 3.2 Zone annotation update

Once Codex returns zone classification, update Supp Note S2 preamble with explicit zone label and commit reference. If zone 3A: cite confidently. If zone 3B rerun: update numbers with rerun results. If zone 3B no-rerun: remove or flag.

### 3.3 Theory connection

If KIMI-THEORY-1 derivation §S.5 (AR(1) Fisher-matrix-weighted anisotropic penalty) cites these numbers, check consistency. Theory predicts degradation monotonic in ρ — confirm empirical 86.33 > 84.57 > 82.12 pattern matches.

### 3.4 Deliverable

Append to `KIMI_ROUND2_CORRELATED_D2D_AUDIT_<date>.md` (or create new): citation map, zone verdict, any text edits needed across manuscript.

---

## 4. Hard constraints

- **No new GPU work unless §2.3 requires it** (budget capped at ~2 GPU-h)
- **No narrative changes** — this is a provenance audit, not a content change
- **Zone-label discipline**: every cite of these numbers gets an explicit zone tag after audit

---

## 5. Coordination

- Codex completes §2 first
- Signal Kimi via AGENT_SYNC "Correlated D2D zone verdict: [3A / 3B / 3C]"
- Kimi completes §3 after signal
- Claude reviews both deliverables before Round-3 integration

---

## 6. Success criteria

- Provenance chain documented from JSON → script → commit
- Zone classification final
- Paper cites updated (if needed)
- Theory-empirical consistency confirmed for AR(1) prediction
- Supp Note S2 ready for final lock
