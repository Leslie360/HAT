# DISPATCH KIMI R10 — Characterization (3 sub-tracks)
**Date:** 2026-04-25 23:00 CST
**Issued by:** Claude
**Assignee:** Kimi (with Codex assist on R10C numerical)
**Authority:** CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN §1
**Priority:** HIGH (closes 3 reviewer-attack vectors)
**Time budget:** ~2-3 days

---

## 0. Mission

Three characterization tasks closing reviewer concerns:
- R10C: OPECT distribution statistics (defends "zero-shot transfer" claim)
- R10F: Literature freshness audit (last 6 months prior art)
- R10H: Energy ε_MAC literature provenance (defends energy claim)

All text/data work, no GPU training.

---

## 1. R10C — OPECT distribution statistical characterization

### Why
Paper claims "zero-shot transfer to OPECT" achieving 88.53±0.08% — but currently no statistics on OPECT D2D distribution vs our literature Gaussian prior. Reviewer: "If OPECT is just Gaussian-like, this isn't really zero-shot transfer."

### What you need to do

#### 1.1 Extract OPECT distribution data
Source: Zhang et al. 2025 OPECT paper (`zhang2025opect` in our bib), specifically the supplementary information tables/figures showing per-device conductance distribution.

Data we need:
- σ_D2D measured (per-programming-level if available)
- Distribution shape: Gaussian / log-normal / heavy-tail?
- Per-level statistics: mean, std, kurtosis, skewness
- Number of devices measured (sample size)

Sources:
- The published Zhang 2025 paper PDF + SI
- Our local `device_profiles/literature_profiles_gpt.json` — check if OPECT entry already has stats
- Existing OPECT case study in `eval_literature_profile.py` — check how we currently use OPECT

#### 1.2 Compare to our literature Gaussian prior
Our framework uses σ_D2D = 10% Gaussian. Compare:
- σ_D2D Gaussian (ours): mean=0, std=0.10, kurtosis=3 (Gaussian)
- σ_D2D OPECT: extract from paper

Generate:
- **QQ plot**: OPECT empirical vs Gaussian(0, σ²) — does it line up?
- **Anderson-Darling test**: tests Gaussianity formally
- **Kurtosis comparison**: Gaussian = 3; if OPECT > 3 → heavy-tailed (interesting!)

#### 1.3 Statistical distance
Compute Wasserstein distance or KS distance between OPECT distribution and our Gaussian prior. Quantifies how different the OPECT zero-shot evaluation actually is.

#### 1.4 Possible outcomes
- **Outcome A**: OPECT ≈ Gaussian → admit honestly: "Zero-shot transfer holds because OPECT distribution is close to our training-time prior; framework's robustness to mismatch *distribution shape* is a separate claim awaiting hardware-calibrated data."
- **Outcome B**: OPECT noticeably non-Gaussian → strong claim: "Zero-shot transfer holds even though OPECT distribution differs by [statistical distance] from training prior; framework demonstrates robustness to distribution-shape mismatch."
- **Outcome C**: OPECT data unavailable in paper SI → admit limit + propose framework-agnostic approach.

### Codex assist
If you need numerical computation help (QQ plot, AD test, KS distance), delegate to Codex. Codex can run the statistical tests in `paper/figures/tikz/` or scripts/.

### Deliverable

| File | Content |
|:--|:--|
| `paper/latex_gpt/supplementary/S_opect_distribution.tex` | New Supp Note — characterization + plots |
| `paper/figures/figS_opect_qq.{png,pdf}` | QQ plot comparison |
| `KIMI_R10C_OPECT_DISTRIBUTION_REPORT_20260425.md` | Numerical findings + paper-safe paragraph for §5.8 |

### Paper-safe paragraph (template for §5.8)

Depending on outcome A/B/C:
- A: "OPECT D2D distribution closely matches our literature Gaussian prior (σ ≈ X%, Anderson-Darling p > 0.05); zero-shot transfer here primarily validates the framework's profile-substitution interface rather than mismatch-distribution-shape robustness, the latter pending hardware-calibrated data (Supp Note S-HW)."
- B: "OPECT D2D distribution differs measurably from our literature Gaussian prior (Wasserstein distance ≈ X, kurtosis ≈ Y vs Gaussian's 3); the maintained 88.53±0.08% accuracy under this distribution shift demonstrates robustness to mismatch-shape variation, beyond simple parameter substitution."

### Time: 1 day

---

## 2. R10F — Literature freshness audit (2025-2026 prior art check)

### Why
Our submitted paper claims novelty for Ensemble HAT (per-epoch D2D resampling) on analog CIM. **Has someone else published this method in 2025-2026?** If yes: we cite + reframe novelty. If no: claim stands. Reviewer will absolutely check this.

### Spec

Search venues for 2025-2026 papers using terms:
- "analog CIM HAT" / "hardware-aware training analog"
- "structured noise injection memristor"
- "device mismatch training resampling"
- "analog-aware training transformer" / "analog vision transformer"
- "in-memory computing CIM transformer noise"

Venues to scan:
- **Nature Electronics, Nature Communications, Nature Comm Eng** (last 12 months)
- **NeurIPS 2025, ICLR 2026, ICML 2025** (analog hardware papers)
- **ISSCC 2025/2026, JSSC 2025-2026** (circuits side)
- **IEEE TED, EDL, T-VLSI** (device side)
- **arXiv** recent — search "analog HAT" / "ensemble HAT" / "hardware-aware training"

Tools:
- Google Scholar with date filter "since 2025"
- Semantic Scholar
- arXiv search

### What to look for

For each potentially-relevant paper:
- Does it propose **per-epoch D2D mask resampling** as a training method? (DIRECT prior art)
- Does it propose **multi-instance HAT** / **distribution-matching HAT**? (close prior art)
- Does it benchmark cross-instance fresh transfer? (related)
- Does it report sub-6-bit ADC cliff for transformers? (related)

### Output

`KIMI_R10F_LITERATURE_FRESHNESS_AUDIT_20260425.md`:

```markdown
# Literature Freshness Audit (2025-2026)

## Search scope
[methodology + venue list + date range]

## Direct prior art (Ensemble HAT-equivalent methods)
- [Paper 1 if found, with full citation + 1-paragraph distinction]

## Close prior art (multi-instance HAT, distribution-matching analog training)
- [Paper 2 if found]

## Related but distinct
- [Paper 3 if found]

## Conclusion
- If no direct prior art found: novelty claim stands.
- If direct prior art: cite + reframe contribution as [specific differentiation].
- New citations to add to refs_gpt.bib: [list]

## Updated novelty paragraph for §1 / §2.1
[Draft 2-3 sentences if reframing needed]
```

### Time: 1 day

---

## 3. R10H — Energy ε_MAC literature provenance table

### Why
Paper reports "11.45× vs FP32 / 2.86× vs INT8" energy speedup. Source: `auto_fitted_profile.json` constants. **Where do these constants come from?** Reviewer: "Show me each ε value's literature source."

### Spec

#### 3.1 Open auto_fitted_profile.json
List every parameter used in energy calculation:
- ε_MAC (per-MAC analog crossbar energy)
- ε_ADC (per-ADC-conversion energy at 6-bit)
- ε_DAC (per-DAC-input energy)
- ε_digital (per-MAC digital fp32 baseline)
- routing overhead percentage
- etc.

#### 3.2 For each parameter, find the literature source

Acceptable sources:
- Cited paper with explicit per-MAC energy number
- IBM Sebastian / Burr 2017-2024 papers
- Rasch 2023 AIHWKit paper
- Crystallized industry numbers (e.g., commercial DAC datasheet)

Document for each ε:
- Value used: X (units)
- Source: Author Year, journal, table/figure ref
- Justification for using this number for organic optoelectronic CIM (vs e.g. ReRAM)

#### 3.3 Build provenance table

`paper/latex_gpt/supplementary/S_energy_provenance.tex`:

```latex
\begin{table}[h]
\caption{Energy parameter literature provenance.}
\begin{tabular}{lccl}
\toprule
Parameter & Value & Units & Source \\
\midrule
$\epsilon_{\text{MAC, analog}}$ & X & pJ/MAC & \citep{xx} fig.\,3 \\
$\epsilon_{\text{ADC, 6bit}}$ & Y & pJ/sample & \citep{yy} table\,1 \\
... & ... & ... & ... \\
\bottomrule
\end{tabular}
\end{table}
```

#### 3.4 If a parameter has no clear source

Be honest:
- "Estimated based on order-of-magnitude bounds from \citep{xx}"
- "Assumed in this work pending fabrication data; sensitivity analysis in Supp Note S-Energy-Sensitivity"

#### 3.5 Energy sensitivity check
If we have time: pick top-3 parameters by sensitivity, do a quick "what if this is 2× higher / lower" analysis. Show that 11.45× number is robust to ±30% variation in any single parameter.

### Deliverable
- `paper/latex_gpt/supplementary/S_energy_provenance.tex` — new table
- `KIMI_R10H_ENERGY_PROVENANCE_REPORT_20260425.md`
- Updated paper-safe paragraph in §6 Discussion energy discussion + reference to new Supp Note

### Time: 4 hours

---

## 4. Constraints (HARD)

- **No new science.** Only characterization of existing claims.
- **No new numbers** that contradict existing claims (if R10C reveals OPECT IS Gaussian-like, you reframe HONESTLY, not silently).
- **Zone discipline**: every cite still maps to 3A/3B/3C.
- **No bug-retrospective language** introduced.
- **Cite responsibly**: every new citation goes into refs_gpt.bib.

---

## 5. Coordination

- **Codex assist**: R10C numerical computation can be delegated. Send Codex a `KIMI→CODEX_R10C_REQUEST.md` with specific computational ask.
- **R9 tracks**: Track A (length surgery) waits until R10 finishes (you'll have new content to cut around).
- **R8 W2**: parallel; you have 50% bandwidth.
- **R10 priority**: R10F > R10C > R10H (R10F is fastest + highest-impact for novelty defense).

---

## 6. Workflow

### Day 1
- R10F literature freshness audit (4-6 hours)
- Start R10C OPECT extraction (read Zhang 2025 paper carefully)

### Day 2
- R10C OPECT analysis + figure (delegate stats to Codex)
- R10H energy provenance table

### Day 3 (buffer)
- Integrate findings into manuscript (after Codex R10A/D land)
- Coordinate with R9 length surgery

---

## 7. Success criteria

- R10C: OPECT statistics published, QQ plot embedded, paper-safe statement reframes "zero-shot transfer" honestly
- R10F: literature audit complete; either novelty stands cleanly OR new prior art cited + reframed
- R10H: every ε in energy calculation has literature provenance OR honest "estimated" label

---

## 8. Cold-start refs

- `paper/latex_gpt/sections/05_results.tex` §5.8 OPECT case study (current OPECT framing)
- `device_profiles/literature_profiles_gpt.json` (existing OPECT entry, if any)
- `auto_fitted_profile.json` (energy ε values)
- `paper/latex_gpt/refs_gpt.bib` — current bib (Zhang 2025 OPECT cite)
- `eval_literature_profile.py` — existing OPECT eval code

**No deadline.** 2-3 days expected.
