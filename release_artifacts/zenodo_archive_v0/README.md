# Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision

Zenodo reproducibility archive v0.0.1  
*Corresponds to manuscript under review, Nature Communications*

---

## Title & citation

**Paper title:** Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision

If you use this archive or the associated code, please cite:

```bibtex
@article{li2026organic,
  title={Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision},
  author={Li, Songqiao and ...},
  journal={Nature Communications},
  year={2026},
  doi={10.5281/zenodo.XXXXXXX}
}
```

> **DOI:** `10.5281/zenodo.XXXXXXX` (placeholder — will be minted on upload)

---

## What's in this archive

This package contains the data and code artifacts needed to reproduce the figures, tables, and key quantitative claims in the manuscript.

| Path | Description |
|:---|:---|
| `source_data/source_data_v1.zip` | 77 files (73 JSON + 2 CSV) containing the raw numerical data behind every main-text and supplementary figure/table |
| `source_data/source_data_v1_MANIFEST.md` | Per-file descriptions and manuscript cross-references |
| `code_snapshot/paper/plot_paper_figures.py` | Python script that regenerates all publication figures from the JSON/CSV bundle |
| `code_snapshot/scripts_gpt/check_locked_numbers.py` | Guard script that re-reads every JSON cited in the manuscript and asserts numerical consistency (`16/16 passed`) |
| `code_snapshot/scripts_gpt/eval_standard_fresh_instance_noamp.py` | Re-evaluates the paper-locked V4 checkpoint on 10 fresh D2D instances without AMP |
| `code_snapshot/scripts_gpt/eval_spatially_correlated_d2d.py` | Stress-test variant that injects spatially correlated D2D mismatch (AR(1) field) |
| `code_snapshot/latex_sections/05_results.tex` | Manuscript Results section most tightly coupled to the late-cycle hardened numbers |
| `code_snapshot/latex_sections/06_discussion.tex` | Manuscript Discussion section |
| `code_snapshot/supplementary.tex` | Supplementary Information LaTeX source |
| `code_snapshot/COMMIT.txt` | Repository HEAD used to assemble this archive |
| `code_snapshot/WORKTREE_STATUS.txt` | Git status at archive creation time |
| `code_snapshot/CODE_SNAPSHOT_LEDGER_20260418.md` | Manuscript-to-code dependency ledger |

The archive is a *snapshot* of the repository at submission time. For training or interactive development, clone the full repository (see Contact).

---

## Quick start

Three commands to reproduce the headline result — **Ensemble HAT 86.37 ± 1.54 %** on CIFAR-10:

```bash
# 1. Install dependencies (conda recommended; pip works with manual CUDA setup)
conda env create -f environment.yml && conda activate LLM

# 2. Train the Ensemble HAT V4 model (100 epochs, ~90 min on a modern GPU)
python train_tinyvit_ensemble.py --experiment V4 --mode train --dataset cifar10 --epochs 100

# 3. Evaluate across 10 fresh D2D instances to obtain the ensemble mean and std
python run_ensemble_hat_fixed.py
```

After step 3, the expected output is `86.37 ± 1.54 %` task accuracy. The best checkpoint is typically reached between epochs 40 and 60.

---

## System requirements

| Component | Minimum | Recommended |
|:---|:---|:---|
| Python | 3.11 | 3.11 |
| PyTorch | ≥ 2.0 | ≥ 2.1 (CUDA 12.1) |
| CUDA | Optional | 12.1 |
| GPU VRAM | — | ≥ 4 GB |
| Disk | ~ 2 GB | ~ 5 GB (with checkpoints) |
| RAM | ~ 8 GB | ~ 16 GB |

A CPU-only fallback exists (PyTorch automatically uses `device="cpu"`), but training is 10–20× slower. We strongly recommend a CUDA-capable GPU for any interactive work.

---

## Data

**CIFAR-10**, **CIFAR-100**, and **Flowers-102** are downloaded automatically by `torchvision` into `./data/` on first use. No manual preparation is required.

**ImageNet ILSVRC2012** must be supplied manually; see `download_data.sh` in the repository for the expected folder layout.

**Custom datasets** are supported as long as they implement the standard PyTorch `Dataset` interface and are registered in the `DATASET_STATS` dictionary of the training script.

---

## Reproducing key results

| Result | Command | Expected output | Runtime |
|:---|:---|:---|:---|
| Ensemble HAT training | `python train_tinyvit_ensemble.py --experiment V4 --mode train --dataset cifar10 --epochs 100` | Best checkpoint saved to `checkpoints/` | ~ 90 min (GPU) |
| Ensemble HAT evaluation | `python run_ensemble_hat_fixed.py` | `86.37 ± 1.54 %` | ~ 2–3 min |
| Standard HAT no-AMP verification | `python code_snapshot/scripts_gpt/eval_standard_fresh_instance_noamp.py` | Fresh-instance mean ≈ 87.95 % | ~ 2 min |
| Spatially correlated D2D stress test | `python code_snapshot/scripts_gpt/eval_spatially_correlated_d2d.py --rho 0.5` | Accuracy degradation curve vs. ρ | ~ 3 min |
| Locked-number validation | `python code_snapshot/scripts_gpt/check_locked_numbers.py` | `16/16 passed` | < 1 sec |
| Regenerate all figures | `python code_snapshot/paper/plot_paper_figures.py` | PDF/PNG files in `paper/figures/` | ~ 30 sec |

> **Note on reproducibility:** Small deviations are expected. PyTorch seeding is sensitive to GPU driver version, CUDA toolkit build, and data-loader worker count. The reported standard deviations capture this run-to-run variation; if your mean falls inside the reported interval, your reproduction is successful.

---

## License

**MIT** (placeholder — pending final author decision).  
The manuscript text and supplementary materials are © the authors, 2026.

---

## Contact

For bugs, feature requests, or usage questions, please open a GitHub issue in the main repository.  
For sensitive or embargoed enquiries: `corresponding.author@institution.edu` (placeholder).

---

## Changelog

### v0.0.1 — 2026-04-19
- Initial release accompanying manuscript submission.
- Contains source-data bundle v1 (77 files), code snapshot, and manuscript-section provenance ledger.
