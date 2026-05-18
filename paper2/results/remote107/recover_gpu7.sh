#!/bin/bash
# Recovery script for GPU7 — idempotent, resilient to single-job failures
set -uo pipefail

PY="/home/lisq753/miniconda3/envs/LLM/bin/python"
SCRIPT="/home/lisq753/projects/HAT/HAT/p3_hat_lm_eval.py"
OUT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"
GPU=7
LOG="robustness_gpu7_recovery_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT/logs"

run_if_missing() {
    local ckpt="$1" analog="$2" s_c2c="$3" s_d2d="$4" n_st="$5" d2d_s="$6" suffix="$7"
    local ckpt_name=$(basename "$ckpt")
    local analog_flag=""
    local fn_suffix="analog"
    [[ "$analog" == "true" ]] && analog_flag="--analog"
    [[ "$analog" == "true" ]] || fn_suffix="clean"
    local out_json="$OUT/lm_eval_${ckpt_name}_${fn_suffix}_${suffix}_standard3.json"
    if [[ -s "$out_json" ]]; then
        echo "[SKIP] $suffix — already exists: $out_json"
        return 0
    fi
    local logfile="$OUT/logs/${LOG}_${suffix}.log"
    echo "[$(date +%H:%M:%S)] Launching $suffix"
    CUDA_VISIBLE_DEVICES="$GPU" "$PY" "$SCRIPT" \
        --checkpoint_dir "$ckpt" --tasks lambada_openai,hellaswag,arc_easy \
        $analog_flag --max_length 2048 --sigma_c2c "$s_c2c" --sigma_d2d "$s_d2d" \
        --n_states "$n_st" --d2d-seed "$d2d_s" --output_suffix "$suffix" \
        --device cuda --fp16 --output_dir "$OUT" > "$logfile" 2>&1 || {
            echo "[$(date +%H:%M:%S)] WARNING: $suffix failed — logged to $logfile"
        }
    echo "[$(date +%H:%M:%S)] Completed $suffix"
}

for s_c2c in 0.05 0.10; do run_if_missing "$CKPT/p69b_fixed500_seed42" true "$s_c2c" 0.02 256 3373 "p69b_mis_c2c_${s_c2c}"; done
for s_d2d in 0.04 0.06 0.10; do run_if_missing "$CKPT/p69b_fixed500_seed42" true 0.01 "$s_d2d" 256 3373 "p69b_mis_d2d_${s_d2d}"; done
for seed in 3373 3374 3375 3376 3377; do run_if_missing "$CKPT/p69b_fixed500_seed42" true 0.01 0.02 256 "$seed" "p69b_seed_${seed}"; done
run_if_missing "$CKPT/p69b_fixed500_seed42" true 0.01 0.02 1024 3373 "p69b_nstates_1024"

echo "[$(date +%H:%M:%S)] GPU7 recovery batch complete."
