#!/bin/bash
# Robustness Sweep for p28b + p69b on GPUs 4/5/6/7 only
# Usage: nohup bash run_robustness_sweep_4567.sh > robustness_sweep.log 2>&1 &

set -euo pipefail

PYTHON="/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_SCRIPT="/home/lisq753/projects/HAT/HAT/p3_hat_lm_eval.py"
OUTPUT_DIR="/home/lisq753/projects/HAT_kv107/paper2/results/remote107"

# Checkpoints
P28B_CKPT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p28b_fixed500_seed42"
P69B_CKPT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p69b_fixed500_seed42"

# Common args
TASKS="lambada_openai,hellaswag,arc_easy"
MAX_LENGTH=2048
D2D_SEED=3373

# GPU pool: only GPU4 for robustness sweep; 5/6/7 reserved for other experiments
GPUS=(4)

# Logging
LOG_PREFIX="robustness_$(date +%Y%m%d_%H%M%S)"
mkdir -p "${OUTPUT_DIR}/logs"

# ---------------------------------------------------------------------------
# Helper: wait for any GPU to become idle (< 90% util and < 20GB mem used)
# ---------------------------------------------------------------------------
wait_for_gpu() {
    while true; do
        for gpu in "${GPUS[@]}"; do
            local util mem
            util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i "$gpu" | tr -d ' ')
            mem=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i "$gpu" | tr -d ' ')
            if [[ "$util" -lt 10 && "$mem" -lt 20000 ]]; then
                echo "$gpu"
                return
            fi
        done
        echo "[$(date +%H:%M:%S)] All GPUs busy, waiting 60s..." >&2
        sleep 60
    done
}

# ---------------------------------------------------------------------------
# Helper: launch eval on a specific GPU
# Args: gpu checkpoint analog sigma_c2c sigma_d2d n_states d2d_seed suffix extra_log
# ---------------------------------------------------------------------------
LAST_PID=""
launch_eval() {
    local gpu="$1"
    local ckpt="$2"
    local analog="$3"
    local s_c2c="$4"
    local s_d2d="$5"
    local n_st="$6"
    local d2d_s="$7"
    local suffix="$8"

    local analog_flag=""
    if [[ "$analog" == "true" ]]; then
        analog_flag="--analog"
    fi

    local logfile="${OUTPUT_DIR}/logs/${LOG_PREFIX}_${suffix}.log"

    echo "[$(date +%H:%M:%S)] Launching ${suffix} on GPU${gpu}"
    echo "  ckpt=${ckpt} analog=${analog} sigma_c2c=${s_c2c} sigma_d2d=${s_d2d} n_states=${n_st} d2d_seed=${d2d_s}"

    CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$EVAL_SCRIPT" \
        --checkpoint_dir "$ckpt" \
        --tasks "$TASKS" \
        $analog_flag \
        --max_length "$MAX_LENGTH" \
        --sigma_c2c "$s_c2c" \
        --sigma_d2d "$s_d2d" \
        --n_states "$n_st" \
        --d2d-seed "$d2d_s" \
        --output_suffix "$suffix" \
        --device cuda \
        --fp16 \
        --output_dir "$OUTPUT_DIR" \
        > "$logfile" 2>&1 &

    LAST_PID=$!
    echo "  PID=$LAST_PID log=$logfile"
}

# ---------------------------------------------------------------------------
# Track PIDs for synchronization
# ---------------------------------------------------------------------------
declare -a PIDS=()
declare -a NAMES=()

queue_job() {
    local gpu="$1"
    shift
    launch_eval "$gpu" "$@"
    PIDS+=("$LAST_PID")
    NAMES+=("$7")
    # If only one GPU in pool, serialize immediately to avoid piling up on same card
    if [[ ${#GPUS[@]} -eq 1 ]]; then
        wait "$LAST_PID" || true
        PIDS=()
        NAMES=()
    fi
}

wait_for_all() {
    if [[ ${#PIDS[@]} -eq 0 ]]; then
        return
    fi
    echo "[$(date +%H:%M:%S)] Waiting for ${#PIDS[@]} jobs: ${NAMES[*]}"
    for pid in "${PIDS[@]}"; do
        wait "$pid" || true
    done
    PIDS=()
    NAMES=()
    echo "[$(date +%H:%M:%S)] Batch complete."
}

# ---------------------------------------------------------------------------
# Sweep definitions (must match 410M protocol)
# ---------------------------------------------------------------------------

# --- p28b sigma_c2c sweep (eval at different c2c noise, fixed d2d=0.02) ---
echo "========================================"
echo "Starting p28b sigma_c2c sweep"
echo "========================================"
for s_c2c in 0.0 0.01 0.02 0.05 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P28B_CKPT" true "$s_c2c" 0.02 256 "$D2D_SEED" "p28b_c2c_${s_c2c}"
done
wait_for_all

# --- p28b sigma_d2d sweep (eval at different d2d noise, fixed c2c=0.01) ---
echo "========================================"
echo "Starting p28b sigma_d2d sweep"
echo "========================================"
for s_d2d in 0.0 0.02 0.04 0.06 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P28B_CKPT" true 0.01 "$s_d2d" 256 "$D2D_SEED" "p28b_d2d_${s_d2d}"
done
wait_for_all

# --- p28b mismatch sweep ---
echo "========================================"
echo "Starting p28b mismatch sweep"
echo "========================================"
# c2c mismatch: train=0.01, eval higher
for s_c2c in 0.02 0.05 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P28B_CKPT" true "$s_c2c" 0.02 256 "$D2D_SEED" "p28b_mis_c2c_${s_c2c}"
done
# d2d mismatch: train=0.02, eval higher
for s_d2d in 0.04 0.06 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P28B_CKPT" true 0.01 "$s_d2d" 256 "$D2D_SEED" "p28b_mis_d2d_${s_d2d}"
done
wait_for_all

# --- p28b D2D seed cross-instance ---
echo "========================================"
echo "Starting p28b D2D seed sweep"
echo "========================================"
for seed in 3373 3374 3375 3376 3377; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P28B_CKPT" true 0.01 0.02 256 "$seed" "p28b_seed_${seed}"
done
wait_for_all

# --- p28b n_states sweep ---
echo "========================================"
echo "Starting p28b n_states sweep"
echo "========================================"
for n_st in 128 256 512 1024; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P28B_CKPT" true 0.01 0.02 "$n_st" "$D2D_SEED" "p28b_nstates_${n_st}"
done
wait_for_all

# --- p69b sigma_c2c sweep ---
echo "========================================"
echo "Starting p69b sigma_c2c sweep"
echo "========================================"
for s_c2c in 0.0 0.01 0.02 0.05 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P69B_CKPT" true "$s_c2c" 0.02 256 "$D2D_SEED" "p69b_c2c_${s_c2c}"
done
wait_for_all

# --- p69b sigma_d2d sweep ---
echo "========================================"
echo "Starting p69b sigma_d2d sweep"
echo "========================================"
for s_d2d in 0.0 0.02 0.04 0.06 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P69B_CKPT" true 0.01 "$s_d2d" 256 "$D2D_SEED" "p69b_d2d_${s_d2d}"
done
wait_for_all

# --- p69b mismatch sweep ---
echo "========================================"
echo "Starting p69b mismatch sweep"
echo "========================================"
for s_c2c in 0.02 0.05 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P69B_CKPT" true "$s_c2c" 0.02 256 "$D2D_SEED" "p69b_mis_c2c_${s_c2c}"
done
for s_d2d in 0.04 0.06 0.10; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P69B_CKPT" true 0.01 "$s_d2d" 256 "$D2D_SEED" "p69b_mis_d2d_${s_d2d}"
done
wait_for_all

# --- p69b D2D seed cross-instance ---
echo "========================================"
echo "Starting p69b D2D seed sweep"
echo "========================================"
for seed in 3373 3374 3375 3376 3377; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P69B_CKPT" true 0.01 0.02 256 "$seed" "p69b_seed_${seed}"
done
wait_for_all

# --- p69b n_states sweep ---
echo "========================================"
echo "Starting p69b n_states sweep"
echo "========================================"
for n_st in 128 256 512 1024; do
    gpu=$(wait_for_gpu)
    queue_job "$gpu" "$P69B_CKPT" true 0.01 0.02 "$n_st" "$D2D_SEED" "p69b_nstates_${n_st}"
done
wait_for_all

echo "========================================"
echo "ALL ROBUSTNESS SWEEPS COMPLETE"
echo "========================================"
echo "Results in: ${OUTPUT_DIR}"
echo "Logs in:    ${OUTPUT_DIR}/logs"
