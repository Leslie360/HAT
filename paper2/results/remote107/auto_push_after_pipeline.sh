#!/bin/bash
# Wait for both pipelines, then commit & push results
PIPELINE1_PID=3238658  # pipeline_d2d_seed.py
PIPELINE2_PID=1448607  # pipeline_fresh_d2d.py
HAT_DIR="/home/lisq753/projects/HAT/HAT"
OUT_DIR="/home/lisq753/projects/HAT_kv107/paper2/results/remote107"

echo "[auto-push] Waiting for pipeline_d2d_seed (PID ${PIPELINE1_PID})..."
while kill -0 ${PIPELINE1_PID} 2>/dev/null; do sleep 60; done
echo "[auto-push] pipeline_d2d_seed finished at $(date)"

echo "[auto-push] Waiting for pipeline_fresh_d2d (PID ${PIPELINE2_PID})..."
while kill -0 ${PIPELINE2_PID} 2>/dev/null; do sleep 60; done
echo "[auto-push] pipeline_fresh_d2d finished at $(date)"

cd "${HAT_DIR}"
git checkout 107-clean
git pull origin 107-clean

# Copy all result JSONs into the repo
mkdir -p results/d2d_seed_ablation
cp ${OUT_DIR}/eval_*_seed*.json results/d2d_seed_ablation/ 2>/dev/null
cp ${OUT_DIR}/hat_*.json results/d2d_seed_ablation/ 2>/dev/null
cp ${OUT_DIR}/.pipeline_d2dseed_state.json results/d2d_seed_ablation/ 2>/dev/null
cp ${OUT_DIR}/.pipeline_fresh_d2d_state.json results/d2d_seed_ablation/ 2>/dev/null
cp ${OUT_DIR}/pipeline_d2dseed.log results/d2d_seed_ablation/ 2>/dev/null
cp ${OUT_DIR}/pipeline_fresh_d2d.log results/d2d_seed_ablation/ 2>/dev/null

# Count results
N_EVAL=$(ls results/d2d_seed_ablation/eval_*_seed*.json 2>/dev/null | wc -l)
N_TRAIN=$(ls results/d2d_seed_ablation/hat_*_seed*.json 2>/dev/null | wc -l)

git add results/d2d_seed_ablation/
git commit -m "D2D seed ablation + fresh-D2D cross-instance results (auto)

Eval results: ${N_EVAL} JSONs
Train results: ${N_TRAIN} JSONs
Completed: $(date +%Y-%m-%d)"

git push origin 107-clean
echo "[auto-push] Done at $(date) — ${N_EVAL} eval + ${N_TRAIN} train results pushed"
