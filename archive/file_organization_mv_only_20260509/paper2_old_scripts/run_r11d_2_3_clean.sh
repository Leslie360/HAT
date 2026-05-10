#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PY=/home/qiaosir/miniconda3/envs/aihwkit/bin/python

run_addnormal() {
  local run_id="$1"
  local inp_res="$2"
  local out_res="$3"
  local sigma="$4"
  local out_dir="paper2_aihwkit_baseline/checkpoints/${run_id}"
  local train_log="paper2_aihwkit_baseline/logs/${run_id}_$(date +%Y%m%d_%H%M%S).log"
  local eval_log="paper2_aihwkit_baseline/logs/${run_id}_fresh_eval_$(date +%Y%m%d_%H%M%S).log"
  mkdir -p "${out_dir}" paper2_aihwkit_baseline/logs
  echo "[clean-queue] TRAIN ${run_id}: inp=${inp_res}, out=${out_res}, sigma=${sigma}, log=${train_log}"
  ${PY} paper2_aihwkit_baseline/train_aihwkit_baseline.py \
    --run-id "${run_id}" \
    --seed 42 \
    --epochs 100 \
    --batch-size 64 \
    --lr 5e-4 \
    --wd 0.05 \
    --workers 0 \
    --device cuda \
    --save-dir "${out_dir}" \
    --log-interval 1 \
    --inp-res "${inp_res}" \
    --out-res "${out_res}" \
    --modifier-std-dev "${sigma}" \
    --early-stop-patience 20 2>&1 | tee -a "${train_log}"
  if [[ ! -s "${out_dir}/best.pt" ]]; then
    echo "[clean-queue] ${run_id} missing best.pt; skip fresh eval"
    return 1
  fi
  echo "[clean-queue] EVAL ${run_id}: log=${eval_log}"
  ${PY} paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "${out_dir}/best.pt" \
    --n-fresh 10 \
    --mc-repeats 5 \
    --workers 0 \
    --device cuda \
    --output "${out_dir}/fresh_eval.json" 2>&1 | tee -a "${eval_log}"
}

echo "[clean-queue] start $(date -Is)"
run_addnormal r11d_2_sigma020_clean 0.00390625 0.00390625 0.20
mean=$(${PY} - <<'PY'
import json
p='paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020_clean/fresh_eval.json'
print(json.load(open(p)).get('mean', 0.0))
PY
)
echo "[clean-queue] R11D-2 clean fresh mean=${mean}"
if ${PY} - <<PY
mean = float('${mean}')
raise SystemExit(0 if mean > 80.0 else 1)
PY
then
  echo "[clean-queue] R11D-2 clean >80, launching conditional R11D-3 sigma=0.30"
  run_addnormal r11d_3_sigma030_clean 0.00390625 0.00390625 0.30
else
  echo "[clean-queue] R11D-2 clean <=80, skip conditional R11D-3"
fi

echo "[clean-queue] complete $(date -Is)"
