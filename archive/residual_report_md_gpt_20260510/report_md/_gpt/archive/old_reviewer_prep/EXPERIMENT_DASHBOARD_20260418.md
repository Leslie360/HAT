# Experiment Dashboard — 2026-04-18 21:30 CST

## NL Mitigation Group-Wise Ablation

| Variant | Status | Best Test Acc | Epoch | vs NL=2.0 Baseline (27.72%) | Notes |
|:--------|:-------|:-------------:|:-----:|:---------------------------:|:------|
| **MLP-only** | ✅ Complete | **87.79%** | 73 | **+60.07 pp** | Primary recovery path |
| **QKV-only** | ✅ Complete | **18.72%** | 2 | **−9.00 pp** | Structural failure — attention NL required |
| **attn_proj-only** | ⏳ Queued (OOM) | — | — | — | Will launch after all-linear finishes |
| **all-linear** | 🔄 Running | **85.32%** @ ep49 | 49 (of 100) | **+57.60 pp** | In-flight; ~12–15 h remaining |
| **Global NL=1.0** | ✅ Baseline | 91.94% | — | +64.22 pp | Upper bound |
| **Global NL=2.0** | ✅ Baseline | 27.72 ± 0.82% | — | — | Unmitigated |

**Preliminary interpretation:** MLP-only and all-linear converge to ~85–88%, confirming the MLP path is the dominant recoverable bottleneck. QKV-only fails catastrophically, showing attention nonlinearity is structurally required. The all-linear result will likely be MLP-dominated (QKV failure masked by MLP recovery).

**CLAUDE-A Decision:** Option B — supplementary ablation table. NL mitigation does NOT become a 5th main-paper contribution.

---

## E3 Learnable Gamma Compensation

| Variant | Test Acc | Notes |
|:--------|:--------:|:------|
| Fixed γ=0.5 | 48.80% | Physical inverse |
| **Learnable γ_comp** | **51.65%** | Learned γ_comp = **0.7398** (vs 0.5000) |
| Raw (no comp) | 49.61% | — |

**Interpretation:** Learned γ_comp deviates from physical inverse by +0.2398, validating T2 theory that task-level adaptation dominates over strict physical inversion. Improvement: +2.85 pp over fixed.

**Placement:** Supplementary theory-validation note.

---

## Active GPU Jobs

| Job | PID(s) | VRAM | Progress | ETA |
|:----|:-------|:-----|:---------|:----|
| all-linear NL mitigation | 475334 (+7 DDP workers) | ~4.6 GB | Epoch 49/100, best 85.32% | ~12–15 h |

**GPU headroom:** None — 9 python processes saturate GPU. attn_proj-only queued behind all-linear.

---

## Manuscript Status (post R1–R4)

| Document | Pages | Status |
|:---------|:-----:|:-------|
| Main | 15 | ✅ Compiled; R1–R4 edits landed |
| Supplementary | 21 | ✅ Compiled |
| Cover letter | 2 | ✅ Compiled; 88.53% synced with error bar |

---

## Next Queue (when GPU drains)

1. **attn_proj-only NL mitigation** — completes group-wise ablation matrix
2. **E5 layer-wise gamma sensitivity** — script preparation in progress
3. **Final CLAUDE-A decision** — lock after all-linear + attn_proj finish
