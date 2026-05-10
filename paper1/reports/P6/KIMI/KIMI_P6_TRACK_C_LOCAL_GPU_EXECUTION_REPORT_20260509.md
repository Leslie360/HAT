# Kimi P6 Track C Report: Local GPU Long-Run Queue

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md`
**Executor:** kimi

---

## 1. Current GPU Status

| GPU | Model | Memory Used | Memory Total | Utilization | Active Jobs |
|-----|-------|-------------|--------------|-------------|-------------|
| 0 | NVIDIA GeForce RTX 5070 Ti | 5626 MiB | 16303 MiB | 41% | 1 active |

**Status:** Running seed123 6-bit PCM rerun.

---

## 2. Executed Queue

### P1: 6-bit PCM seed123 Source Rerun (LAUNCHED)

| Attribute | Value |
|-----------|-------|
| Command | `r11d4_train_pcm.py --run-id r11d_6bit_pcm_seed123 --seed 123 --epochs 100 --batch-size 64 --lr 0.001 --wd 0.05 --momentum 0.0 --device cuda --workers 0 --save-dir paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123 --inp-res 0.015625 --out-res 0.015625 --modifier-std-dev 0.10 --early-stop-patience 10 --early-stop-min-delta 0.01` |
| Start | 2026-05-09 |
| PID | 114296 |
| Elapsed | ~10 min (epoch 9/100) |
| ETA | ~1.6h |
| Log | `logs/_gpt/p6_6bit_seed123_source_rerun_20260509.log` |
| Backup | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123_P6_BACKUP_20260509/` |

**Kill criterion:** NaN, source_best < 55% or > 85%, OOM, hang > 3h.

**Post-run steps:**
1. Run `eval_aihwkit_fresh.py` (10 instances x 5 MC)
2. Run `eval_aihwkit_drift_extended.py` (0s, 1h, 1d)
3. Copy artifacts to `canonical_json/pcm_6bit_seed123/`
4. Re-run `check_local_pcm_precision_ladder.py`

---

## 3. Skipped Jobs (Justified)

| Priority | Task | Reason Skipped |
|----------|------|----------------|
| P2 | Existing-data fresh/drift re-eval smoke for 4/6/8-bit | Already current; no config change since P5 |
| P3 | Thesis-only proportional HAT fresh eval | No ready script/checkpoint found that is safe and isolated from Paper-1 |
| P4 | Work-2 local unit/smoke tests | KV-cache import passes; full eval deferred to remote |

---

## 4. Safety Log

| Check | Result |
|-------|--------|
| nvidia-smi before launch | 346 MiB / 16GB, 1% util |
| Memory after launch | 5626 MiB / 16GB (34% used) |
| No other GPU jobs | Confirmed |
| Sequential execution | Yes (only 1 job) |
| Early stop configured | Yes (patience=10, min_delta=0.01) |
| Log tee'd | Yes |

---

## 5. Verdict

GPU is running one justified safe job (6-bit seed123 rerun). No other jobs launched because:
- Existing PCM evaluations are already current
- No safe thesis-only script found
- Work-2 KV tests are remote-blocked

**Next GPU action:** Post-run eval (fresh + drift) after seed123 training completes (~1.5h).

---

*Report by kimi. GPU queue executed on 2026-05-09.*
