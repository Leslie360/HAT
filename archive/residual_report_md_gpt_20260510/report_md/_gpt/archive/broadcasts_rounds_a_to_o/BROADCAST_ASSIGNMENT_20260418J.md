> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round J Broadcast — 2026-04-19 22:35 (external-review triage response)

**Author:** Claude
**Trigger:** `EXTERNAL_REVIEW_COMPILATION_20260419.md` (5 reviewers) + `KIMI_TRIAGE_EXTERNAL_REVIEW_20260419.md`. 3 blockers + 6 should-fix + 4 nice-to-have.
**Quota:** Kimi ✅ plentiful, Codex ⚠️ tight, Gemini ❌ frozen.

---

## External-review synthesis

| Reviewer | Verdict | Load-bearing reason |
|:--|:--|:--|
| A | Major Revision | Title/abstract over-promises "deployment" vs. Discussion's hedge |
| B | Minor Revision | Scientifically mature; framing refinement only |
| C | Minor Revision | 2 concrete errors (SX.Y miss + two-level MC undisclosed) hurt first impression |
| D | Minor Revision | Honest bounding + statistical rigor |
| E | Major Revision (achievable) | i.i.d. Gaussian D2D is the biggest vulnerability; one correlated ablation disarms it |

**Consensus:** Competitive Major-Revision submission. 3 blockers are low-effort / high-impact.

---

## Verification of reviewer claims against current disk state

| Claim | Reality | Action |
|:--|:--|:--|
| B-1: SX.Y note missing | **FALSE — actually at `supplementary.tex:715`** (Reviewer C read stale snapshot) | Mark ✅ no action |
| B-2: two-level MC undisclosed | **TRUE** — `03_methodology.tex` does not state the 10-instance × 5-MC hierarchy | Fix required |
| B-3: MLP fresh-instance ~32% invisible | **TRUE** — Table S16 caption has no mention | Fix required |
| S-1: spatially-correlated D2D absent | **TRUE** — only i.i.d. Gaussian | GPU ablation proposed |

Only B-2, B-3, S-1 remain as real blockers. B-1 is already solved.

---

## Task dispatch

### KIMI — Round J text edits (primary executor)

#### 🔴 CRITICAL — 3 remaining blockers (~30 min total)

| ID | Item | Location | Exact edit |
|:--|:--|:--|:--|
| **K-Q1** | **B-2: Disclose two-level MC hierarchy** | `paper/latex_gpt/sections/03_methodology.tex` near Eq. 4 (Ensemble HAT section) | Add: *"Each fresh-instance mean is itself the mean of 5 forward-pass MC evaluations; the reported ±1.54\% is the standard deviation across the 10 per-instance means."* |
| **K-Q2** | **B-3: MLP fresh-instance ~32% disclosure** | Table S16 interpretation note (supp §NL ablation) | Add: *"Note that the MLP-linearized model achieves \textasciitilde 32\% fresh-instance transfer accuracy under the same 10-array evaluation protocol used for Ensemble HAT, compared to 86.37$\pm$1.54\% for Ensemble HAT, confirming that this ablation is a training-diagnostic tool rather than a deployment-grade mitigation."* |
| **K-Q3** | **B-1 verification**: grep `supplementary.tex` for `Note SX.Y` and `sections/06_discussion.tex` line 47; confirm the note is reachable. Already ✅ — deliverable is a 1-line audit `KIMI_B1_VERIFICATION_20260419.md`. | two files | log pass |

#### 🟡 Should-fix — text layer (~1.5 h)

| ID | Item | Location | Edit |
|:--|:--|:--|:--|
| **K-Q4** | **S-2: framing hedge** in abstract | `00_abstract.tex` first sentence | Start with: *"We present a simulation framework for..."* (preserve subsequent content). Mirror in §4.5 Limitations: *"Validation against fabricated organic arrays is deferred to future work."* |
| **K-Q5** | **S-4: soften CrossSim 14.43 pp wording** | `06_discussion.tex:47` | Replace *"a 14.43~pp gap"* → *"a large qualitative divergence (14.43 pp at n=3, preliminary; see Supp Note SX.Y)"* |
| **K-Q6** | **S-5: ImageNet failure-mode prediction** | §4.5 Limitations | Add 3 sentences covering: (i) training overhead of per-epoch D2D resampling at ImageNet scale; (ii) 6-bit ADC cliff may shift to 8-bit for deeper MLPs with finer decision boundaries; (iii) attention-head specialization from fresh init vs. fine-tuning. |
| **K-Q7** | **S-6: forward pointers** for pre-defined equations | §5 Results, first citation of Eq. 1 / Eq. 3 / Eq. 8 | Add "(formally defined in Section~\ref{sec:methodology}, Eq.~\ref{...})" on each first use. Note: Eq. 1 already has the pointer (CX-BI). Add for the other two. |
| **K-Q8** | **N-1: 10.00% collapsed-predictor wording** | §5 Results (intro paragraph) or §6 Discussion first mention | Add: *"This 10.00\% reflects a collapsed single-class predictor on class-balanced CIFAR-10 — every fresh instance produces the same degenerate label map — not a noisy dispersion around chance."* |
| **K-Q9** | **N-2: per-batch HAT baseline to main text** | §5.3 or §5.4 | One sentence: *"Per-batch D2D resampling degrades to 86.16\%, while the fixed-mask baseline collapses to 10.00\%, confirming that structured epoch-level resampling is the load-bearing design choice."* |
| **K-Q10** | **N-3: write-verify overhead** | §4.5 Limitations | One sentence: *"The energy model assumes ideal single-shot programming; iterative write-verify overhead for 4-bit conductance states is not included."* |
| **K-Q11** | **N-4: energy placeholder qualifier** | §7 Conclusion | Where energy numbers appear, restore the "first-order upper bound under placeholder constants" qualifier. |

#### 🟡 Post-CX-BB dependent

| ID | Item | Trigger |
|:--|:--|:--|
| **K-Q12** | **Fold C-1 re-run result** into manuscript | After CX-BB JSON lands and Claude reviews |
| **K-Q13** | **Consistency sweep v2** | After K-Q1–K-Q11 land |
| **K-Q14** | **Final readthrough** | After K-Q13 passes |

---

### CODEX — Round J (GPU + scripts; tight quota)

| ID | Item | Type | Priority | Gate |
|:--|:--|:--|:--:|:--|
| **CX-CA** | **S-1 spatial-correlation D2D ablation** | GPU + code | HIGH (thesis + rebuttal) | After CX-BB finishes (ep59 no-AMP re-run). ~4–8 h. |
| **CX-CB** | **S-3 Figure 1 visual disambiguation** | matplotlib | MED | Anytime CPU — add hatch pattern to deterministic bars + dashed outline |
| **CX-CC** | **Submission bundle rebuild (CX-BK carry-over)** | bundle | MED | After K-Q1–Q11 land + recompile |
| **CX-CD** | **Re-run check_locked_numbers.py** | script | LOW | After CX-CC |

**CX-CA spec:**
- Sampling: 2D spatial covariance over crossbar grid. Start with AR(1) with ρ=0.3 (moderate); if time permits also ρ=0.5 (strong).
- Protocol: load canonical V4 Ensemble HAT checkpoint; evaluate under (a) i.i.d. Gaussian D2D (baseline), (b) correlated D2D ρ=0.3. 10 fresh instances × 5 MC runs each. Same eval harness as `eval_standard_fresh_instance_noamp.py`.
- Target metric: fresh-instance transfer mean±std. **Success condition = ranking preserved (Ensemble > Standard)**; absolute accuracy may drop.
- Output: `report_md/_gpt/json_gpt/fresh_instance_eval_v4_ensemble_correlated_d2d.json` + 1-table summary `CODEX_S1_CORRELATED_D2D_20260420.md`.

**Codex NOT doing:** any tex edits (all absorbed into K-Q1–Q11). This preserves Codex quota for the GPU experiment.

---

### CLAUDE self

| ID | Task |
|:--|:--|
| **CLAUDE-AL** | Audit Kimi K-Q1–Q11 edits before Codex recompile |
| **CLAUDE-AM** | Interpret CX-BB C-1 result when JSON lands |
| **CLAUDE-AN** | Interpret CX-CA correlated-D2D result (go/no-go on Reviewer E objection) |
| **CLAUDE-AO** | Final read of `RESPONSE_LETTER_FINAL_20260419.md` — confirm reviewer-facing framing matches post-Round-J manuscript |
| **CLAUDE-AP** | Spot-check submission bundle post-CX-CC |

---

### USER (unchanged — still blocking submission)

- Acknowledgements text (funding/grant line)
- Corresponding author + email
- Suggested reviewers (3–5)

---

## Execution pipeline

```
t0 (now):
  Kimi starts K-Q1..Q11 (parallel text edits, ~1.5 h total)
  CX-BB + CX-AB still running on GPU (do not disturb)
  Claude monitors + audits as edits land

t+1.5h:
  Kimi done; Claude CLAUDE-AL audits
  If CX-BB finishes → CLAUDE-AM interpret
  Codex CX-CB Figure 1 redraw (CPU, parallel)

t+2-3h:
  CX-BB done, C-1 result folded into manuscript (K-Q12)
  Codex launches CX-CA (correlated D2D, GPU now free)
  Kimi K-Q13 consistency sweep v2

t+6-10h:
  CX-CA done; CLAUDE-AN interpret
  Result added to manuscript or supplementary
  Codex CX-CC bundle rebuild + CX-CD locked-numbers

t+10h:
  Kimi K-Q14 final readthrough
  CLAUDE-AO response-letter pass
  CLAUDE-AP bundle spot-check

Submission ready pending user metadata.
```

---

## Termination criteria for Round J

- ✅ K-Q1, K-Q2 landed (2 remaining real blockers closed)
- ✅ K-Q4–Q11 text fixes landed
- ✅ CX-BB C-1 result interpreted + folded (via K-Q12)
- ✅ CX-CA correlated-D2D result interpreted (via CLAUDE-AN); ranking-preserved claim or documented caveat
- ✅ main/supp/cover recompile clean; 16/16 (or updated) locked numbers pass
- ✅ Submission bundle rebuilt (CX-CC)

---

## Deferred (no submission impact)

- CX-AC joint MLP-Linear + Ensemble HAT training (thesis-only)
- Zenodo DOI pre-reserve
- Full 10,000-image CrossSim re-run
- Chinese PROVENANCE_AUDIT translation

---

**End of broadcast.** Kimi: K-Q1–Q11 all in parallel, each <15 min. Codex: stand by for CX-CA after CX-BB finishes; do CX-CB anytime. Claude: audit pipeline. Gemini: frozen.
