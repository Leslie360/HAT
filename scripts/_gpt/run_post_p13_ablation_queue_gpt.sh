#!/bin/bash
# Sequential post-P13 queue: P14-A Flowers-102 V2 control, then P14-B CIFAR-10 data ablation.

set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
LOG_DIR="${ROOT}/logs/_gpt"
QUEUE_LOG="${LOG_DIR}/post_p13_ablation_queue_20260411.log"

mkdir -p "${LOG_DIR}"

{
  echo "============================================================"
  echo "Post-P13 queue started at $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Step 1/2: P14-A Flowers-102 V2 control"
  echo "============================================================"
} | tee -a "${QUEUE_LOG}"

"${ROOT}/scripts/_gpt/run_flowers102_noise_ablation_gpt.sh" 2>&1 | tee -a "${QUEUE_LOG}"

{
  echo "============================================================"
  echo "Step 2/2: P14-B CIFAR-10 data ablation"
  echo "============================================================"
} | tee -a "${QUEUE_LOG}"

"${ROOT}/scripts/_gpt/run_tinyvit_cifar10_data_ablation_gpt.sh" 2>&1 | tee -a "${QUEUE_LOG}"

{
  echo "============================================================"
  echo "Post-P13 queue finished at $(date '+%Y-%m-%d %H:%M:%S')"
  echo "============================================================"
} | tee -a "${QUEUE_LOG}"
