# Post-Submission Rebuttal Logistics Playbook
**Internal use only — do not circulate outside team.**
*Derived from: `RESPONSE_LETTER_FINAL_20260419.md`, `KIMI_REBUTTAL_ARSENAL_V1_20260420.md`, `CLAUDE_REBUTTAL_PREP_20260420.md`*

---

## (a) Triage Protocol

**First reader:** Response-letter owner reads within 4 h of review receipt and tags every objection in a shared tracker.

| Tag | Definition | Representative triggers |
|-----|-----------|------------------------|
| **CRITICAL** | Undermines core claim, simulator credibility, or could trigger rejection. | "Simulation-only, no hardware validation" (C-1); "10.00 % collapse is a bug" (C-3); "Fixed analog/digital split never ablated" (C-2); "Risk-aware title oversell" (C-5). |
| **SHOULD-FIX** | Weakens robustness or scope but does not invalidate comparative conclusions. | "ImageNet missing" (R1); "Energy placeholder" (R2); "Heavy-tailed D2D" (K-1); "IR drop ignored" (K-2); "Temperature drift" (K-3); "ADC rationale" (K-4); "Statistical power n=10" (K-10); "Incomplete multi-seed" (C-4). |
| **NICE** | Cosmetic, wording, or figure-clarity issue; address with a sentence or caption tweak. | "Fig. 4 mixed deterministic/MC bars" (R11); "Best-checkpoint reporting" (R10); "NL=2.0 is surrogate not bound" (R4); "CIFAR-10 vs CIFAR-100 headline" (K-8). |

**Escalation rule:** Any CRITICAL tag pings the full team within 1 h. No response letter is drafted until CRITICAL items have an assigned owner and a coverage-audit line number.

---

## (b) Decision Tree — Verbal vs Experiment

```
Does the manuscript ALREADY contain evidence that bounds the objection?
├── YES → Can we cite a specific section, table, figure, or JSON file?
│   ├── YES → VERBAL RESPONSE (Tier 1)
│   │          Acknowledge + cite + explain why the omission scopes,
│   │          rather than invalidates, the claim.
│   └── NO  → VERBAL + PRE-EMPTIVE TEXT (Tier 1a)
│             Add one clarifying sentence in §1, §3.1, §6.5, or §6.6
│             (allowed under "pre-emptive clarification" rule).
└── NO  → Is the missing evidence a quick evaluation-only run
          (no retraining, <24 h wall time)?
          ├── YES → TIER 2 EXPERIMENT
          │          Launch screening pass (5 arrays × 3 MC),
          │          integrate if ranking survives; else honestly frame
          │          as limitation.
          └── NO  → TIER 3 EXPERIMENT
                     Requires new training run or large-scale pilot.
                     Default is "spec ready, deferred to revision"
                     unless editor explicitly mandates it.
```

**Hard constraint:** Do not commit to a Tier-3 experiment in the response letter unless the editor’s letter explicitly requests it. Instead, attach the pre-staged spec as proof of readiness.

---

## (c) Pre-Staged Spec Mapping

| Spec | Objection type it answers | Verbal coverage already in manuscript? | Launch trigger |
|------|--------------------------|----------------------------------------|----------------|
| **G-BB1** Heavy-tailed conductance stress-test | "Gaussian D2D invalid; real devices have log-normal/Pareto tails" (K-1, R3 extension) | §6.5 disclaims heavy tails; profile interface (§3.3) ready. | Reviewer explicitly demands distributional robustness data. |
| **G-BB2** IR-drop preliminary modeling | "Position-dependent IR drop / sneak paths ignored" (K-2, R3 extension) | §3.6 and §6.5 flag IR drop; §6.6 defers circuit-aware layer. | Reviewer asks for spatial-bias quantification. |
| **G-AA2** ImageNet pilot scoping | "Empirical scope limited to small-scale datasets" (R1) | §1 scopes to "edge vision"; cover letter pre-registers ImageNet pilot. | Editor mandates scale-up; otherwise cite as future work. |
| **G-AA3** Joint MLP-Linear + Ensemble HAT | "No path to push retention above 79 % plateau" (K-9) or "attention-side collapse structural" (R4) | §6.5 notes state-dependent retention support; §6.6 defers adaptive calibration. | **Thesis-only.** Do NOT launch during rebuttal unless editor explicitly instructs. |
| **Live spec: §5.4 + §6.4 ADC sweep** | "Why 6-bit specifically?" (K-4) | Empirical sweep already present. | None — purely verbal. |
| **Live spec: §5.8 fresh-instance protocol** | "Statistical power of n = 10" (K-10); "Ensemble frequency heuristic" (K-5) | 10 × 5 MC reported; no batch ablation. | Verbal for power; Tier 2 if batch-frequency ablation demanded. |
| **Live spec: §3.3 + §6.5 NL surrogate** | "NL = 2.0 is gradient-scaling approximation" (R4, K-7) | Disclosed as approximation; group-wise ablations in supplementary. | Verbal + cite supplementary. |

---

## (d) Rebuttal-Letter Template Structure

Follow the `RESPONSE_LETTER_FINAL_20260419.md` proven format. Every objection gets exactly four blocks:

1. **Objection.** One-sentence reviewer summary (quote if short).
2. **Manuscript evidence.** Bullet or sentence citing §, Table, Figure, or JSON file with line-level precision. If none exists, state "Response-only argument; no manuscript overclaim."
3. **Response.** 3–4 sentences maximum. Structure: (i) acknowledge the concern honestly, (ii) bound its impact on the core claim, (iii) cite evidence or explain why the omission is scoped.
4. **Changes to the manuscript.** One of:
   - `None.` (most common — response-only)
   - `Pre-emptive: one sentence added to §X.Y to clarify scope.`
   - `Supplementary Note SX.Z added.` (for Tier-2 experiments)

**Closing block:** "Summary of Pre-Emptive Changes Implemented" — list every cover-letter tweak, §6.5 tightening, and supplementary addition so the editor sees transparency without hunting.

---

## (e) Timing Budget — Revised Manuscript Turnaround

| Tier | Work | Wall-clock estimate |
|------|------|---------------------|
| **Tier 1** | Verbal response + citation audit | 48–72 h |
| **Tier 1a** | + pre-emptive one-sentence text patch | +12 h |
| **Tier 2** | + supplementary eval-only MC campaign (no retraining) | +3–5 days (compute-bound) |
| **Tier 3** | + new training run or ImageNet-scale pilot | +14–21 days |

**Default posture:** Promise Tier 1/1a turnaround (≤72 h for draft, ≤1 week for final package). If the editor’s decision letter imposes a hard deadline (e.g., 10 days), scope down to Tier 1–2 only. G-AA3 (joint training) is explicitly excluded from the rebuttal timing budget; it is thesis-fork compute.

---

## (f) 72-Hour Action Checklist

| Time | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| **H0** | Receive reviews. First reader skims all comments and tags CRITICAL / SHOULD-FIX / NICE in tracker. | Response-letter owner | Triage tracker with line-level objection IDs |
| **H4** | Team lead confirms triage. Assign each item an evidence owner and a response drafter. | Team lead | Assignment matrix |
| **H12** | Coverage audit complete: every objection mapped to manuscript §, table, figure, JSON, or spec. | Evidence owner | `REBUTTAL_COVERAGE_AUDIT_YYYYMMDD.md` |
| **H24** | Draft response letter complete for all CRITICAL and SHOULD-FIX items. Decision tree applied (verbal vs Tier 2). | Response drafter | `RESPONSE_DRAFT_v0.md` |
| **H36** | If Tier-2 experiments approved, launch compute jobs (G-BB1 screening, G-BB2 stub, etc.). | Compute lead | Slurm/job IDs logged in tracker |
| **H48** | Internal review: fact-check every citation, confirm no manuscript overclaim, sanity-check tone. | Independent reader | Annotated draft with corrections |
| **H60** | Tier-2 results back. Integrate into response if ranking survives; otherwise pivot to honest limitation framing. | Evidence owner | Updated draft + supplementary figure |
| **H72** | Final proofread, cover letter finalized, package locked. | Team lead | `RESPONSE_LETTER_FINAL_YYYYMMDD.md` ready for submission |

**Contingency:** If a CRITICAL objection surfaces that lacks any pre-staged spec (e.g., a completely novel hardware-validation demand), convene an emergency 30-min scoping call at H6 and decide whether to draft a "spec-deferred" response or pivot to Tier 3.

---

*Playbook generated: 2026-04-20*
*Verified against: R1–R11 response letter, KIMI arsenal K-1–K-10, CLAUDE prep C-1–C-5, G-BB1/2 and G-AA2/3 specs.*
