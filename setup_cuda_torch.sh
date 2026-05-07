#!/bin/bash
# Quick CUDA PyTorch install helper for this project
# Usage: cd HAT && bash setup_cuda_torch.sh
#
# This script tries pip with retries. If the network is flaky,
# it will fall back to a CPU-only warning.

set -e

PYTHON=$(which python)
echo "Python: $PYTHON"

# Uninstall CPU torch first
echo "Uninstalling existing torch/torchvision..."
pip uninstall -y torch torchvision torchaudio 2>/dev/null || true

# Install CUDA 12.6 wheels with retries
for i in 1 2 3; do
    echo "Attempt $i/3: installing torch + torchvision (CUDA 12.6)..."
    if pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126 --timeout 120; then
        echo "Success!"
        $PYTHON -c "import torch; print('torch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda if torch.cuda.is_available() else 'N/A')"
        exit 0
    fi
    echo "Attempt $i failed. Retrying in 10s..."
    sleep 10
done

echo "All pip attempts failed. Trying conda fallback..."
conda install -y pytorch torchvision pytorch-cuda=12.6 -c pytorch -c nvidia 2>/dev/null || true

$PYTHON -c "import torch; print('torch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())" || {
    echo "Installation failed. PyTorch is likely still CPU-only."
    exit 1
}
