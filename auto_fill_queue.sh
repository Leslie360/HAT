#!/bin/bash
# Auto-fill remaining tasks onto idle GPUs. GPU 2 is reserved for others.
cd /home/lisq753/project/HAT/original_repo
SAVE_DIR="checkpoints/_gpt/cross_arch_tinyimagenet"

# Remaining tasks queue (ordered by priority)
declare -a TASKS=(
  "vit_small_patch16_224:standard:456"
)

# GPUs to monitor (exclude 2)
declare -a GPUS=(0 1 3 4 5 6 7)

launch_task() {
  local arch=$1 hat=$2 seed=$3 gpu=$4
  local log="$SAVE_DIR/${arch}_${hat}_seed${seed}.log"
  echo "[$(date '+%H:%M:%S')] GPU $gpu idle -> launching $arch $hat seed=$seed"
  PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    CUDA_VISIBLE_DEVICES=$gpu \
    conda run -n hat python -u train_vit_tinyimagenet.py \
    --arch "$arch" --hat-type "$hat" \
    --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
    --seed "$seed" --device cuda --amp --pretrained \
    --data-root ../data/tiny-imagenet-200 \
    --save-dir "$SAVE_DIR" \
    > "$log" 2>&1 &
  echo "PID: $!"
}

task_idx=0
while [ $task_idx -lt ${#TASKS[@]} ]; do
  for gpu in "${GPUS[@]}"; do
    used=$(nvidia-smi --id=$gpu --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')
    if [ "$used" -lt 500 ]; then
      IFS=':' read -r arch hat seed <<< "${TASKS[$task_idx]}"
      launch_task "$arch" "$hat" "$seed" "$gpu"
      task_idx=$((task_idx + 1))
      if [ $task_idx -ge ${#TASKS[@]} ]; then
        echo "[$(date '+%H:%M:%S')] All tasks launched. Queue empty."
        exit 0
      fi
      sleep 10
    fi
  done
  sleep 60
done
