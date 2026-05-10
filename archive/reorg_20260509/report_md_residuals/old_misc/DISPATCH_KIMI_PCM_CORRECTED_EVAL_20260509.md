# DISPATCH — Kimi PCM Corrected Eval-Only Emergency Queue

Date: 2026-05-09
Owner: Kimi
Coordinator: Codex
Reviewers: DS + Mimo
Broadcast source: `/home/qiaosir/projects/BROADCAST.md`

## 0. Why This Task Exists

DS has identified a systemic fresh-eval bug for the PCM precision ladder:

- `eval_aihwkit_fresh.py` intended to set `modifier_enable_during_test=True`.
- Before the May 7 fix, `load_state_dict` could silently restore training-time tile state and set `modifier_enable_during_test=False`.
- Therefore old PCM fresh numbers for 4/6/8-bit may have been measured with ADD_NORMAL noise effectively OFF.

This invalidates the current Paper-1 PCM precision ladder until corrected eval-only results are available.

**Do not retrain for this task.** Use existing checkpoints and corrected `eval_aihwkit_fresh.py` only.

## 1. Hard Rules

1. Do not touch Paper-1 figures, LaTeX, or PDFs.
2. Do not run 5-bit seed456/789. 5-bit is currently killed pending DS override.
3. Do not rewrite manuscript claims until corrected 4/6/8-bit eval is complete.
4. Every fresh eval JSON must show:
   - `rpu_config_spec.modifier_enable_during_test=true`
   - `tile_audit_all_enabled=true`
   - all tile audit entries have `modifier_enable_during_test=true`
5. If any eval JSON fails tile audit, stop immediately and report.

## 2. Primary Queue: Corrected Fresh Eval For Existing PCM Checkpoints

Run corrected fresh eval on these checkpoints.

### 4-bit PCM UnitCell

| Run | Checkpoint |
|---|---|
| pcm4_seed123 | `paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/best.pt` |
| pcm4_seed456 | `paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/best.pt` |
| pcm4_seed789 | `paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/best.pt` |

Use `inp_res=0.0625`, `out_res=0.0625`.

### 6-bit PCM UnitCell

| Run | Checkpoint |
|---|---|
| pcm6_seed123 | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/best.pt` |
| pcm6_seed456 | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/best.pt` |
| pcm6_seed789 | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/best.pt` |

Use `inp_res=0.015625`, `out_res=0.015625`.

Optional diagnostic only, not paper canonical unless Codex approves:

| Run | Checkpoint |
|---|---|
| pcm6_seed457_diag | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/best.pt` |

### 8-bit PCM UnitCell

| Run | Checkpoint |
|---|---|
| pcm8_seed123 | `paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/best.pt` |
| pcm8_seed456 | `paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/best.pt` |
| pcm8_seed789 | `paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/best.pt` |

Use `inp_res=0.00390625`, `out_res=0.00390625`.

## 3. Command Template

Run from project root:

```bash
cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PY=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
```

For each row:

```bash
RUN=<run_name>
CKPT=<checkpoint_path>
INP=<inp_res>
OUTRES=<out_res>
OUTDIR=paper2_aihwkit_baseline/checkpoints/${RUN}_corrected_eval_20260509
mkdir -p "$OUTDIR" paper2_aihwkit_baseline/logs

$PY paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint "$CKPT" \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output "$OUTDIR/fresh_eval_corrected.json" \
  --inp-res "$INP" \
  --out-res "$OUTRES" \
  --modifier-std-dev 0.10 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_fresh_corrected_20260509.log
```

## 4. Suggested Bash Driver

Kimi may write a temporary script, but the final report must include exact commands. A safe loop is:

```bash
run_eval() {
  local RUN=$1
  local CKPT=$2
  local RES=$3
  local OUTDIR=paper2_aihwkit_baseline/checkpoints/${RUN}_corrected_eval_20260509
  mkdir -p "$OUTDIR" paper2_aihwkit_baseline/logs
  $PY paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "$CKPT" \
    --n-fresh 10 \
    --mc-repeats 5 \
    --workers 0 \
    --device cuda \
    --output "$OUTDIR/fresh_eval_corrected.json" \
    --inp-res "$RES" \
    --out-res "$RES" \
    --modifier-std-dev 0.10 \
    2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_fresh_corrected_20260509.log
}

run_eval pcm4_seed123 paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/best.pt 0.0625
run_eval pcm4_seed456 paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/best.pt 0.0625
run_eval pcm4_seed789 paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/best.pt 0.0625
run_eval pcm6_seed123 paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/best.pt 0.015625
run_eval pcm6_seed456 paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/best.pt 0.015625
run_eval pcm6_seed789 paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/best.pt 0.015625
run_eval pcm8_seed123 paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/best.pt 0.00390625
run_eval pcm8_seed456 paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/best.pt 0.00390625
run_eval pcm8_seed789 paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/best.pt 0.00390625
```

Only after these nine finish, optionally run:

```bash
run_eval pcm6_seed457_diag paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/best.pt 0.015625
```

## 5. Required Report

Write:

`compute_vit/report_md/_gpt/KIMI_PCM_CORRECTED_EVAL_RESULTS_20260509.md`

Report must start with:

| Precision | Seed | Old fresh | Corrected fresh | Delta | Tile audit | Verdict |
|---|---:|---:|---:|---:|---|---|

Then include:

1. exact commands;
2. git SHA and `git status --short` summary;
3. checkpoint paths;
4. output JSON paths;
5. log paths;
6. `tile_audit_all_enabled` for every run;
7. mean/std across seeds for 4/6/8-bit;
8. verdict among:
   - `PCM LADDER SALVAGED`
   - `PCM LADDER REFRAMED`
   - `PCM LADDER KILLED`

## 6. Decision Rules

After corrected eval:

### Salvage path

If corrected results are monotonic or near-monotonic and interpretable, e.g.:

```text
8-bit highest/stable, 6-bit intermediate/seed-sensitive, 4-bit lower or drift-limited
```

then Paper-1 can retain a PCM precision-retention section with revised numbers and softer claims.

### Reframe path

If corrected results are all around 65-70% with high seed variance, then remove `6-bit Pareto midpoint` language and reframe PCM as:

```text
PCM UnitCell supports training under physical constraints, but deployment accuracy is highly sensitive to eval-time modifier noise and seed dynamics.
```

### Kill path

If 4/6/8-bit corrected evals collapse, PCM ladder leaves main text and becomes a cautionary appendix; Paper-1 centers on the IdealDevice/Ensemble-HAT algorithmic contribution.

## 7. DS Assignment

DS must audit after Kimi returns:

- Is `eval_aihwkit_fresh.py` definitely applying noise after `load_state_dict`?
- Are all tile audit entries true?
- Are resolution values correct for 4/6/8-bit?
- Are the old and corrected results comparable except for the noise-on fix?
- Does `modifier_enable_during_test=True` represent the intended physical fresh-instance protocol, or does it double-count noise relative to drift/fresh semantics?

DS output:

`compute_vit/report_md/_gpt/DS_PCM_CORRECTED_EVAL_AUDIT_20260509.md`

## 8. Mimo Assignment

Mimo should prepare narrative fallback after Kimi/DS return, not before.

Possible outcomes:

- If ladder survives: revise `Pareto midpoint` to `observed transition point` and include seed sensitivity.
- If ladder weakens: make 8-bit the drift-safe deployment reference, 4-bit the trainable but drift-limited regime, and 6-bit a seed-sensitive transition.
- If ladder dies: move PCM to limitations/cautionary evidence and center paper on algorithmic cross-instance robustness.

Mimo output:

`compute_vit/report_md/_gpt/MIMO_PCM_NARRATIVE_FALLBACK_20260509.md`

## 9. Codex Ruling

No paper claim using PCM 4/6/8-bit fresh accuracy is allowed until this eval-only queue and DS audit are complete.
