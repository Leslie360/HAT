#!/bin/bash
set -euo pipefail

PY="/home/lisq753/miniconda3/envs/LLM/bin/python"
SCRIPT="/home/lisq753/projects/HAT/HAT/p3_hat_lm_eval.py"
OUT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"
GPU=4
LOG="robustness_gpu4_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT/logs"

WAIT_PID=4163444
if kill -0 "$WAIT_PID" 2>/dev/null; then
    echo "[$(date +%H:%M:%S)] Waiting for existing job PID=$WAIT_PID on GPU${GPU}..."
    while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 60; done
    echo "[$(date +%H:%M:%S)] Existing job finished. Starting batch."
fi

eval_job() {
    local ckpt="$1" analog="$2" s_c2c="$3" s_d2d="$4" n_st="$5" d2d_s="$6" suffix="$7"
    local analog_flag=""
    [[ "$analog" == "true" ]] && analog_flag="--analog"
    local logfile="$OUT/logs/${LOG}_${suffix}.log"
    echo "[$(date +%H:%M:%S)] Launching $suffix"
    CUDA_VISIBLE_DEVICES="$GPU" "$PY" "$SCRIPT" \
        --checkpoint_dir "$ckpt" --tasks lambada_openai,hellaswag,arc_easy \
        $analog_flag --max_length 2048 --sigma_c2c "$s_c2c" --sigma_d2d "$s_d2d" \
        --n_states "$n_st" --d2d-seed "$d2d_s" --output_suffix "$suffix" \
        --device cuda --fp16 --output_dir "$OUT" > "$logfile" 2>&1
    echo "[$(date +%H:%M:%S)] Completed $suffix"
}

for s_d2d in 0.06 0.10; do eval_job "$CKPT/p28b_fixed500_seed42" true 0.01 "$s_d2d" 256 3373 "p28b_d2d_${s_d2d}"; done
for s_c2c in 0.02 0.05 0.10; do eval_job "$CKPT/p28b_fixed500_seed42" true "$s_c2c" 0.02 256 3373 "p28b_mis_c2c_${s_c2c}"; done
for s_d2d in 0.04 0.06 0.10; do eval_job "$CKPT/p28b_fixed500_seed42" true 0.01 "$s_d2d" 256 3373 "p28b_mis_d2d_${s_d2d}"; done
for n_st in 128 256; do eval_job "$CKPT/p28b_fixed500_seed42" true 0.01 0.02 "$n_st" 3373 "p28b_nstates_${n_st}"; done

echo "[$(date +%H:%M:%S)] GPU4 batch complete."
