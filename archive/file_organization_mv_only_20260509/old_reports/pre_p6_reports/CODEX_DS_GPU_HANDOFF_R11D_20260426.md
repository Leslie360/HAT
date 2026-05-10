# CODEX ↔ DS GPU Lane Handoff — R11D Path C
**Date:** 2026-04-26 18:10 CST
**From:** Codex
**To:** DeepSeek / Claude / Gemini / Kimi / Remote
**User rule:** DS task == Codex task. If Codex quota/availability stops, DS continues the same GPU lane, not a competing lane.

## 1. Role Rule
Codex and DS are a single execution lane for Claude's GPU experiments.

- Codex currently executes R11D-1/2/3 locally.
- DS is the explicit fallback / continuation executor.
- DS should not duplicate a running Codex experiment on the same local GPU unless Claude or the user asks for a replicate seed.
- If Codex becomes unavailable, DS should inspect the sessions/logs below and continue from the current state.

## 2. Current Active Experiment
### R11D-1 — AIHWKit 4-bit precision
Status: running.

Active tmux sessions:
```bash
tmux list-sessions | grep codex_r11d
```
Expected sessions:
```text
codex_r11d1_4bit       # training
codex_r11d1_evalwatch  # waits for training, then runs 10×5 fresh eval
codex_r11d23_queue     # waits for R11D-1 evalwatch, then runs R11D-2/3
```

Training log:
```bash
tail -f paper2_aihwkit_baseline/logs/r11d_1_4bit_20260426_174917.log
```

Output dir:
```bash
paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/
```

Latest observed at 18:10 CST:
```text
Epoch 17/100 | Train 9.91% | Test 10.00% | Best 15.01%
```

Interpretation: 4-bit AIHWKit is currently collapsing near random chance. Not final until early stop/fresh eval completes.

## 3. R11D-1 Exact Training Command
Script:
```bash
bash paper2_aihwkit_baseline/run_r11d_1_4bit.sh
```

Core parameters:
```bash
/home/qiaosir/miniconda3/envs/aihwkit/bin/python paper2_aihwkit_baseline/train_aihwkit_baseline.py \
  --run-id r11d_1_4bit \
  --seed 42 \
  --epochs 100 \
  --batch-size 64 \
  --lr 5e-4 \
  --wd 0.05 \
  --workers 0 \
  --device cuda \
  --save-dir paper2_aihwkit_baseline/checkpoints/r11d_1_4bit \
  --log-interval 1 \
  --inp-res 0.0625 \
  --out-res 0.0625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 20
```

Environment:
```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
```

## 4. Auto Fresh Eval
Watcher script:
```bash
bash paper2_aihwkit_baseline/watch_r11d_1_4bit_eval.sh
```

Target output:
```bash
paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json
```

If watcher fails but `best.pt` exists, DS should manually run:
```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
/home/qiaosir/miniconda3/envs/aihwkit/bin/python paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/best.pt \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json
```

## 5. Queued Follow-up Experiments
Sequential queue is already armed:
```bash
bash paper2_aihwkit_baseline/queue_r11d_2_3_after_r11d1.sh
```

Queue behavior:
1. Waits for `codex_r11d1_evalwatch` to finish.
2. Runs R11D-2 sigma0.20, 8-bit, 100 epochs, patience 20.
3. Runs 10×5 fresh eval.
4. If R11D-2 fresh mean >80%, runs conditional R11D-3 sigma0.30.

Queue log:
```bash
tail -f paper2_aihwkit_baseline/logs/r11d_2_3_queue.log
```

## 6. DS Takeover Checklist
If Codex becomes unavailable, DS should:

1. Check sessions:
```bash
tmux list-sessions | grep codex_r11d
```

2. Check current R11D-1 progress:
```bash
tail -80 paper2_aihwkit_baseline/logs/r11d_1_4bit_20260426_174917.log
```

3. If training session ended, verify fresh eval:
```bash
ls -lh paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json
```

4. If fresh eval missing but `best.pt` exists, run the manual eval command from §4.

5. If R11D-2 queue did not start after R11D-1 eval, start:
```bash
tmux new-session -d -s codex_r11d23_queue \
  "cd /home/qiaosir/projects/compute_vit && bash paper2_aihwkit_baseline/queue_r11d_2_3_after_r11d1.sh 2>&1 | tee -a paper2_aihwkit_baseline/logs/r11d_2_3_queue.log"
```

6. After each completed run, append concise result to `report_md/_gpt/AGENT_SYNC_gpt.md`.

## 7. Coordination Notes
- Gemini should not launch duplicate R11D-1 on the same GPU. It should consume the resulting JSON for the operating-envelope plot.
- Kimi should continue theory/cadence text, using R11D outputs as they land.
- Claude should treat Codex/DS as one continuous GPU executor for R11D.
- Remote can run independent replicate/stress variants if physically separate resources are available; label them as remote replicates, not local canonical runs.
