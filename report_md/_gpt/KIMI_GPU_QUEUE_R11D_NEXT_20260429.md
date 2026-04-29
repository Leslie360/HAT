# Kimi GPU Queue — R11D Next Experiments After 3-Seed Closure

**Date:** 2026-04-29  
**Owner:** Kimi GPU scheduler  
**Coordinator:** Codex  
**Status:** 3-seed PCM source/fresh/drift closure complete.

## 1. Locked Result To Preserve

Use `outputs/R11D_FINAL_3SEED_SUMMARY_20260429.md` as the current local evidence lock. Mirrored copy: `report_md/_gpt/R11D_FINAL_3SEED_SUMMARY_20260429.md`.

Core 3-seed result:

| Config | Source best | Fresh eval | Drift 0s | Drift 1h | Drift 24h | 24h drop |
|---|---:|---:|---:|---:|---:|---:|
| 4-bit PCM | 76.71 ± 0.46% | 76.6845 ± 0.37% | 76.64 ± 0.40% | 74.04 ± 0.85% | 72.64 ± 0.71% | -4.01pp |
| 8-bit PCM | 77.64 ± 0.68% | 77.5955 ± 0.64% | 77.61 ± 0.80% | 77.49 ± 0.52% | 77.57 ± 0.61% | -0.04pp |

Decision:

- Training/fresh claim is closed: 4-bit PCM is stable and only ~0.9pp behind 8-bit.
- Drift is now the main caveat: 4-bit loses ~4pp at 24h; 8-bit is drift-stable.
- Next experiments must explain this trade-off, not merely add more seed repetitions.

## 2. Batch A — Eval-Only, Run First

Purpose: turn the 24h drift caveat into a curve and test real deployment combined noise.

Run this immediately. It launches no training:

```bash
cd /home/qiaosir/projects/compute_vit
bash paper2_aihwkit_baseline/run_kimi_r11d_extended_eval_20260429.sh
```

This script performs:

1. Extended drift curve for all 6 corrected checkpoints:
   - times: 0, 10min, 30min, 1h, 3h, 6h, 12h, 24h, 48h, 72h
   - output: `extended_drift_eval.json`
2. Combined fresh+drift pilot for all 6 corrected checkpoints:
   - times: 0, 1h, 24h
   - `n_fresh=5`, `mc_repeats=3`
   - output: `fresh_drift_eval.json`

Why this matters:

- Current fresh eval has no drift.
- Current drift eval has no test-time fresh noise.
- Real deployment has both. We need know whether 4-bit's 24h -4pp drift becomes worse under fresh D2D/C2C realizations.

Kill criteria:

- If any `tile_audit_all_enabled` is false in fresh+drift output, stop and report.
- If fresh+drift 8-bit at 24h drops >1pp relative to fresh-only, debug before interpreting 4-bit.
- If fresh+drift 4-bit at 24h falls below 70%, mark 4-bit as retention-limited deployment mode and use 8-bit for retention-critical headline.

Return after Batch A:

```text
run_id, bit, seed, extended_drift_0, 10m, 30m, 1h, 3h, 6h, 12h, 24h, 48h, 72h,
fresh_drift_0_mean, fresh_drift_1h_mean, fresh_drift_24h_mean, status
```

## 3. Batch B — Preset Dependence Check, Run After Batch A

Purpose: verify the conclusion is not an artifact of `PCMPresetUnitCell`.

Run strict `PCMPresetDevice` comparison with fresh v2 artifact names:

```bash
cd /home/qiaosir/projects/compute_vit
bash paper2_aihwkit_baseline/run_pcm_preset_comparison.sh
```

This now writes to:

- `t13v2_r11d_5a_pcm_PCMPresetDevice_seed123`
- `t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123`

Do not reuse historical invalid `PCMPresetDevice_seed42` directories.

After each training completes, run fresh and drift eval:

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit

for RUN in \
  t13v2_r11d_5a_pcm_PCMPresetDevice_seed123 \
  t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123; do
  $PYTHON paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt" \
    --n-fresh 10 --mc-repeats 5 --batch-size 64 --workers 0 --device cuda \
    --output "paper2_aihwkit_baseline/checkpoints/${RUN}/fresh_eval.json"
  $PYTHON paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
    --checkpoint "paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt" \
    --batch-size 64 --workers 0 --device cuda \
    --drift-times 0 3600 86400 \
    --output "paper2_aihwkit_baseline/checkpoints/${RUN}/drift_eval.json"
done
```

Interpretation:

- If PCMPresetDevice is within ~2pp of UnitCell, claim is preset-robust.
- If PCMPresetDevice collapses or drifts differently, frame R11D as `PCMPresetUnitCell`-specific and use preset comparison as a limitation/supplementary caution.

Soft stop:

- Do not kill just because early epochs are low; valid PCM runs improve late.
- If epoch 50 test is <45% or NaN appears, stop and report as likely incompatible preset/regime.

## 4. Batch C — Clean Oracle / Training-Noise Necessity

Purpose: convert the existing diagnostic oracle result into clean provenance.

Run only after Batch A/B or if Claude explicitly asks for the regularization proof first.

8-bit clean no-modifier run:

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit
RUN=r11d_5a_pcm_oracle_seed123_clean
mkdir -p "paper2_aihwkit_baseline/checkpoints/${RUN}" paper2_aihwkit_baseline/logs
$PYTHON paper2_aihwkit_baseline/r11d4_train_pcm.py \
  --run-id "$RUN" \
  --seed 123 \
  --epochs 100 \
  --batch-size 64 \
  --lr 0.001 \
  --wd 0.05 \
  --momentum 0.0 \
  --device cuda \
  --workers 0 \
  --save-dir "paper2_aihwkit_baseline/checkpoints/${RUN}" \
  --log-interval 1 \
  --inp-res 0.00390625 \
  --out-res 0.00390625 \
  --modifier-std-dev 0.0 \
  --early-stop-patience 0 \
  2>&1 | tee "paper2_aihwkit_baseline/logs/${RUN}_$(date +%Y%m%d_%H%M%S).log"
```

Interpretation:

- If clean no-modifier stays near previous diagnostic ~61%, training-time modifier noise is essential regularization/noise exposure.
- If it recovers near 77%, previous oracle result was provenance-contaminated and must be retracted.

## 5. Batch D — Optional 6-bit Pareto Bridge

Only run after Batch A and if GPU time remains. This is not required for the current R11D claim but could strengthen the precision/drift Pareto story.

One-seed pilot first:

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit
RUN=r11d_6bit_pcm_seed123
mkdir -p "paper2_aihwkit_baseline/checkpoints/${RUN}" paper2_aihwkit_baseline/logs
$PYTHON paper2_aihwkit_baseline/r11d4_train_pcm.py \
  --run-id "$RUN" \
  --seed 123 \
  --epochs 100 \
  --batch-size 64 \
  --lr 0.001 \
  --wd 0.05 \
  --momentum 0.0 \
  --device cuda \
  --workers 0 \
  --save-dir "paper2_aihwkit_baseline/checkpoints/${RUN}" \
  --log-interval 1 \
  --inp-res 0.015625 \
  --out-res 0.015625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 0 \
  2>&1 | tee "paper2_aihwkit_baseline/logs/${RUN}_$(date +%Y%m%d_%H%M%S).log"
```

Run fresh/drift after it. Continue to seeds 456/789 only if 6-bit gives either:

- source/fresh within 0.5pp of 8-bit, or
- 24h drift drop clearly below 4-bit and above 8-bit, forming a useful Pareto bridge.

## 6. What Not To Run Now

- Do not repeat 4-bit/8-bit UnitCell seeds. The 3-seed table is closed.
- Do not run R11D11 progressive unless a specific mechanism question is raised; current 8-bit progressive result is poor.
- Do not run Remote 105 architecture/multi-dataset jobs locally.
- Do not run Remote 107 KV-cache jobs locally.
- Do not start multiple local training jobs in parallel on the single RTX 5070 Ti.

## 7. Reporting Requirement

After each batch, Kimi should append a short report to the hub and return:

```text
batch_id, run_id, command, checkpoint_dir, source_best, fresh_mean, drift/fresh_drift table, verdict, use_in_paper=yes/no
```
