#!/bin/bash
# Monitor the 4 robustness queue scripts; alert if any die
LOG="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/monitor_queues.log"
GPU4_PID=837609
GPU5_PID=812523
GPU6_PID=838926
GPU7_PID=814451

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Monitor started. Tracking PIDs: GPU4=$GPU4_PID GPU5=$GPU5_PID GPU6=$GPU6_PID GPU7=$GPU7_PID" >> "$LOG"

while true; do
    for gpu in 4 5 6 7; do
        pid_var="GPU${gpu}_PID"
        pid="${!pid_var}"
        if ! kill -0 "$pid" 2>/dev/null; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: GPU${gpu} queue script (PID=$pid) has died!" >> "$LOG"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ACTION: Run recover_gpu${gpu}.sh to resume." >> "$LOG"
        fi
    done
    sleep 300
done
