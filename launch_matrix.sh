#!/bin/bash
set -e
cd /home/lisq753/project/HAT/original_repo
SAVE_DIR="checkpoints/_gpt/cross_arch_tinyimagenet"
mkdir -p "$SAVE_DIR"
GPUS=(1 2 3 4 5 6 7)
SEEDS=(123 456 789)
ARCHS=(vit_small_patch16_224 deit_small_patch16_224)
HATS=(standard ensemble proportional)

idx=0
for arch in "${ARCHS[@]}"; do
  for hat in "${HATS[@]}"; do
    for seed in "${SEEDS[@]}"; do
      gpu=${GPUS[$((idx % 7))]}
      echo "Launching $arch $hat seed=$seed on GPU $gpu"
      PYTHONUNBUFFERED=1 CUDA_VISIBLE_DEVICES=$gpu \
        conda run -n hat python -u train_vit_tinyimagenet.py \
        --arch "$arch" --hat-type "$hat" \
        --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
        --seed "$seed" --device cuda --amp --pretrained \
        --data-root ../data/tiny-imagenet-200 \
        --save-dir "$SAVE_DIR" \
        > "$SAVE_DIR/${arch}_${hat}_seed${seed}.log" 2>&1 &
      idx=$((idx + 1))
      sleep 5
    done
  done
done
wait
echo "All 18 configs launched."
