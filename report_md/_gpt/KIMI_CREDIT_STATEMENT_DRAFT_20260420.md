# K-T3: CRediT Author Contributions — Draft

**Paper:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision  
**Venue:** Nature Communications  
**Date:** 2026-04-20  
**Status:** Draft — awaiting author initials

---

## Ready-to-insert LaTeX paragraph

Paste the following block into the manuscript after the Acknowledgements section (or as instructed by the Nature Communications author-guidelines CRediT upload portal).

```latex
\section*{Author contributions}

The following CRediT (Contributor Roles Taxonomy) attribution applies:

\textbf{Conceptualization:} [Author Initials]  
\textbf{Methodology:} [Author Initials]  
\textbf{Software:} [Author Initials]  
\textbf{Validation:} [Author Initials]  
\textbf{Formal Analysis:} [Author Initials]  
\textbf{Investigation:} [Author Initials]  
\textbf{Resources:} [Author Initials]  
\textbf{Data Curation:} [Author Initials]  
\textbf{Writing -- Original Draft:} [Author Initials]  
\textbf{Writing -- Review \& Editing:} [Author Initials]  
\textbf{Visualization:} [Author Initials]  
\textbf{Supervision:} [Author Initials]  
\textbf{Project Administration:} [Author Initials]  
\textbf{Funding Acquisition:} [Author Initials]
```

---

## Scope notes for assignment (based on manuscript source)

Use these notes to decide which initials map to each role.

| CRediT Role | Scope of work in this study |
|:---|:---|
| **Conceptualization** | Formulation of the profile-driven simulation concept; hybrid analog–digital deployment partition; risk-aware evaluation philosophy; research questions (ADC cliff, front-end compensation, fresh-instance transfer, nonlinear-write bottleneck). |
| **Methodology** | Design of the mixed-signal inference stack (`analog_layers.py`, `analog_layers_ensemble.py`); hardware-aware training (HAT) and Ensemble HAT formalism (Eq. 2–4); inverse-gamma front-end compensation (Eq. 5–7); profile-driven substitution interface (JSON parameter bundles); Sobol sensitivity decomposition (Eq. 8); Monte Carlo evaluation protocol; first-order energy model. |
| **Software** | PyTorch-native simulation framework implementation; training scripts (`train_tinyvit.py`, `train_convnext.py`, `train_resnet18.py`, `train_tinyvit_ensemble.py`); evaluation pipelines (`eval_*.py`); physical noise pipeline (`physical_noise_pipeline.py`); device-profile utilities (`device_profile_utils.py`); inference analysis tools (`inference_analysis_utils.py`); experiment orchestration scripts in `scripts/_gpt/`; plotting and figure-generation scripts (`plot_paper_figures.py`, `plot_convnext_results.py`, `plot_resnet18_results.py`). |
| **Validation** | Sanity-checking via `check_locked_numbers.py`; reproducibility verification; checkpoint behavior audits; CrossSim comparison baselines; numerical consistency sweeps; statistical validation runs. |
| **Formal Analysis** | Sobol-index estimation over the 63-point D2D–ADC grid; iso-accuracy contour analysis; fresh-instance statistical analysis (mean-of-means protocol, $n=10$ arrays × 5 MC evaluations); one-sample $t$-test for Ensemble HAT significance ($p<10^{-15}$). |
| **Investigation** | Execution of the Tiny-ViT experiment family (V1–V8), ConvNeXt experiment family (C1–C4), and ResNet-18 baselines on CIFAR-10, CIFAR-100, and Flowers-102; ADC resolution sweeps; retention drift time-series; proportional-noise and severe-NL ($NL=2.0$) stress tests; fresh-instance cadence scans (fixed / epoch / batch); OPECT zero-shot transfer case study; inverse-gamma ($\gamma_{\text{phys}}$) and dark-current ($I_{\text{dark}}$) sweep; layer-wise nonideality ablations; learnable-$\gamma$ compensation ablations; correlated-D2D stress test. |
| **Resources** | Provision of compute infrastructure (GPUs, WSL/local cluster); pre-trained ImageNet checkpoints for Tiny-ViT-5M; dataset hosting / access; doctoral measurement exports underlying the fitted device profiles. |
| **Data Curation** | Fitting and packaging of literature-derived device profiles (Zhang2025 OPECT, Vincze2025 standard, measured-device summaries); generation of source-data bundles (`release_artifacts/source_data_v1/` — 73 JSON + 2 CSV files); provenance tracking in `source_data_v1/MANIFEST.md`; checkpoint inventory and tiered-release planning (`CHECKPOINT_INVENTORY_20260418.md`). |
| **Writing – Original Draft** | LaTeX manuscript composition (main text 15 pp, supplementary 21 pp, cover letter); abstract and section drafting; equation derivation and notation lock; figure caption authoring; bibliography curation (`refs_gpt.bib`). |
| **Writing – Review & Editing** | Cross-agent proofreading passes; notation audits; figure-provenance verification; citation-integrity checks; consistency sweeps (`check_locked_numbers.py`); response-letter drafting. |
| **Visualization** | Main-text figures (Fig. 2–7): retention curves, iso-accuracy contour map, cross-dataset accuracy bars, HAT recovery bars, Ensemble HAT concept diagram, zero-shot transfer bars, physical-compensation curves; supplementary figures (Figs. S1–S10): schematic overviews, noise-sensitivity curves, ADC-layerwise nonideality, cadence scans, fresh-instance ablations, gradient-distortion maps, SNR/frontend trade-offs, Pareto energy-accuracy plots. |
| **Supervision** | Scientific oversight of research direction; framework architecture decisions; experimental design approval; manuscript structure and framing guidance. |
| **Project Administration** | Multi-agent coordination workflow management; experiment scheduling and queueing; repository hygiene and Git policy enforcement; submission-bundle assembly; pre-submission checklist execution. |
| **Funding Acquisition** | Acquisition of financial support for the project, including grants, scholarships, or departmental funding. |

---

## Action required

1. Replace every `[Author Initials]` with the appropriate author initials (e.g., `S.L., A.B.`).
2. Verify that every author who qualifies for a role is listed; no author should be omitted from roles they performed.
3. Nature Communications may require this statement at submission via their online portal; keep this file as the master reference.
