# DISPATCH GEMINI G-HOSTILE-V2 — Spec Only (Hold Until Trigger)
**Date:** 2026-04-25 01:30 CST
**Issued by:** Claude
**Assignee:** Gemini
**Priority:** SPEC PREPARED — DO NOT EXECUTE YET
**Authority:** CLAUDE_FORWARD_ROADMAP §6 Round-7 trigger
**Status:** STANDING SPEC

---

## 0. Trigger conditions (ALL must hold before firing)

1. 8×40GB cross-arch matrix returned and Kimi has integrated cross-arch supplementary section
2. R4-6 Work 2 KV-cache preview decision made (either landed or formally deferred)
3. Cover letter v6 final-locked with all numbers
4. Claude has done one final read-through of integrated manuscript

When all 4 conditions met, Claude or user signals "G-HOSTILE-V2 GO" and Gemini fires.

---

## 1. Objective

Simulate a hostile reviewer at Nature Electronics. Find every weakness a critical reviewer would attack. Final bug-insurance before submission.

This supersedes the earlier `GEMINI_HOSTILE_REVIEW_POST_FIX_20260513.md` (which simulated review on the post-fix narrative — useful but stale).

---

## 2. Scope

Read the **fully integrated submission package**:
- `paper/latex_gpt/main.pdf` (compiled)
- `paper/latex_gpt/cover_letter.pdf`
- `paper/latex_gpt/supplementary_main.pdf`
- (NOT thesis chapters — they're separate artifact for PhD defense, not submission package)

---

## 3. Hostile reviewer persona to simulate

A senior researcher in analog CIM with 15+ years experience, who:
- Has published in Nature Electronics
- Knows Rasch / IBM AIHWKit / Sebastian / Eleftheriou / Burr lineage
- Is suspicious of "novel HAT method" claims unless deeply theoretically grounded
- Will demand silicon validation if you claim "deployment-fidelity"
- Will sniff for cherry-picked seeds, eval leakage, hyperparameter sensitivity
- Is a stickler for honest limitations and reproducibility
- Has a low tolerance for paper-padding — every claim must earn its space

---

## 4. Attack vectors (do all)

### 4.1 Methodology attacks
- Ensemble HAT: is the per-epoch resampling really doing the work, or is it an artifact of batch-level training noise? Cite the empirical ablation (88.41 epoch / 86.16 per-batch / 87.18 fixed) — does this stand up?
- Theory derivation: is the second-order Taylor expansion legitimate, or does it break down at realistic σ_D2D = 10%?
- Gauss-Newton approximation in implicit-regularizer derivation — is the approximation tight in the regimes where Ensemble HAT actually wins?

### 4.2 Empirical attacks
- The 86.37±1.54% Ensemble HAT vs 10.00±0.00% Standard HAT collapse: is the 10% really chance, or is it an unstable single-class predictor? (Answer should be in §5.5 — verify they actually addressed this)
- Cross-host parity: is the local CX-M vs remote R-M discrepancy (~1-2 pp Standard, ~4 pp Proportional) explained by batch size alone or is there host-dependence? (See `cross_host_parity_mseries.csv`)
- Iso-accuracy map: 63 points, 10 MC each = 630 evaluations. Is the variance estimate tight? Is the 6-bit cliff actually 7pp every row, or only on average?
- Stage-2 ADC per-instance recal Δ ≈ 0: is this because per-instance cal genuinely doesn't matter, or because the implementation didn't actually change the calibration target meaningfully?

### 4.3 Hardware attacks
- Literature-prior σ_D2D = 10%: where does this come from? Is it representative of organic CIM specifically, or is it borrowed from ReRAM/PCM literature?
- OPECT zero-shot: cite exact numbers from zhang2025opect Supp. If we're claiming validation against measured device profile, we should be exact about which profile fields we used
- ADC hook calibration physical validity: Gemini already audited this in G-AUDIT-ADC-HOOK. Re-check if the integrated paper still claims more than the audit supports

### 4.4 Reproducibility attacks
- Code release commit hash pinned? Verifiable via `test_*.py` suite?
- Random seeds documented? Multi-seed numbers reported with std?
- Hyperparameter sensitivity? Lr / batch / epoch choices justified?
- Compute budget transparency?

### 4.5 Narrative attacks
- "Hardware-instance overfitting" — is this concept truly novel, or does it exist under different names in adjacent literature (concept-shift, calibration-set vs deployment-set, etc.)?
- The three-scenario evidence spine: are the three really independent, or does Scenario 2 (OPECT) inherit assumptions from Scenario 1 (canonical)?
- Severe-NL ~80-82% recovery: is this paper-grade for Nature Electronics, or does the reviewer want >90%?

### 4.6 Citations + positioning attacks
- Did we cite the most recent (2025-2026) analog CIM transformer papers?
- Did we acknowledge Rasch IBM AIHWKit explicitly as the conceptual ancestor of the train-surrogate / eval-ADC-hook discipline?
- Did we position correctly vs the latest organic optoelectronic CIM efforts?

---

## 5. Output format

`report_md/_gpt/GEMINI_HOSTILE_REVIEW_V2_<YYYYMMDD>.md`:

```markdown
# Gemini Hostile Review v2
Date: <YYYY-MM-DD>
Reviewer persona: senior analog CIM researcher
Verdict: <ACCEPT / MAJOR REVISIONS / MINOR REVISIONS / REJECT> + rationale

## Section-by-section attacks

### Abstract
- Issue: ...
- Severity: HIGH / MEDIUM / LOW
- Author defensible? YES / NO / PARTIAL
- Recommended response: <silent fix / defend in revision / patch in current submission>

### §5.7 Severe-NL recovery
... (repeat for every section)

## Killer attacks (would block acceptance)
<List with severity)

## Defensible attacks (would survive in revision)
<List with proposed responses)

## Polish opportunities (would strengthen submission)
<List with low-cost-high-value priority)
```

---

## 6. Constraints

- **Read the integrated PDF, not sidecars** — review what reviewer will actually see
- **No code-audit scope** — that's done. This is paper-content audit.
- **No new theory derivations** — assess what's there, don't propose alternatives
- **Honest hostile** — not gratuitously hostile. A reviewer who finds nothing to attack is suspicious.
- **Severity discipline**: HIGH = blocks acceptance; MEDIUM = needs response in revision; LOW = polish

---

## 7. Success criteria

After Claude reviews Gemini's hostile-v2 report:
- Killer attacks (if any) get patched before submission
- Defensible attacks get response strategy ready
- Polish opportunities prioritized for last-pass edits
- Manuscript is genuinely defensible, not just-passing

---

## 8. Timing

- **Trigger**: ALL 4 conditions in §0 met
- **Execution**: ~1 day
- **Claude follow-up**: ~1 day to triage findings + plan responses
- **Submission timeline**: review complete + responses planned → ready for PhD-graduation-gated submission

---

## 9. Until trigger fires

Gemini stays in standing-monitor mode. No proactive audits. This dispatch is spec-only and waits for explicit GO signal.
