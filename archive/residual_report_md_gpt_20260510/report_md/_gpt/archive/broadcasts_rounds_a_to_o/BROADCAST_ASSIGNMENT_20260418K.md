> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round K Broadcast — 2026-04-19 02:15 (post-Round-J landings, quota Kimi > Gemini > Codex)

**Author:** Claude
**Trigger:** Round J largely complete. CX-BB confirmed 10.00% collapse REAL (not AMP artifact). CX-AB locked all-linear at 32.60±9.18%. CX-CA smoke shows ranking preserved (iid 87.45 vs ρ=0.3 86.78, Δ=0.67 pp). Codex landed B-1/B-2/B-3 + Fig 1 hatching. Full CX-CA still on GPU.
**Quota:** Kimi ✅ plentiful · Gemini 🟡 medium · Codex 🔴 tight (preserve for GPU harvest + bundle).

---

## Round-J landing snapshot (truth on disk)

| Item | State | Evidence |
|:--|:--|:--|
| B-1 SX.Y reachability | ✅ verified | `KIMI_B1_VERIFICATION_20260419.md`; `supplementary.tex:715` |
| B-2 two-level MC disclosure | ✅ landed | `paper/latex_gpt/sections/03_methodology.tex` near Eq. 4 |
| B-3 MLP fresh-instance ~32% caveat | ✅ landed | `supplementary.tex:789` |
| K-Q8 collapsed-predictor wording | ✅ landed | `05_results.tex:41` |
| K-Q10 write-verify overhead | ✅ landed | `06_discussion.tex:43` |
| K-Q11 placeholder qualifier | ✅ landed | `06_discussion.tex:38` |
| K-Q4 abstract framing hedge | 🟡 verify | `00_abstract.tex` |
| K-Q5 CrossSim 14.43 pp softening | 🟡 verify | `06_discussion.tex:47` |
| K-Q7 forward pointers Eq.3/Eq.8 | 🟡 verify | `05_results.tex` |
| K-Q9 per-batch HAT one-liner | 🟡 verify | `05_results.tex` |
| K-Q6 ImageNet failure-mode prediction | 🟡 verify | `06_discussion.tex` §4.5 |
| CX-BB no-AMP rerun | ✅ done | `fresh_instance_eval_v4_standard_noamp.md` (10.00±0.00%) |
| CX-AB all-linear lane | ✅ done | `NL_FRESH_INSTANCE_CONTROLS_ALL_ONLY_20260418.md` (32.60±9.18%) |
| CX-CA spatial corr smoke | ✅ done | `_SMOKE_CORRELATED_D2D.md` (iid 87.45, ρ=0.3 86.78) |
| CX-CA full run (10×5) | 🟡 in flight | host WSL launcher `82739` |
| CX-CB Fig 1 hatching + footer | ✅ landed | `paper/figures/fig4_accuracy_comparison.png` |
| Main + supp recompile | ✅ clean | no undefined / overfull / underfull |

**3 reviewer-blocking items closed in source.** Remaining work is fold-in of confirmed evidence + final polish.

---

## KIMI — Round K (HEAVIEST allocation)

Quota allows broad text work. Run K-R1–K-R6 in parallel where possible; each <30 min.

### 🔴 CRITICAL — fold confirmed evidence into manuscript

| ID | Item | Where | What to write |
|:--|:--|:--|:--|
| **K-R1** | **CX-BB confirmation: 10.00% collapse is REAL** | `05_results.tex` (after K-Q8 collapsed-predictor sentence) and Supp Note SX.Y | Add: *"This collapse was independently confirmed under FP32 inference (no AMP) across 10 fresh D2D instances × 5 MC evaluations: 10.00 ± 0.00% (`fresh_instance_eval_v4_standard_noamp.json`). The single-class predictor is a deterministic outcome of fixed-mask training under epoch-resampled D2D, not a numerical artifact."* |
| **K-R2** | **CX-AB confirmation: all-linear lane = 32.60±9.18%** | Supp NL ablation table caption (Table SX.N) | Add row + footnote: *"`all-linear` upper-bound control: 87.49\% in-domain, 32.60 ± 9.18\% fresh-instance (10 × 5 protocol). Linearizing every analog block does not restore deployment-grade transfer, confirming the diagnostic-only framing of MLP-only and QKV-only ablations."* |
| **K-R3** | **CX-CA smoke note (preliminary, full pending)** | New Supp paragraph or Limitations §4.5 | Add hedged sentence: *"A preliminary single-instance probe with separable AR(1) ρ=0.3 spatial correlation across the crossbar grid yields 86.78\% versus 87.45\% under the matched i.i.d. baseline (Δ = 0.67 pp), consistent with rank preservation; the full 10 × 5 sweep across ρ ∈ \{0.3, 0.5\} is in flight and will replace this note when complete."* |

### 🟡 SHOULD-FIX — verify Round-J residuals actually landed

| ID | Item | Action |
|:--|:--|:--|
| **K-R4** | **Verify K-Q4, K-Q5, K-Q6, K-Q7, K-Q9** all present in source | grep each tex file; produce 1-page audit `KIMI_ROUND_J_RESIDUAL_AUDIT.md` listing PASS/FAIL with line numbers. If any FAIL, land the missing edit per K-Q spec in Round J broadcast. |
| **K-R5** | **K-Q13 consistency sweep v2** | Re-grep entire `paper/latex_gpt/` for: (a) any `86.37` not paired with `±1.54`; (b) any `10.00%` not labelled as collapsed-predictor; (c) any `14.43` not paired with the SX.Y forward pointer; (d) any `32.12` or `32.60` without "diagnostic" or "fresh-instance" framing. Report `KIMI_CONSISTENCY_SWEEP_V2_20260419.md`. |
| **K-R6** | **`RESPONSE_LETTER_FINAL_20260419.md` finalize** | Update against current source state: (i) add CX-BB no-AMP confirmation under Reviewer C/D Q on 10.00% authenticity; (ii) add CX-AB all-linear=32.60% under Reviewer A/B Q on mitigation breadth; (iii) add CX-CA smoke under Reviewer E Q on i.i.d. assumption; (iv) flag B-1 was Reviewer C reading a stale snapshot. |

### 🟡 POST-CX-CA (gated)

| ID | Item | Trigger |
|:--|:--|:--|
| **K-R7** | **Replace K-R3 hedge with full result** | When `fresh_instance_eval_v4_ensemble_correlated_d2d.json` lands. Use Δ < 1 pp wording if ranking preserved across both ρ; otherwise escalate. |
| **K-R8** | **K-Q14 final readthrough** | After K-R1–K-R6 land + K-R7 fold + Codex bundle rebuild. End-to-end main + supp + cover. |

---

## GEMINI — Round K (medium quota; stateless design briefs)

Stateless: each task self-contained, output a single Markdown deliverable. Do NOT modify source tex directly.

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-Z1** | **Why does AR(1) ρ=0.3 preserve ranking?** Mechanism paragraph | `GEMINI_CORRELATED_D2D_MECHANISM.md` (≤300 words) | Argue why moderate spatial correlation in D2D variability does not collapse Ensemble HAT advantage: tile-level averaging in QKᵀ projections, residual-path variance budget, AR(1) eigenvalue decay vs. effective receptive field. Cite generic neuromorphic/CIM literature. Goal: feed into K-R3/K-R7 fold-in as scientific justification, not just empirical observation. |
| **G-Z2** | **Mechanistic story for 10.00% single-class collapse** | `GEMINI_SINGLE_CLASS_COLLAPSE_MECHANISM.md` (≤300 words) | Explain why fixed-mask training under epoch-resampled D2D converges to a degenerate single-class predictor at fresh-instance time. Logit margin under shifted-mean perturbation, optimizer's exploitation of train-time D2D realization, attention head specialization. This deepens K-Q8 / K-R1. |
| **G-Z3** | **Thesis chapter integration brief** | `GEMINI_THESIS_INTEGRATION_BRIEF.md` (≤500 words) | Outline how the three confirmed results (10.00% collapse REAL · 32.60% all-linear · CX-CA ranking preservation) reshape the thesis chapter on hardware-aware training. Suggest section ordering, cross-references to the manuscript, what the thesis can claim that the NC paper cannot. |
| **G-Z4** | **D2D-correlation sensitivity figure design** | `GEMINI_FIG_CORR_D2D_SPEC.md` (≤200 words + ASCII sketch) | Spec a publication-quality figure for the eventual full CX-CA result: x-axis ρ ∈ {0, 0.3, 0.5}, y-axis fresh-instance accuracy, error bars from MC, dual-curve (Standard fixed-mask vs Ensemble HAT). Include caption draft. Codex will execute later. |

**Gemini NOT doing:** any source-tex edits, any GPU work, any bundle work.

---

## CODEX — Round K (TIGHT quota; GPU harvest + bundle only)

Reserve quota strictly for tasks that nobody else can do.

| ID | Item | Type | Priority | Gate |
|:--|:--|:--|:--:|:--|
| **CX-DA** | **Harvest CX-CA full correlated-D2D JSON** when run completes | GPU monitor + report | HIGH | When `fresh_instance_eval_v4_ensemble_correlated_d2d.json` appears. Produce `CODEX_S1_CORRELATED_D2D_20260420.md` with the agreed table format: ρ × {iid, 0.3, 0.5} × {Standard, Ensemble HAT} fresh-instance mean ± std. Notify Claude + Kimi. |
| **CX-DB** | **Submission bundle rebuild** (CX-CC carry-over) | bundle | MED | After K-R1–K-R6 land **AND** CX-DA folded via K-R7. Rebuild `outputs/submission_bundle_20260419/` with refreshed main.pdf, supplementary_main.pdf, cover_letter.pdf, source_data, README. |
| **CX-DC** | **Re-run `check_locked_numbers.py`** | script | LOW | After CX-DB. Append result to `AGENT_SYNC_gpt.md`. |

**Codex DEFERRED (no Round K execution):**
- CX-AC joint MLP-Linear + Ensemble HAT training (thesis-only, not on submission path)
- Any new tex edits (Kimi has the text layer)
- Any new figure work beyond CX-CB (already done)

---

## CLAUDE self

| ID | Task |
|:--|:--|
| **CLAUDE-AQ** | Audit K-R1–K-R6 landing in source on completion |
| **CLAUDE-AR** | Cross-check K-R7 fold-in against CX-DA harvest table for numerical match |
| **CLAUDE-AS** | Spot-check submission bundle (CX-DB) — verify PDF page counts, source_data presence |
| **CLAUDE-AT** | Final read of `RESPONSE_LETTER_FINAL_20260419.md` post-K-R6 |
| **CLAUDE-AU** | Decide go/no-go on submission once user supplies metadata |

---

## USER (still blocking submission — unchanged)

- Acknowledgements text (funding/grant line) — *user wrote: "123，是学校单位，我自己写"*
- Corresponding author + email — user-owned
- Suggested reviewers (3–5) — user-owned

---

## Execution pipeline

```
t0 (now):
  Kimi launches K-R1, K-R2, K-R3 in parallel (fold confirmed evidence)
  Kimi launches K-R4 audit + K-R5 sweep in parallel
  Gemini launches G-Z1–G-Z4 in parallel (all stateless)
  Codex stands by on CX-DA monitor; CX-CA still in flight

t+1h:
  K-R1–R3 landed; K-R4/R5 audits in
  Gemini deliverables in
  Claude CLAUDE-AQ audit
  Kimi K-R6 finalizes response letter

t+2-4h:
  CX-CA full JSON lands → CX-DA harvest → CODEX_S1 report
  Kimi K-R7 folds full result (replaces K-R3 hedge)
  Claude CLAUDE-AR cross-check

t+5-7h:
  Codex CX-DB bundle rebuild; CX-DC locked-numbers
  Kimi K-R8 final readthrough
  Claude CLAUDE-AS bundle spot-check + CLAUDE-AT response letter

t+8h:
  Submission ready pending user metadata.
```

---

## Termination criteria for Round K

- ✅ K-R1, K-R2 landed (CX-BB + CX-AB folded)
- ✅ K-R3 (smoke hedge) → K-R7 (full result) landed
- ✅ K-R4 audit shows all Round-J residuals PASS (or any FAIL fixed)
- ✅ K-R5 consistency sweep v2 clean
- ✅ K-R6 response letter finalized against current source
- ✅ CX-DA harvest produces locked correlated-D2D table
- ✅ CX-DB bundle rebuilt; CX-DC locked-numbers pass
- ✅ Gemini G-Z1–Z4 design briefs available for thesis + future figure work
- ✅ Main + supp + cover recompile clean

---

**End of Round K broadcast.** Kimi is the workhorse this round. Gemini drafts the scientific framing/design briefs. Codex preserves quota for GPU harvest + bundle only. Gemini frozen state lifted (medium quota). Order of operations matters for K-R7 ↔ CX-DA gate.
