# R11D Fair-Comparison Experiment Suite

**task_id:** r11d_fair_comparison_20260428
**priority:** P0
**estimated_time:** 6-8h (3 training runs × ~2h each + eval)

---

## 1. Background

R11D series currently has results at mixed precisions:
- R11D-1: 4-bit AIHWKit + ADD_NORMAL(0.10) → 14.64%
- R11D-2: 8-bit AIHWKit + ADD_NORMAL(0.20) → 87.52%
- R11D-4: 8-bit PCM lr=5e-4 → 61.10%
- R11D-5a: 8-bit PCM lr=1e-3 → 76.96%

**Problem**: 4-bit vs 8-bit is not a fair comparison. We need experiments at the **same precision** to isolate the effect of device model (PCM vs ADD_NORMAL vs pure ideal).

**Currently running** (wasting GPU, should be killed):
- R11D-5b PCM lr=5e-3 → plateaued at ~67%, epoch 71/100
- R11D-5c PCM lr=1e-3 mom=0.9 → epoch 15/100, no improvement trend

---

## 2. Step-by-Step Instructions

### Step 1: Kill current training runs

```bash
kill 20817 81799 2>/dev/null || true
```

These are R11D-5b and R11D-5c. Both are underperforming R11D-5a (76.96%) and wasting GPU time.

### Step 2: Create run script for R11D-6 (AIHWKit 8-bit Pure Baseline)

File: `paper2_aihwkit_baseline/run_r11d6_pure_baseline.sh`

This is **8-bit ideal analog** (no PCM, no ADD_NORMAL noise modifier). It answers: "what accuracy does pure aihwkit 8-bit get without any device noise?"

```bash
#!/bin/bash
set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_6_pure_baseline"
LOG="paper2_aihwkit_baseline/logs/r11d_6_pure_baseline_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-6: 8-bit Pure Baseline (no modifier) ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/train_aihwkit_baseline.py \
    --run-id r11d_6_pure_baseline \
    --seed 42 \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --workers 0 \
    --device cuda \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --inp-res 0.00390625 \
    --out-res 0.00390625 \
    --modifier-std-dev 0.0 \
    --early-stop-patience 20 \
    2>&1 | tee -a "$LOG"

echo "=== R11D-6 training complete ==="
```

**Key**: `--modifier-std-dev 0.0` disables the ADD_NORMAL weight modifier.

### Step 3: Create run script for R11D-7 (PCM 4-bit lr=1e-3)

File: `paper2_aihwkit_baseline/run_r11d7_pcm_4bit.sh`

This is **4-bit PCM** with the same hyperparameters as R11D-5a. It answers: "is PCM's degradation due to the device model or the 8-bit precision?"

```bash
#!/bin/bash
set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit"
LOG="paper2_aihwkit_baseline/logs/r11d_7_pcm_4bit_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-7: PCM 4-bit lr=1e-3 ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d4_train_pcm.py \
    --run-id r11d_7_pcm_4bit \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --inp-res 0.0625 \
    --out-res 0.0625 \
    2>&1 | tee -a "$LOG"

echo "=== R11D-7 training complete ==="
```

**Key**: `--inp-res 0.0625 --out-res 0.0625` sets 4-bit resolution (1/16).

### Step 4: Create run script for R11D-8 (HAT-inspired PCM 8-bit 100-epoch)

File: `paper2_aihwkit_baseline/run_r11d8_hat_pcm.sh`

This is the **full 100-epoch run** of the fixed HAT-inspired PCM script (v2).

```bash
#!/bin/bash
set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm"
LOG="paper2_aihwkit_baseline/logs/r11d_8_hat_pcm_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-8: HAT-inspired PCM 8-bit full run ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d_hat_pcm.py \
    --run-id r11d_8_hat_inspired_pcm \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --hat-std-dev 5.0 \
    --hat-mode scaled \
    --hat-start-epoch 1 \
    --early-stop-patience 20 \
    2>&1 | tee -a "$LOG"

echo "=== R11D-8 training complete ==="
```

### Step 5: Execute training runs (sequential, same GPU)

Run in this order:

```bash
cd /home/qiaosir/projects/compute_vit
chmod +x paper2_aihwkit_baseline/run_r11d6_pure_baseline.sh
chmod +x paper2_aihwkit_baseline/run_r11d7_pcm_4bit.sh
chmod +x paper2_aihwkit_baseline/run_r11d8_hat_pcm.sh

# Run sequentially (only one GPU)
./paper2_aihwkit_baseline/run_r11d6_pure_baseline.sh
./paper2_aihwkit_baseline/run_r11d7_pcm_4bit.sh
./paper2_aihwkit_baseline/run_r11d8_hat_pcm.sh
```

**NOTE**: Do NOT run in parallel. There is only one GPU and R11D-5b/5c just occupied it for hours.

### Step 6: Fresh-instance evaluation for all new runs

After each training completes, run fresh eval:

```bash
# R11D-6 fresh eval
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_6_pure_baseline/best.pt \
    --n-fresh 10 --batch-size 64 --device cuda \
    --output paper2_aihwkit_baseline/checkpoints/r11d_6_pure_baseline/fresh_eval.json

# R11D-7 fresh eval
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit/best.pt \
    --n-fresh 10 --batch-size 64 --device cuda \
    --output paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit/fresh_eval.json

# R11D-8 fresh eval
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm/best.pt \
    --n-fresh 10 --batch-size 64 --device cuda \
    --output paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm/fresh_eval.json
```

### Step 7: Drift evaluation for all new runs

```bash
# R11D-6 drift eval
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_drift.py \
    --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_6_pure_baseline/best.pt \
    --batch-size 64 --device cuda \
    --output paper2_aihwkit_baseline/checkpoints/r11d_6_pure_baseline/drift_eval.json

# R11D-7 drift eval
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_drift.py \
    --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit/best.pt \
    --batch-size 64 --device cuda \
    --output paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit/drift_eval.json

# R11D-8 drift eval
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_drift.py \
    --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm/best.pt \
    --batch-size 64 --device cuda \
    --output paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm/drift_eval.json
```

### Step 8: Results summary

After all experiments complete, write a summary report to:
`report_md/_gpt/R11D_FAIR_COMPARISON_RESULTS_20260428.md`

Include this table:

| Run | Precision | Device Model | lr | Best Acc | Fresh Eval | Drift (0s→1h→24h) |
|-----|-----------|--------------|-----|----------|------------|-------------------|
| R11D-1 | 4-bit | AIHWKit + ADD_NORMAL(0.10) | 5e-4 | 14.64% | — | — |
| R11D-2 | 8-bit | AIHWKit + ADD_NORMAL(0.20) | 5e-4 | 87.52% | — | — |
| R11D-5a | 8-bit | PCM | 1e-3 | 76.96% | 76.74±0.09% | 76.70→76.72→76.73% |
| R11D-6 | 8-bit | AIHWKit (pure, no modifier) | 1e-3 | TBD | TBD | TBD |
| R11D-7 | 4-bit | PCM | 1e-3 | TBD | TBD | TBD |
| R11D-8 | 8-bit | HAT-inspired PCM | 1e-3 | TBD | TBD | TBD |

**Key questions to answer in the report**:
1. How much of PCM's degradation (vs R11D-2's 87.52%) is due to the PCM device model vs hyperparameter mismatch? (Compare R11D-6 vs R11D-5a)
2. Is PCM's poor 4-bit result (R11D-1: 14.64%) due to 4-bit itself or the ADD_NORMAL baseline? (Compare R11D-7 vs R11D-1)
3. Does HAT-inspired training improve PCM robustness? (Compare R11D-8 vs R11D-5a)

---

## 3. Expected outcomes

- R11D-6 should reveal the "ceiling" of aihwkit 8-bit without noise modifiers. If it's ~85%+, then PCM's 76.96% is genuinely a device-model penalty of ~10pp.
- R11D-7 should show whether PCM at 4-bit is completely unusable or just needs better hyperparameters.
- R11D-8 should show whether per-epoch D2D resampling (HAT idea) helps PCM robustness.

## 4. Error handling

- If `train_aihwkit_baseline.py` crashes with `--modifier-std-dev 0.0`, try `0.0001` instead (some aihwkit versions reject exactly 0).
- If any run OOMs, reduce batch-size to 32.
- If HAT-inspired script crashes, check `r11d_hat_pcm.py` has the v2 fixes applied (per-layer scalar D2D, default std_dev=5.0).
