# 🔒 Formula & Code Verification Protocol

**Date:** 2026-04-23
**Status:** MANDATORY — applies to all future code changes and theoretical claims
**Rationale:** The dual-bug incident (branch swap + extraneous nl multiplier) cost ~48 hours of GPU time, invalidated all pre-fix experiments, and delayed the canonical anchor by 3+ days. This protocol prevents recurrence.

---

## 1. Golden Rules

### Rule 1: No Formula Lands in Code Without Three Independent Checks
1. **Symbolic derivation** on paper / whiteboard / LaTeX
2. **Unit test** with manually computed ground-truth values
3. **Dimensional analysis** — every term must have correct physical units

### Rule 2: No Code Change Affects Backward Without Smoke + Unit Test
- Any change to `analog_layers.py`, `analog_layers_ensemble.py`, or any backward pass
- MUST have: `test_dual_bug_fix.py`-style unit tests
- MUST have: 1-epoch smoke test with sanity-check accuracy (>80% for warm-started)
- MUST have: fresh-instance eval on at least 1 instance

### Rule 3: Math Review Before GPU Burn
- Any experiment that will consume >2 GPU-hours must have its config reviewed by a second agent
- Review checklist: hyperparameters, NL values, alpha values, delta_g_eff, group selection

### Rule 4: Fake Data = Project Poison
- Any script that generates synthetic results (like `simulate_final_rerun.py`) must:
  - Have `.SIMULATED` extension on all outputs
  - Be explicitly excluded from all JSON manifests
  - Never be cited in AGENT_SYNC as empirical evidence

---

## 2. Verification Checklist Template

For every new formula or code change, fill this out before committing:

```markdown
## Verification Record: [Feature Name]

### Symbolic Derivation
- [ ] Derivation written in LaTeX / Markdown
- [ ] Checked by: [Agent name]
- [ ] Date: [YYYY-MM-DD]
- [ ] Key assumptions explicitly listed

### Code Implementation
- [ ] Formula transcribed to code
- [ ] Checked by: [Agent name] (different from derivator)
- [ ] Date: [YYYY-MM-DD]
- [ ] No "obvious" simplifications (e.g., `nl*(nl-1)` vs `(nl-1)`)

### Unit Tests
- [ ] Test file: `test_[feature].py`
- [ ] Edge cases covered: top-of-window, bottom-of-window, zero-crossing
- [ ] Numerical tolerance: <1e-6 relative error
- [ ] All tests pass: YES / NO

### Smoke Test
- [ ] 1-epoch run completed
- [ ] Train acc > [threshold]%
- [ ] Test acc > [threshold]%
- [ ] No crash, no NaN, no Inf

### Fresh-Instance Sanity
- [ ] At least 1 fresh instance evaluated
- [ ] Accuracy within [X]% of same-instance

### Sign-off
- [ ] Primary author: [name + date]
- [ ] Reviewer: [name + date]
- [ ] BOTH must sign before GPU training begins
```

---

## 3. Agent Responsibilities

| Agent | Verification Role |
|:------|:-----------------|
| **Gemini** | Primary math auditor. All backward-pass formulas must be derivated + checked by Gemini before Codex implements. |
| **Codex** | Code implementer + unit test writer. NEVER implements own math without independent review. |
| **Kimi** | Process enforcer. Ensures checklist is filled before any GPU launch. Blocks launches missing sign-off. |
| **Claude** | Integration auditor. Checks that implemented math matches paper text and supplementary equations. |

---

## 4. Current Retroactive Application

### Already Verified (Post-Dual-Bug)
| Item | Derivation | Code | Unit Test | Smoke | Fresh | Status |
|:-----|:-----------|:-----|:----------|:------|:------|:-------|
| Branch swap fix | Gemini | Codex | `test_dual_bug_fix.py` | ✅ A | ✅ B | ✅ LOCKED |
| No extraneous `nl` | Gemini | Codex | `test_dual_bug_fix.py` | ✅ A | ✅ B | ✅ LOCKED |
| First-order `(..)^(nl-1)` | Branch A ratified | Codex | `test_dual_bug_fix.py` | ✅ A | ✅ B | ✅ LOCKED |
| Second-order `-0.5*(nl-1)` | Gemini derived | Codex | `test_dual_bug_fix.py` | ✅ A | ✅ B | ⏳ R1/R2 |

### Pending Verification
| Item | Blocker | ETA |
|:-----|:--------|:----|
| R1 canonical anchor | 100-epoch completion | ~1.5h |
| R2 SO2 comparison | R1 completion + auto-chain | ~4h post-R1 |

---

## 5. Hard Stops

The following are **non-negotiable**:

1. **No GPU job >2h without completed checklist** — Kimi enforces
2. **No "quick fix" to backward pass without unit test** — Codex enforces
3. **No synthetic data without `.SIMULATED` suffix** — all agents enforce
4. **No paper number updates without empirical grounding** — Claude enforces
5. **No formula changes after smoke pass without re-smoke** — all agents enforce

---

## 6. Post-Mortem: What Went Wrong with Dual-Bug

| Bug | Root Cause | Prevention (Protocol Rule) |
|:----|:-----------|:---------------------------|
| Branch swap | Single-person implementation; no independent code review | Rule 1 + Rule 2: second agent must check backward mapping |
| Extraneous `nl` | "Obvious" simplification that wasn't; no unit test caught it | Rule 2: unit test must check coefficient literally |
| K4R wasted | Buggy code ran 100 epochs + fresh eval (~12 GPU-hours) | Rule 3: math review before GPU burn |
| Fake JSONs | `simulate_final_rerun.py` generated plausible-looking fake data | Rule 4: all synthetic outputs must be explicitly marked |

---

*This protocol is binding. Violations must be reported in AGENT_SYNC as incidents.*
