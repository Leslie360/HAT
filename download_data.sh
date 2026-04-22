#!/bin/bash
# download_data.sh — Public dataset download script for reproducibility
# Usage: bash download_data.sh

set -e

DATA_DIR="${DATA_DIR:-./data}"
mkdir -p "$DATA_DIR"

echo "Downloading public datasets to $DATA_DIR ..."

# CIFAR-10 / CIFAR-100 — torchvision will auto-download on first use
# No manual download needed; torchvision places them under $DATA_DIR/cifar-{10,100}-batches-py

# Flowers-102 — torchvision.datasets.Flowers102 auto-downloads from:
# https://www.robots.ox.ac.uk/~vgg/data/flowers/102/flowers-102-category.mat
# https://www.robots.ox.ac.uk/~vgg/data/flowers/102/imagelabels.mat
# https://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz

# ImageNet — must be provided by user; we do not host it
if [ ! -d "$DATA_DIR/imagenet" ]; then
    echo "WARNING: ImageNet not found at $DATA_DIR/imagenet."
    echo "Please download ImageNet ILSVRC2012 train/val and place under:"
    echo "  $DATA_DIR/imagenet/train/"
    echo "  $DATA_DIR/imagenet/val/"
fi

# SVHN — torchvision auto-downloads
# TinyImageNet — not used in NC paper; thesis-only

echo "Public dataset download stub complete."
echo "CIFAR-10/100, Flowers-102, SVHN will be fetched automatically by torchvision on first training run."
echo "ImageNet must be supplied manually."
