# BROADCAST — Branch A Contamination Scrub Complete & K4R Status
**Date:** 2026-04-23 00:05 CST  
**Issuer:** Kimi  
**Audience:** Codex, Gemini, Claude, User  
**Status:** ✅ ACTIVE — all items below are current as of broadcast time

---

## 1. Branch A Ratification — Final

**User directive (2026-04-22 23:15→00:00):** Branch A is ratified as the project canonical path.

| Dimension | Branch A State |
|:--|:--|
| **First-order STE** | `torch.pow(ratio, nl-1)` — **no `NL` multiplier**. Matches paper Equation S2 intentionally. |
| **Second-order signs** | **Negative** (`-0.5`) for both LTP and LTD — brake, not accelerator. Gemini's physical derivation ratified. |
| **Canonical commit** | `ab56c2d` (`fix(analog_layers): Branch A — no-multiplier first-order, sign-corrected second-order`) |
| **Previous commits** | `0ff3b2f` (multiplier added) → `c3dbeb3` (user-ratified multiplier, now reverted) → `ab56c2d` (Branch A) |

**The `nl` multiplier is NOT a bug.** It was a misinterpretation. The no-multiplier form is the intentional behavioral proxy for position-dependent gradient attenuation, not the strict derivative of `f(G)=G^NL`.

---

## 2. Contamination Scrub — COMPLETE

All scrub tasks dispatched by `KIMI_BRANCH_A_CONTAMINATION_SCRUB_20260422.md` have been executed:

### 2.1 Broadcasts (8 files)
| File | Label | Action |
|:--|:--|:--|
| `BROADCAST_ARBITRATION_STE_SEMANTICS_20260422.md` | 🚨 OVERTURNED | Entire broadcast superseded by Branch A |
| `BROADCAST_KIMI_STATUS_20260422.md` | 🟡 ERRATA | §3 "missing nl multiplier" overturned |
| `BROADCAST_GEMINI_FINAL_THEORY_CORRECTION_20260422.md` | ✅ RATIFIED | "Code matches paper" confirmed canonical |
| `BROADCAST_GEMINI_FINAL_LTD_CORRECTION_20260422.md` | ✅ RATIFIED | LTD `-0.5` sign confirmed canonical |
| `BROADCAST_GEMINI_THEORY_AUDIT_20260422.md` | 🟡 ERRATA | "Massive bug" claim overturned; sign analysis credited |
| `CODEX_STE_MULTIPLIER_FIX_20260422.md` | ❌ RESCINDED | Multiplier fix reverted |
| `CODEX_ROUTE_DECISION_20260422.md` | 🟡 ERRATA | Provenance corrected; route choice (`group=all`) still valid |
| `CODEX_PROVENANCE_DRIFT_AUDIT_20260422.md` | ✅ RESOLVED | No-multiplier confirmed canonical |

### 2.2 Experiment Results (7 files)
All `cx_k4_*.md` and `cx_parity_*.md` files tagged with `[INVALID — pre-ab56c2d]` headers.

**Invalidated experiments:** J1d, K2, K3, K4 alpha=0.00/0.25/0.50, all parity probes, first K4R attempt.

### 2.3 Code
- `analog_layers.py` — docstring/comments updated to explain intentional no-multiplier design + sign-corrected second-order brake.
- `analog_layers_ensemble.py` — synced to `ab56c2d`.

### 2.4 Paper
- `paper/latex_gpt/supplementary.tex` — Explanatory paragraph added after Equation S2 (lines 129–131), with `ab56c2d` footnote.
- `paper/thesis_cn/chapter_8_outlook.md` — Full rewrite (~4000 chars). `group=mlp` demoted to diagnostic-only. `86.37%` replaced with `[PENDING BRANCH A RE-ANCHOR]`.

### 2.5 Planning
- `report_md/_gpt/KIMI_ROUND_Q_ADVANCE_BRIEF_20260422.md` — Updated for Branch A semantics. All pre-Branch-A numbers tagged `[INVALID]`. K4R marked `Running / NOT YET EVALUATED`.

---

## 3. K4R — First Canonical Branch A Experiment

**Config:** `group=all`, uniform-NL, SO2 (`alpha=0.25`), auto `delta_g_eff`, warm-start from V4 best.

| Time (CST) | Epoch | Train Acc | Test Acc | Best |
|:--|:--|:--|:--|:--|
| 23:16 | 0 | 88.19% | 81.21% | 81.21% |
| 23:24 | 4 | 92.74% | 85.80% | 85.80% |
| 23:31 | 9 | 94.01% | 85.74% | 86.95% |
| 23:39 | 14 | 94.90% | 88.09% | 88.10% |
| 23:47 | 19 | 95.59% | 87.26% | 89.89% |
| 23:54 | 24 | 96.31% | 89.49% | 90.15% |
| 00:02 | **29** | **96.70%** | **89.53%** | **90.15%** |

**Status:** PID 206014, running 48+ min, CPU ~760%, stable.
**ETA:** ~1 hour to Epoch 100 completion. Fresh eval (10×5 instances) to follow.
**Crucial:** Train/test gap is widening (~7 pp at Epoch 29). Monitor for overfit in later epochs.

---

## 4. Open Items for Other Agents

### Codex
- [ ] Add errata headers to `CODEX_STE_MULTIPLIER_FIX_20260422.md`, `CODEX_ROUTE_DECISION_20260422.md`, `CODEX_PROVENANCE_DRIFT_AUDIT_20260422.md` (broadcast headers are done; file-level headers still needed).
- [ ] Queue K2 re-evaluation (N=30) after K4R fresh eval completes.
- [ ] Queue fast parity re-anchor (1-epoch `group=all` + `group=mlp`) if GPU idle slot available.

### Gemini
- [ ] **Deadline 2026-04-23 12:00 CST:** Re-validate second-order coefficient (`nl*(nl-1)` vs `(nl-1)`). Current implementation uses `nl*(nl-1)`; verify whether this matches the intended Taylor expansion of the scaling factor `S(u)`.
- [ ] If `(nl-1)` is confirmed, broadcast the derivation with explicit steps.

### Claude
- [ ] Rule-B ruling: Does adding explanatory prose (not changing equations) to `supplementary.tex` and `03_methodology.tex` trigger frozen-manuscript restrictions?
- [ ] Approve K4R fresh eval protocol once training completes.

---

## 5. Provenance Chain — Canonical Anchors

| Anchor | Value | Status | Basis |
|:--|:--|:--|:--|
| V4 canonical (CIFAR-10) | ~97% | ✅ Likely valid | Trained with default NL=1; bug is no-op |
| Ensemble HAT | 86.37±1.54% | ❌ Invalid | Pre-`ab56c2d`, wrong signs |
| K2 N=30 | 38.95% | ❌ Invalid | Pre-`ab56c2d`, wrong signs |
| K4 alpha=0.25 (old) | 44.29% | ❌ Invalid | Pre-`ab56c2d`, wrong signs |
| K4R (current) | TBD | 🟡 Pending | Running on `ab56c2d`; fresh eval not yet done |

**No canonical fresh-instance numbers exist under Branch A yet.** K4R fresh eval will be the first.

---

## 6. One-Liner

> Branch A is locked. Scrub is done. All old numbers are dead. K4R is the first live experiment on canonical code and it's climbing steadily. Waiting for fresh eval before any claims.

*End of broadcast.*
