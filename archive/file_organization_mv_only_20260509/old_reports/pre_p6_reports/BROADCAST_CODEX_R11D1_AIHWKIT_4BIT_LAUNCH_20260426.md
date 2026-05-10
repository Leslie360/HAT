# BROADCAST — Codex R11D-1 AIHWKit 4-bit Launch
**Date:** 2026-04-26 17:55 CST
**From:** Codex
**To:** Claude / Kimi / Gemini / DeepSeek / Remote
**Authority:** User request: "查看广播，完成Claude的任务" + `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md`

## Summary
Codex read Claude's Round-11D Path C plan and picked up the immediately executable GPU task R11D-1 because no AIHWKit train/eval process was active locally.

R10E fresh eval rerun is complete and consistent with Claude's report:
- `paper2_aihwkit_baseline/checkpoints/fresh_eval.json`
- 10 fresh instances, current local JSON: **87.282 ± 0.1286%**
- Compatible with the earlier rounded Claude headline **87.34 ± 0.14%**.

## Code changes applied for R11D reproducibility
Patched:
- `paper2_aihwkit_baseline/train_aihwkit_baseline.py`
- `paper2_aihwkit_baseline/eval_aihwkit_fresh.py`

New training CLI knobs:
- `--inp-res`
- `--out-res`
- `--modifier-std-dev`
- `--run-id`
- `--early-stop-patience`
- `--early-stop-min-delta`

New eval CLI knobs:
- `--mc-repeats`
- `--fresh-seed-base`
- `--inp-res`
- `--out-res`
- `--modifier-std-dev`

Checkpoint/history now record:
- RPU config spec
- code SHA256
- git commit hash
- CUDA device name
- PyTorch version
- full experiment args

Reason: Claude's R11D plan requires changing 4-bit / sigma / eval sigma repeatedly. Hardcoding `make_rpu_config()` per run is unsafe and not audit-friendly.

## R11D-1 active run
Experiment: **AIHWKit 4-bit precision**

Config:
```bash
--run-id r11d_1_4bit
--seed 42
--epochs 100
--batch-size 64
--lr 5e-4
--wd 0.05
--workers 0
--device cuda
--save-dir paper2_aihwkit_baseline/checkpoints/r11d_1_4bit
--log-interval 1
--inp-res 0.0625
--out-res 0.0625
--modifier-std-dev 0.10
--early-stop-patience 20
```

Active tmux sessions:
- training: `codex_r11d1_4bit`
- post-train fresh eval watcher: `codex_r11d1_evalwatch`

Logs/output:
- train log: `paper2_aihwkit_baseline/logs/r11d_1_4bit_20260426_174917.log`
- checkpoint dir: `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/`
- watcher log: `paper2_aihwkit_baseline/logs/r11d_1_4bit_evalwatch.log`
- final fresh eval target: `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json`

Watcher behavior:
- waits for the training tmux session to end
- if `best.pt` exists, runs `eval_aihwkit_fresh.py --n-fresh 10 --mc-repeats 5`
- eval uses the checkpoint's saved RPU config by default, so the 4-bit config is inherited

## First epoch sanity check
R11D-1 epoch 1:
- Train: **15.76%**
- Test: **15.01%**
- Best: **15.01%**
- epoch time: **68.2 s**

Comparison anchor: R10E 8-bit baseline epoch 1 test was **46.70%**.

Interpretation: this is already a strong severe-precision stress signal, but not a final verdict. Need continue until recovery, early stop, or 100 epochs.

## Coordination
- Codex is not taking Kimi's theory/cadence work.
- Codex is not taking Gemini's plotting/audit work.
- DeepSeek/Remote can use the new CLI knobs to run R11D-2/R11D-3 without editing source:

R11D-2 template:
```bash
/home/qiaosir/miniconda3/envs/aihwkit/bin/python paper2_aihwkit_baseline/train_aihwkit_baseline.py \
  --run-id r11d_2_sigma020 \
  --seed 42 \
  --epochs 100 \
  --batch-size 64 \
  --lr 5e-4 \
  --wd 0.05 \
  --workers 0 \
  --device cuda \
  --save-dir paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020 \
  --log-interval 1 \
  --inp-res 0.00390625 \
  --out-res 0.00390625 \
  --modifier-std-dev 0.20 \
  --early-stop-patience 20
```

Fresh eval template:
```bash
/home/qiaosir/miniconda3/envs/aihwkit/bin/python paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/best.pt \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/fresh_eval.json
```

## Next Codex action
Monitor R11D-1. If it reaches early-stop or epoch 100, report:
- best source accuracy
- full epoch trajectory
- 10×5 fresh eval mean/std
- Path C verdict versus Ensemble HAT 4-bit operating envelope.
