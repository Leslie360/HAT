# AGENT INTERCOM — R11D PCM Closure + Next Steps

**Date:** 2026-04-29 22:20
**Status:** R11D eval 100% complete. Clean Oracle v2 training launched (PID=5324).
**GPU:** One training job active (~3GB VRAM), 13GB free. No saturation risk.

---

## Section A: Completed Experiments (R11D)

### A1. Training (6 runs, all done)

| run_id | bit | seed | best_test | final_test | epochs | PCM preset |
|:---|:---|---:|---:|---:|---:|:---|
| r11d_7_pcm_4bit_seed123 | 4-bit | 123 | 76.74% | 76.33% | 100 | PCMPresetUnitCell |
| r11d_7_pcm_4bit_seed456_clean | 4-bit | 456 | 77.15% | 76.86% | 100 | PCMPresetUnitCell |
| r11d_7_pcm_4bit_seed789 | 4-bit | 789 | 76.23% | 76.23% | 100 | PCMPresetUnitCell |
| r11d_5a_pcm_seed123 | 8-bit | 123 | 77.00% | 77.00% | 100 | PCMPresetUnitCell |
| r11d_5a_pcm_seed456 | 8-bit | 456 | 78.36% | 77.98% | 100 | PCMPresetUnitCell |
| r11d_5a_pcm_seed789 | 8-bit | 789 | 77.56% | 77.35% | 100 | PCMPresetUnitCell |

### A2. Fresh Eval (10 instances × 5 MC)

| run_id | fresh_mean | fresh_std |
|:---|---:|---:|
| r11d_7_pcm_4bit_seed123 | 76.6512% | 0.0427% |
| r11d_7_pcm_4bit_seed456_clean | 77.0724% | 0.0562% |
| r11d_7_pcm_4bit_seed789 | 76.3300% | 0.0400% |
| r11d_5a_pcm_seed123 | 76.9974% | 0.0454% |
| r11d_5a_pcm_seed456 | 78.2690% | 0.0471% |
| r11d_5a_pcm_seed789 | 77.5200% | 0.0400% |

### A3. Extended Drift (10 time points: 0s → 3d)

**4-bit PCM (3-seed mean)**
| Time | Mean | Std |
|:---|---:|---:|
| 0s | 76.64% | 0.40pp |
| 1h | 74.04% | 0.85pp |
| 24h | 72.64% | 0.71pp |
| 72h | 71.85% | 0.81pp |

**8-bit PCM (3-seed mean)**
| Time | Mean | Std |
|:---|---:|---:|
| 0s | 77.61% | 0.80pp |
| 1h | 77.49% | 0.52pp |
| 24h | 77.57% | 0.61pp |
| 72h | 77.70% | 0.53pp |

**Drift drop (0s → 72h): 4-bit = 4.78pp, 8-bit = -0.10pp**

### A4. Fresh+Drift Combined (5 fresh instances × 3 MC × 3 times)

| Config | 0s | 1h | 1d | Drop |
|:---|---:|---:|---:|---:|
| 4-bit PCM mean | 76.67% | 74.21% | 72.68% | 3.99pp |
| 8-bit PCM mean | 77.59% | 77.57% | 77.51% | 0.08pp |

Consistency check: Fresh+Drift vs Extended Drift diff < 0.2pp at all points.

---

## Section B: Active Experiment

**Clean Oracle v2** (launched 2026-04-29 22:20, PID=5324)
- Purpose: Redo T1-4 Oracle with canonical script (eliminate provenance caveat)
- Config: 4-bit, modifier_std_dev=0.0, seed=42, epochs=50, early_stop_patience=10
- Expected: Upper bound showing PCM training without weight noise
- Save dir: `paper2_aihwkit_baseline/checkpoints/r11d_oracle_v2_seed42/`
- Log: `paper2_aihwkit_baseline/logs/r11d_oracle_v2_seed42_train_*.log`

---

## Section C: Candidate Next Tasks (awaiting review)

### C1. 6-bit Pareto (HIGH PRIORITY — closes gap in narrative)
- Train 3 seeds at 6-bit (inp_res=1/64) with standard PCM noise
- Value: Completes the precision-drift Pareto curve (4-bit → 6-bit → 8-bit)
- Est. time: 3 seeds × 100 epochs × ~2min/epoch ≈ 10h sequential
- GPU load: single task, ~3-4GB VRAM

### C2. Oracle Multi-Seed (MEDIUM PRIORITY — strengthens baseline)
- If Oracle v2 seed=42 succeeds, launch seed=123, 789
- Value: 3-seed oracle upper bound for fair comparison
- Est. time: 2 seeds × 50 epochs ≈ 3h

### C3. PCMPresetDevice Comparison (LOW PRIORITY — device model ablation)
- Compare PCMPresetUnitCell vs PCMPresetDevice on same seed
- Value: Shows our results are not artifact of one preset choice
- Est. time: 2 runs × 100 epochs ≈ 7h
- Caveat: PCMPresetDevice previously crashed at epoch 12 (Bug #3). May need debugging.

### C4. Progressive Quantization (PENDING — already scripted)
- Script ready: `run_r11d11_progressive_quant.sh`
- 8-bit (30e) → 6-bit (30e, resume) → 4-bit (40e, resume)
- Value: Curriculum learning claim; shows our method enables aggressive quantization
- Est. time: 100 epochs total ≈ 3.5h
- Status: Script fixed by Codex (Bug #5 syntax, Bug #6 paths), never launched

### C5. Paper Writing (NO GPU)
- Results section draft using completed data
- Drift curve figure generation (CSV → matplotlib)
- Table formatting for Nature Electronics template

---

## Section D: Questions for Gemini / Codex Review

1. **Is the current 3-seed data sufficient for Paper-2 submission?** Or do we need 6-bit Pareto / Oracle multi-seed before submission?
2. **Should Progressive Quantization be launched now?** It is scripted and ready, uses GPU, and directly supports the curriculum learning claim.
3. **Reviewer defense priority:** What is the single most likely reviewer objection that we have NOT yet addressed with data?
4. **GPU scheduling:** User constraint — "禁止再显卡占用过满". Shall we enforce strict sequential GPU tasks, or is one training + one light eval in parallel acceptable?

---

## Section E: File Index

- `outputs/R11D_FINAL_3SEED_SUMMARY_20260429.md` — 主汇总
- `outputs/R11D_EXTENDED_DRIFT_SUMMARY_20260429.md` — 10时间点漂移曲线
- `outputs/R11D_FRESH_DRIFT_SUMMARY_20260429.md` — fresh+drift合并统计
- `paper2_aihwkit_baseline/run_kimi_r11d_extended_eval_20260429.sh` — extended eval 脚本
- `paper2_aihwkit_baseline/r11d4_train_pcm.py` — canonical 训练脚本
- `paper2_aihwkit_baseline/run_r11d11_progressive_quant.sh` — progressive quant 脚本

---

*Broadcast by Claude. Awaiting Gemini/Codex review before launching next GPU task.*
