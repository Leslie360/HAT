#!/bin/bash
# Pipeline health check — run every 30 min via crontab
# Logs status and detects stalls/failures.

LOG=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/pipeline_health.log
STATE=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/.pipeline_state.json
PIPELINE_LOG=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/pipeline_runner.log

echo "[$(date '+%Y-%m-%d %H:%M')] --- Health Check ---" >> "$LOG"

# 1. Is the pipeline runner alive?
RUNNER_PID=$(pgrep -f pipeline_runner.py | head -1)
if [ -z "$RUNNER_PID" ]; then
    echo "  ❌ pipeline_runner.py NOT RUNNING" >> "$LOG"
    # Check if we have a final state (pipeline finished normally)
    if [ -f "$STATE" ]; then
        FINISHED=$(python3 -c "import json; d=json.load(open('$STATE')); print(d.get('finished_at',''))" 2>/dev/null)
        if [ -n "$FINISHED" ]; then
            echo "  ✅ Pipeline finished at $FINISHED" >> "$LOG"
        else
            echo "  ⚠️  Pipeline died without finishing!" >> "$LOG"
            echo "  ⚠️  Check $PIPELINE_LOG for errors" >> "$LOG"
        fi
    else
        echo "  ⚠️  No state file — pipeline may not have started" >> "$LOG"
    fi
else
    echo "  ✅ Runner alive (PID $RUNNER_PID)" >> "$LOG"

    # 2. How many tasks completed?
    if [ -f "$STATE" ]; then
        DONE=$(python3 -c "import json; d=json.load(open('$STATE')); print(len(d.get('completed',[])))" 2>/dev/null)
        PHASE=$(grep "Phase.*:" "$PIPELINE_LOG" 2>/dev/null | tail -1)
        echo "  📊 Tasks done: $DONE/40" >> "$LOG"
        echo "  📊 Phase: $PHASE" >> "$LOG"
    fi

    # 3. Active GPU count
    GPU_COUNT=$(ps aux | grep -E "p3_hat_train|p3_hat_eval" | grep -v grep | wc -l)
    echo "  🎮 Active GPU tasks: $GPU_COUNT" >> "$LOG"

    # 4. Last log lines (for context)
    LAST_LINES=$(tail -3 "$PIPELINE_LOG" 2>/dev/null)
    echo "  📝 Last log:" >> "$LOG"
    echo "     $LAST_LINES" >> "$LOG"

    # 5. Staleness check: if no progress in last 30 min and tasks remain
    RECENT=$(python3 -c "
import json, os
state_file='$STATE'
plog='$PIPELINE_LOG'
if os.path.exists(plog):
    mtime = os.path.getmtime(plog)
    import time
    age = time.time() - mtime
    print(f'{age:.0f}')
else:
    print('0')
" 2>/dev/null)
    if [ -n "$RECENT" ] && [ "$RECENT" -gt 2400 ] 2>/dev/null; then
        echo "  ⚠️  Pipeline log stale ($RECENT seconds since last update)" >> "$LOG"
    fi
fi

echo "" >> "$LOG"
