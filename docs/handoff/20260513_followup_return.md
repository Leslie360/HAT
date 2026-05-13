# Remote 105 Follow-up Return — ViT Seed2025 And DeiT Control Completion

**Date:** 2026-05-13  
**Branch:** `105-remote-results`  
**Executor:** Codex / Remote105

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|---|
| ViT seed2025 digital + proportional | Complete | ~22 | Yes | ViT becomes mixed (`2/4` seeds favor proportional) |
| DeiT seed789 ensemble + standard controls | Complete | ~20 | No | Control story unchanged: ensemble partial recovery, standard collapse |
| ViT noise-off + seed789 `30x5` fresh follow-ups | Complete | ~2 | No | Stability claim preserved |

---

## 1. ViT Seed2025 Follow-up

| HAT | Source (%) | Fresh (%) | Std (%) | Fresh-Source (pp) |
|---|---:|---:|---:|---:|
| digital | 50.00 | 50.00 | 0.00 | 0.00 |
| proportional | 49.77 | 49.85 | 0.08 | +0.08 |

**P-D fresh gap (seed2025):** `-0.15pt`  
**P-D source gap (seed2025):** `-0.23pt`

Interpretation:

- seed2025 does **not** support `proportional > digital` on ViT;
- it slightly favors digital;
- it also keeps seed456 digital (54.58%) in the "high outlier" regime relative to seeds 123 / 789 / 2025.

---

## 2. Updated ViT Aggregate

| Seed | ViT Prop − Digital (Fresh, pp) |
|---:|---:|
| 123 | +0.17 |
| 456 | -0.68 |
| 789 | +4.55 |
| 2025 | -0.15 |
| **Mean** | **+0.97** |

**Wins for proportional:** `2/4`

Updated interpretation:

- ViT is no longer "provisionally positive" in a directional sense;
- ViT is now **mixed / high-variance**;
- the positive mean persists, but it is strongly influenced by seed789.

---

## 3. DeiT Seed789 Control Completion

| HAT | Source (%) | Fresh (%) | Std (%) | Fresh-Source (pp) |
|---|---:|---:|---:|---:|
| ensemble | 44.73 | 39.92 | 0.35 | -4.81 |
| standard | 41.28 | 5.77 | 0.68 | -35.51 |

Interpretation:

- `ensemble` still shows only partial recovery;
- `standard` still collapses catastrophically;
- completing DeiT seed789 does not change the control story.

---

## 4. Additional Diagnostics

### ViT Noise-Off

| Checkpoint | Noise-Off (%) | Source (%) |
|---|---:|---:|
| ViT proportional seed456 | 53.99 | 54.06 |
| ViT proportional seed789 | 55.49 | 55.85 |

### Seed789 Extended Fresh Eval (`30x5`)

| Checkpoint | Fresh Mean (%) | Fresh Std |
|---|---:|---:|
| DeiT proportional seed789 | 56.32 | 0.12 |
| ViT proportional seed789 | 55.46 | 0.11 |

Interpretation:

- proportional checkpoints remain stable across fresh instances;
- the engineering stability claim survives the extra diagnostics;
- the uncertainty is about **relative advantage over digital on ViT**, not fresh-instance collapse.

---

## 5. Caveat

`vit_small_patch16_224_proportional_seed2025` and `deit_small_patch16_224_ensemble_seed789` were evaluated from saved `best.pt` after training logs stopped before an explicit terminal `Finished.` line. No checkpoint corruption was observed, and the reported fresh-eval results are tied to the saved `best.pt` payloads.

---

## 6. Recommendation

Remote105 should now be interpreted as:

- **DeiT:** strong positive validation for proportional HAT;
- **ViT:** mixed / high-variance outcome, not a stable positive validator;
- **Overall:** do not claim strong positive cross-architecture superiority on ViT from Remote105 alone.

No additional experiment is required for this batch unless the local team explicitly wants one last ViT tie-break seed despite the now-mixed `2/4` outcome.
