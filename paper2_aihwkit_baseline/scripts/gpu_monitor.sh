#!/bin/bash
# GPU Training Monitor — Auto-kill on crash/divergence/stall
# Runs continuously, checks every 60 seconds

LOG="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/logs/gpu_monitor_$(date +%Y%m%d).log"
CKPT_BASE="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/checkpoints"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Monitor started" >> "$LOG"

# Kill criteria thresholds
MIN_ACC_EPOCH_10=30   # If test acc < 30% at epoch 10, kill (catastrophic failure)
NAN_DETECTED=1        # If NaN in log, kill immediately
STALL_MINUTES=10      # If no log update for 10 min, kill

monitor_process() {
    local pid="$1"
    local name="$2"
    local log_file="$3"
    local ckpt_dir="$4"

    # Check if process alive
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $name PID=$pid DEAD" >> "$LOG"
        return 1
    fi

    # Check for NaN / Divergence / FATAL in log
    if [[ -f "$log_file" ]]; then
        local last_lines=$(tail -20 "$log_file" 2>/dev/null)
        if echo "$last_lines" | grep -qi "NaN\|Divergence\|FATAL\|traceback\|killed"; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] $name CRITICAL: NaN/Divergence/FATAL detected. Killing PID=$pid" >> "$LOG"
            kill -9 "$pid" 2>/dev/null
            return 1
        fi

        # Check epoch and accuracy for early kill
        local latest_epoch_line=$(echo "$last_lines" | grep "Epoch " | tail -1)
        if [[ -n "$latest_epoch_line" ]]; then
            local epoch=$(echo "$latest_epoch_line" | grep -oP 'Epoch\s+\K[0-9]+')
            local test_acc=$(echo "$latest_epoch_line" | grep -oP 'Test\s+\K[0-9.]+')

            if [[ -n "$epoch" && -n "$test_acc" ]]; then
                # Kill if epoch >= 10 and test_acc < threshold
                if [[ "$epoch" -ge 10 && "$(echo "$test_acc < $MIN_ACC_EPOCH_10" | bc -l)" -eq 1 ]]; then
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $name KILL: epoch=$epoch test=$test_acc% < ${MIN_ACC_EPOCH_10}% threshold. Killing PID=$pid" >> "$LOG"
                    kill -9 "$pid" 2>/dev/null
                    return 1
                fi
            fi
        fi

        # Check stall: no log update for STALL_MINUTES
        local log_mtime=$(stat -c %Y "$log_file" 2>/dev/null)
        local now=$(date +%s)
        local stall_sec=$((now - log_mtime))
        if [[ "$stall_sec" -gt "$((STALL_MINUTES * 60))" ]]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] $name STALL: no log update for ${stall_sec}s. Killing PID=$pid" >> "$LOG"
            kill -9 "$pid" 2>/dev/null
            return 1
        fi
    fi

    return 0
}

while true; do
    # Detect running training processes dynamically
    # R11D-7 seed=456
    seed456_pid=$(pgrep -f "r11d_7_pcm_4bit_seed456" | head -1)
    if [[ -n "$seed456_pid" ]]; then
        monitor_process "$seed456_pid" "R11D-7-seed456" \
            "/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/logs/r11d_7_pcm_4bit_seed456_*.log" \
            "$CKPT_BASE/r11d_7_pcm_4bit_seed456"
    fi

    # T1-3 PresetDevice
    t13_pid=$(pgrep -f "r11d_5a_pcm_PCMPresetDevice_seed42" | head -1)
    if [[ -n "$t13_pid" ]]; then
        monitor_process "$t13_pid" "T1-3-PresetDevice" \
            "/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/logs/t13_preset_comparison_master_*.log" \
            "$CKPT_BASE/r11d_5a_pcm_PCMPresetDevice_seed42"
    fi

    # R11D-5a seeds (when they start)
    for seed in 123 456; do
        pid=$(pgrep -f "r11d_5a_pcm_seed${seed}" | head -1)
        if [[ -n "$pid" ]]; then
            monitor_process "$pid" "R11D-5a-seed${seed}" \
                "/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/logs/r11d_5a_pcm_seed${seed}_*.log" \
                "$CKPT_BASE/r11d_5a_pcm_seed${seed}"
        fi
    done

    sleep 60
done
