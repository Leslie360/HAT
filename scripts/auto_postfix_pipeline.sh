#!/bin/bash
# Autonomous pipeline: monitors training completion and auto-launches fresh eval
# Runs until all postfix experiments are evaluated

LOG="logs/_gpt/auto_pipeline.log"
echo "[$(date)] Auto pipeline started" >> "$LOG"

# Config: which experiments to auto-eval after training
declare -A CHECKPOINTS
CHECKPOINTS["proportional"]="checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_best.pt"
CHECKPOINTS["standard"]="checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_best.pt"

declare -A EVAL_CMDS
EVAL_CMDS["proportional"]="/home/qiaosir/miniconda3/envs/LLM/bin/python eval_fresh_instances_postfix.py --checkpoint checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_best.pt --exp-id V4 --model-type tinyvit --nl-ltp 2.0 --nl-ltd -2.0 --noise-mode proportional --num-instances 10 --mc-runs 5"
EVAL_CMDS["standard"]="/home/qiaosir/miniconda3/envs/LLM/bin/python eval_fresh_instances_postfix.py --checkpoint checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_best.pt --exp-id V3 --model-type tinyvit --nl-ltp 2.0 --nl-ltd -2.0 --num-instances 10 --mc-runs 5"

declare -A EVAL_LOGS
EVAL_LOGS["proportional"]="logs/_gpt/postfix_proportional_hat_fresh_eval.log"
EVAL_LOGS["standard"]="logs/_gpt/postfix_standard_hat_fresh_eval.log"

declare -A EVAL_JSONS
EVAL_JSONS["proportional"]="report_md/_gpt/json_gpt/postfix_proportional_hat_fresh_eval.json"
EVAL_JSONS["standard"]="report_md/_gpt/json_gpt/postfix_standard_hat_fresh_eval.json"

# Track which ones are done
declare -A DONE
DONE["proportional"]=0
DONE["standard"]=0
DONE["v1"]=0

poll_training() {
    local name=$1
    local last_pt=$2
    if [ ! -f "$last_pt" ]; then
        echo "no_ckpt"
        return
    fi
    local mtime=$(stat -c %Y "$last_pt")
    local now=$(date +%s)
    local age=$((now - mtime))
    echo "$age"
}

while true; do
    # Check if training processes are still alive
    PROP_PID=$(pgrep -f "postfix_proportional.*train" | head -1)
    STD_PID=$(pgrep -f "postfix_standard_hat.*train" | head -1)
    V1_PID=$(pgrep -f "postfix_v1_baseline.*train" | head -1)

    # Proportional HAT
    if [ "$DONE[proportional]" = "0" ]; then
        PROP_AGE=$(poll_training "proportional" "checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_last.pt")
        if [ -z "$PROP_PID" ] || [ "$PROP_AGE" -gt 300 ]; then
            echo "[$(date)] Proportional HAT training appears complete (PID=$PROP_PID, age=${PROP_AGE}s)" >> "$LOG"
            if [ ! -f "${EVAL_JSONS[proportional]}" ]; then
                echo "[$(date)] Launching Proportional HAT fresh eval..." >> "$LOG"
                ${EVAL_CMDS[proportional]} > "${EVAL_LOGS[proportional]}" 2>&1
                echo "[$(date)] Proportional HAT fresh eval DONE" >> "$LOG"
            else
                echo "[$(date)] Proportional HAT eval already exists" >> "$LOG"
            fi
            DONE["proportional"]=1
        fi
    fi

    # Standard HAT
    if [ "$DONE[standard]" = "0" ]; then
        STD_AGE=$(poll_training "standard" "checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_last.pt")
        if [ -z "$STD_PID" ] || [ "$STD_AGE" -gt 300 ]; then
            echo "[$(date)] Standard HAT training appears complete (PID=$STD_PID, age=${STD_AGE}s)" >> "$LOG"
            if [ ! -f "${EVAL_JSONS[standard]}" ]; then
                echo "[$(date)] Launching Standard HAT fresh eval..." >> "$LOG"
                ${EVAL_CMDS[standard]} > "${EVAL_LOGS[standard]}" 2>&1
                echo "[$(date)] Standard HAT fresh eval DONE" >> "$LOG"
            else
                echo "[$(date)] Standard HAT eval already exists" >> "$LOG"
            fi
            DONE["standard"]=1
        fi
    fi

    # V1 Baseline (no fresh eval needed, just monitor completion)
    if [ "$DONE[v1]" = "0" ]; then
        V1_AGE=$(poll_training "v1" "checkpoints/_gpt/postfix_v1_baseline/V1_fp32_digital_baseline_last.pt")
        if [ -z "$V1_PID" ] || [ "$V1_AGE" -gt 300 ]; then
            echo "[$(date)] V1 Baseline training complete (PID=$V1_PID, age=${V1_AGE}s)" >> "$LOG"
            DONE["v1"]=1
        fi
    fi

    # Exit if all done
    if [ "${DONE[proportional]}" = "1" ] && [ "${DONE[standard]}" = "1" ] && [ "${DONE[v1]}" = "1" ]; then
        echo "[$(date)] ALL TASKS COMPLETE. Exiting." >> "$LOG"
        break
    fi

    sleep 60
done
