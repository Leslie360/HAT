#!/usr/bin/env bash
# GPU process monitor: waits for run_tinyvit_groupwise_nl_comp to finish,
# then auto-launches the learnable gamma compensation experiment (E3).
# Background this script and it will poll every 60 seconds.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_DIR/logs/learnable_gamma_gpt"
MONITOR_LOG="$LOG_DIR/monitor_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$LOG_DIR"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$MONITOR_LOG"
}

log "Monitor started. Watching for 'run_tinyvit_groupwise_nl_comp' processes."
log "Once all such processes exit, E3 (learnable gamma_comp) will auto-launch."

# Poll every 60 seconds
while true; do
    # Check WSL side for the target process
    COUNT=$("/mnt/c/Windows/System32/wsl.exe" -d Ubuntu-22.04 bash -lc \
        'ps aux | grep run_tinyvit_groupwise_nl_comp | grep -v grep | wc -l' 2>/dev/null || echo "1")

    # Trim whitespace/newlines
    COUNT=$(echo "$COUNT" | tr -d '[:space:]')

    if [ -z "$COUNT" ]; then
        COUNT=0
    fi

    log "Active run_tinyvit_groupwise_nl_comp processes: $COUNT"

    if [ "$COUNT" -eq 0 ]; then
        log "All target processes have exited. Launching E3 experiment NOW."

        # Launch E3 via host WSL
        "/mnt/c/Windows/System32/wsl.exe" -d Ubuntu-22.04 bash -lc \
            "cd $REPO_DIR && \
             source /home/qiaosir/miniconda3/etc/profile.d/conda.sh && \
             conda activate LLM && \
             /home/qiaosir/miniconda3/envs/LLM/bin/python \
                $REPO_DIR/scripts/_gpt/run_learnable_gamma_compensation_gpt.py \
                --gamma_phys 2.0 \
                --epochs 100 \
                --batch_size 128 \
                --seed 42 \
                --log_interval 10 \
                --dataset cifar10 \
                --num_workers 2 \
                2>&1 | tee $LOG_DIR/e3_main_run_$(date +%Y%m%d_%H%M%S).log" &

        E3_PID=$!
        log "E3 launched with background PID=$E3_PID"
        log "Monitor exiting. Good luck with the experiment!"
        exit 0
    fi

    sleep 60
done
