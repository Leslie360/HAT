#!/bin/bash
# Wait for 6-bit seed123 pilot evals, decide whether to queue seed456/789.

set -euo pipefail
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd "$PROJECT"
RUN="r11d_6bit_pcm_seed123"
DIR="paper2_aihwkit_baseline/checkpoints/${RUN}"
LOG="paper2_aihwkit_baseline/logs/watch_6bit_pilot_and_queue_$(date +%Y%m%d_%H%M%S).log"
DECISION="${DIR}/pilot_decision.json"
mkdir -p paper2_aihwkit_baseline/logs "$DIR"

echo "[watch] waiting for ${RUN} fresh_eval.json and drift_eval.json" | tee -a "$LOG"
while true; do
  if [[ -f "${DIR}/fresh_eval.json" && -f "${DIR}/drift_eval.json" && -f "${DIR}/training_history.json" ]]; then
    break
  fi
  if ! pgrep -f "r11d4_train_pcm.py .*--run-id ${RUN}" >/dev/null && [[ -f "${DIR}/best.pt" ]]; then
    echo "[watch] training process absent but eval files not complete yet; waiting for wrapper/eval" | tee -a "$LOG"
  fi
  sleep 60
done

"$PYTHON" - <<'PY' > "$DECISION"
import json
from pathlib import Path
run = Path('paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123')
h = json.loads((run/'training_history.json').read_text())
f = json.loads((run/'fresh_eval.json').read_text())
d = json.loads((run/'drift_eval.json').read_text())
best = float(h['best_acc'])
fresh = float(f['mean'])
res = {r['t_label']: float(r['accuracy']) for r in d['results']}
d0 = res.get('0s (no drift)')
d1d = res.get('1d')
drop = None if d0 is None or d1d is None else d0 - d1d
# Locked references from local 3-seed summaries.
fresh_8bit = 77.5955
fresh_threshold = fresh_8bit - 0.5
# Continue only if it is near 8-bit fresh or is a useful drift-Pareto bridge.
continue_multiseed = (fresh >= fresh_threshold) or (fresh >= 76.0 and drop is not None and 0.3 <= drop <= 3.7)
out = {
    'run_id': 'r11d_6bit_pcm_seed123',
    'best_test': best,
    'fresh_mean': fresh,
    'drift_0s': d0,
    'drift_1d': d1d,
    'drift_drop_0s_to_1d': drop,
    'fresh_threshold_within_0p5pp_of_8bit': fresh_threshold,
    'continue_multiseed': continue_multiseed,
    'criteria': 'continue if fresh >= 77.0955 OR fresh >= 76.0 and 0.3 <= drift_drop <= 3.7',
}
print(json.dumps(out, indent=2))
PY

cat "$DECISION" | tee -a "$LOG"
DECISION_VALUE=$("$PYTHON" - <<'PY'
import json
from pathlib import Path
print('yes' if json.loads(Path('paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/pilot_decision.json').read_text())['continue_multiseed'] else 'no')
PY
)
if [[ "$DECISION_VALUE" == "yes" ]]; then
  echo "[watch] pilot passed; launching seed456/789 follow-up" | tee -a "$LOG"
  nohup bash paper2_aihwkit_baseline/run_kimi_r11d_6bit_multiseed_20260430.sh > paper2_aihwkit_baseline/logs/6bit_multiseed_master_$(date +%Y%m%d_%H%M%S).log 2>&1 &
  echo "[watch] launched PID=$!" | tee -a "$LOG"
else
  echo "[watch] pilot did not pass follow-up criteria; leaving GPU free for next queue" | tee -a "$LOG"
fi
