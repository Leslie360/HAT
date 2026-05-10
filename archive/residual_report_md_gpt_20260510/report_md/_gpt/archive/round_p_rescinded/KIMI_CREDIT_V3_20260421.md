<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# CRediT Author-Position Matrix Audit — v3 (Post-Pivot)

**Paper:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision
**Venue:** Nature Communications (resubmission) + Doctoral Dissertation
**Date:** 2026-04-21
**Version:** v3 — updated after negative-result pivot
**Status:** Draft — pending author confirmation

---

## 1. Role Legend

| Symbol | Meaning |
|:------:|:--------|
| ● | Lead contribution — primary responsible party |
| ○ | Supporting contribution — substantive assistance or secondary execution |
| — | No contribution to this role |

---

## 2. Author–Role Matrix

| Author | Conceptualization | Methodology | Software | Validation | Formal Analysis | Investigation | Resources | Data Curation | Writing — Original Draft | Writing — Review & Editing | Visualization | Supervision | Project Administration | Funding Acquisition |
|:-------|:-----------------:|:-----------:|:--------:|:----------:|:---------------:|:-------------:|:---------:|:-------------:|:------------------------:|:--------------------------:|:-------------:|:-----------:|:----------------------:|:-------------------:|
| **Songqiao Li** | ● | ● | ● | ● | ● | ● | ○ | ● | ● | ● | ● | — | ● | — |
| **[Advisor placeholder]** | ● | ○ | — | — | — | — | ● | — | ○ | ● | — | ● | ○ | ● |
| **[Collaborator 1 — device physics]** | ○ | ● | — | ○ | — | ○ | ● | ○ | — | ○ | — | — | — | — |
| **[Collaborator 2 — code review]** | — | ○ | ● | ● | — | — | — | — | — | ● | — | — | — | — |
| **[Collaborator 3 — CrossSim validation]** | — | ○ | ○ | ● | ○ | ○ | — | ○ | — | ○ | ○ | — | — | — |

---

## 3. Role Definitions Aligned to This Study

| CRediT Role | Scope of Work in This Study |
|:---|:---|
| **Conceptualization** | Formulation of the profile-driven simulation concept; hybrid analog–digital deployment partition; risk-aware evaluation philosophy; research questions (ADC cliff, front-end compensation, fresh-instance transfer, nonlinear-write bottleneck); *post-pivot:* structural-limit hypothesis and falsification-experiment design. |
| **Methodology** | Design of the mixed-signal inference stack (`analog_layers.py`, `analog_layers_ensemble.py`); hardware-aware training (HAT) and Ensemble HAT formalism (Eq. 2–4); inverse-gamma front-end compensation (Eq. 5–7); profile-driven substitution interface (JSON parameter bundles); Sobol sensitivity decomposition (Eq. 8); Monte Carlo evaluation protocol; first-order energy model; *post-pivot:* CX-J1 falsification protocol and ceiling-testing framework. |
| **Software** | PyTorch-native simulation framework implementation; training scripts (`train_tinyvit.py`, `train_convnext.py`, `train_resnet18.py`, `train_tinyvit_ensemble.py`); evaluation pipelines (`eval_*.py`); physical noise pipeline (`physical_noise_pipeline.py`); device-profile utilities (`device_profile_utils.py`); inference analysis tools (`inference_analysis_utils.py`); experiment orchestration scripts in `scripts/_gpt/`; plotting and figure-generation scripts (`plot_paper_figures.py`, `plot_convnext_results.py`, `plot_resnet18_results.py`). |
| **Validation** | Sanity-checking via `check_locked_numbers.py`; reproducibility verification; checkpoint behavior audits; CrossSim comparison baselines; numerical consistency sweeps; statistical validation runs; *post-pivot:* falsification-experiment replication (CX-J1b/c/d), structural-hypothesis stress-testing, and triplicate verification of the ~30 % ceiling. |
| **Formal Analysis** | Sobol-index estimation over the 63-point D2D–ADC grid; iso-accuracy contour analysis; fresh-instance statistical analysis (mean-of-means protocol, $n=10$ arrays × 5 MC evaluations); one-sample $t$-test for Ensemble HAT significance ($p<10^{-15}$); *post-pivot:* structural-limit hypothesis formalization, proof-sketch derivation, and failure-mode taxonomy. |
| **Investigation** | Execution of the Tiny-ViT experiment family (V1–V8), ConvNeXt experiment family (C1–C4), and ResNet-18 baselines on CIFAR-10, CIFAR-100, and Flowers-102; ADC resolution sweeps; retention drift time-series; proportional-noise and severe-NL ($NL=2.0$) stress tests; fresh-instance cadence scans (fixed / epoch / batch); OPECT zero-shot transfer case study; inverse-gamma ($\gamma_{\text{phys}}$) and dark-current ($I_{\text{dark}}$) sweep; layer-wise nonideality ablations; learnable-$\gamma$ compensation ablations; correlated-D2D stress test; *post-pivot:* MLP-linearization ablation, all-linear upper-bound test, QKV-only linearization control, joint MLP-linear + Ensemble HAT experiment, and higher-order surrogate scoping (CX-J1d design). |
| **Resources** | Provision of compute infrastructure (GPUs, WSL/local cluster); pre-trained ImageNet checkpoints for Tiny-ViT-5M; dataset hosting / access; doctoral measurement exports underlying the fitted device profiles. |
| **Data Curation** | Fitting and packaging of literature-derived device profiles (Zhang2025 OPECT, Vincze2025 standard, measured-device summaries); generation of source-data bundles (`release_artifacts/source_data_v1/` — 73 JSON + 2 CSV files); provenance tracking in `source_data_v1/MANIFEST.md`; checkpoint inventory and tiered-release planning (`CHECKPOINT_INVENTORY_20260418.md`); *post-pivot:* failure-mode table assembly, falsification-experiment metadata tagging, and structural-limit dataset versioning. |
| **Writing — Original Draft** | LaTeX manuscript composition (main text 15 pp, supplementary 21 pp, cover letter); abstract and section drafting; equation derivation and notation lock; figure caption authoring; bibliography curation (`refs_gpt.bib`); *post-pivot:* negative-result narrative reframing, falsification-subsection drafting, structural-limit hypothesis prose, and thesis-only chapter integration (Ch. 4–6 expansion). |
| **Writing — Review & Editing** | Cross-agent proofreading passes; notation audits; figure-provenance verification; citation-integrity checks; consistency sweeps (`check_locked_numbers.py`); response-letter drafting; *post-pivot:* pivot-ratification document review, rebuttal-arsenal alignment, and thesis-v0 lock checklist execution. |
| **Visualization** | Main-text figures (Fig. 2–7): retention curves, iso-accuracy contour map, cross-dataset accuracy bars, HAT recovery bars, Ensemble HAT concept diagram, zero-shot transfer bars, physical-compensation curves; supplementary figures (Figs. S1–S10): schematic overviews, noise-sensitivity curves, ADC-layerwise nonideality, cadence scans, fresh-instance ablations, gradient-distortion maps, SNR/frontend trade-offs, Pareto energy-accuracy plots; *post-pivot:* failure-mode taxonomy table, structural-limit ceiling diagrams, and falsification-experiment summary figures. |
| **Supervision** | Scientific oversight of research direction; framework architecture decisions; experimental design approval; manuscript structure and framing guidance; *post-pivot:* negative-result pivot ratification and thesis-scope boundary decisions. |
| **Project Administration** | Multi-agent coordination workflow management; experiment scheduling and queueing; repository hygiene and Git policy enforcement; submission-bundle assembly; pre-submission checklist execution; *post-pivot:* expanded CX-J1 queue management, thesis/NC scope partitioning, and archival planning. |
| **Funding Acquisition** | Acquisition of financial support for the project, including grants, scholarships, or departmental funding. |

---

## 4. Change Log: v1 → v2 → v3

### v1 (Pre-submission, 2026-04-12)
- Optimistic framing: all contributions positioned as positive advances.
- Validation scope limited to reproducibility checks and CrossSim baseline.
- Formal analysis confined to Sobol indices and iso-accuracy contours.
- No falsification experiments; no structural-limit hypothesis.

### v2 (Reviewer response, 2026-04-14 to 04-17)
- Added Collaborator 3 (CrossSim validation) to address Reviewer 3’s framework-comparison request.
- Expanded Validation to include numerical-consistency sweeps and statistical reruns.
- Methodology updated to include inverse-gamma front-end compensation (elevated to contribution #2).
- Writing — Review & Editing expanded with response-letter drafting and red-team audit.

### v3 (Post-pivot, 2026-04-18 to 04-21)
**Pivot trigger:** All training-recipe modifications (MLP-linear, all-linear, joint MLP-linear + Ensemble HAT) failed to break the ~30 % fresh-instance accuracy ceiling under severe non-linearity ($NL = 2.0$). The narrative shifted from "mitigation succeeds" to "structural limit rigorously characterized."

**Matrix changes relative to v2:**

| Change | Rationale |
|:---|:---|
| **Songqiao Li — Formal Analysis: upgraded to ●** | Derivation of the structural-limit proof sketch, dynamic-range collapse argument, and failure-mode taxonomy required original theoretical work not present in v1/v2. |
| **Songqiao Li — Investigation: intensified ●** | CX-J1 falsification suite (b/c/d) added ~60 GPU hours of controlled experiments; MLP-only, all-linear, QKV-only, and joint-training variants executed specifically to test the structural hypothesis. |
| **Songqiao Li — Validation: intensified ●** | Triplicate verification of the ceiling (10 arrays × 5 MC evaluations × 3 recipe variants); falsification-experiment replication protocol established. |
| **Songqiao Li — Data Curation: intensified ●** | New metadata taxonomy for negative-result experiments (ceiling-broken flag, source-vs-fresh pairing, NL severity tier); failure-mode table (5 rows × 4 columns) assembled as standalone citable object. |
| **Songqiao Li — Writing — Original Draft: intensified ●** | Complete narrative reframing: §5.3 rewritten as "definitive negative result"; new falsification subsection added; Discussion expanded with Popperian framing; thesis Ch. 4–6 expanded by ~15 pp. |
| **Songqiao Li — Visualization: intensified ●** | New figure type: ceiling-bar comparison (rows 1–5 of failure-mode table); structural-limit schematic; CX-J1 experiment-flow diagram. |
| **Collaborator 1 — Conceptualization: added ○** | Device-physics input on conductance-power-law interpretation and dynamic-range collapse mechanism; review of structural-limit proof sketch for physical plausibility. |
| **Collaborator 1 — Validation: added ○** | Independent sanity check of measured-device profile fits against physical model predictions; confirmation that NL = 2.0 is within realistic OPECT operating range. |
| **Collaborator 2 — Validation: upgraded ○ → ●** | Code-review role expanded to include falsification-experiment audit (CX-J1 script review, checkpoint integrity verification, and regression-test design for negative-result paths). |
| **Collaborator 3 — Formal Analysis: added ○** | CrossSim validation extended to include surrogate-fidelity comparison (first-order vs. higher-order Taylor) and independent reproduction of the ~30 % ceiling under shared-regime parameters. |
| **Collaborator 3 — Investigation: added ○** | Execution of CrossSim-side MLP-linearization control to confirm framework-agnostic nature of the ceiling. |
| **[Advisor] — Supervision: unchanged ●** | Ratified the negative-result pivot; approved thesis-scope expansion (Ch. 4–6) and NC-main narrative revision. |

---

## 5. Notes on the Pivot

### 5.1 What Changed Scientifically
In v1/v2, the research program was framed as a sequence of successful mitigations: HAT recovers accuracy, Ensemble HAT recovers fresh-instance transfer, inverse-gamma compensates dark current. The implicit promise was that further engineering would continue to yield gains.

The pivot occurred when the CX-J1 experiment suite demonstrated that **no training-recipe modification breaks the ~30 % ceiling under severe non-linearity ($NL \ge 2.0$)**. This transformed the paper’s (and thesis’s) central claim from "we solved fresh-instance transfer" to "we rigorously mapped the boundary of what is solvable with training-recipe modifications alone, and we provide a falsifiable structural hypothesis for why."

### 5.2 What Changed in Attribution
The pivot did not introduce new authors, but it **redistributed effort intensity**:

- **Primary author (Songqiao Li)** absorbed the bulk of new work: falsification experiments, theoretical formalization, narrative reframing, and thesis expansion. Every role already held as ● became more labor-intensive; Formal Analysis and Data Curation upgraded from ○ to ●.
- **Device-physics collaborator** gained new relevance because the structural-limit argument hinges on conductance-power-law physics. Their input shifted from passive consultation to active review of the proof sketch.
- **Code-review collaborator** became critical for trust in negative results. A positive result is self-evident; a negative result requires exhaustive verification that no bug or parameter error explains the failure. This demanded independent code audit and regression-test design.
- **CrossSim validation collaborator** expanded scope from "confirm our numbers" to "reproduce the ceiling in an independent simulator," strengthening the claim of framework-agnostic structural limits.

### 5.3 What Did Not Change
- **Resources and Funding Acquisition** roles are unchanged; the pivot required no new hardware or external funding.
- **Advisor supervision** was already ●; the pivot was ratified rather than initiated by the advisor.
- **Collaborator 2’s Software role** remained ○ because no new framework modules were required—only audit and regression infrastructure.

### 5.4 Transparency Statement
This matrix reflects the *actual* distribution of labor as reconstructed from commit logs, experiment timestamps (`logs/`), design memos (`report_md/_gpt/GEMINI_*`, `CODEX_*`), and agent coordination records (`BROADCAST_ASSIGNMENT_*`). All authors will be asked to confirm or amend their row before final submission. Any discrepancies between perceived and actual contribution will be resolved by adding ○ marks rather than removing ● marks, consistent with an inclusive attribution policy.

---

## 6. Action Items

| # | Action | Owner | Deadline |
|:--|:-------|:------|:---------|
| 1 | Replace bracketed placeholders with real names and affiliations | Songqiao Li | Before submission |
| 2 | Circulate matrix to all authors for confirmation | Songqiao Li | 2026-04-23 |
| 3 | Resolve any disputed ○/● marks via inclusive policy (add, do not remove) | All authors | 2026-04-25 |
| 4 | Upload finalized CRediT to Nature Communications author portal | Songqiao Li | At submission |
| 5 | Archive v3 matrix in `release_artifacts/zenodo_archive_v0/` | Songqiao Li | At submission |

---

*Document generated by Kimi Code CLI subagent (Task K-X28).
Based on: `KIMI_CREDIT_STATEMENT_DRAFT_20260420.md`, `THESIS_VS_PAPER_SCOPE_20260418.md`, `KIMI_FAILURE_MODE_TABLE_20260421.md`, `GEMINI_STRUCTURAL_LIMIT_THEORY_20260421.md`, and `CLAUDE_CE_PIVOT_RATIFICATION.md`.*
