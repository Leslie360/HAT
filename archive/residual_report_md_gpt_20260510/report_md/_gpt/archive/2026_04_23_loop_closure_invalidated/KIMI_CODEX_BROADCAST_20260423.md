<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# CODEX_BROADCAST — Round Q Day 2 (2026-04-23)
## Classification: ARCHIVAL — Branch A Canonical
## Provenance: kimi-cli
## Canonical Commit: ab56c2d

---

## 1. Executive Summary

On 2026-04-22/23, Branch A was ratified as the sole canonical STE semantics path, overturning the prior user-ratified multiplier interpretation. Commit `ab56c2d` locks the no-multiplier first-order form (`torch.pow(ratio, nl-1)`) and negative-sign second-order correction (`-0.5`) into the codebase. A full contamination scrub was executed across broadcasts, experiment result files, code comments, and paper/thesis prose, invalidating all pre-`ab56c2d` K-series results. K4R—the first canonical Branch A experiment—was launched (`group=all`, uniform-NL, SO2 `alpha=0.25`) and is approaching completion. Defense collateral, thesis Chapter 8, and the auto-eval launcher were updated to Branch A compliance in parallel. No canonical fresh-instance numbers yet exist under the new semantics.

---

## 2. Completed Work

- **STE Semantics Arbitration finalization (Branch A ratified)**
  - No-multiplier first-order (`ratio^(nl-1)`) confirmed as intentional behavioral proxy for position-dependent gradient attenuation, matching paper Equation S2.
  - Negative second-order signs (`-0.5` for both LTP and LTD) ratified per Gemini's physical derivation; brake semantics, not accelerator.
  - Prior user-ratified multiplier interpretation (`nl * ratio^(nl-1)`) rescinded; `c3dbeb3` reverted.

- **Code commit `ab56c2d` (canonical)**
  - `analog_layers.py`: first-order restored to no-multiplier, second-order signs corrected to negative.
  - `analog_layers_ensemble.py`: synced to `ab56c2d`; docstring updated with Branch A provenance.

- **K4R launched (alpha=0.25, group=all, uniform-NL + SO2)**
  - Warm-started from V4 best checkpoint.
  - Config: `--protected-group all --nl-ltp 2.0 --nl-ltd -2.0 --use-second-order-ste --second-order-alpha 0.25 --delta-g-eff -1.0`.
  - Auto-eval monitor deployed via `scripts/_gpt/launch_cx_k4r_fresh_eval.sh`.

- **86.37% contamination scrub across 4 files (~10 instances tagged `[INVALID]`)**
  - `KIMI_DEFENSE_SLIDES_CONTENT_20260423.md`
  - `KIMI_DEFENSE_SLIDES_OUTLINE_20260423.md`
  - `KIMI_PRESS_RELEASE_20260420.md`
  - `KIMI_PAPER_2_DEEP_SCOPE_20260420.md`
  - Pre-Branch-A ensemble HAT result (86.37 ± 1.54%) explicitly voided in all locations.

- **OPECT 88.53% tagged `[PENDING]`**
  - Pre-Branch-A zero-shot transfer result under Zhang 2026 literature profile voided; awaiting K4R re-anchor before any OPECT claim can be restated.

- **Defense slides expanded to 12 slides (~3,900 words)**
  - `report_md/_gpt/KIMI_DEFENSE_SLIDES_OUTLINE_20260423.md` (outline, 13 sections, 12 content slides)
  - `report_md/_gpt/KIMI_DEFENSE_SLIDES_CONTENT_20260423.md` (speaker notes / content, ~3,895 words)
  - Branch A compliance banner added; all pre-`ab56c2d` numbers tagged `[INVALID]` or `[PENDING]`.

- **Blog draft + Public FAQ created**
  - `report_md/_gpt/KIMI_BLOG_DRAFT_20260420.md`
  - `report_md/_gpt/KIMI_PUBLIC_FAQ_20260420.md`
  - Note: drafted 2026-04-20; numbers held pending K4R re-anchor.

- **Thesis Ch.8 rewritten (Branch A compliant)**
  - `paper/thesis_cn/chapter_8_outlook.md`: ~4,000-character rewrite.
  - `group=all` elevated to mainline; `group=mlp` demoted to diagnostic-only.
  - 86.37% replaced with `[PENDING BRANCH A RE-ANCHOR]`.

- **K4R auto-eval monitor deployed**
  - Shell script `scripts/_gpt/launch_cx_k4r_fresh_eval.sh` queues 10×5 fresh-instance evaluation immediately upon training completion.

---

## 3. Running Experiments

| Experiment | Status | Detail |
|:-----------|:-------|:-------|
| **K4R** | Epoch 59/100, best = 90.54% | PID 206014; train/test gap ~8 pp; ETA ~60 min to Epoch 100 |
| **Fresh-instance eval** | Queued | 10 instances × 5 runs each; triggered by `launch_cx_k4r_fresh_eval.sh` post-training |

---

## 4. File Inventory

| Path | Action | Description |
|:-----|:-------|:------------|
| `compute_vit/analog_layers.py` | Modified | Branch A canonical STE: no-multiplier first-order, negative second-order signs |
| `compute_vit/analog_layers_ensemble.py` | Modified | Synced to `ab56c2d`; provenance header added |
| `compute_vit/paper/latex_gpt/supplementary.tex` | Modified | Explanatory paragraph added after Equation S2 (lines 129–131) with `ab56c2d` footnote |
| `compute_vit/paper/latex_gpt/sections/03_methodology.tex` | Modified | Methodology footnote referencing Branch A semantics |
| `compute_vit/paper/thesis_cn/chapter_8_outlook.md` | Rewritten | Branch A compliant; `group=all` mainline, `group=mlp` diagnostic |
| `compute_vit/report_md/_gpt/BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md` | Created | Master scrub status broadcast |
| `compute_vit/report_md/_gpt/KIMI_DEFENSE_SLIDES_CONTENT_20260423.md` | Created | 12-slide speaker notes (~3,895 words), Branch A compliant |
| `compute_vit/report_md/_gpt/KIMI_DEFENSE_SLIDES_OUTLINE_20260423.md` | Created | 12-slide outline, Branch A compliant |
| `compute_vit/report_md/_gpt/cx_k4_train_k4_alpha_0p00.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/report_md/_gpt/cx_k4_train_k4_alpha_0p25.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/report_md/_gpt/cx_k4_train_k4_alpha_0p50.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/report_md/_gpt/cx_parity_all_so2_auto.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/report_md/_gpt/cx_parity_j1d_historical_auto.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/report_md/_gpt/cx_parity_j1d_literal_zero.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/report_md/_gpt/cx_parity_mlp_noso2_fixed.md` | Tagged | `[INVALID — pre-ab56c2d]` header added |
| `compute_vit/scripts/_gpt/launch_cx_k4r_fresh_eval.sh` | Created | Auto-eval launcher for post-training fresh-instance assessment |

---

## 5. Decisions Made

- **Branch A = canonical (no-multiplier, negative second-order)**
  - *Rationale:* The no-multiplier form matches paper Equation S2 intentionally; it is a behavioral proxy for position-dependent gradient attenuation, not a strict derivative of `f(G)=G^NL`. The negative second-order sign is physically grounded as a brake term. Branch B (multiplier) is formally rescinded.

- **`group=all` mainline, `group=mlp` diagnostic-only**
  - *Rationale:* `group=all` with uniform-NL and per-epoch D2D resampling is the only configuration with demonstrated hardware-instance generalization under canonical semantics. `group=mlp` mixed-NL exposes configuration conflicts and STE sensitivity; retained for diagnostic contrast but not cited as a primary result.

- **V4 ~97% likely valid (NL=1 default)**
  - *Rationale:* Default NL=1.0 renders the STE surrogate identity; both first-order and second-order terms collapse to no-ops, so the sign/multiplier bug cannot propagate. V4 is therefore insulated from the semantics drift.

- **All pre-`ab56c2d` K-series invalid**
  - *Rationale:* J1d, K2, K3, K4 (alpha=0.00/0.25/0.50), all parity probes, and the first K4R attempt were executed with wrong second-order signs (positive `ltp_corr` / `ltd_corr`). Internal rankings may retain qualitative value, but absolute numbers are void.

---

## 6. Outstanding Risks

- **K4R may plateau <90% fresh-instance**
  - Train/test gap is widening (~8 pp at Epoch 59); overfit plateau remains a live concern. If fresh-instance mean falls below 90%, the severe-NL regime may need architectural intervention beyond STE tuning.

- **86.37% appears in additional files not yet audited**
  - Contamination scrub focused on high-visibility deliverables (slides, press release, paper scope). Historical memos (`KIMI_HAT_AS_REGULARIZER_NOTE_20260420.md`, `AGENT_SYNC_gpt.md`, etc.) may still cite the voided number without `[INVALID]` guardrails.

- **V4 canonical validity needs confirmation**
  - While theoretically insulated (NL=1), no formal fresh-instance re-evaluation has been run on the exact `ab56c2d` commit. A fast parity anchor (1–5 epochs) would close this residual risk.

---

## 7. Next Actions (Prioritized)

1. **P0 — Await K4R completion + execute fresh-instance eval (10×5)**
   - Do not declare any canonical severe-NL numbers until this eval finishes.
2. **P1 — Codex errata headers on CODEX_* broadcasts**
   - `CODEX_STE_MULTIPLIER_FIX_20260422.md` (rescinded)
   - `CODEX_ROUTE_DECISION_20260422.md` (errata)
   - `CODEX_PROVENANCE_DRIFT_AUDIT_20260422.md` (resolved)
3. **P1 — Audit remaining files for 86.37% / 88.53% contamination**
   - Target: `AGENT_SYNC_gpt.md`, `KIMI_HAT_AS_REGULARIZER_NOTE_20260420.md`, thesis Ch.5/6 drafts, any locked markdown in `paper/`.
4. **P2 — Gemini second-order coefficient validation deadline (2026-04-23 12:00 CST)**
   - Confirm whether coefficient is `nl*(nl-1)` (code comment claim) or `(nl-1)` (Gemini `S'(u)` derivation). Broadcast derivation if `(nl-1)` wins.
5. **P2 — Fast V4 parity anchor on `ab56c2d`**
   - 1-epoch smoke test to confirm NL=1 insulation and rule out unexpected regression.
6. **P3 — Queue K2 re-evaluation (N=30)**
   - Only after K4R fresh-eval confirms the corrected STE landscape is viable.

---

*Broadcast compiled: 2026-04-23 00:xx CST*
*Canonical anchor: `ab56c2d`*
*All pre-`ab56c2d` numbers are `[INVALID]` unless explicitly re-validated.*
