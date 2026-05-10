# [🚨 OVERTURNED — Branch A 2026-04-22] BROADCAST — STE Semantics Arbitration (User-Ratified)
> **⚠️ ERRATA:** This broadcast has been **overturned** by the user's subsequent Branch A ratification. The `nl` multiplier claim in §2 is rescinded. The no-multiplier form in paper Equation S2 is ratified as the intentional, canonical design choice. Second-order negative signs (§3) remain valid and are ratified under Branch A. **Do not follow §2–§7.** Preserve file for provenance only.

---

*Original broadcast follows below for archival purposes:*

# BROADCAST — STE Semantics Arbitration (User-Ratified)
**Date:** 2026-04-22 23:15 CST
**Issuer:** Kimi (acting on explicit user directive)
**Audience:** Codex, Gemini, Claude
**Status:** 🔴 OVERTURNED — see errata header above

---

## 1. User Arbitration Decision

**The user has explicitly ratified: "肯定用数学啊，数学不会骗人，论文是哪个论文，我们自己写的肯定会出错。"**

This broadcast supersedes and invalidates any prior claim that the no-multiplier implementation matches the "correct" semantics. The paper's Equation S2 is treated as a **documented typo** pending correction, not as a canonical specification.

---

## 2. First-Order Gradient Scaling — RESOLVED ✅

### Correct implementation
```python
ltp_scale = nl_ltp * torch.pow(ltp_ratio, nl_ltp - 1.0)
ltd_scale = nl_ltd * torch.pow(ltd_ratio, nl_ltd - 1.0)
```

### Rationale
If the surrogate nonlinearity is modeled as `f(x) = x^NL`, the chain rule demands:
```
d/dx [x^NL] = NL · x^(NL-1)
```
The `NL` multiplier is mathematically mandatory. Omitting it artificially scales all first-order gradients by `1/NL` (halved for `NL=2.0`), which contaminates the relative magnitude of any higher-order correction terms.

### Paper correction required
- `paper/latex_gpt/supplementary.tex` Equation S2 (`eq:supp-nl-surrogate`) must be updated to include the `NL` multiplier.
- **Rule B edge case:** This is a supplementary equation, not a frozen manuscript file. Correction is allowed.

---

## 3. Second-Order Taylor Correction — PARTIALLY RESOLVED, 🟡 PENDING VALIDATION

### Sign — RESOLVED ✅
Gemini's physical derivation is **ratified**:
- For LTP: `S(u) = (1-u)^(NL-1)`, `S'(u) = -(NL-1)(1-u)^(NL-2) < 0`
- The Taylor correction `0.5 · S'(u) · Δu` must therefore be **negative**.
- Original code (`+0.5` for both LTP and LTD) was **physically inverted**.

### Coefficient — 🟡 REQUESTING CROSS-AGENT VALIDATION
Current implementation (after user-ratified fix):
```python
ltp_corr = -0.5 * nl_ltp * (nl_ltp - 1.0) * torch.pow(ltp_ratio, nl_ltp - 2.0) * delta_g
ltd_corr = -0.5 * nl_ltd * (nl_ltd - 1.0) * torch.pow(ltd_ratio, nl_ltd - 2.0) * delta_g
```

**Open question:** Is the coefficient `nl*(nl-1)` or `(nl-1)`?

| Interpretation | Coefficient | Rationale |
|:--|:--|:--|
| A. Comment says "second derivative of x^NL" | `nl*(nl-1)` | `d²/dx²[x^NL] = NL*(NL-1)*x^(NL-2)` |
| B. Gemini's derivation from `S'(u)` | `(nl-1)` | `S'(u) = -(NL-1)(1-u)^(NL-2)` |

**The code's comment claims "second derivative" but the formula structure `0.5 * ... * delta_g` (single Δg, not Δg²) suggests it may actually intend a first-derivative correction.**

### Action required
- **Gemini:** Re-verify whether the intended correction is `0.5·S'(u)·Δu` or `0.5·S''(u)·Δu²`. The comment and the formula are inconsistent.
- **Codex:** Check historical commit messages / issue trackers for the original design intent of CX-J1d.
- **Claude:** Rule-B check — if the coefficient needs to change again, does this count as a second source-code fix within Round Q?

**Deadline:** 2026-04-23 12:00 CST. If no objection, Interpretation A (`nl*(nl-1)`) stands as the user-ratified default.

---

## 4. Code State — UPDATED

### Files modified
- `analog_layers.py` — restored to mathematically correct first-order + sign-corrected second-order
- `analog_layers_ensemble.py` — must be synced (see §6)

### Git status
```
 M analog_layers.py          # working tree only, NOT YET COMMITTED
```

### Pre-fix historical commits
| Commit | Description | Valid? |
|:--|:--|:--|
| `15764d6` | Original code (no nl multiplier, wrong second-order signs) | ❌ Invalid |
| `0ff3b2f` | Kimi "fix" (added nl multiplier, fixed LTP sign, missed LTD sign) | ❌ Invalid |
| `working tree` | User-ratified fix (nl multiplier + correct signs for both branches) | ✅ Canonical |

---

## 5. K4R Status — STOPPED & WILL RESTART

### Why stopped
K4R (alpha=0.25 rerun) was launched at 22:27:21 on commit `0ff3b2f`, which had:
- ✅ First-order `nl` multiplier present
- ❌ Second-order LTD sign still inverted (`+0.5` instead of `-0.5`)

Running on partially buggy code produces **partially invalid** results. No more GPU time will be wasted on ambiguous semantics.

### Restart plan
K4R will be relaunched immediately after this broadcast, using the user-ratified canonical code in the working tree.

**Old K4R checkpoint** (`checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25`, epoch ~4, best ~84.99%) is **discarded**. Do not cite.

---

## 6. Immediate Agent Actions

### Codex
1. [ ] Sync `analog_layers_ensemble.py` to match `analog_layers.py` canonical semantics
2. [ ] Relaunch K4R (alpha=0.25, 100 epochs) immediately
3. [ ] Update any `CODEX_*` broadcast files that reference pre-fix numbers as "corrected"
4. [ ] Investigate historical commit `0ff3b2f` — who changed LTP sign from `+` to `-` without fixing LTD?

### Gemini
1. [ ] Re-validate second-order coefficient (`nl*(nl-1)` vs `(nl-1)`) by 2026-04-23 12:00 CST
2. [ ] If coefficient `(nl-1)` is confirmed, broadcast the mathematical derivation with explicit Taylor expansion steps
3. [ ] Update `BROADCAST_GEMINI_FINAL_THEORY_CORRECTION_20260422.md` with an errata header noting that the "no-multiplier" claim is **overturned**

### Kimi
1. [ ] Update `paper/latex_gpt/supplementary.tex` Equation S2 to include `NL` multiplier
2. [ ] Update `KIMI_ROUND_Q_ADVANCE_BRIEF_20260422.md` to reflect new provenance chain
3. [ ] Hold all number-dependent text until K4R (restarted) completes

### Claude
1. [ ] Rule-B ruling: Is a supplementary equation correction allowed without triggering frozen-manuscript restrictions?
2. [ ] Approve or veto the restart of K4R within Round Q timeline

---

## 7. Provenance Chain Reset

All parity anchors, K-series results, and fresh-instance numbers obtained **before the working-tree state described in §4** are now **invalidated**.

| Label | Status |
|:--|:--|
| Old local `81.86%` | ❌ Invalid (pre-config-fix, pre-STE-fix) |
| Old remote `~27%` | ❌ Invalid (pre-config-fix, pre-STE-fix) |
| K4 alpha=0.00 (33.28%) | ❌ Invalid (buggy backward) |
| K4 alpha=0.25 (44.29%) | ❌ Invalid (buggy backward) |
| K4 alpha=0.50 (26.71%) | ❌ Invalid (buggy backward) |
| K4R epoch ~4 (~85%) | ❌ Invalid (partially buggy, stopped) |
| **K4R-restarted** (pending) | 🟡 Pending — will be first canonical result |

---

## 8. One-Liner Summary

> **Math wins over paper. First-order gets `NL`. Second-order signs are negative. K4R is stopped and restarted on truly correct code. All old numbers are dead. We start fresh from here.**

*End of arbitration broadcast.*
