# GPU 榨干调度计划 — 2026-04-28

**Status:** ACTIVE — R11D-6b + R11D-7 running
**Goal:** Zero GPU idle time between training jobs
**Last updated:** 02:08

---

## Current Situation

| Run | Epoch | Best Test | ETA | Note |
|:-----|:------|:----------|:----|:-----|
| R11D-6b | 20/100 | 81.93% | ~2.1h | early-stop patience=20; may finish earlier if plateau |
| R11D-7 | 23/100 | 49.92% | ~1.9h | Still climbing, likely runs full 100 |

**Critical observation:** R11D-6b best stuck at 81.93% since epoch 18. If no improvement for 20 epochs, early stop triggers at ~epoch 38 → **finishes ~02:35** (much earlier than 100-epoch ETA).

---

## Timeline (Best-Case: R11D-6b Early-Stops)

```
02:08  NOW        [R11D-6b] ████████████░░░░░░░░░░░░░░░░░░░░  epoch 20/100 (may stop at 38)
       NOW        [R11D-7]  ██████████████░░░░░░░░░░░░░░░░░░  epoch 23/100

02:35  EST        [R11D-6b] ██████████████████████████████████  DONE (early stop @ epoch 38)
02:35-02:50      [GPU]     R11D-6b fresh eval (10min) + drift eval (5min)

02:50-04:15      [R11D-7]  ██████████████████████████████████  Continue training (alone on GPU)

04:15  EST        [R11D-7]  ██████████████████████████████████  DONE
04:15-04:30      [GPU]     R11D-7 fresh eval + drift eval

04:30-06:30      [R11D-8]  ██████████████████████████████████  HAT-inspired PCM 100-epoch train

06:30-06:45      [GPU]     R11D-8 fresh eval + drift eval

06:45-07:30      [R11D-8-SWA] ██████████████████████████████  SWA continuation (25 epochs from best.pt)

07:30-07:45      [GPU]     R11D-8-SWA eval

07:45  DONE       All core experiments + SWA ablation complete
```

## Timeline (Worst-Case: Both Run Full 100 Epochs)

```
02:08  NOW        Both running in parallel
~04:10 EST        Both finish ~simultaneously
04:10-04:40      Serial eval: R11D-7 (15min) → R11D-6b (15min)
04:40-06:40      R11D-8 train
06:40-06:55      R11D-8 eval
06:55-07:40      R11D-8-SWA train
07:40-07:55      R11D-8-SWA eval
```

---

## Task Queue (Priority Order)

### P0 — Must Complete (blocks paper narrative)

| # | Task | GPU Time | Dependencies |
|:--|:-----|:---------|:-------------|
| 0 | ~~R11D-6b train~~ | ~~2.1h~~ | ~~Running~~ |
| 0 | ~~R11D-7 train~~ | ~~1.9h~~ | ~~Running~~ |
| 1 | R11D-6b fresh eval | 10min | R11D-6b done |
| 2 | R11D-6b drift eval | 5min | #1 done |
| 3 | R11D-7 fresh eval | 10min | R11D-7 done |
| 4 | R11D-7 drift eval | 5min | #3 done |
| 5 | R11D-8 train (HAT-inspired PCM) | 2.0h | #0 done |
| 6 | R11D-8 fresh eval | 10min | #5 done |
| 7 | R11D-8 drift eval | 5min | #6 done |

### P1 — High ROI (almost free)

| # | Task | GPU Time | Dependencies | Expected Gain |
|:--|:-----|:---------|:-------------|:--------------|
| 8 | R11D-8-SWA continuation | 0.5h | #5 done | 0.5-1.5pp |
| 9 | R11D-8-SWA eval | 15min | #8 done | — |
| 10 | R11D-8-Dropout ablation | 2.0h | #9 done | 0.5-1pp |

### P2 — Algorithm Innovation (if P0+P1 complete and GPU still available)

| # | Task | GPU Time | Dependencies |
|:--|:-----|:---------|:-------------|
| 11 | SAM for Analog (Analog-SAM) | 2.0h | P1 done |
| 12 | Distillation (Noisy Teacher) | 2.0h | P1 done |

### P3 — CPU-Only Tasks (run during GPU training gaps)

| # | Task | When |
|:--|:-----|:-----|
| A | Write R11D-6b/7/8 results summary | After each eval |
| B | Prepare SAM experiment script | During R11D-8 training |
| C | Prepare Distillation script | During R11D-8 training |
| D | Update manuscript tables | As results arrive |

---

## Automation Plan

To ensure zero idle time, use a polling watcher script that:

1. Detects when `best.pt` appears in checkpoint dir
2. Auto-launches fresh eval → drift eval → next training job
3. Logs all transitions to `broadcast.md`

**Command to monitor:**
```bash
# Run this in a background tmux pane
while true; do
  if [ -f checkpoints/r11d_6b_pure_baseline/best.pt ] && [ ! -f checkpoints/r11d_6b_pure_baseline/.eval_done ]; then
    # launch eval scripts
    touch checkpoints/r11d_6b_pure_baseline/.eval_done
  fi
  sleep 60
done
```

---

## Contingency: If R11D-6b Diverges Again

| Scenario | Action |
|:---------|:-------|
| 6b test acc < 70% at epoch 30 | Kill immediately; retry with lr=5e-4 |
| 6b test acc 70-80% at epoch 30 | Let it run; may be aihwkit 8-bit ceiling |
| 6b test acc > 85% at epoch 50 | Excellent; PCM penalty is real and large |

---

## Sign-off

Approved by user: "重新安排gpu任务优先级，尽量榨干资源"
Executor: Claude
Next checkpoint: When R11D-6b or R11D-7 completes
