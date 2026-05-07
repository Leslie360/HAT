# P1 Figure-Ready Scripts Return — Remote107

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|:---:|
| 107-P1-FIGDATA | Complete | 0 | No | PASS |

---

## 1. Exact Commands

All scripts run without GPU.

```bash
# Install matplotlib (one-time)
/home/lisq753/miniconda3/envs/LLM/bin/python -m pip install matplotlib --quiet

# Generate all three figures
/home/lisq753/miniconda3/envs/LLM/bin/python scripts/plot_k107_ablation.py
/home/lisq753/miniconda3/envs/LLM/bin/python scripts/plot_k107_epsc_stress.py
/home/lisq753/miniconda3/envs/LLM/bin/python scripts/plot_k107_scale_trend.py
```

---

## 2. Git SHA

| Item | Value |
|:---|:---|
| Branch | `107-clean` |
| Commit when generated | `d8e3b17` (current HEAD) |
| Eval commit (source data) | `cc0a3ab` (recorded in CSV/JSON metadata) |

---

## 3. Environment

| Item | Value |
|:---|:---|
| Python | 3.10 (conda env `LLM`) |
| matplotlib | 3.10.1 |
| Platform | Linux x86_64, 8× NVIDIA 32GB GPUs |

---

## 4. Input Files

| Script | Input | Source |
|:---|:---|:---|
| `plot_k107_ablation.py` | `baseline_digital_current.json`, `p0b_ablation/summary.csv` | committed deliverable |
| `plot_k107_epsc_stress.py` | `epsc_stress/summary.csv` | committed deliverable |
| `plot_k107_scale_trend.py` | `p0b_ablation/summary.csv`, `p1b_1b/*.json`, `p2d8b_2d8b/*.json` | committed deliverable |

All inputs are committed CSV/JSON; scripts contain no hardcoded PPL values except annotation labels.

---

## 5. Output Files

| File | Size | Description |
|:---|---:|:---|
| `deliverable/figures/k107_ablation_ladder.pdf` | 29K | Fig 1: Paired ablation ladder (PDF vector) |
| `deliverable/figures/k107_ablation_ladder.png` | 78K | Fig 1: PNG preview |
| `deliverable/figures/k107_epsc_stress.pdf` | 25K | Fig 2: EPSC stress with kill line (PDF vector) |
| `deliverable/figures/k107_epsc_stress.png` | 73K | Fig 2: PNG preview |
| `deliverable/figures/k107_scale_trend.pdf` | 30K | Fig 3: Scale trend 410M/1B/2.8B (PDF vector) |
| `deliverable/figures/k107_scale_trend.png` | 77K | Fig 3: PNG preview |

---

## 6. Numeric Tables

### Fig 1 — Paired Ablation Ladder (mean across 3 train seeds)

| Step | PPL | Δ vs previous |
|:---|---:|---:|
| Digital baseline (unpatched) | 22.185 | — |
| HAT digital / no patch (B1) | 19.043 | −3.142 |
| Patch / no noise (B2) | 19.060 | +0.017 |
| D2D = 0.02 (B3) | 19.483 | +0.423 |
| D2D = 0.05 (B4) | 19.644 | +0.161 |

### Fig 2 — EPSC Stress (mean ± std, n=9 per config)

| Config | sigma_c2c | sigma_d2d | Mean PPL | Std | Max |
|:---|:---:|:---:|:---:|:---:|:---:|
| EPSC-e1 | 0.05 | 0.05 | 19.718 | 0.061 | 19.814 |
| EPSC-e2 | 0.10 | 0.10 | 20.116 | 0.070 | 20.231 |
| EPSC-e3 | 0.15 | 0.15 | 20.762 | 0.073 | 20.869 |
| EPSC-e4 | 0.00 | 0.20 | 20.604 | 0.094 | 20.754 |
| EPSC-e5 | 0.01 | 0.10 | 19.861 | 0.068 | 19.974 |

Kill line: 25 PPL. All configs PASS.

### Fig 3 — Scale Trend (mean ± std)

| Model | D2D=0.02 | D2D=0.05 | n |
|:---|:---:|:---:|:---:|
| Pythia-410M | 19.483 ± 0.065 | 19.644 ± 0.058 | 9 |
| Pythia-1B | 14.597 ± 0.023 | 14.819 ± 0.032 | 6 |
| Pythia-2.8B | 13.333 ± 0.018 | 13.431 ± 0.007 | 6 |

---

## 7. Acceptance Criteria

| Criterion | Status |
|:---|:---:|
| Scripts run without GPU | ✅ |
| Scripts read committed CSV/JSON | ✅ |
| Vector PDF + PNG preview produced | ✅ |
| Evaluator protocol labeled in caption | ✅ |
| Draft quality (not final polish) | ✅ |

---

## 8. One-Sentence Recommendation

Figures are draft-ready for internal review; once manuscript figure templates are decided, only color palette and font sizing need adjustment — the data pipelines are fully reproducible from committed files.
