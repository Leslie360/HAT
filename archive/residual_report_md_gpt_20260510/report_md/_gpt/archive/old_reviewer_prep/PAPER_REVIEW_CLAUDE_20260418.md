# Paper Review — Claude, 2026-04-18

**Scope:** `paper/latex_gpt/sections/00_abstract.tex` → `08_appendix.tex` + `cover_letter.tex`.
**Trigger:** User request — audit along four dimensions: (1) 物理映射尚未覆盖的部分（未来方向）, (2) 数据严谨性, (3) 计算表述清晰度, (4) 缩写首次出现的全称, plus 文件/项目管理.
**Type:** Review memo only. No `.tex` edits in this pass. Fixes registered as CLAUDE-F on the task ledger.

---

## §1 Abbreviation first-use audit

Nature Communications style rule: expand every abbreviation at first textual appearance; re-use allowed thereafter. I grep'd every section; the table below lists each abbreviation I could find in the main text and whether it was expanded.

| # | Abbrev | Full form | First appearance | Status | Proposed fix |
|:--|:--|:--|:--|:--:|:--|
| A1 | **ADC** | analog-to-digital converter | `00_abstract.tex:5` | ✗ never expanded (used ~15×) | abstract: `reducing analog-to-digital converter (ADC) resolution below 6 bits…` |
| A2 | **OPECT** | organic photoelectrochemical transistor | `00_abstract.tex:5` | ✗ never expanded (critical for an organic-device paper) | abstract or intro: `organic photoelectrochemical transistor (OPECT)` on first mention |
| A3 | **HAT** | hardware-aware training | `00_abstract.tex:5` (abstract) | ✗ in abstract; ✅ later in §1:9 | abstract: add `hardware-aware training (HAT)` at first use; intro's parenthetical is a duplicate |
| A4 | **D2D** | device-to-device | `00_abstract.tex:5` | ✗ in abstract; ✅ later in §1:9 | abstract: `device-to-device (D2D) variability` first time |
| A5 | **C2C** | cycle-to-cycle | `03_methodology.tex:17` (parenthetical) | ⚠️ defined in §3 but used unexpanded in §6 summary stress-test sentence | OK if §3 remains first use; if abstract ever cites it, expand there |
| A6 | **NL** | nonlinear write | `00_abstract.tex:5` (`NL=2.0`) | ✗ never expanded; symbol used without glossary | abstract: `severe nonlinear write (NL=2.0)`; methodology: add `NL_{LTP}` / `NL_{LTD}` definition the first time |
| A7 | **LTP / LTD** | long-term potentiation / long-term depression | `03_methodology.tex:46` | ✗ never expanded | §3 first use: `NL_{LTP}=1` (long-term potentiation) / `NL_{LTD}=-1` (long-term depression)` |
| A8 | **CNN** | convolutional neural network | `01_introduction.tex:17` | ✗ not expanded | §1 contribution-4 sentence: `across convolutional neural network (CNN) and Vision Transformer (ViT) backbones` |
| A9 | **ViT** | Vision Transformer | `01_introduction.tex:7` | ✗ not expanded (paper title uses "Vision"; body uses "ViT" freely) | same as A8 |
| A10 | **MLP** | multi-layer perceptron | `01_introduction.tex:17` (contribution-4 "MLP path") | ✗ never expanded | §1 contribution-4: `multi-layer perceptron (MLP) path of the transformer` |
| A11 | **SRAM** | static random-access memory | `01_introduction.tex:5` | ✗ not expanded | §1:5: `conventional static random-access memory (SRAM) and emerging resistive memories` |
| A12 | **STE** | straight-through estimator | `03_methodology.tex:28` ("straight-through quantizer") + `03_methodology.tex:46` ("STE backward pass") | ⚠️ full phrase appears early but abbreviation is introduced later without a linking parenthesis | §3 first use: `…via a straight-through quantizer $Q_n(\cdot)$` → `…via a straight-through estimator (STE) quantizer` |
| A13 | **MC** | Monte Carlo | `05_results.tex:18` (Fig 4 caption), `05_results.tex:51` ("10 MC runs per point") | ✗ never expanded | §5 first use: `$10$ Monte Carlo (MC) runs per point` |
| A14 | **IR drop** | current–resistance drop (Ohm's-law voltage drop on array wires) | `06_discussion.tex:30` (compound stress), `01:19` (limitations preview) | ⚠️ term is standard in analog-IC community but unfamiliar to a general bio/photonics reviewer | §1:19 first use: `array-level parasitics (current–resistance / IR drop, sneak paths)` |
| A15 | **FP32** | 32-bit floating-point (single precision) | `01:7`, `05:8`, `06:38` | ⚠️ conventional but paper lists it next to "FP32 digital baseline" — some reviewers want it spelled | §5:8 first use: `Digital FP32 (single-precision) baselines are …` |
| A16 | **DNTT** | dinaphtho-thieno-thiothiophene (material name) | `03:46` via citation | ⚠️ material names are typically left abbreviated but first mention in a broad-readership journal benefits from one expansion | §3:46: `measured DNTT (dinaphtho-thieno-thiothiophene) transients` |
| A17 | **QAT** | quantization-aware training | `01:9` ("quantization-aware training") | ✅ full form appears; abbreviation never instantiated, which is acceptable | no action |
| A18 | **PCM / RRAM** | phase-change memory / resistive random-access memory | `05:82` (Fig 10 caption: "PCM and RRAM") | ✗ not expanded | Fig 10 caption: `phase-change memory (PCM) and resistive random-access memory (RRAM)` |
| A19 | **S_ADC / S_D2D** | first-order Sobol index for (ADC / D2D) | `00_abstract.tex` (`S_ADC=0.98`) implied later | ⚠️ symbol used before §6 paragraph that defines Sobol | abstract caveat: `a first-order Sobol decomposition over a 63-point D2D–ADC grid` already does the job; verify the abstract wording does not drop "first-order" |
| A20 | **pp** | percentage points | `01:15` ("+5.8 percentage points") | ✅ expanded on first use | no action |
| A21 | **LSB** | least significant bit | supplementary ADC table (`+0.5 LSB`) | ⚠️ supp-only; confirm supp has one expansion | supp first use: `one half of the least significant bit (LSB)` |
| A22 | **GELU / LayerNorm / softmax** | non-abbreviations that some journals still italicize | `06:26` ("softmax exponentiates") | no action | no action |
| A23 | **SNR** | signal-to-noise ratio | supp figures `\SuppFigSnr` | ⚠️ confirm supp expands on first use | supp first use |
| A24 | **PPF / RC-16 / RC-64** | paired-pulse facilitation / retention-class labels | `数据_博士/` + `DOCTOR_MEASURED_PROFILE_*` | supp-only; verify expansion there | supp first use |

**Recommendation:** a single consolidated pass through abstract + §1 + §3 + §5 fixes A1–A11, A13. A14–A16 / A18 are one-liners. A12 / A19 require coordination between §3 and abstract. Total edit budget: ~15 inline parentheticals, zero page-count impact.

---

## §2 Data rigor — missing error bars, unstated n, unstated tests

| # | Claim (location) | Rigor gap | What's needed |
|:--|:--|:--|:--|
| D1 | `88.53%` OPECT zero-shot accuracy (abstract, §5:77, §7:9, cover letter) | single point value, no error bar, no n, no MC spread | either re-run as $n$-run MC and report `mean ± std`, or explicitly state "single-inference deterministic evaluation under fixed profile" in abstract footnote / §5 sentence |
| D2 | `97.39%` V2 zero-noise hybrid control (§5:13) | no error bar | add `n=? runs, mean ± std`; per `p14_flowers_v2_result.json` it's a 10-run result at `91.30±0.00%`, but that's Flowers; the `97.39%` is CIFAR-10 V2 — verify n |
| D3 | `+5.8 pp` inverse-gamma (`89.85% vs 84.04%`) (§5:46, intro) | no error bar on either endpoint; no explicit `n` | A2.3 sweep is a 5×4 grid; state `n=? seeds per cell; values are seed means` |
| D4 | `p < 10^{-15}` Ensemble HAT vs standard (§5:63) | no test name (Welch's t? paired-t? bootstrap?), no n, no df | state `n=10 fresh arrays per arm, two-sample Welch's t-test, df=…` (or whatever it actually is — PROVENANCE §11 G3 already flagged; Codex CX-D to identify) |
| D5 | Cadence values `88.41% / 87.18% / 86.16%` (§5:63) | three point values; no spread across seeds | either cite supp spread or add ±std inline |
| D6 | retention plateau "near 79%" (§5:36) | quantitative values in `CANONICAL_RESULT_LOCK §3` (91.63 / 82.66 / 79.13 / 79.05 / 79.35 / 79.51%) but main text has only the narrative | one sentence citing the canonical table or a supp row |
| D7 | `23.86% → 60.54%` ConvNeXt CIFAR-100 HAT (§5:29) and similar CIFAR-100 cells | best-checkpoint values per `CANONICAL_RESULT_LOCK §2`; allowed by rule but readers may not know — text should say so once | §5.2 add one clause: `values reported are best-checkpoint accuracies per the rule stated in the Supplementary Methods` |
| D8 | compound stress `2% C2C, 3% D2D, 6-bit ADC, 1% IR drop, 1% sneak path, 1000s retention → 89.61%` (§6:30) | single-run value; IR drop / sneak path entered as ad-hoc placeholders, not from a physical model | state n-run spread AND explicitly mark IR drop / sneak path as first-order placeholders (§6 already does this weakly; strengthen) |
| D9 | `14.43 pp` CrossSim gap (§6:47, in-line) | MC spread is in supp but main-text sentence gives one number | add `(5-seed means; see Supp Table …)` |
| D10 | 63-point grid × 10 MC/pt → Sobol index | seed-reuse policy not documented | §3.4 or §5.6 add one sentence on seed policy (`seeds redrawn per grid point` vs `shared seed across grid`) |
| D11 | Zhang proxy C2C-insensitivity table (`08_appendix.tex:76–88`) | honest interpretation is given but the all-identical rows will prompt a reviewer complaint regardless | keep current caveat but add one-line foot: `rows repeat exactly because C2C sampling noise is sub-resolution under the MC precision used` |
| D12 | Energy claim `~11×, ~60% digital` (§6:38) | already de-rated to rounded figures after the Energy-Precision broadcast; ensure the placeholder-constants caveat survives all subsequent edit passes | flag for the pre-submission consistency sweep |
| D13 | Fig 4 caption "Error bars denote ±1 σ where MC statistics are available" (§5:18) | mixing cells with / without error bars in one figure is a reviewer red flag | either compute MC for the bare-bar cells or split into two panels |

**Priority:** D1 / D4 are the two items that will most likely draw a reviewer. D3 is the second largest — it's the +5.8-pp headline and has no statistic. D10 is a methodological loose end that costs one sentence.

---

## §3 Calculation clarity — equations and procedures that need one more line

| # | Location | Issue | Minimum fix |
|:--|:--|:--|:--|
| C1 | Eq. 4 `scale recovery` (§3:18–27) | two cases labeled "standard" and "retention-time recalibration" — but main text never says which case is used in which experiment | one sentence at end of §3.2: `Unless otherwise stated, we use the standard-calibration branch; the retention-recalibration branch is used only for the V8 retention-drift experiments (§5.3).` |
| C2 | Eq. 8 photocurrent shot noise | `Var[ε_shot] ∝ I_photo` is a verbal caption; proportionality constant is silent | one line: `ε_shot ∼ N(0, κ I_photo)` with κ defined in terms of photon-count gain, or state κ is absorbed into the per-profile calibration |
| C3 | Eq. 6 / Eq. 7 Ensemble HAT expectation | "resample M at each epoch" is prose; not clear how the expectation is estimated — one sample per epoch? Multiple? Per-batch? | §3.2 last paragraph: `the expectation in Eq. (6) is Monte Carlo–estimated with one freshly sampled mismatch map M per training epoch, held constant across all mini-batches within that epoch.` |
| C4 | Eq. 11 Sobol index (§3.4) | estimator not specified: Saltelli? pick–freeze? direct variance partitioning over the grid? | §3.4 second sentence: `We estimate each S_i directly from the 7×9 grid of MC means as Var(mean_grid[X_i]) / Var(Y), without resampling; the narrow MC variance within each cell contributes a known lower-bound correction …` |
| C5 | `p < 10^{-15}` (§5:63) | test-statistic type invisible; reader cannot reproduce | one clause: `…(two-sample Welch's t-test on 10 fresh-instance means, df=18).` |
| C6 | "baseline gradient-scaling approximation" (abstract, §5, §7) | referred to four times but mathematically defined only as "NL modifies STE backward pass according to present conductance state, Supp Eq. S2" | main text should carry one self-contained line — the reader should not have to pull up the supp to know what the anchor number is anchored against |
| C7 | hybrid mapping policy (§3.1, §2.3) | "dense linear operators execute on crossbars; control-heavy operators remain digital" is a policy, not a list | add a short bullet list or table: `Analog: query/key/value projections, output projections, feed-forward layers, patch embeddings. Digital: softmax, layer norm, GELU, positional encoding, residual add, class token.` This is already half-stated in §2.3 — lift the list into §3.1 or appendix. |
| C8 | Energy model | verbal description only; no equation in main text | appendix add: `E_total = Σ_layer (N_MAC^analog · e_analog + N_MAC^digital · e_digital) + α · interconnect`, with e_analog / e_digital stated as placeholder constants and α as the 10–50 % routing-overhead range |
| C9 | "10 MC runs per point" | seed reuse policy and whether the same MC seeds feed all models is unclear | §4 one sentence: `MC noise realizations are drawn independently per grid point; architectures and seeds do not share perturbation samples.` (or whatever the code actually does — confirm against `run_contour_sweep.py`) |
| C10 | Fresh-instance evaluation Eq. 7 | `M' ∼ p(M)` — shape of p(M) restated? | §3.2 after Eq. 7: `Each fresh array corresponds to an i.i.d. Gaussian draw $M' \sim \mathcal{N}(0, \sigma_{D2D}^2)$ held constant over the evaluation pass, distinct from the C2C perturbation that re-samples per forward pass.` |
| C11 | Iso-accuracy "consistent ~7 pp jump at 5→6-bit" (§5:51) | "consistent" not defined (min? mean? max across the D2D rows?) | one clause: `mean across all seven D2D levels; the per-row jump ranged from 5.8 to 8.1 pp` |

**Priority:** C3 / C4 / C5 / C6 are the four that a reviewer focused on reproducibility will target. C7 is the one that a hardware reviewer will ask.

---

## §4 Physical mapping — what the current framework does NOT model (future directions)

This is the "物理映射很多还没做" catalog you flagged. Paper already has a one-line limitations preview in `01:19` and `06:43`, but neither enumerates. The items below are graded by (a) how much a reviewer will push on them, (b) effort to add, (c) thesis-chapter potential.

### 4.1 Already modeled (for contrast)

- Conductance window $[G_{min}, G_{max}]$ with differential mapping (Eq. 4 in §3)
- n-state quantization via STE
- C2C Gaussian injection per forward pass
- D2D Gaussian injection held constant per hardware instance
- Readout ADC bit-width (hard quantization of MVM output)
- Double-exponential retention with $\tau_1, \tau_2, A_0$
- Nonlinear write as STE-backward surrogate ($NL_{LTP}, NL_{LTD}$)
- Sublinear photoresponse $I \propto P^\gamma$ + inverse-gamma compensation
- Dark current $I_{dark}$
- Shot noise $\varepsilon_{shot}$ with variance $\propto I_{photo}$ (no spatial correlation)

### 4.2 Not yet modeled — by reviewer pressure priority

| # | Phenomenon | Current treatment | Reviewer pressure | Effort to add |
|:--|:--|:--|:--:|:--:|
| **P1** | **IR drop as a spatial function of row current, wire R, array size** | 1% placeholder scalar injected in compound-stress §6.6 | **HIGH** — organic devices have high conductance → larger IR drops; reviewer will ask for a `V(i,j) = V_in − Σ R_w · I(k,j)` sweep | MED (1–2 weeks) — thesis chapter fit |
| **P2** | **Sneak-path currents** | 1% placeholder scalar in compound stress | HIGH | MED — couples to P1 |
| **P3** | **Spatial correlation of D2D** (devices close on array are correlated) | i.i.d. Gaussian only | MED | LOW (1 day) — inject Gaussian random field instead of i.i.d. |
| **P4** | **Non-Gaussian / heavy-tail / 1/f noise** | all Gaussian | MED | MED — requires measured-device characterization |
| **P5** | **Temperature coefficient** (γ, I_dark, σ_D2D vs T) | not modeled; cited temp-resilient devices in §2 but no thermal term in equations | MED — organic devices are famously T-sensitive | MED — extend profile interface with T-dependent entries |
| **P6** | **Forward write pulse dynamics** | NL only affects backward STE; forward write assumed ideal "program to target" | LOW — standard approximation for inference-focused papers | HIGH — requires pulse-level simulator |
| **P7** | **Endurance / cycle-dependent drift** | not modeled | LOW | MED |
| **P8** | **Optical crosstalk between pixels** (dense photodetector array) | not modeled | MED — mentioned in §2 citations but not injected | MED |
| **P9** | **DAC / input-side quantization noise** | input assumed continuous | LOW | LOW — one-liner addition |
| **P10** | **Sample-and-hold / integration capacitor dynamics** | not modeled | LOW | MED |
| **P11** | **Supply-voltage variation** | not modeled | LOW | LOW |
| **P12** | **Program/verify noise** (iterative write) | not modeled | LOW | MED |
| **P13** | **Retained-state deformation from NL** (not just gradient) | NL affects training backward only | MED — reviewer may argue NL also bends the stored weight read-out | MED — inject NL into forward G-state as well |
| **P14** | **Photon shot noise at low intensity** | captured via $\varepsilon_{shot}$ but variance constant $\kappa$ is implicit | LOW | LOW |

### 4.3 Recommended framing in the paper

- **Keep main-text Limitations list short** — enumerate P1, P2, P5 explicitly; group P3, P4 under "noise-model refinement"; defer P6-P14 to a supplementary table or the "Outlook" paragraph.
- **Add a concrete future-work chart** at the end of §6 or in a new supp section `S-future-work`: a 2-column table (phenomenon / motivating citation) makes "framework-first, circuit-next" an explicit roadmap rather than a hand-wave.
- **Thesis angle:** P1, P2, P5, P3, P4 together are a full chapter: "from behavioral to circuit-aware simulation". This is the natural extension of the current paper; positioning it this way also inoculates the NC submission against "you should have done IR drop" reviewer attacks — the answer becomes "that is the next chapter, explicitly scoped here".
- **E6 (γ × NL joint sweep) in Gemini's Evidence Matrix** is orthogonal to P1–P14; it's an interaction study within already-modeled phenomena. Both should be in the thesis.

---

## §5 File / project management

### 5.1 Good state

- `paper/latex_gpt/sections/` clean (nine `.tex` files, all self-contained, `% !TeX root` headers present).
- `CANONICAL_RESULT_LOCK_gpt.md` plays the role of a style-guide and number-lock. Cited from `PROVENANCE_AUDIT_20260418.md`.
- `08_appendix.tex` is **not** an empty stub — it's 149 lines, has 3-seed V4 summary + provenance matrix + retention comparison + auto-fitter description. (Task-ledger phrasing that called it "regen target — currently empty stub" is outdated; fix on next ledger pass.)
- `_archive/` consolidation committed as `a7fa088`.
- `PROJECT_INDEX.md` master registry exists.

### 5.2 Needs attention

| # | Item | Why | Owner |
|:--|:--|:--|:--|
| M1 | `paper/` still has legacy `.md` drafts (01-07 chapter drafts, `PAPER_OUTLINE.md`, `FIG1_FIG2_BRIEF_gpt.md`, `FIGURE_CAPTION_DRAFTS_gpt.md`, `参考文献库.md`) | TX-32 still ⛔; these are pre-`latex_gpt/` artifacts and will confuse reviewers if the public repo exposes them | Codex CX-C (GPU-idle) |
| M2 | `report_md/_gpt/` has 70+ dispatches / broadcasts; stale-dispatch lifecycle not defined | audit found two dispatches referencing agents (Kimi) that are now back online; policy question | Claude next round |
| M3 | `_archive/paper-drafts/` referenced in TX-32 spec but directory doesn't yet exist | created on first TX-32 execution | Codex, same |
| M4 | Outer repo `/home/qiaosir/projects/` has 0 tracked files (C1) | addressed strategically in `REPRODUCIBILITY_PACKAGE_PLAN §3.1`; no outer-repo init intended; needs one-line disclosure in `PROJECT_INDEX.md §1` | Claude — fold into next ledger pass |
| M5 | `数据_博士/` (C4) WSL-private; manuscript references fitted JSONs only, not raw | `grep` on `paper/latex_gpt/` confirms no direct `\input` of `数据_博士` path; safe for NC. Flag remains valid for thesis. | no action until thesis lane |
| M6 | `checkpoints/` 25 GB no mirror (C3) | plan in `REPRODUCIBILITY_PACKAGE_PLAN`; executing via CX-E + CLAUDE-E this round | in-flight |
| M7 | `paper/latex_gpt/supplementary.tex` page count drift | supp was 15pp in some logs, 16pp in others, currently 21pp per `pdfinfo` | one-time audit pre-submission; non-urgent |
| M8 | CLAUDE_TASK ledger internal duplication (header still says "Phase 2 修正版" even though we're in Round B of 2026-04-18 dispatches) | cosmetic — but confusing for a reader scanning the file | lightweight rewrite of the opening block when CX-A drains |
| M9 | No pre-submission "`check_locked_numbers.py`" guard script | PROVENANCE_AUDIT §12 recommendation; would re-read each Locked-Number JSON and assert the manuscript matches; one-time cost then zero | Codex, future round (after CX-D provenance gaps are filled) |
| M10 | `08_appendix.tex:71` mentions "Zhang 2025 OPECT values for σ_C2C and σ_D2D are transparent proxy estimates" — good — but the provenance table immediately above (`tab:provenance`) should cross-link to `PROVENANCE_AUDIT_20260418.md` for reviewers | nice-to-have footnote | Claude |

### 5.3 Report/memo lifecycle proposal

`report_md/_gpt/` currently mixes three categories in the same directory:

1. **Active coordination** (dispatches with ⏳, `AGENT_SYNC`, `CLAUDE_TASK`, active broadcasts)
2. **Reference / locked state** (`CANONICAL_RESULT_LOCK`, `FIGURE_CAPTION_LOCK`, `PROVENANCE_AUDIT`, `THESIS_VS_PAPER_SCOPE`, `REPRODUCIBILITY_PACKAGE_PLAN`)
3. **Closed / historical** (delivered dispatches that are no longer ⏳, completed audit memos, etc.)

Proposal: after CX-A drains, introduce `report_md/_gpt/_closed/YYYY-MM-DD/` subdirs for category 3, keep categories 1–2 at top level. Do not force this before CX-A — live dispatches moving mid-round would break traceability.

---

## §6 Prioritized action items (downstream of this review)

| # | Action | Owner | Blocks | Cost |
|:--|:--|:--|:--|:--:|
| R1 | Abbreviation pass (A1–A4, A6–A11, A13) in abstract + §1 + §3 + §5 | Claude | — | 30 min |
| R2 | Data-rigor pass D1/D3/D4 + D10 — add n, test name, error bars | Claude + Codex coordinate | R4 statistical recompute where needed | 1 h |
| R3 | Calculation-clarity pass C3/C4/C5/C6/C7 — five one-liners | Claude | — | 45 min |
| R4 | Physical-mapping §4 framing into §6 Limitations + §6 Outlook | Claude | thesis chapter scoping | 1 h |
| R5 | M1/M3 TX-32 archive `paper/` legacy drafts | Codex CX-C | GPU idle | 20 min |
| R6 | M8 ledger header rewrite + M10 appendix cross-link | Claude | post-CX-A | 30 min |
| R7 | Recompile + verify 14/21/2 page counts + logs clean | Codex | R1–R4 | 10 min |
| R8 | Update `PROVENANCE_AUDIT §11` with newly-flagged gaps from this review (esp. D1 / D4 / C5) | Codex (CX-D continuation) | — | 30 min |

**Do NOT start R1–R4 before CLAUDE-A NL decision lands.** If CX-A MLP-linear succeeds (L1 ≥ 80%), contribution #4 rewrites cascade through the same paragraphs; doing an abbreviation pass now would force a second edit round.

**Do start R5 (TX-32)** when GPU idles — it's independent.

---

## §7 Summary

- **Abbreviations:** 11 real gaps (A1–A4, A6–A11, A13). The two that a reviewer will definitely flag are **ADC** (used 15+ times, never expanded) and **OPECT** (headline organic-device term, never expanded).
- **Data rigor:** `88.53%` OPECT (D1) and `p<10^{-15}` (D4) are the two claims that can't survive reviewer scrutiny as currently phrased. `+5.8 pp` inverse-gamma (D3) also has no stated error bar.
- **Calculation clarity:** C3 (Ensemble HAT expectation estimator), C4 (Sobol estimator), C5 (test name), C6 (gradient-scaling definition), C7 (mapping-policy operator list) are the five highest-value one-liners.
- **Physical mapping:** 14-item future-work list (P1–P14); recommend enumerating P1/P2/P5 in Limitations and framing P1–P5 as "next-chapter" thesis scope.
- **File management:** 10 items; none are blockers, four are cleanup (M1, M3, M7, M8), rest are nice-to-have.

---

**End of review. Actions registered as CLAUDE-F (this memo) + follow-up rows R1–R8 in `CLAUDE_TASK_gpt.md`. No `.tex` edits in this pass.**
