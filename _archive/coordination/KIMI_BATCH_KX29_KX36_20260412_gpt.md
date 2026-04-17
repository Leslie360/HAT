# [Kimi] 2026-04-12 — KX29-KX36 Full Batch Delivery

## Executive Summary

Completed full-batch submission-package closeout (KX29-KX36). Deliverables include: reviewer-accessible code archive plan, source-data workbook blueprint, NC portal fieldbook, cover-letter/rebuttal pack 2.0, public release boundary audit, non-science risk sweep, filename audit, and end-to-end adversarial preflight.

---

## [Kimi] KX29: Reviewer-Accessible Code Archive Plan [HIGH]

### Archive Root Layout

```
organic_cim_review_2026/
├── README_REVIEWERS.md              # Entry point for reviewers
├── LICENSE                          # Apache 2.0
├── INSTALL.md                       # Installation instructions
├── REQUIREMENTS.txt                 # Python dependencies
│
├── src/                             # Core simulation framework
│   ├── __init__.py
│   ├── analog_layers.py             # Analog CIM layers with noise/ADC/energy
│   ├── device_profile_utils.py      # Profile loading and validation
│   ├── train_tinyvit.py             # Tiny-ViT training/evaluation
│   ├── train_convnext.py            # ConvNeXt training/evaluation
│   └── run_device_comparison.py     # Zero-shot profile transfer
│
├── device_profiles/                 # JSON device profiles
│   ├── canonical_organic.json
│   ├── zhang_2025_opect.json
│   └── README_PROFILES.md
│
├── configs/                         # Reproducibility configs
│   ├── V1_baseline.yaml
│   ├── V4_canonical_hat.yaml
│   └── ...
│
├── scripts/                         # Utility scripts
│   ├── run_noise_sweep.py
│   ├── eval_fresh_instances.py
│   └── plot_paper_figures.py
│
├── docs/                            # Documentation
│   ├── DEVICE_PROFILE_GUIDE.md
│   ├── EXPERIMENT_REGISTRY.md
│   └── PHYSICS_STACK.md
│
├── paper_figures/                   # High-res figure PDFs
│   ├── fig1_system_architecture.pdf
│   ├── fig2_weight_mapping.pdf
│   └── ...
│
├── results_summary/                 # Key result tables (CSV)
│   ├── table1_fp32_baselines.csv
│   ├── table2_result_summary.csv
│   └── experiment_matrix.csv
│
└── tests/                           # Smoke tests for reviewers
    ├── test_imports.py
    └── test_profile_loading.py
```

### Must Include

| Category | Files | Why |
|:---------|:------|:----|
| Core framework | `analog_layers.py`, `device_profile_utils.py` | Central to main claims |
| Entry points | `train_tinyvit.py`, `train_convnext.py` | Reproducibility |
| Device profiles | `canonical_organic.json`, `zhang_2025_opect.json` | Profile-driven methodology |
| Configs | YAML files for V1-V8, C1-C4 | Seeded reproducibility |
| Docs | Profile guide, experiment registry | Reviewer understanding |
| Results | Summary CSVs | Data verification |
| Tests | Smoke tests | Quick validation |

### Must Exclude

| Category | Pattern | Why |
|:---------|:--------|:----|
| Internal coordination | `*_TASK_*.md`, `*_HANDOFF_*.md`, `*_DISPATCH_*.md` | Development history, not science |
| Coverage tracking | `REVIEWER_COVERAGE_MATRIX*.md` | Internal audit artifacts |
| Large checkpoints | `*.pt`, `checkpoints/` | Too large; can be regenerated |
| Raw logs | `logs/_gpt/` | Internal debugging |
| Draft figures | `figures/draft_*` | Not publication-ready |
| Temp directories | `_codex_smoke_*`, `tmp/` | Transient artifacts |

### README Text Draft (for reviewers)

```markdown
# Organic Optoelectronic CIM Simulation Framework — Reviewer Package

This archive contains the simulation framework and reproducibility artifacts 
for the Nature Communications submission "Hardware-Aware Simulation of 
Organic Optoelectronic Compute-in-Memory Inference for Edge Vision."

## Quick Validation (5 minutes)

```bash
# 1. Install dependencies
pip install -r REQUIREMENTS.txt

# 2. Run smoke tests
python tests/test_imports.py

# 3. Load device profiles
python -c "from src.device_profile_utils import load_profile; \
           print(load_profile('device_profiles/canonical_organic.json'))"
```

## Reproducing Key Results

### Figure 3: Cross-dataset accuracy
```bash
python scripts/plot_paper_figures.py --figure accuracy_comparison
```

### Table 2: Ensemble HAT fresh-instance evaluation
```bash
python src/train_tinyvit.py --mode eval \
  --checkpoint results_summary/checkpoints/V4_ensemble_hat_best.pt \
  --eval-runs 10 --fresh-instances
```

## Structure

- `src/`: Core simulation framework
- `device_profiles/`: Literature-derived and canonical device profiles
- `configs/`: Experiment configurations matching manuscript
- `results_summary/`: Key numerical results in CSV format
- `paper_figures/`: High-resolution figure PDFs

## Source Data

Numerical source data for all figures and tables is provided in 
`results_summary/` as CSV files. See `SOURCE_DATA_README.md` for mapping.

## Contact

For technical issues with this archive: [author email]
For editorial correspondence: Nature Communications submission system
```

### How Reviewers Should Run / Inspect

1. **Import test**: `python -c "import src.analog_layers"` — verifies dependencies
2. **Profile loading**: Load JSON profiles, verify schema
3. **Config validation**: Check YAML configs match manuscript Table S1
4. **Figure regeneration**: Run plotting scripts, compare to paper
5. **Numerical verification**: Check CSV results match table values

### Risk If Omitted

- **Without code**: NC policy violation (custom code must be available)
- **Without configs**: Reviewers cannot verify reproducibility claims
- **Without docs**: Reviewers cannot understand profile-driven methodology
- **With internal files**: Unprofessional appearance, potential confusion

---

## [Kimi] KX30: Source-Data Workbook Blueprint [HIGH]

### File Mapping (Excel Workbook Structure)

**Master workbook**: `source_data_nc_submission.xlsx`

| Sheet Name | Content | Source Path | Notes |
|:-----------|:--------|:------------|:------|
| `Fig3_Accuracy` | Cross-dataset accuracy bars | `json_gpt/cross_dataset_results.json` | FP32, Noisy, HAT values |
| `Fig4_HAT_Recovery` | Degradation/recovery trajectory | `json_gpt/hat_recovery_results.json` | With error bars |
| `Fig5_Energy` | Energy breakdown components | `json_gpt/energy_breakdown.json` | µJ values, percentages |
| `FigS1_Asymmetry` | EXP-A asymmetry sweep | `asymmetry_sweep_results_gemini.json` | 0%,1%,2%,5%,10% |
| `FigS2_Nonideality` | EXP-B IR drop/sneak sweep | `nonideality_sweep_results_gemini.json` | 12-condition grid |
| `Table1_Baselines` | FP32 baselines | `paper/05_results.md` | All architectures |
| `Table2_Results` | Main result summary | `paper/05_results.md` | With error bars |
| `Experiment_Matrix` | Full V1-V8, C1-C4 mapping | `supplementary.tex` | Canonical vs stress |

### Detailed Sheet Schemas

#### Sheet: Fig3_Accuracy
```
| Architecture | Dataset | FP32 (%) | Noisy (%) | HAT (%) | MC_Runs | Notes |
|:-------------|:--------|:---------|:----------|:--------|:--------|:------|
| Tiny-ViT | CIFAR-10 | 98.06 | 97.39 | 97.52 | 10 | 3-seed baseline |
| Tiny-ViT | CIFAR-100 | 86.94 | 44.06 | 65.48 | 10 | |
| Tiny-ViT | Flowers-102 | 97.97 | 4.81 | 22.48 | 10 | |
| ConvNeXt | CIFAR-10 | 90.74 | 23.86 | 60.54 | 10 | single-run |
| ... | ... | ... | ... | ... | ... | ... |
```

#### Sheet: FigS1_Asymmetry (EXP-A)
```
| Asymmetry (%) | Accuracy (%) | Std (%) | MC_Runs | Status |
|:--------------|:-------------|:--------|:--------|:-------|
| 0 | 91.78 | 0.05 | 10 | Baseline |
| 1 | 90.29 | 0.06 | 10 | Tolerated |
| 2 | 85.73 | 0.08 | 10 | Degradation |
| 5 | 33.81 | 1.20 | 10 | Collapse |
| 10 | 10.00 | 0.00 | 10 | Chance level |
```

#### Sheet: FigS2_Nonideality (EXP-B)
```
| IR_Drop (%) | Sneak_Path (%) | Accuracy (%) | Delta (pp) | Status |
|:------------|:---------------|:-------------|:-----------|:-------|
| 0 | 0 | 91.86 | 0.00 | Baseline |
| 1 | 0 | 91.52 | -0.34 | Robust |
| 3 | 0 | 90.21 | -1.65 | Robust |
| 0 | 1 | 91.34 | -0.52 | Robust |
| 0 | 2 | 90.45 | -1.41 | Robust |
| 3 | 2 | 89.70 | -2.16 | <2.5% loss |
```

### Schematic Figures (No Numerical Source Data)

These figures are **conceptual schematics**, not data plots:
- **Fig.1** (System architecture): Block diagram, no numerical data
- **Fig.2** (Weight-to-conductance mapping): Illustrative schematic
- **Fig.S3** (Ensemble HAT concept): Conceptual diagram

**Action**: Provide final PDFs only, no CSV source data.

### Bundle Delivery

- **Filename**: `source_data_nc_submission.xlsx` (+ `source_data_csvs.zip` for individual files)
- **Size**: < 5 MB (Excel) + < 2 MB (CSV zip)
- **Format**: Excel with multiple sheets for editorial convenience; CSV zip for programmatic access
- **Delivery**: Private link at submission; public release at acceptance

---

## [Kimi] KX31: Submission Portal Fieldbook [HIGH]

### NC Submission System Fields

| Field / Category | What to Prepare | Evidence Location | Owner | Blocking? |
|:-----------------|:----------------|:------------------|:------|:---------:|
| **Manuscript PDF** | `main.pdf` (4.8 MB) | `paper/latex_gpt/main.pdf` | Codex | ✅ Yes |
| **Supplementary PDF** | `supplementary_main.pdf` (9.1 MB) | `paper/latex_gpt/supplementary_main.pdf` | Codex | ✅ Yes |
| **Cover Letter** | `cover_letter.pdf` (63 KB) | `paper/latex_gpt/cover_letter.pdf` | Codex | ✅ Yes |
| **Article Type** | "Article" (not Review/Comment) | Cover letter | Author | ✅ Yes |
| **Title** | 95 characters max | `main.tex:25-26` | Author | ✅ Yes |
| **Abstract** | 150 words (cover letter) / full abstract | `sections/00_abstract.tex` | Author | ✅ Yes |
| **Keywords** | 8 keywords | `main.tex:38` | Author | ✅ Yes |

### Authorship Metadata

| Field | What to Prepare | Evidence | Owner | Blocking? |
|:------|:----------------|:---------|:------|:---------:|
| **Author list** | Name, affiliation, email | Manuscript front matter | Author | ✅ Yes |
| **ORCID** | If available | Author records | Author | 🟡 No |
| **Current address** | If different from affiliation | Author records | Author | 🟡 No |
| **Contributions** | CRediT roles | `07_conclusion.tex:20` | Author | 🟡 No |
| **Corresponding author** | Email for correspondence | Cover letter | Author | ✅ Yes |

### Disclosure Fields

| Field | What to Prepare | Evidence | Owner | Blocking? |
|:------|:----------------|:---------|:------|:---------:|
| **Competing interests** | "None declared" | `07_conclusion.tex:17` | Author | ✅ Yes |
| **Related manuscripts** | Confirm no overlap | Author knowledge | Author | ✅ Yes |
| **Prior dissemination** | Confirm no preprint | Cover letter L47 | Author | ✅ Yes |
| **Permissions** | None (no personal comms) | — | — | 🟡 No |

### Reviewer Management

| Field | What to Prepare | Evidence | Owner | Blocking? |
|:------|:----------------|:---------|:------|:---------:|
| **Suggested reviewers** | 2-4 names + emails + affiliations | Author network | Author | 🟡 No |
| **Excluded reviewers** | None (or list if any) | Author knowledge | Author | 🟡 No |
| **Editor requests** | None | — | — | 🟡 No |

### Data/Code Availability (Portal Fields)

| Field | What to Prepare | Evidence | Owner | Blocking? |
|:------|:----------------|:---------|:------|:---------:|
| **Data availability statement** | Public datasets only | `07_conclusion.tex:11` | Author | ✅ Yes |
| **Code availability** | "Available at submission" | `07_conclusion.tex:14` | Author | ✅ Yes |
| **Accession codes** | None (no sequence data) | — | — | 🟡 No |

### Upload Slots (NC System)

| Slot | File | Status | Blocking? |
|:-----|:-----|:------:|:---------:|
| Manuscript | `main.pdf` | ✅ Ready | Yes |
| Supplementary | `supplementary_main.pdf` | ✅ Ready | No (optional) |
| Cover Letter | `cover_letter.pdf` | ✅ Ready | Yes |
| Source Data | `source_data_nc_submission.xlsx` | 🔄 Prepare | No (on request) |
| Code Archive | `organic_cim_review_2026.zip` | 🔄 Prepare | No (private link) |

---

## [Kimi] KX32: Cover-Letter + Rebuttal Pack 2.0 [HIGH]

### Editor-Facing Novelty Bullets (8 items)

1. **Cross-disciplinary gap closure**: First systematic bridge between organic device characterization (materials science) and modern vision transformer deployment (ML systems), addressing a long-standing disconnect in the neuromorphic community.

2. **Profile-driven methodology**: Novel JSON-based device profile interface enabling seamless substitution of literature-derived or measured parameters without code modification—distinct from fixed-device simulators like AIHWKIT.

3. **Ensemble HAT discovery**: Identification of catastrophic hardware-instance overfitting in standard HAT (10% accuracy on fresh D2D) and its resolution via per-epoch D2D resampling (86.37±1.54%)—a new training paradigm for analog CIM.

4. **Hierarchy revision**: Demonstration that quantization is not the dominant bottleneck; instead, converter precision (6-bit cliff), fresh-instance robustness, and nonlinear write dynamics drive deployment risk.

5. **Organic-specific physics**: First simulation framework natively supporting optoelectronic frontend compensation, state-dependent proportional noise, and strong write nonlinearity (NL=2.0 boundary at 27.72%).

6. **Quantified sensitivity bounds**: EXP-A/EXP-B provide first quantitative bounds on differential-pair asymmetry (2% threshold) and array non-idealities (<2.5% loss at 3% IR drop + 2% sneak)—actionable for hardware designers.

7. **Literature-to-deployment bridge**: Zhang 2025 OPECT case study demonstrates zero-shot evaluation of external device profiles, validating the "materials-to-system" workflow.

8. **Reproducibility infrastructure**: Complete seeded execution pipeline with Monte Carlo evaluation, checkpoint lineage, and deterministic cuDNN settings for execution-trace reproducibility.

### Likely Editor Concern → One-Paragraph Answer (6 items)

| Concern | Answer |
|:--------|:-------|
| **Simulation-only without hardware validation** | The framework is explicitly positioned as a "first-order behavioral decision bridge" rather than a predictive circuit emulator. This scope is appropriate for early-stage materials evaluation: it enables researchers to assess which device characteristics constrain deployment before committing to full chip fabrication. The profile-driven interface is designed to accept measured parameters as they become available, closing the loop between characterization and simulation. |
| **Comparison to mature simulators (AIHWKIT/CrossSim)** | A shared-regime sanity check (ResNet-18, 4-bit, matched noise) shows consistent qualitative trends (96.88% → 91.80%) with AIHWKIT. Full physics equivalence is not claimed; the contribution lies in organic-specific features (optoelectronic frontend, state-dependent noise, profile substitution) absent from inorganic-optimized toolkits. |
| **Statistical rigor (single vs multi-seed)** | Key results carry error bars: Ensemble HAT (86.37±1.54%), C4 three-seed (84.75±0.72%), NL=2.0 (27.72±0.82%). Auxiliary single-run controls are explicitly labeled. ConvNeXt C4 three-seed demonstrates framework reproducibility; Tiny-ViT V4 Ensemble HAT uses 10-run MC across fresh instances. |
| **Energy model credibility** | The 273.94 µJ estimate is explicitly framed as a "first-order upper-bound" rather than routed chip measurement. Sensitivity analysis shows the qualitative advantage persists even with 50% unmodeled routing overhead (gain reduces from 11.45x to 9.90x). ADC energy <0.1% reflects amortization across large array operations (6-bit SAR). |
| **Scope appropriateness for NC** | The work sits at the intersection of materials science, device engineering, and ML systems—NC's core interdisciplinary scope. The Ensemble HAT finding (training-time regularization for D2D robustness) has implications beyond organic devices, while the profile-driven interface offers a reusable methodology for emerging device technologies. |
| **Prior publication / preprint** | The work is submitted exclusively to Nature Communications with no prior preprint or conference publication. The framework was developed specifically for this submission. |

### Likely Reviewer Attack → One-Paragraph Rebuttal (6 items)

| Attack | Rebuttal |
|:-------|:---------|
| **"10%→86% recovery is just data augmentation"** | Ensemble HAT resamples D2D masks—weight-space augmentation tied to physical device variability. This is distinct from standard input augmentation: it explicitly targets the hardware-instance overfitting exposed in §5.4. The 86.37% generalizes to fresh physical instances without pre-deployment calibration, validating the physical relevance. |
| **"ADC energy <0.1% contradicts CIM literature"** | The <0.1% reflects behavioral model assumptions: 6-bit SAR ADC at throughput-matched sampling, amortized across 128×128 differential-pair MACs. This is consistent with hybrid architectures where analog MACs dominate operation count. The manuscript explicitly qualifies this as a first-order estimate; reviewer feedback may motivate more detailed peripheral modeling in revision. |
| **"Scale masking is unproven hypothesis"** | The masking mechanism is quantified: σ_w ≈ 0.05 vs. Δ_w/2 ≈ 0.067 satisfies the sub-LSB condition. The hypothesis is further supported by its conditional failure under proportional noise (§5.6)—exactly the regime where per-state noise exceeds quantization bins. |
| **"No COMSOL validation for NL=2.0 boundary"** | The 27.72% boundary is explicitly framed as the limit of the gradient-scaling approximation, not a fundamental materials constraint. Pulse-faithful validation would require finite-element device physics simulation beyond behavioral scope—acknowledged in §6.6 limitations. |
| **"Flowers-102 failure unexplained"** | The zero-noise hybrid control (91.30%) demonstrates the failure is driven by noise-data interaction, not pure data starvation. Domain shift and hyperparameter mismatch remain viable alternatives; the manuscript treats data-floor as a working hypothesis rather than settled claim (§6.3). |
| **"Missing coupled ablations (C2C×D2D×NL×ADC)"** | Full factorial ablation would expand scope ~5× beyond the current 109 tracked reviewer items. The present matrix prioritizes deployment-critical regimes per organic CIM literature. Coupled studies are deferred to future work—standard scope boundary for simulation methodology papers. |

---

## [Kimi] KX33: Public Release Boundary Audit [MED]

### Safe to Publish (Release-Ready)

| Path/Pattern | Contents | Reason |
|:-------------|:---------|:-------|
| `README.md` | Project overview, quick start | Public-facing documentation |
| `LICENSE` | Apache 2.0 full text | License compliance |
| `src/*.py` | Core framework modules | Open-source contribution |
| `device_profiles/*.json` | Example device profiles | Demonstrates profile-driven approach |
| `docs/*.md` | User guides (profile, experiment, physics) | Community adoption support |
| `paper/latex_gpt/` | LaTeX sources (optional) | Academic transparency |
| `results_summary/*.csv` | Key numerical results | Data verification |

### Should Move Behind `internal/` (Not Public)

| Path/Pattern | Contents | Reason |
|:-------------|:---------|:-------|
| `report_md/_gpt/` | Agent coordination files | Internal workflow, not science |
| `*_TASK_*.md` | Task assignments | Project management artifacts |
| `*_HANDOFF_*.md` | Inter-agent handoffs | Development history |
| `*_DISPATCH_*.md` | Dispatch instructions | Internal coordination |
| `REVIEWER_COVERAGE*.md` | Coverage tracking | Internal audit artifacts |
| `EXPERIMENT_AUDIT_TRAIL*.md` | Verification logs | Internal quality control |
| `logs/_gpt/` | Detailed execution logs | Debugging artifacts, large size |
| `checkpoints/*.pt` | Model weights | Large files; can be regenerated |

### Should Summarize Instead of Raw

| Current | Recommended | Reason |
|:--------|:------------|:-------|
| Full `json_gpt/` directory | Curated `results_summary/*.csv` | Raw JSONs are verbose; CSVs sufficient |
| All experiment logs | Key result extracts with pointers | Logs are voluminous |
| Internal debate notes | Clean methodology description | Editorial narrative, not process |

### Recommended Release Structure

```
orgoptedge-cim-framework/          # Public repository
├── README.md
├── LICENSE
├── REQUIREMENTS.txt
├── src/                           # Core code
├── device_profiles/               # Example profiles
├── configs/                       # Reproducibility configs
├── docs/                          # User documentation
├── tests/                         # Smoke tests
├── results/                       # Curated CSV summaries
└── paper/                         # LaTeX sources (optional)

orgoptedge-cim-internal/           # Private/internal (optional)
├── report_md/_gpt/                # Full coordination history
├── logs/                          # Complete execution logs
├── checkpoints/                   # Model weights
└── experiments/                   # Raw experiment data
```

---

## [Kimi] KX34: Submission-Risk Sweep for Non-Science Items [MED]

### Risk Items (8 items)

| # | Risk | Why Editorial Office Cares | Minimum Action |
|:-:|:-----|:---------------------------|:---------------|
| 1 | **Author affiliation ambiguity** | NC requires institutional email verification | Confirm all affiliations current and correct |
| 2 | **Corresponding author unclear** | Editorial correspondence routing | Designate single corresponding author with active email |
| 3 | **Competing interests statement mismatch** | Policy compliance | Verify "None declared" is accurate for all authors |
| 4 | **Prior dissemination undisclosed** | Double-submission prevention | Confirm no preprint posted (arXiv, bioRxiv, etc.) |
| 5 | **Related manuscript overlap** | Self-plagiarism detection | Verify no overlapping submissions elsewhere |
| 6 | **File naming inconsistency** | Professional presentation | Use `Li_2026_NC_manuscript.pdf` style naming |
| 7 | **ORCID missing** | Author identification | Add ORCID iDs if available (not blocking) |
| 8 | **Permissions for adapted figures** | Copyright compliance | N/A (all figures original) — confirm in form |

### Editorial Office Red Flags to Avoid

- ❌ Generic email (gmail/yahoo) as corresponding author
- ❌ "TBD" or placeholder text in any field
- ❌ Missing institutional affiliation for any author
- ❌ Unclear distinction between authors and contributors
- ❌ Conflicting competing interests statements

---

## [Kimi] KX35: Final Package Filename + Asset Audit [MED]

### Current → Recommended Naming

| Current File | Recommended Submission Name | Why |
|:-------------|:----------------------------|:----|
| `main.pdf` | `Li_2026_NC_manuscript.pdf` | Professional, identifiable |
| `supplementary_main.pdf` | `Li_2026_NC_supplementary.pdf` | Consistent naming |
| `cover_letter.pdf` | `Li_2026_NC_cover_letter.pdf` | Editorial tracking |
| `source_data.xlsx` | `Li_2026_NC_source_data.xlsx` | Consistent prefix |
| `organic_cim_review.zip` | `Li_2026_NC_code_archive.zip` | Identifiable, versioned |

### Asset Hierarchy (Submission Package)

```
Li_2026_NC_submission_package/
├── 01_manuscript/
│   └── Li_2026_NC_manuscript.pdf
├── 02_supplementary/
│   └── Li_2026_NC_supplementary.pdf
├── 03_cover_letter/
│   └── Li_2026_NC_cover_letter.pdf
├── 04_source_data/
│   ├── Li_2026_NC_source_data.xlsx
│   └── README_source_data.txt
├── 05_code_archive/
│   ├── Li_2026_NC_code_archive.zip
│   └── README_code.txt
└── 06_latex_source/ (optional)
    └── latex_source.zip
```

### Portal Upload Mapping

| NC Portal Slot | Local File | Upload Order |
|:---------------|:-----------|:------------:|
| Manuscript | `Li_2026_NC_manuscript.pdf` | 1 |
| Supplementary | `Li_2026_NC_supplementary.pdf` | 2 |
| Cover Letter | `Li_2026_NC_cover_letter.pdf` | 3 |
| Source Data (if requested) | `Li_2026_NC_source_data.xlsx` | 4 |
| Code Description | Link to `Li_2026_NC_code_archive.zip` | 5 |

---

## [Kimi] KX36: End-to-End Adversarial Preflight [MED]

### Final Risk Assessment (Pre-Submission)

| Category | Risk Level | Mitigation Status |
|:---------|:----------:|:------------------|
| **Scientific claims** | 🟢 Low | All key claims have error bars |
| **Statistical rigor** | 🟢 Low | Multi-seed where critical, MC everywhere |
| **Simulation scope** | 🟢 Low | Explicitly limited to "first-order behavioral" |
| **Code availability** | 🟡 Medium | Archive plan ready, needs assembly |
| **Source data** | 🟡 Medium | Workbook spec ready, needs assembly |
| **Submission metadata** | 🟡 Medium | Manual form fields pending |
| **File naming** | 🟢 Low | Spec provided, easy fix |

### Preflight Checklist (Author Must Verify)

- [ ] All PDFs compile without errors
- [ ] Title ≤ 100 characters (current: 95 ✅)
- [ ] Abstract < 150 words (cover letter)
- [ ] 8 keywords specified
- [ ] Author affiliations current
- [ ] Corresponding author email active
- [ ] Competing interests "None" accurate
- [ ] No preprint posted
- [ ] No overlapping submissions
- [ ] Code archive assembled and tested
- [ ] Source data workbook assembled
- [ ] Suggested reviewers identified (2-4)
- [ ] File naming follows `Li_2026_NC_*` pattern

### Go/No-Go Decision Matrix

| Condition | Status | Decision |
|:----------|:------:|:---------|
| Manuscript clean | ✅ | GO |
| Supplementary clean | ✅ | GO |
| Cover letter ready | ✅ | GO |
| Code archive ready | 🔄 | GO after assembly |
| Source data ready | 🔄 | GO after assembly |
| Metadata confirmed | 🔄 | GO after form completion |

**Final verdict**: 🟢 **GO for submission** once code archive and source data are assembled (2-3 hours work).

---

## Summary: KX29-KX36 Deliverables

| Task | Status | Key Output |
|:-----|:------:|:-----------|
| KX29 | ✅ | Code archive layout + README draft |
| KX30 | ✅ | Source-data workbook schema (8 sheets) |
| KX31 | ✅ | NC portal fieldbook (all fields mapped) |
| KX32 | ✅ | Cover-letter 2.0 + 6 editor concerns + 6 reviewer rebuttals |
| KX33 | ✅ | Public/private file boundary audit |
| KX34 | ✅ | 8 non-science risk items + mitigation |
| KX35 | ✅ | Professional filename scheme + asset hierarchy |
| KX36 | ✅ | End-to-end preflight + go/no-go matrix |

**All KX29-KX36 tasks complete.**

---

*Batch delivery completed: 2026-04-12*
*Mode: Full-batch closeout (Kimi primary execution)*
