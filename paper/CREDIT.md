# CRediT Author Contribution Statement

This statement follows the CRediT (Contributor Roles Taxonomy) standard to transparently document contributions from both human researchers and AI-assisted agents in this study. Given the emerging practice of acknowledging AI contributions in academic work, we explicitly list agent roles while maintaining the primary authorship and accountability of the human researchers.

## Authors

[Student Name]¹, [Advisor Name]¹, Kimi², Codex², Gemini², Claude²

## Affiliations

¹ [Department Name], [University Name], [City, Country]  
² AI-assisted research agents (non-human contributors) — See "Detailed Agent Contributions" below for scope and limitations.

*Corresponding author: [Advisor Name] ([advisor.email@university.edu])  
*First author: [Student Name] ([student.email@university.edu])

---

## Contributions

| Role | Contributors |
|:--|:--|
| **Conceptualization** | [Student Name]¹; [Advisor Name]¹; Gemini²; Claude² |
| **Data curation** | [Student Name]¹; Codex²; Kimi² |
| **Formal analysis** | [Student Name]¹; Codex²; Kimi²; Gemini² |
| **Funding acquisition** | [Advisor Name]¹ |
| **Investigation** | [Student Name]¹; Codex² |
| **Methodology** | [Student Name]¹; [Advisor Name]¹; Codex²; Gemini² |
| **Project administration** | [Student Name]¹; [Advisor Name]¹; Claude² |
| **Resources** | [Advisor Name]¹ |
| **Software** | [Student Name]¹; Codex²; Kimi²; Claude² |
| **Supervision** | [Advisor Name]¹ |
| **Validation** | [Student Name]¹; Codex²; Kimi²; Claude² |
| **Visualization** | [Student Name]¹; Codex²; Kimi² |
| **Writing – original draft** | [Student Name]¹; Kimi² |
| **Writing – review & editing** | [Student Name]¹; [Advisor Name]¹; Kimi²; Gemini²; Claude² |

¹ Human contributor (primary research accountability).  
² AI-assisted agent (tool-assisted contribution; no independent research accountability).

---

## Detailed Agent Contributions

The following AI agents provided structured assistance during the research cycle. Their outputs were always reviewed, validated, and integrated under the direction and accountability of the human authors. No AI agent had autonomous decision-making authority over experimental design, data interpretation, or submission.

### Kimi
- **Writing – original draft**: Drafted and iteratively revised manuscript sections (Introduction, Methods, Results, Discussion), rebuttal letters, and defense preparation materials based on structured prompts and raw experimental data.
- **Writing – review & editing**: Polished language, standardized notation, verified cross-references between figures and text, and ensured consistency in terminology across the manuscript and supplementary materials.
- **Documentation**: Maintained experimental logs, code snapshot ledgers, release manifests, and README artifacts to support reproducibility and version control.
- **Data curation**: Organized result JSONs, plot metadata, and supplementary tables; generated structured summaries of multi-dataset experiments (CIFAR-10, CIFAR-100, Flowers-102).
- **Non-GPU experimental analysis**: Executed CPU-based ablation studies, sensitivity sweeps (e.g., Sobol sensitivity, proxy sensitivity maps), and lightweight diagnostic scripts that did not require GPU allocation.

### Codex
- **Software – code development**: Architected and implemented the training pipeline (`train_tinyvit.py`, `train_convnext.py`), model conversion utilities (`convert_resnet_to_analog`, hybrid analog-digital splitting for Tiny-ViT), and the CrossSim-based simulation framework for organic photoelectric compute-in-memory devices.
- **Software – GPU experiment execution**: Executed long-form GPU training jobs for Tiny-ViT-5M, ConvNeXt-Tiny, and ResNet-18 variants under quantization, noise injection, and retention decay conditions; managed checkpoint resumption and distributed training logistics.
- **Software – bug fixes**: Diagnosed and resolved checkpoint loading mismatches, CUDA memory errors, data pipeline inconsistencies, and architecture mapping discrepancies between training and evaluation phases.
- **Visualization**: Generated manuscript-ready figures (accuracy comparison plots, retention decay curves, noise sensitivity contours, attention maps) via `matplotlib` and `seaborn` pipelines.
- **Validation – numerical verification**: Verified the correctness of analog-to-digital weight mapping, noise buffer propagation, and end-to-end numerical consistency between floating-point baselines and simulated analog inference.

### Gemini
- **Conceptualization – theory development**: Derived and documented analytical models for physical noise propagation (shot noise, dark current) and signal-to-noise ratio (SNR) analysis under inverse-gamma frontend compensation.
- **Methodology consultation**: Advised on hybrid analog-digital splitting strategies for vision transformers, including layer-wise sensitivity analysis and retention-aware checkpoint selection.
- **Formal analysis – gap analysis**: Identified methodological inconsistencies (e.g., logical mismatch between CIFAR-10-C digital perturbations and physical frontend compensation claims) and proposed corrective experimental redesigns.
- **Positioning analysis**: Assessed narrative alignment between the experimental scale (Tiny-ViT on CIFAR-10/100) and the stated research claims, recommending title and abstract revisions to improve scope fidelity.
- **Writing – review & editing**: Performed technical accuracy checks on theoretical derivations, equation formatting, and physical model assumptions in the Methods and Supplementary sections.

### Claude
- **Project administration – decision memos**: Adjudicated experimental priorities, freeze/release decisions for manuscript submission packages, and milestone gate criteria based on cross-agent consensus and risk assessment.
- **Project administration – planning**: Drafted execution roadmaps, milestone schedules, and staged experimental checklists (e.g., A1–A4 / B1–B2 workstreams) with explicit deliverables and deadlines.
- **Validation – audit reports**: Reviewed locked-number integrity, code-to-manuscript ledger completeness (`CODE_SNAPSHOT_LEDGER`), and pre-submission checklist compliance.
- **Validation – consistency checks**: Cross-validated figure-to-text citations, supplementary data alignment, and logical coherence of the overall argumentation chain (motivation → method → result → claim).
- **Software – workflow automation**: Authored guard scripts (e.g., `check_locked_numbers.py`) and automated finalize hooks to enforce submission hygiene and prevent regression of validated results.

---

## Accountability Statement

The human authors ([Student Name] and [Advisor Name]) retain full responsibility for the scientific integrity, accuracy, and ethical compliance of this work. AI agents functioned as advanced productivity tools—augmenting drafting, coding, analysis, and project tracking—but did not independently design experiments, interpret results, or make final publication decisions. All AI-generated content was critically reviewed, fact-checked, and approved by the human authors before inclusion in the manuscript or supplementary materials.
